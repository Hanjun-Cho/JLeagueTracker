import re
from db.models import Team
from scraper.scraper import scrape_page, get_href

def scrape_player_list(team: Team) -> list:
    players = []
    url = f"http://soccer.phew.homeip.net/injury_news/team/?start=0&sort=position&team={team.injury_tracker_id}"
    soup = scrape_page(url, "#main_table tr")

    player_table = soup.find("table", id="main_table")
    rows = player_table.find_all("tr")

    for i in range(1, len(rows)):
        columns = rows[i].find_all(["td", "th"])

        back_number = columns[0].get_text(strip=True)
        position = columns[1].get_text(strip=True)

        name = columns[2]
        name_text = name.get_text(strip=True)
        tracker_source = get_href(name)

        match = re.search(r"id=(\d+)", tracker_source)

        if not match:
            print(f"error: ID not found in tracker source ({tracker_source})")
            return []

        player_id = int(match.group(1))

        player = {
            "id": player_id,
            "name": name_text,
            "position": position,
            "back_number": back_number,
            "team": team.EN_name,
            "team_id": team.id
        }

        players.append(player)

    return players
