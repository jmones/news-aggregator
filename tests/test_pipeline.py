from news_aggregator.fetcher import Article
from news_aggregator.filter import filter_articles
from news_aggregator.summarizer import summarize_text


def test_filter_articles():
    articles = [Article(url="http://x", title="AI startup", text="New advances in AI"), Article(url="http://y", title="Sports", text="Football season")]
    filtered = filter_articles(articles, ["ai"])
    assert len(filtered) == 1


def test_summarize_text():
    text = "The first sentence. The second sentence. Third one."
    summary = summarize_text(text, max_sentences=2)
    assert summary.startswith("The first sentence.")
    assert "The second sentence." in summary
