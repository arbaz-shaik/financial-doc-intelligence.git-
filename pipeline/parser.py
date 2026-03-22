from bs4 import BeautifulSoup
import re
from pathlib import Path
from src.logger import get_logger
logger = get_logger(__name__)

class DocumentParser:
        def parse_html(self, raw_html: str) -> str:
            try: 
                soup = BeautifulSoup(raw_html, "html.parser")
                for tag in soup(["script", "style"]):
                    tag.decompose()
                text = soup.get_text(separator="\n")   
                text = re.sub(r'\n{3,}', '\n\n', text)   
                text = re.sub(r' {2,}', ' ', text) 
                return text
            except Exception as e:
                logger.error(f"parsing error {e}")
                return ""
                
if __name__ == "__main__":
    parser = DocumentParser()
    with open("data/raw/AAPL-10K-2025-09-27.html", "r", encoding="utf-8") as f:
        raw_html = f.read()
    text = parser.parse_html(raw_html)
    Path("data/processed").mkdir(parents=True, exist_ok=True)
    with open("data/processed/AAPL-10K-2025-09-27.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print("Parsed text saved to data/processed/AAPL-10K-2025-09-27.txt")