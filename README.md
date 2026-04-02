# News Aggregator (Python)

This workspace provides a minimal news aggregator that:
- downloads articles from provided news URLs,
- extracts top topics using AI,
- creates summaries for each topic.

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
3. Set OpenAI API key:
   ```bash
   export OPENAI_API_KEY="your-key-here"
   ```
4. Run with sample URLs:
   ```bash
   python -m news_aggregator.main --urls $(cat urls.txt) --num-topics 5 --summary-lines 3
   ```

## Website Generation

The project includes GitHub Actions to automatically generate a website with daily news summaries.

### Setup
1. In your GitHub repo, go to Settings > Secrets and variables > Actions.
2. Add a new repository secret named `OPENAI_API_KEY` with your OpenAI API key.
3. Go to Settings > Pages, set source to "Deploy from a branch", select `gh-pages` branch.
4. Push the code; the action will run and deploy the site.

The website updates daily at noon UTC, or manually via Actions tab.

## Structure

- `src/news_aggregator/fetcher.py`: URL fetching + parsing
- `src/news_aggregator/summarizer.py`: AI topic extraction and summarization
- `src/news_aggregator/main.py`: CLI orchestration
- `urls.txt`: List of news URLs
- `.github/workflows/deploy.yml`: GitHub Actions for website

