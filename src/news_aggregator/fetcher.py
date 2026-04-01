import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import Iterable, List, Optional

@dataclass
class Article:
    url: str
    title: str
    text: str


def fetch_article(url: str, timeout=15) -> Optional[Article]:
    try:
        resp = requests.get(url, timeout=timeout, headers={"User-Agent": "news-aggregator/1.0"})
        resp.raise_for_status()
        soup = BeautifulSoup(resp.content, "lxml")
        title = soup.title.string.strip() if soup.title and soup.title.string else url
        paragraphs = [p.get_text(" ", strip=True) for p in soup.find_all("p")]
        text = "\n\n".join(p for p in paragraphs if p)
        if not text:
            return None
        return Article(url=url, title=title, text=text)
    except Exception:
        return None


def fetch_articles(urls: List[str]) -> List[Article]:
    articles = []
    for url in urls:
        article = fetch_article(url)
        if article:
            articles.append(article)
    return articles
