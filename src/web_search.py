import requests
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")


def google_search(query, max_results) -> list[dict]:
    if not GOOGLE_API_KEY or not GOOGLE_CSE_ID:
        raise ValueError("Faltan GOOGLE_API_KEY o GOOGLE_CSE_ID en el .env")

    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_API_KEY,
        "cx": GOOGLE_CSE_ID,
        "q": query,
        "num": max_results,
    }

    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()

    data = r.json()
    items = data.get("items", [])

    return [
        {
            "title": it.get("title", ""),
            "url": it.get("link", ""),
            "snippet": it.get("snippet", ""),
        }
        for it in items
    ]

def extract_page_text(url, max_chars=4000):
    import requests
    from bs4 import BeautifulSoup

    r = requests.get(url, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    for tag in soup(["script", "style"]):
        tag.decompose()

    return " ".join(soup.stripped_strings)[:max_chars]