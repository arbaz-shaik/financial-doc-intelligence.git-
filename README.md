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

# Phase 2

# # Data Pipeline

## Overview

This pipeline is used to grab data from sources using their APIs, clean the HTML, extract the text, then split them into chunks and store those chunks with metadata.

## Architecture

```
Data Sources → SEC Client / News Client API → Parser → Chunker → Store
```

## Data Sources

### 1. SEC EDGAR

We did it in 2 steps — fetch then download.

This source gives company filings by ticker or CIK number. With this API the system can pull any section from quarterly and annual reports.

**Access income statements, balance sheets and cash flow statements in just three lines of Python code:**

```python
from sec_api import XbrlApi

xbrlApi = XbrlApi("YOUR_API_KEY")
xbrl_json = xbrlApi.xbrl_to_json(htm_url="sec.gov/.../aapl-20200926.htm")

print(xbrl_json["StatementsOfIncome"])
print(xbrl_json["BalanceSheets"])
print(xbrl_json["StatementsOfCashFlows"])
```

**Implement the Download API in seconds and gain access to the entire EDGAR database:**

```python
from sec_api import RenderApi

renderApi = RenderApi(api_key="YOUR_API_KEY")
filing_content = renderApi.get_filing("sec.gov/.../tm2119986d1_8k.htm")
print(filing_content)
```

### 2. NewsAPI

This API gives us real-time news and headlines in JSON format.

```python
date = datetime.today() - timedelta(days=days_back)
response = httpx.get(
    "https://newsapi.org/v2/everything",
    params={
        "q": query,
        "from": date.strftime("%Y-%m-%d"),
        "sortBy": "popularity",
        "apiKey": self.api_key,
    },
)
```

## Pipeline Steps

### 1. Fetching

This fetches the data from real-time sources.

**SEC EDGAR:**

1. First we fetch their recent filings, accession number, and primary documents.
2. Then using this formatted URL it downloads the data:

```python
url = f"https://www.sec.gov/Archives/edgar/data/320193/{filing['accessionNumber'].replace('-', '')}/{filing['primaryDocument']}"
print(url)
output_dir = Path("data/raw")
```

### 2. Parsing & Cleaning

We pass the fetched data to the parser and it uses BeautifulSoup to remove the `<script>` tags from the HTML and keep the text. This returns a string.

### 3. Chunking

This is the most interesting and important part of the pipeline. The main objective is to take the string and convert it into a list of objects (chunks) with metadata.

1. First we create a dataclass for a chunk with its metadata.
2. Then a Chunker class which takes chunk size and overlap as parameters.
3. The Chunker class takes the metadata and string, splits the text with the given chunk size and overlap, then appends each chunk to a list and returns the list of chunks.

### 4. Storing the Chunks

It has 2 methods — save chunks and load chunks. This gets interesting here because we can't convert the list directly to a JSON object.

- **`save_chunks()`** — Takes a list of chunks and a filename. Converts each chunk to a dict using `asdict()` and writes it to a file using `json.dumps()`.
- **`load_chunks()`** — Loads JSON objects from the file, converts each object using `json.loads(line)`, appends them to a list, and returns the list.
- **`stats()`** — Returns a dict of stats:

```python
{
    "total_chunks": len(chunks),
    "by_source": by_source,
    "by_company": by_company
}
```

And finally a `run.py` which connects the pipeline.

## How to Run

```bash
# Full ingestion
make ingest

# Specific source only
python -m pipeline.run --mode sec --companies AAPL

# Multiple companies
python -m pipeline.run --mode sec --companies AAPL,MSFT
```

**Example output:**

```
Processing SEC filing for AAPL...
Processing 72 news articles for AAPL...
{'total_chunks': 2225, 'by_source': {'sec': 1928, 'news': 297}, 'by_company': {'AAPL': 2225}}
```

```bash
# View stats
python -m pipeline.run --stats
```

```
Processing SEC filing for AAPL...
Processing 72 news articles for AAPL...
{'total_chunks': 1671, 'by_source': {'sec': 1446, 'news': 225}, 'by_company': {'AAPL': 1671}}
```

## Configuration

| Variable | Default | Description |
| --- | --- | --- |
| `CHUNK_SIZE` | 512 | Characters per chunk |
| `CHUNK_OVERLAP` | 50 | Overlap between chunks |
| `NEWS_API_KEY` | — | Required for news fetching |

## Error Handling

| Failure Type | How It's Handled |
| --- | --- |
| API timeout (SEC / NewsAPI) | Retries up to 3 times with exponential backoff, then skips |
| HTTP errors (4xx / 5xx) | Logs the status code and skips the document |
| Corrupt HTML / PDF | Logs a `ParseError`, skips the file, continues |
| Empty or too-short text | Skipped at chunking stage (minimum length threshold) |
| Missing metadata fields | Defaults applied where safe; logged as warning |

## what i learned:
    this phase taught me alot and took mode of my time :
    I learned how to fecth and clean the data from the servers using api key. 
    learned how parse the data using beautiful soup.
    learned how to chunk and the data and store them.
    most impoertant how to build this data pipline 
    
    and my concepts related to chunking beautifulsoup and class became alot clearer. 
