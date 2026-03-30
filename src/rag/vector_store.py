import chromadb

class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="./data/vectors")
        self.collection = self.client.get_or_create_collection(name="documents", metadata={"hnsw:space": "cosine"})

    def add_chunk(self, chunks: list[dict], embeddings: list[list[float]] ) -> int:
        ids =[]
        metadatas=[]
        documents=[]

        for chunk in chunks :
            ids.append (chunk["chunk_id"])
            documents.append (chunk["text"])
            metadatas.append(
                 {
        "source": chunk.get("source"),
        "company": chunk.get("company"),
        "doc_type": chunk.get("doc_type"),
        "date": chunk.get("date"),
        "section": chunk.get("section") or "unknown"
    
            })
        self.collection.add(
            ids= ids,
            documents = documents,
            metadatas= metadatas,
            embeddings = embeddings
        )

        return len(chunks)
    
    def search(
        self,
        query_embedding: list[float],
        top_k: int | None = 5,
        source_filter: str | None = None,
        company_filter: str | None = None
    ) -> list[dict]:

        where_clause = {}

        if source_filter:
            where_clause["source"] = source_filter

        if company_filter:
            where_clause["company"] = company_filter

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where_clause if where_clause else None
        )

        output = []

        for i in range(len(results["ids"][0])):
            output.append({
                "id": results["ids"][0][i],
                "text": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i]
            })

        return output
            
    def count(self) -> int:
        return self.collection.count()


