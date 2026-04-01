from src.rag.embedder import Embedder
from src.rag.vector_store import VectorStore
from src.rag.llm import LLM
from src.rag.prompts import RAG_PROMPT
from src.logger import get_logger

class SimpleRAG:
    def __init__(self, embedder : Embedder, store: VectorStore, llm: LLM):
        self.embedder = embedder
        self.store = store
        self.llm = llm
        self.logger = get_logger(__name__)
        

    def ask(self, question: str , top_k : int = 4, filter : str|None = None):
        self.logger.info(f"Received question : {question}")
        try:
            system_prompt = "You are a precise financial analyst. Only use provided context."

            question_embedding = self.embedder.embed(question)
            results = self.store.search(question_embedding, top_k, filter)
            if not results:
                self.logger.warning("No chunks retrieved for question")
                return {
                    "question": question,
                    "answer": "No relevant documents found for your question.",
                    "sources": []
                }

            context = "\n".join(
                f"[{r['id']}] {r['text']}" for r in results
            )



            return {
        "question": question,
        "answer": self.llm.generate(
    system_prompt=system_prompt,
    user_prompt=RAG_PROMPT.format(context=context, question=question)
),
        "sources": [
            {
                "chunk_id": r["id"],
                "text": r["text"][:200],
                "metadata": r["metadata"],
                "relevance": 1 - r["distance"]
            }
            for r in results
        ]
    }
    
        except Exception as e :
            self.logger.error("Error in RAG pipeline", exc_info=True)
            raise
