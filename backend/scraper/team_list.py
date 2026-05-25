from db.models import Team
from scraper.scraper import scrape_page, get_href

def scrape_team_list(team: Team) -> dict:
    ret = {}
    url = f"https://www.transfermarkt.com/{team.transfermarkt}/startseite/verein/{team.id}/plus/1"
    soup = scrape_page(url, ".items tbody tr")
    player_table = soup.find("table", class_="items")
    rows = player_table.find_all("tr")

    for i in range(1, len(rows)):
        back_number = rows[i].select_one("div.rn_nummer")
        name = rows[i].select_one("td.hauptlink")
        birthdate = rows[i].select("td.zentriert")
        
        if not back_number or not name:
            continue

        back_number_text = back_number.get_text(strip=True)
        name_text = name.get_text(strip=True)
        birthdate_text = birthdate[1].get_text(strip=True)
        transfermarkt_URL = get_href(name)
        ret[back_number_text] = {}
        ret[back_number_text]["URL"] = "https://www.transfermarkt.com" + transfermarkt_URL
        ret[back_number_text]["name"] = name_text
        ret[back_number_text]["dob"] = birthdate_text.split(" ")[0]
    return ret
