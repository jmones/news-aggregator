import re
import os
import requests
from .fetcher import Article


GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama3-8b-8192"  # Free tier model


def extract_topics_and_summarize(all_text: str, num_topics: int = 5, summary_lines: int = 3) -> dict:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        # Fallback to heuristic
        return extract_topics_heuristic(all_text, num_topics, summary_lines)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    prompt = f"Analyze the following news articles and identify the top {num_topics} topics. For each topic, provide a {summary_lines}-line summary. Format as: Topic 1: [summary]\n\nTopic 2: [summary]\n\nArticles:\n{all_text[:3000]}"
    
    data = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that analyzes news articles."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 1000,
        "temperature": 0.5
    }
    
    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        content = response.json()["choices"][0]["message"]["content"].strip()
        
        # Parse the response
        topics = {}
        parts = content.split("\n\n")
        for part in parts:
            if ": " in part:
                topic, summary = part.split(": ", 1)
                topics[topic.strip()] = summary.strip()
        
        return topics if topics else {"Summary": content}
    except Exception as e:
        # Fallback
        return extract_topics_heuristic(all_text, num_topics, summary_lines)


def extract_topics_heuristic(all_text: str, num_topics: int = 5, summary_lines: int = 3) -> dict:
    # Simple fallback: extract keywords and summarize
    words = re.findall(r'\b\w{4,}\b', all_text.lower())
    word_freq = {}
    for word in words:
        if word not in ['that', 'with', 'from', 'this', 'they', 'have', 'been', 'will', 'said', 'were']:
            word_freq[word] = word_freq.get(word, 0) + 1
    
    top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:num_topics]
    
    topics = {}
    for i, (word, freq) in enumerate(top_words, 1):
        # Simple summary
        sentences = re.split(r"(?<=[.!?])\s+", all_text)
        relevant = [s for s in sentences if word in s.lower()][:summary_lines]
        summary = " ".join(relevant) if relevant else f"Topic related to {word}."
        topics[f"Topic {i}: {word.title()}"] = summary
    
    return topics


def summarize_text(text: str, max_sentences: int = 3) -> str:
    # Keep for fallback or individual
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    sentences = [s.strip() for s in sentences if s.strip()]
    return " ".join(sentences[:max_sentences])


def summarize_article(article: Article, max_sentences: int = 3) -> str:
    return summarize_text(article.text, max_sentences)
