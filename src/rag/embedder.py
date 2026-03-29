from sentence_transformers import SentenceTransformer
class Embedder:
    def __init__(self,model ="all-MiniLM-L6-v2"):
       self.model = SentenceTransformer(model)

    def embed(self,text:str) -> list[float]:
      return self.model.encode(text).tolist()
        
        
    def embed_batch(self,text:list[str])-> list[list[float]]:
        return self.model.encode(text).tolist()