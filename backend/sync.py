from service.team_service import create_team
from fastapi import Depends 
from service.player_service import create_player, get_player_link, update_ordb_id, update_wyscout_id
from service.task_service import create_missing_EN_name_task, create_missing_dob_task, create_missing_ordb_id_task, create_missing_transfermarkt_URL_task, create_missing_wyscout_id_task, get_task, remove_task
from scraper import player_list
from scraper.main import load_teams
from db.models import Base
from sqlalchemy.orm import Session
from db.db import get_session, engine

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

            if player_obj.wyscout_id is None:
                create_missing_wyscout_id_task(db, player_obj)
                print(f"{player_obj.get_name()} missing wyscout ID")

    db.commit()

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

    db.commit()

def link_wyscout(db: Session = Depends(get_session)):
    import csv

    teams = load_teams()

    with open("Wyscout_J1_25.csv", "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            name = " ".join(row["Full name"].split())
            dob = row["Birthday"]
            team = get_team("wyscout", row["Team"], teams)

            if player := get_player_link(db, name, dob, team):
                if player.wyscout_id is not None:
                    print(f"PASS {name}")
                    continue

                update_wyscout_id(db, player.id, row["Wyscout id"])
                task = create_missing_wyscout_id_task(db, player)

                if task is not None:
                    remove_task(db, task.id)

                print(f"COMPLETED {name}")
            else:
                if len(team) > 0:
                    print(f"unable to find {name} ({dob}, {team})")

    db.commit()
                
def get_team(type: str, team: str, teams: list) -> str:
    for team_name in teams:
        if teams[team_name]["alternate_names"][type] == team:
            return team_name
    return ""

def link_teams(db: Session = Depends(get_session)):
    teams = load_teams()

    for team_name in teams:
        create_team(db, team_name, teams[team_name])
        print(f"CREATED {team_name}")
        
    db.commit()

def update():
    db = next(get_session())
    try:
        link_teams(db)
    finally:
        db.close()

update()
