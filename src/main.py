from datetime import UTC, datetime

from fastapi import FastAPI, HTTPException
from src.models import CompanyResponse , Company, QuestionRequest
from src.storage import CompanyStore
from src.config import settings
from src.logger import get_logger
from fastapi.responses import JSONResponse
from src.rag.embedder import Embedder
from src.rag.vector_store import VectorStore
from src.rag.llm import LLM
from src.rag.qa import SimpleRAG



embedder = Embedder()
llm = LLM()
vector_store = VectorStore()
store = CompanyStore()
rag = SimpleRAG(embedder= embedder, store= vector_store, llm= llm)

app =FastAPI(title=settings. API_NAME)
logger = get_logger(__name__)




@app.get("/health")
async def root():
    logger.info("Health check requested")
    return{"status":"Healthy"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello, {name}!"}

@app.get("/companies")
async def get_companies():
    results = store.list_all()
    return {"results": results, "count": len(results)}

@app.post("/companies/ask/")
async def ask(request: QuestionRequest):
    result = rag.ask(
        question=request.question,
        top_k=request.top_k,
        filter=request.source_filter,
        date_from=request.date_from
    )
    return result

@app.post("/companies", response_model=CompanyResponse)
async def new_company(company: Company):
    store.add(company.ticker, company)
    return CompanyResponse(company=company, added_at=datetime.now(UTC).isoformat())



@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    logger.error(f"An error occurred: {str(exc)}")
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

@app.get("/companies/search/")
async def search_companies(sector:str = None, name:str = None):
    if sector:
        results= store.search_by_sector(sector)
    elif name:
        results= store.search_by_name(name)   
    else:
        results= []
    return {"results": results, "count" :len(results)}



@app.get("/companies/{ticker}")
async def get_company(ticker:str):
    company = store.get(ticker)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

        
    