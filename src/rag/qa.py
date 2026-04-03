from src.rag.embedder import Embedder
from src.rag.vector_store import VectorStore
from src.rag.llm import LLM
from src.rag.prompts import RAG_TEST_PROMPT_V3
from src.logger import get_logger
from src.rag.reranker import Reranker


class SimpleRAG:
    def __init__(self, embedder : Embedder, store: VectorStore, llm: LLM):
        self.embedder = embedder
        self.store = store
        self.llm = llm
        self.logger = get_logger(__name__)
        self.reranker = Reranker(llm =self.llm)
        

    def ask(self, question: str , top_k : int = 4, filter : str|None = None, date_from: str | None = None):

        self.logger.info(f"Received question : {question}")
        try:
            system_prompt = "You are a precise financial analyst. Only use provided context."

            question_embedding = self.embedder.embed(question)
            results = self.store.search(
            query_embedding=question_embedding,
            top_k=top_k,
            source_filter=filter,
            date_from=date_from)
            if not results:
                self.logger.warning("No chunks retrieved for question")
                return {
                    "question": question,
                    "answer": "No relevant documents found for your question.",
                    "sources": []
                }
            
            
            rerank_chunk = self.reranker.rerank(question=question, chunks= results, top_k= top_k )

            context = "\n".join(
                f"[{r['id']}] {r['text']}" for r in rerank_chunk
            )



            return {
        "question": question,
        "answer": self.llm.generate(
    system_prompt=system_prompt,
    user_prompt=RAG_TEST_PROMPT_V3.format(context=context, question=question)
),
        "sources": [
            {
                "chunk_id": r["id"],
                "text": r["text"][:200],
                "metadata": r["metadata"],
                "relevance": 1 - r["distance"]
            }
            for r in rerank_chunk
        ]
    }
    
        except Exception:
            self.logger.error("Error in RAG pipeline", exc_info=True)
            raise
