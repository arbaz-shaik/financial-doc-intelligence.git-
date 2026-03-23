from pathlib import Path
import json
from dataclasses import asdict
from pipeline.chunker import Chunk
from src.logger import get_logger
logger = get_logger(__name__)

class ChunkStore:
    def __init__(self, directory: str,):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
    
    def save_chunks(self, chunks: list[Chunk], filename: str)->int :
        try:    
            with open(self.directory / f"{filename}.jsonl", "a", encoding="utf-8") as f:
                for chunk in chunks:
                    chunk_dict = asdict(chunk)
                    f.write(json.dumps(chunk_dict) +"\n")
            return len(chunks)
        except PermissionError  as e:
            logger.error(f" permission denied {e}")
            return -1
        except OSError as e:
            logger.error(f"wrong path {e}" )
            return -1

   
    def load_all_chunks(self) -> list[dict]:
        try:
            chunk_list = []
            for filepath in self.directory.glob("*.jsonl"):
                with open(filepath, "r", encoding="utf-8") as f:
                    for line in f:
                        chunk_list.append(json.loads(line))
            return chunk_list
        except FileNotFoundError as e:
            logger.error(f"file not found {e}")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"JSONDecodeError {e} ")
            return []
        
    def stats(self) -> dict:
        chunks = self.load_all_chunks()
        by_source = {}
        by_company = {}
        for chunk in chunks:
            source = chunk["source"]
            company = chunk["company"]
            by_source[source] = by_source.get(source, 0) + 1
            by_company[company] = by_company.get(company, 0) + 1
        return {
            "total_chunks": len(chunks),
            "by_source": by_source,
            "by_company": by_company
        }
            
