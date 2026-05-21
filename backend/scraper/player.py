from scraper.scraper import scrape_page 

def scrape_player_birthday(player_url: str) -> str:
    soup = scrape_page(player_url, ".spielerdatenundfakten")
    birthday = soup.select_one('span[itemprop="birthDate"]')
    birthday_text = birthday.get_text(strip=True)
    birthday_age_split = birthday_text.split(" ")
    return birthday_age_split[0]
