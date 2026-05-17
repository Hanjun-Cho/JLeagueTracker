import json

def load_teams():
    with open("./scraper/teams.json", "r", encoding="utf-8") as f:
        teams = json.load(f)
    return teams 
