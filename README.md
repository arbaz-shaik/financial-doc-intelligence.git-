# FINANCIAL DOC INTELLIGENCE

> An end-to-end AI-powered platform that ingests financial documents, answers natural language questions with cited sources, flags risk signals, and serves predictions — deployed on AWS with full CI/CD, monitoring, and evaluation.

> I am doing this project in 6 phases to avoid overcomplicating it and complete it under 40 days.

## The Phases

- [Phase 1 -- REST API](#phase-1--rest-api-days-16)
- [Phase 2 -- Data Pipeline](#phase-2--data-pipeline-days-714)
- [Phase 3 -- RAG Q&A](#phase-3--rag-qa-days-1522)
- [Phase 4 -- LangGraph Agent](#phase-4--langgraph-agent-days-2328)
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

# Data Ingestion Pipeline

## What This Does
[2-3 sentences: what data sources, what processing, what output]

## How to Run

### Setup
[how to install dependencies, set up .env]

### Run the Pipeline
[exact command to run it]

### Run Tests
[exact command]

## Example Output
[paste your stats here — total chunks, by source, by company]

## Project Structure
pipeline/
├── sec_client.py    — [one line description]
├── news_client.py   — [one line description]
├── parser.py        — [one line description]
├── chunker.py       — [one line description]
├── store.py         — [one line description]
└── run.py           — [one line description]

## What I Learned
# Block 2.7 — Error Handling & Logging

## What Was Added

Added try/except error handling and structured JSON logging across all pipeline components.

## Files Modified

| File | Changes |
|------|---------|
| `pipeline/sec_client.py` | try/except for network errors, JSON decode errors. Logger replaces print statements. |
| `pipeline/news_client.py` | try/except for HTTP errors, JSON decode errors. Logger added. |
| `pipeline/parser.py` | try/except for malformed HTML. Logger added. |
| `pipeline/store.py` | try/except for file permissions, missing files, corrupted JSONL. Logger added. |

## Error Handling Strategy

Each method catches specific exceptions and returns a safe default so the pipeline doesn't crash:

| Exception | Where | Safe Default |
|-----------|-------|-------------|
| `httpx.ConnectError` | SEC/News clients | `[]` or `""` |
| `httpx.HTTPError` | SEC/News clients | `[]` or `""` |
| `json.JSONDecodeError` | SEC/News clients, ChunkStore | `[]` |
| `PermissionError` | ChunkStore | `-1` |
| `OSError` | ChunkStore | `-1` |
| `FileNotFoundError` | ChunkStore | `[]` |

## Logging

All pipeline files use the structured JSON logger from Phase 1:

```python
from src.logger import get_logger
logger = get_logger(__name__)

logger.info("Starting fetch for AAPL")
logger.error(f"HTTP error: {e}")
```

## Tests

All 11 tests pass after changes:

```
pytest tests/ -v
====================== 11 passed, 1 warning ======================
```