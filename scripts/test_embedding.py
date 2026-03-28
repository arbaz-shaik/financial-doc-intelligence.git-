from src.rag.embedder import Embedder
import numpy as np
from pipeline.store import ChunkStore

def cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
    a = np.array(vec1)
    b = np.array(vec2)

    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return np.dot(a, b) / (norm_a * norm_b)


def test():

    store = ChunkStore("data/chunks")
    chunks =  store.load_all_chunks()
    text1 = chunks[100]["text"]
    text2 = chunks[101]["text"]
    text3 = chunks[200]["text"]
    embedder = Embedder()

    embedding_text1 = embedder.embed(text1)
    embedding_text2 = embedder.embed(text2)
    embedding_text3 = embedder.embed(text3)


    similarity_12= cosine_similarity(embedding_text1, embedding_text2)
    
    similarity_23 = cosine_similarity(embedding_text2, embedding_text3)

    # out curiosity 
    similarity_11= cosine_similarity(embedding_text1, embedding_text1)

    print(f" similarity between chunk 1 and 2{similarity_12}")
    print(f" similarity between chunk 2 and 2{similarity_23}")
    print(f" similarity between chunk 1 and 1{similarity_11}")





    sentence_a = "I love learning machine learning"
    sentence_b = "I enjoy studying AI and machine learning"
    sentence_c = "The weather is very hot today"

    embedding_a = embedder.embed(sentence_a)
    embedding_b = embedder.embed(sentence_b)
    embedding_c = embedder.embed(sentence_c)

    similarity_ab = cosine_similarity(embedding_a, embedding_b)
    similarity_ac = cosine_similarity(embedding_a, embedding_c)

    print(f"A vs B (similar): {similarity_ab:.4f}")
    print(f"A vs C (different): {similarity_ac:.4f}")


if __name__ == "__main__":
    test()