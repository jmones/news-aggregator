from typing import Iterable
from .fetcher import Article


def filter_articles(articles: Iterable[Article], keywords: list[str]) -> list[Article]:
    if not keywords:
        return list(articles)

    lower_keys = [k.lower() for k in keywords]
    matched = []
    for article in articles:
        text = (article.title + " " + article.text).lower()
        if any(k in text for k in lower_keys):
            matched.append(article)
    return matched
