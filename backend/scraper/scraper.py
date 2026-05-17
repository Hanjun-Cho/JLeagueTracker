from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def get_href(element):
    a_tag = element.find("a")
    if a_tag and a_tag.has_attr("href"):
        return a_tag["href"]
    return ""

def scrape_page(url, selector):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_selector(selector)
        html = page.content()
        soup = BeautifulSoup(html, "html.parser")
        browser.close()
    return soup
