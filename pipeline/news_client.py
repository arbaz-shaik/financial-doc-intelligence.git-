from datetime import datetime, timedelta
import httpx
from pipeline.chunker import Chunker


class NewsClient:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch_news(self, query: str, days_back: int = 30) -> list[dict]:
        date = datetime.today() - timedelta(days=days_back)
        response = httpx.get(
            "https://newsapi.org/v2/everything",
            params={
                "q": query,
                "from": date.strftime("%Y-%m-%d"),
                "sortBy": "popularity",
                "apiKey": self.api_key,
            },
        )
        results = []
        data = response.json()
      
        for article in response.json()["articles"]:
            results.append({
                "title": article["title"],
                "description": article["description"],
                "url": article["url"],
                "date": article["publishedAt"][:10],
                "text": article["content"] or article["description"],
                "company": query,
            })
        return results


if __name__ == "__main__":
    from src.config import settings

    client = NewsClient(api_key=settings.news_api_key)
    articles = client.fetch_news("Apple",days_back=7)
   

    chunker = Chunker(chunk_size=512, chunk_overlap=50)
    for article in articles[:3]:
        chunks = chunker.chunk_text(article["text"], {
            "source": "news",
            "company": article["company"],
            "doc_type": "news",
            "date": article["date"],
            "section": None
        })
        print(f"\n{article['title']}: {len(chunks)} chunks")