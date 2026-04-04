from src.rag.embedder import Embedder
from src.rag.vector_store import VectorStore
from src.rag.llm import LLM
from src.rag.prompts import RAG_TEST_PROMPT_V3
from src.rag.reranker import Reranker
from src.agent.state import AgentState


embedder = Embedder()
store = VectorStore()
llm = LLM()
reranker = Reranker(llm=llm)
prompt = RAG_TEST_PROMPT_V3


def retrieve(state: AgentState) -> dict:
    #call the embed and to embed the questions
    embed_question = embedder.embed(state['question'])

    #call the store.search to search the relavent chunks
    retrieved_chunks = store.search(query_embedding= embed_question,top_k=state['top_k'],source_filter=state['source_filter'], date_from=state['date_from'])

    #create a ranked chunks function get all reranked chunks
    ranked_chunks = reranker.rerank(question=state['question'], chunks=retrieved_chunks,top_k=state['top_k'])

    #return all reranked chunks
    context ="\n".join(
        f"[{r['id']}] {r['text']}" for r in ranked_chunks
    )

    sources= [
            {
                "chunk_id": r["id"],
                "text": r["text"][:200],
                "metadata": r["metadata"],
                "relevance": 1 - r["distance"]
            }
            for r in ranked_chunks
        ]

    return {
        "embed_question": embed_question,
        "retrieved_chunks": ranked_chunks,
        "context": context,
        "sources": sources
    }

def generate_node(state: AgentState):
   
    
    answer= llm.generate( system_prompt =  "You are a precise financial analyst. Only use provided context.",user_prompt=RAG_TEST_PROMPT_V3.format(context=state['context'], question=state['question'])
   )

    return{
        "answer":answer
    }

def  risk_flagger_node(state: AgentState):
    return{
        "risk_flags": []
    }



    



