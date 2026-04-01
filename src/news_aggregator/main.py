import argparse
from .fetcher import fetch_articles
from .filter import filter_articles
from .summarizer import summarize_article


def main() -> int:
    parser = argparse.ArgumentParser("News Aggregator")
    parser.add_argument("--urls", nargs="+", required=True, help="News article URLs")
    parser.add_argument("--keywords", nargs="*", default=[], help="Keywords for interest filtering")
    parser.add_argument("--summary-sentences", type=int, default=3, help="Summary length in sentences")
    args = parser.parse_args()

    print("Fetching articles...")
    articles = fetch_articles(args.urls)
    print(f"Fetched {len(articles)} articles")

    selected = filter_articles(articles, args.keywords)
    print(f"Filtered {len(selected)} articles using keywords: {args.keywords}")

    for idx, article in enumerate(selected, 1):
        summary = summarize_article(article, args.summary_sentences)
        print("---")
        print(f"Article {idx}: {article.title}")
        print(f"URL: {article.url}")
        print("Summary:")
        print(summary)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
