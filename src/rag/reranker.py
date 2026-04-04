from src.rag.llm import LLM
class Reranker:

    def __init__(self, llm : LLM):
        self.llm = llm
        
    def rerank(self, question: str, chunks: list[dict], top_k: int = 5) -> list[dict]:
        if not chunks:
            return []

        chunk_list = "\n\n".join(
            f"[{i}] {c['text'][:300]}" for i, c in enumerate(chunks)
        )

        prompt = f"""Question: {question}

    Chunks:
    {chunk_list}

    Rank these chunks by relevance to the question.
    Return ONLY a comma-separated list of chunk numbers, most relevant first.
    Example output: 3,1,0,4,2"""

        response = self.llm.generate(
            system_prompt="You are a relevance ranker. Output only comma-separated numbers. No explanation.",
            user_prompt=prompt
        )

        try:
            indices = [int(x.strip()) for x in response.split(",")]
            return [chunks[i] for i in indices if i < len(chunks)][:top_k]
        except (ValueError, IndexError):
            return chunks[:top_k]  