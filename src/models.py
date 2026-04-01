from pydantic import BaseModel, Field
class Company(BaseModel):
    name: str
    ticker: str= Field(max_length=5)
    sector: str
    description: str | None = None
  
class CompanyResponse(BaseModel):
    company :Company
    added_at: str

class QuestionRequest(BaseModel) :
    question : str
    top_k : int = 5
    source_filter : str | None = None

class SourceInfo(BaseModel):
    chunk_id : str
    text : str 
    metadata: dict
    relevance : float

class AnswerResponse(BaseModel):
    question: str
    answer : str
    sources : list[SourceInfo]



    