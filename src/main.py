from fastapi import FastAPI, HTTPException
from src.models import CompanyResponse , Company
from src.storage import CompanyStore
from src.config import settings

store = CompanyStore()

app =FastAPI(title=settings. API_NAME)

@app.get("/health")
async def root():
    return{"status":"Healthy"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello, {name}!"}

@app.get("/companies")
async def get_companies():
    return {"companies": ["Company A", "Company B", "Company C"]}

@app.post("/companies", response_model=CompanyResponse)
async def new_company(company: Company):
    store.add(company.ticker, company)
    return CompanyResponse(company=company, added_at="2024-06-01T12:00:00Z")

@app.get("/companies/{ticker}")
async def get_company(ticker:str):
    company  = store.get(ticker)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company