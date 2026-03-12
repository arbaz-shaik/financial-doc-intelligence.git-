from pydantic import BaseModel, Field
class Company(BaseModel):
    name: str
    ticker: str= Field(max_length=5)
    sector: str
    description: str | None = None
  
class CompanyResponse(BaseModel):
    company :Company
    added_at: str



    