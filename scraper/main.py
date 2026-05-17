import player_list
import json

def load_teams():
    with open("teams.json", "r", encoding="utf-8") as f:
        teams = json.load(f)
    return teams 

if __name__ in "__main__":
    teams = load_teams() 

    for team in teams:
        print(team)
        player_list.scrape_player_list(teams[team])

