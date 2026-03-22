import json

import httpx
from pathlib import Path
from src.config import settings
from src.logger import get_logger
logger = get_logger(__name__)


class SECClient:
    def __init__(self, UserAgent: str) -> None:
        self.base_url = "https://data.sec.gov/submissions/"
        self.headers = {"User-Agent": UserAgent}
    
    def search(self, CIK:str, form:str = "10-K") -> dict:
        try:
            response = httpx.get(self.base_url + f"CIK{CIK}.json", headers=self.headers)
            recent = response.json()["filings"]["recent"]
            results =[]
            for i in range(len(recent["form"])):
                if recent["form"][i] == form:
                    results.append({
                        "accessionNumber": recent["accessionNumber"][i],
                        "filingDate": recent["filingDate"][i],
                        "reportDate": recent["reportDate"][i],
                        "primaryDocument": recent["primaryDocument"][i]
                    })
            return results 
        except httpx.HTTPError as e:
            print(f"HTTP error occurred: {e}")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error occurred: {e}")
            return []

    def download(self, url:str):
        try:
            response = httpx.get(url, headers=self.headers, timeout=30)
            return response.text
        except httpx.ConnectError as e:
            print(f"httpx.ConnectError error occurred: {e}")
            return ""

        except httpx.HTTPError as e:
            logger.error(f"HTTP error occurred: {e}")
            return ""



if __name__ == "__main__": 
    print("Script started")
    client = SECClient(settings.sec_user_agent)
    results = client.search("0000320193")
    filing = results[0]
    url = f"https://www.sec.gov/Archives/edgar/data/320193/{filing['accessionNumber'].replace('-', '')}/{filing['primaryDocument']}"
    print(url)
    output_dir = Path("data/raw")
    output_dir.mkdir(parents=True, exist_ok=True)
    html = client.download(url)
    with open(output_dir / f"AAPL-10K-{filing['reportDate']}.html", "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Saved to data/raw/AAPL-10K-{filing['reportDate']}.html")
