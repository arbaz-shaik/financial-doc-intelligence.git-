from src.rag.llm import LLM
class Reranker:

    def __init__(self, llm : LLM):
        self.llm = llm
       

    def rerank(self, question: str, chunks: list[dict], top_k: int = 5) -> list[dict]:

        if not chunks:
            return []

        chunk_list = "/n/n".join(
                f"[{i}], {c["text"][:300]}" for i, c in enumerate(chunks)
            )
        
        prompt = f"""Question, {question}
        Chunk = {chunk_list}

Rank these chunks by relevance to the question.
Return ONLY a comma-separated list of chunk numbers, most relevant first.
Example output: 3,1,0,4,2"


"""

     


            
       

        scored_chunks =[]
        system_prompt = """
                You are a strict relevance evaluator.

                Given a question and a chunk, rate how relevant the chunk is for answering the question.

                Rules:
                - Use only the provided question and chunk.
                - Do not use external knowledge.
                - Be strict in scoring.

                Output only a single integer from 1 to 10.

                Do not include any explanation or extra text.

                """
        prompt = """
                Question:
                {question}

                Chunk:
                {chunk}

                Task:
                Rate how relevant the chunk is for answering the question.

                Scale:
                1 = not relevant at all
                10 = directly answers the question

                Output only a single integer (1-10).
                """



        for chunk in chunks:
            
            user_prompt = prompt.format(question= question, chunk = chunk["text"])
            response = self.llm.generate(system_prompt, user_prompt).strip()
            try:
                score = int(response)
            except ValueError:
                score = 5  # Default score if parsing fails

            scored_chunks.append({"chunk": chunk, "score": score})


        scored_chunks.sort(key=lambda x: x["score"], reverse=True)

        reranked_chunks = [item["chunk"] for item in scored_chunks]


                

        return reranked_chunks[:top_k]


            

    

    