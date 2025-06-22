import logging
from app import fetch_health_it_news, summarize_news

# Configure logging to see the same logs as the app
logging.basicConfig(level=logging.DEBUG)

def main():
    print("Testing fetch_health_it_news()...")
    articles = fetch_health_it_news()

    if articles:
        print(f"Successfully fetched {len(articles)} articles.")
        # Print details of the first few articles for brevity
        for i, article in enumerate(articles[:2]):
            print(f"Article {i+1} Title: {article.get('title')}")
            print(f"Article {i+1} Category: {article.get('category')}")
            print(f"Article {i+1} Published At: {article.get('publishedAt')}")
            print("---")

        print("\nTesting summarize_news()...")
        # Summarize a subset of articles to speed up testing and reduce API calls
        summary = summarize_news(articles[:5])
        print("\nSummary:")
        print(summary)
    else:
        print("No articles fetched. Check News API key and network connectivity.")

if __name__ == "__main__":
    main()
