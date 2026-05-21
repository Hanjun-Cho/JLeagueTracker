from db.models import Base
from scraper.player import scrape_player_birthday
from scraper.team_list import scrape_team_list
from sqlalchemy.orm import Session
from db.db import get_session, engine
from service.task_service import create_task, get_task, remove_task
from scraper import player_list
from scraper.main import load_teams
from service.player_service import create_player, get_players_from_team, update_dob, update_transfermarkt_URL
from fastapi import Depends, FastAPI
from routes.dashboard import dashboard_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(dashboard_router, prefix="/dashboard")

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(engine)

def load_all_players(db: Session = Depends(get_session)):
    teams = load_teams()

    for team_name in teams:
        print(team_name)
        players = player_list.scrape_player_list(teams[team_name], team_name)

        for player in players:
            player_obj = create_player(db, player)

            if player_obj.EN_name == None:
                task_data = {
                    "name": f"{player_obj.JP_name} is missing ENGLISH NAME",
                    "task_type": "MISSING EN_NAME",
                    "player_id": player_obj.id
                }
                create_task(db, task_data)

            if player_obj.transfermarkt_URL == None:
                task_data = {
                    "name": f"{player_obj.JP_name} is missing TRANSFERMARKT URL",
                    "task_type": "MISSING TRANSFERMARKT_URL",
                    "player_id": player_obj.id
                }
                create_task(db, task_data)

            print(f"FINISHED {player_obj.JP_name}")

def load_transfermarkt(db: Session):
    teams = load_teams()

    for team_name in teams:
        print(team_name)
        team_URLs = scrape_team_list(teams[team_name])
        players = get_players_from_team(db, team_name)

        for player in players:
            if not player.EN_name:
                task_data = {
                    "name": f"{player.JP_name} is missing ENGLISH NAME",
                    "task_type": "MISSING EN_NAME",
                    "player_id": player.id
                }
                create_task(db, task_data)
                print(f"NO EN_NAME {player.JP_name}")
                continue

            if player.transfermarkt_URL is not None:
                if player.date_of_birth is not None:
                    continue

                birthday = scrape_player_birthday(player.transfermarkt_URL)
                update_dob(db, player.id, birthday)

                task = get_task(db, {"name": f"{player.JP_name} is missing DATE OF BIRTH"})

                if task:
                    remove_task(db, task.id)

                print(f"UPDATED DOB {player.JP_name} {player.EN_name} -> {birthday}")
                continue

            url_key = player.EN_name + player.back_number
            if url_key in team_URLs:
                update_transfermarkt_URL(db, player.id, team_URLs[url_key])
                
                task = get_task(db, {"name": f"{player.JP_name} is missing TRANSFERMARKT URL"})

                if task:
                    remove_task(db, task.id)

                print(f"ADDED {player.JP_name} {player.EN_name} -> {team_URLs[url_key]}")
            else:
                task_data = {
                    "name": f"{player.JP_name} is missing TRANSFERMARKT URL",
                    "task_type": "MISSING TRANSFERMARKT_URL",
                    "player_id": player.id
                }
                create_task(db, task_data)

                task_data = {
                    "name": f"{player.JP_name} is missing DATE OF BIRTH",
                    "task_type": "MISSING DATE_OF_BIRTH",
                    "player_id": player.id
                }
                create_task(db, task_data)
                print(f"X {player.JP_name} {player.EN_name}")

def update():
    db = next(get_session())
    try:
        load_transfermarkt(db)
    finally:
        db.close()
