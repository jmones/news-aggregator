import argparse
from .fetcher import fetch_articles
from .summarizer import extract_topics_and_summarize


def main() -> int:
    parser = argparse.ArgumentParser("News Aggregator")
    parser.add_argument("--urls", nargs="+", required=True, help="News article URLs")
    parser.add_argument("--num-topics", type=int, default=5, help="Number of top topics to extract")
    parser.add_argument("--summary-lines", type=int, default=3, help="Lines per topic summary")
    args = parser.parse_args()

    print("Fetching articles...")
    articles = fetch_articles(args.urls)
    print(f"Fetched {len(articles)} articles")

    if not articles:
        print("No articles fetched.")
        return 1

    # Combine all article texts
    all_text = "\n\n".join(f"Title: {a.title}\n{a.text}" for a in articles)

    print("Extracting top topics and summarizing...")
    try:
        topics = extract_topics_and_summarize(all_text, args.num_topics, args.summary_lines)
        for topic, summary in topics.items():
            print(f"\n--- {topic} ---")
            print(summary)
    except ValueError as e:
        print(f"Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
