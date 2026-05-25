from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def get_href(element):
    a_tag = element.find("a")
    if a_tag and a_tag.has_attr("href"):
        return a_tag["href"]
    return ""

def scrape_page(url, selector):
    retries = 3

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        for attempt in range(retries):
            page = browser.new_page()

            try:
                page.goto(url)
                page.wait_for_selector(selector, timeout=10000)
                html = page.content()
                soup = BeautifulSoup(html, "html.parser")
                page.close()
                browser.close()
                return soup
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                page.close()

                if attempt == retries - 1:
                    browser.close()
                    raise
