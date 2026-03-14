# FINANCIAL DOC INTELLIGENCE

> An end-to-end AI-powered platform that ingests financial documents, answers natural language questions with cited sources, flags risk signals, and serves predictions — deployed on AWS with full CI/CD, monitoring, and evaluation.

> I am doing this project in 6 phases to avoid overcomplicating it and complete it under 40 days.

## The Phases

- [Phase 1 — REST API](#phase-1--rest-api-days-16)
- [Phase 2 — Data Pipeline](#phase-2--data-pipeline-days-714)
- [Phase 3 — RAG Q&A](#phase-3--rag-qa-days-1522)
- [Phase 4 — LangGraph Agent](#phase-4--langgraph-agent-days-2328)
- [Phase 5 — Cloud Deployment](#phase-5--cloud-deployment-days-2936)
- [Phase 6 — Evaluation & Polish](#phase-6--evaluation--polish-days-3740)

## Architecture

![Architecture](docs/architecture-diagram.png)

## Phase 1

I created API endpoints to get the company name, to set, and to update them. till now we have created 6 endpoints. might go up to 12 as we progress.

## Tech Stack

- Python 3.11
- FastAPI
- Pydantic
- pytest

## How to Run

1. Clone the repo
```bash
git clone https://github.com/your-username/financial-doc-intelligence.git
cd financial-doc-intelligence
```

2. Create a virtual environment
```bash
python -m venv .venv
```

Activate it:
```bash
# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

## How to Test

I used pytest for testing and to avoid writing long commands again and again, I used a Makefile.

If you have make:
```bash
make test
```

Otherwise:
```bash
pytest tests/ -v
```

## API Endpoints

| Method | Endpoint               | Description              |
| ------ | ---------------------- | ------------------------ |
| GET    | /health                | Health check             |
| POST   | /companies             | Add a company            |
| GET    | /companies             | List all companies       |
| GET    | /companies/search/     | Search by sector or name |
| GET    | /companies/{ticker}    | Get company by ticker    |

## What I Learned from Phase 1

- Creating models for validation using Pydantic
- Creating endpoints with FastAPI
- How logging works and why we need it

## What's Next

Phase 2: Data Pipeline — SEC filing ingestion, document parsing, and chunking