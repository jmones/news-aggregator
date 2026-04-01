import re
from .fetcher import Article


def summarize_text(text: str, max_sentences: int = 3) -> str:
    # simple heuristic summarizer: split paragraphs to sentences and return first N
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    sentences = [s.strip() for s in sentences if s.strip()]
    return " ".join(sentences[:max_sentences])


def summarize_article(article: Article, max_sentences: int = 3) -> str:
    return summarize_text(article.text, max_sentences)
