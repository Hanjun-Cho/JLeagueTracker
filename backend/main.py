from sqlalchemy.orm import Session
from db.db import get_session
from service.task_service import create_task
from scraper import player_list
from scraper.main import load_teams
from service.player_service import create_player
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
