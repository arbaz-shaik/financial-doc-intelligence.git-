from dataclasses import dataclass
@dataclass
class Chunk:
    text : str
    chunk_id : str
    source : str
    company : str
    doc_type : str
    date : str
    section : str|None
    chunk_index : int
    total_chunks : int

class Chunker:
    def __init__(self, chunk_size:int, chunk_overlap:int):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    try:
        def chunk_text(self, text: str, metadata: dict) -> list[Chunk]:
            chunks =[]
            start =0
            while start < len(text):
                end = min(start + self.chunk_size, len(text))
                chunk_text = text[start:end]
                chunk_id = f"{metadata['company']}-{metadata['doc_type']}-chunk-{len(chunks):04d}"
                if end < len(text):
                    last_period = chunk_text.rfind(".")
                    if last_period != -1:
                        end = start + last_period + 1
                        chunk_text = text[start:end]
                chunks.append(Chunk(
                    text=chunk_text,
                    chunk_id=chunk_id,
                    source=metadata['source'],
                    company=metadata['company'],
                    doc_type=metadata['doc_type'],
                    date=metadata['date'],
                    section=metadata['section'],
                    chunk_index=len(chunks),
                    total_chunks=0
                ))
                start += self.chunk_size - self.chunk_overlap
            for chunk in chunks:
                chunk.total_chunks = len(chunks)
            return chunks
    except Exception:
        print ("")

if __name__ == "__main__":
    chunker = Chunker(chunk_size=512, chunk_overlap=50)
    with open("data/processed/AAPL-10K-2025-09-27.txt", "r", encoding="utf-8") as f:
        text = f.read()
    
    metadata = {
        "source": "sec",
        "company": "AAPL",
        "doc_type": "10-K",
        "date": "2025-09-27",
        "section": None
    }
    
    chunks = chunker.chunk_text(text, metadata)
    for chunk in chunks[100:103]:
        print(chunk.text[:200])
        print("---")

