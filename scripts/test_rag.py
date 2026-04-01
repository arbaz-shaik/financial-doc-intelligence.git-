from src.rag.qa import SimpleRAG
from src.rag.embedder import Embedder 
from src.rag.vector_store import VectorStore
from src.rag.llm import LLM

def test_rag():
   q1="What are Apple's main risk factors?"
   q2="What did Apple report about iPhone revenue?"
   q3="What is Apple's services business strategy?"
   q4="What recent news has been reported about Apple?"
   embedder = Embedder()
   store = VectorStore()
   llm = LLM()
   rag= SimpleRAG(embedder,store,llm)
   questions = [q1, q2, q3, q4]
   for q in questions:
        result = rag.ask(q)
        print(f"\nQ: {q}")
        print(f"A: {result['answer'][:300]}")
        print(f"Sources: {len(result['sources'])} chunks used")
        print(f"Top source: {result['sources'][0]['chunk_id']}")

if __name__ =="__main__":
   test_rag()

    




