from scraper.team_list import scrape_team_list
from service.team_service import get_all_teams, get_team_by_alternate, get_team_by_name
from fastapi import Depends 
from service.player_service import create_player, get_player_by_team_and_number, get_player_link, update_dob, update_ordb_id, update_wyscout_id
from service.task_service import create_missing_EN_name_task, create_missing_dob_task, create_missing_ordb_id_task, create_missing_team_id_task, create_missing_transfermarkt_URL_task, create_missing_wyscout_id_task, get_task, remove_task
from scraper import player_list
from scraper.main import load_teams
from db.models import Base, Player
from sqlalchemy.orm import Session
from db.db import get_session, engine

Base.metadata.create_all(engine)

def update_tasks(db: Session = Depends(get_session)):
    teams = get_all_teams(db)

    for team in teams:
        print(team.EN_name)
        players = player_list.scrape_player_list(team)

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

    with open("ORDB_JLeague.csv", "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        count = 0
        for row in reader:
            count += 1
            name = row["Name"]
            dob = row["Date Of Birth"]
            
            if len(dob) == 0:
                continue

            team = get_team_by_alternate(db, row["Based Club Name"], "ordb")

            if team is None:
                print(f"{row['Based Club Name']} could not be found")
                continue

            if player := get_player_link(db, name, dob, team.id):
                if player.ordb_id is not None:
                    print(f"PASS {name}")
                    continue

                update_ordb_id(db, player.id, row["\ufeffFM ID"])
                task = create_missing_ordb_id_task(db, player)

                if task is not None:
                    remove_task(db, task.id)

                print(f"{count} COMPLETED {name}")
            else:
                print(f"{count} unable to find {name} ({dob}, {team.EN_name})")
    db.commit()

def link_wyscout(db: Session = Depends(get_session)):
    import csv

    with open("Wyscout_J2_J3_26.csv", "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        counter = 0

        for row in reader:
            name = " ".join(row["Full name"].split())
            dob = row["Birthday"]
            team = get_team_by_alternate(db, row["Team"], "wyscout")

            if team is None:
                print(f"{row['Team']} could not be found")
                continue

            if player := get_player_link(db, name, dob, team.id):
                if player.wyscout_id is not None:
                    print(f"PASS {name}")
                    continue

                update_wyscout_id(db, player.id, row["Wyscout id"])
                task = create_missing_wyscout_id_task(db, player)

                if task is not None:
                    remove_task(db, task.id)

                print(f"{counter} COMPLETED {name}")
            else:
                print(f"{counter} unable to find {name} ({dob}, {row['Team']})")
            counter += 1

            if counter == 100:
                db.commit()
                counter = 0

def get_JP_names(db: Session = Depends(get_session)):
    teams = get_all_teams(db)

    for team in teams:
        print(f"{team.EN_name}")
        players = player_list.scrape_player_list(team)

        for player in players:
            create_player(db, player)
            print(f"COMPLETED {player['name']} -> {player['team']}")

    db.commit()

def get_EN_names(db: Session = Depends(get_session)):
    teams = get_all_teams(db)

    for team in teams:
        print(f"{team.EN_name}")
        data = scrape_team_list(team)
        
        for number in data:
            player = get_player_by_team_and_number(db, team.id, number)

            if player is None:
                print(f"Couldn't Find a #{number} from {team.EN_name}")
                continue

            if player.date_of_birth is not None:
                print(f"PASSED {player.EN_name}")
                continue

            player.transfermarkt_URL = data[number]["URL"]
            player.EN_name = data[number]["name"]
            player = update_dob(db, player.id, data[number]["dob"])

            if player is not None:
                print(f"COMPLETED {player.EN_name}, {player.back_number} -> {player.transfermarkt_URL} ({player.date_of_birth})")

        db.commit()
                
def get_team(type: str, team: str, teams: list) -> str:
    for team_name in teams:
        if teams[team_name]["alternate_names"][type] == team:
            return team_name
    return ""

def update():
    db = next(get_session())
    try:
        update_tasks(db)
    finally:
        db.close()

update()
