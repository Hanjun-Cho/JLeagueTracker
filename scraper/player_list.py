import scraper
import re

def scrape_player_list(team):
    soup = scraper.scrape_page(team['injury_tracker'], "#main_table tr")

    player_table = soup.find("table", id="main_table")
    rows = player_table.find_all("tr")

    for i in range(1, len(rows)):
        columns = rows[i].find_all(["td", "th"])

        name = columns[2]
        name_text = name.get_text(strip=True)
        tracker_source = scraper.get_href(name)

        match = re.search(r"id=(\d+)", tracker_source)

        if not match:
            print(f"error: ID not found in tracker source ({tracker_source})")
            return

        player_id = int(match.group(1))
        print(f"{name_text} ({player_id})")

