import argparse
from .fetcher import fetch_articles
from .summarizer import extract_topics_and_summarize


def main() -> int:
    parser = argparse.ArgumentParser("News Aggregator")
    parser.add_argument("--urls", nargs="+", required=True, help="News article URLs")
    parser.add_argument("--num-topics", type=int, default=5, help="Number of top topics to extract")
    parser.add_argument("--summary-lines", type=int, default=3, help="Lines per topic summary")
    parser.add_argument("--output", help="Output file for HTML website")
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
        if args.output:
            generate_html(topics, args.output)
            print(f"Website generated at {args.output}")
        else:
            for topic, summary in topics.items():
                print(f"\n--- {topic} ---")
                print(summary)
    except ValueError as e:
        print(f"Error: {e}")
        return 1

    return 0


def generate_html(topics: dict, output_file: str):
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>News Aggregator</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #333; }}
        h2 {{ color: #555; }}
        p {{ line-height: 1.6; }}
    </style>
</head>
<body>
    <h1>Top News Topics</h1>
    <p>Generated on {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
"""
    for topic, summary in topics.items():
        html += f"""
    <h2>{topic}</h2>
    <p>{summary.replace('\n', '<br>')}</p>
"""
    html += """
</body>
</html>
"""
    with open(output_file, 'w') as f:
        f.write(html)


if __name__ == "__main__":
    raise SystemExit(main())
