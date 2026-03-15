import httpx
from pathlib import Path
from src.config import settings


class SECClient:
    def __init__(self, UserAgent: str) -> None:
        self.base_url = "https://data.sec.gov/submissions/"
        self.headers = {"User-Agent": UserAgent}

    def search(self, CIK:str, form:str = "10-K") -> dict:
       
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
    
    
    def download(self, url:str):
        response = httpx.get(url, headers=self.headers, timeout=30)
        return response.text


if __name__ == "__main__": 
    print("Script started")
    client = SECClient(settings.sec_user_agent)
    results = client.search("0000320193")
    filing = results[0]
    url = f"https://www.sec.gov/Archives/edgar/data/320193/{filing['accessionNumber'].replace('-','')}/{filing['primaryDocument']}"
    print(url)
    output_dir = Path("data/raw")
    output_dir.mkdir(parents=True, exist_ok=True)
    html = client.download(url)
    with open(output_dir / f"AAPL-10K-{filing['reportDate']}.html", "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Saved to data/raw/AAPL-10K-{filing['reportDate']}.html")
