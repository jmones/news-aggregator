import re
import os
from openai import OpenAI
from .fetcher import Article


def extract_topics_and_summarize(all_text: str, num_topics: int = 5, summary_lines: int = 3) -> dict:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set. Please set it to use LLM features.")

    client = OpenAI(api_key=api_key)
    try:
        prompt = f"Analyze the following news articles and identify the top {num_topics} topics. For each topic, provide a {summary_lines}-line summary based on the articles. Format as: Topic 1: [summary]\n\nTopic 2: [summary]\n\n etc.\n\nArticles:\n{all_text[:4000]}"  # Limit text length
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that analyzes news articles."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.5
        )
        content = response.choices[0].message.content.strip()
        # Parse the response
        topics = {}
        parts = content.split("\n\n")
        for part in parts:
            if ": " in part:
                topic, summary = part.split(": ", 1)
                topics[topic.strip()] = summary.strip()
        return topics
    except Exception as e:
        raise ValueError(f"LLM error: {e}")


def summarize_text(text: str, max_sentences: int = 3) -> str:
    # Keep for fallback or individual
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    sentences = [s.strip() for s in sentences if s.strip()]
    return " ".join(sentences[:max_sentences])


def summarize_article(article: Article, max_sentences: int = 3) -> str:
    return summarize_text(article.text, max_sentences)
