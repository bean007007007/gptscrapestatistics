import sqlite3
import time
from urllib.parse import quote_plus
import requests
from bs4 import BeautifulSoup

DB_PATH = "vacatures.db"
SEARCH_QUERY = "junior systeembeheerder"
BASE_URL = "https://www.vacaturebank.nl"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS vacancies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            company TEXT,
            location TEXT,
            summary TEXT,
            link TEXT UNIQUE
        )
        """
    )
    conn.commit()
    conn.close()


def save_vacancy(data):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        INSERT OR IGNORE INTO vacancies(title, company, location, summary, link)
        VALUES(?,?,?,?,?)
        """,
        (data.get("title"), data.get("company"), data.get("location"), data.get("summary"), data.get("link")),
    )
    conn.commit()
    conn.close()


def parse_listing(listing):
    title_tag = listing.find("h2")
    title = title_tag.get_text(strip=True) if title_tag else None
    company_tag = listing.find(class_="company")
    company = company_tag.get_text(strip=True) if company_tag else None
    location_tag = listing.find(class_="location")
    location = location_tag.get_text(strip=True) if location_tag else None
    summary_tag = listing.find(class_="summary")
    summary = summary_tag.get_text(strip=True) if summary_tag else None
    link_tag = title_tag.find("a") if title_tag else None
    link = BASE_URL + link_tag["href"] if link_tag and link_tag.has_attr("href") else None
    return {
        "title": title,
        "company": company,
        "location": location,
        "summary": summary,
        "link": link,
    }


def scrape_page(session, page):
    url = f"{BASE_URL}/vacatures/?q={quote_plus(SEARCH_QUERY)}&page={page}"
    resp = session.get(url, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    listings = soup.select(".vacancy")
    for listing in listings:
        data = parse_listing(listing)
        if data["link"]:
            save_vacancy(data)


def scrape(max_pages=1, delay=1.0):
    init_db()
    with requests.Session() as session:
        for page in range(1, max_pages + 1):
            scrape_page(session, page)
            time.sleep(delay)


if __name__ == "__main__":
    scrape(max_pages=5)
