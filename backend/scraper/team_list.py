from scraper.scraper import scrape_page, get_href

def scrape_team_list(team: dict) -> dict:
    ret = {}
    soup = scrape_page(team['transfermarkt'], ".items tbody tr")
    player_table = soup.find("table", class_="items")
    rows = player_table.find_all("tr")

    for i in range(1, len(rows)):
        back_number = rows[i].select_one("div.rn_nummer")
        name = rows[i].select_one("td.hauptlink")
        
        if not back_number or not name:
            continue

        back_number_text = back_number.get_text(strip=True)
        name_text = name.get_text(strip=True)
        transfermarkt_URL = get_href(name)
        ret[name_text + back_number_text] = "https://www.transfermarkt.com" + transfermarkt_URL

    return ret
