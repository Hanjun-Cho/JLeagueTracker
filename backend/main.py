import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from scraper import player_list
from scraper.main import load_teams
from service.player_service import create_player
from db.models import Base

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL is not set")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
session = SessionLocal()

def load_all_players():
    teams = load_teams()

    for team_name in teams:
        print(team_name)
        players = player_list.scrape_player_list(teams[team_name], team_name)

        for player in players:
            create_player(session, player)
            print(f"FINISHED {player['name']}")
