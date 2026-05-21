from db.models import Base
from scraper.player import scrape_player_birthday
from scraper.team_list import scrape_team_list
from sqlalchemy.orm import Session
from db.db import get_session, engine
from service.task_service import create_missing_EN_name_task, create_missing_dob_task, create_missing_ordb_id_task, create_missing_transfermarkt_URL_task, create_task, get_task, remove_task
from scraper import player_list
from scraper.main import load_teams
from service.player_service import create_player, get_player, get_player_link, get_players_from_team, update_dob, update_ordb_id, update_transfermarkt_URL, update_wyscout_id
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

def update_tasks(db: Session = Depends(get_session)):
    teams = load_teams()

    for team_name in teams:
        print(team_name)
        players = player_list.scrape_player_list(teams[team_name], team_name)

        for player in players:
            player_obj = create_player(db, player)

            if player_obj.EN_name is None:
                create_missing_EN_name_task(db, player_obj)
                print(f"{player_obj.get_name()} missing EN_name")
            if player_obj.transfermarkt_URL is None:
                create_missing_transfermarkt_URL_task(db, player_obj)
                print(f"{player_obj.get_name()} missing transfermarkt URL")
            
            if player_obj.date_of_birth is None:
                create_missing_dob_task(db, player_obj)
                print(f"{player_obj.get_name()} missing date of birth")

            if player_obj.ordb_id is None:
                create_missing_ordb_id_task(db, player_obj)
                print(f"{player_obj.get_name()} missing ordb ID")

def link_ordb(db: Session = Depends(get_session)):
    import csv

    teams = load_teams()

    with open("ORDB_JLeague.csv", "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        count = 0
        for row in reader:
            count += 1
            name = row["Name"]
            dob = row["Date Of Birth"]
            
            if len(dob) == 0:
                continue

            team = get_team("ordb", row["Based Club Name"], teams)

            if player := get_player_link(db, name, dob, team):
                update_ordb_id(db, player.id, row["FM ID"])
                print(f"{count} COMPLETED {name}")
            else:
                print(f"{count} unable to find {name} ({dob}, {team})")

def link_wyscout(db: Session = Depends(get_session)):
    import csv

    teams = load_teams()

    with open("Wyscout_J1.csv", "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            name = " ".join(row["Full name"].split())
            dob = row["Birthday"]
            team = get_team("wyscout", row["Team"], teams)

            if player := get_player_link(db, name, dob, team):
                update_wyscout_id(db, player.id, row["Wyscout id"])
                print(f"COMPLETED {name}")
            else:
                if len(team) > 0:
                    print(f"unable to find {name} ({dob}, {team})")
                
def get_team(type: str, team: str, teams: list) -> str:
    for team_name in teams:
        if teams[team_name]["alternate_names"][type] == team:
            return team_name
    return ""

def update():
    db = next(get_session())
    try:
        link_ordb(db)
        link_wyscout(db)
        update_tasks(db)
    finally:
        db.close()

#update()
