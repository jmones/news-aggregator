# News Aggregator (Python)

This workspace provides a minimal news aggregator that:
- downloads articles from provided news URLs,
- filters items based on your interests,
- creates simple summaries.

## Quick start

1. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run with sample URLs and keywords:
   ```bash
   python -m news_aggregator.main --urls https://example.com/news1 https://example.com/news2 --keywords AI machine learning --summary-sentences 3
   ```

## Structure

- `src/news_aggregator/fetcher.py`: URL fetching + parsing
- `src/news_aggregator/filter.py`: interest filtering
- `src/news_aggregator/summarizer.py`: summary extraction
- `src/news_aggregator/main.py`: CLI orchestration

