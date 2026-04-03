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
- ChromaDB
- sentence-transformers
-  Groq


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
POST ask | /companies/ask/         | post the question

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

# Phase 3
## The flow 

embed question -> ChromaDB finds similar chunks ->reranker scores them ->LLM generates answer with citations.


## key features
Key Features

Semantic search using ChromaDB for efficient vector retrieval

LLM-based reranking to improve result relevance

Citation-backed responses for transparency and traceability

Date and source-based filtering for precise context selection

Multiple prompt variants for robust evaluation and performance testing


# # Response

```json
{
  "question": "What are Apple's main risk factors?",
  "answer": "Based on the provided context, Apple's main risk factors include:\n\n1. Supply shortages and price increases [AAPL-10-K-chunk-0128]\n2. Design and manufacturing defects that could harm the Company's reputation [AAPL-10-K-chunk-0202]\n3. Risks related to the collection, use, protection, and transfer of personal data [AAPL-10-K-chunk-0176]\n4. Litigation or government investigations with uncertain outcomes [AAPL-10-K-chunk-0090]\n5. Political events, trade and other international disputes, geopolitical tensions, conflict, terrorism, natural disasters, public health issues, industrial accidents, and other business interruptions [AAPL-10-K-chunk-0083]\n\nThese risk factors could materially adversely affect the Company's business, results of operations, financial condition, and stock price. [AAPL-10-K-chunk-0128], [AAPL-10-K-chunk-0202], [AAPL-10-K-chunk-0176], [AAPL-10-K-chunk-0090] \n\nNote that the context does not provide a comprehensive or prioritized list of risk factors, but rather highlights various potential risks that could impact the Company.",
  "sources": [
    {
      "chunk_id": "AAPL-10-K-chunk-0128",
      "text": "remains subject to significant risks of supply shortages and price increases that can materially adversely affect its business, results of operations, financial condition and stock price.\nApple Inc. |",
      "metadata": {
        "company": "AAPL",
        "date": "2025-09-27",
        "source": "sec",
        "section": "unknown",
        "doc_type": "10-K"
      },
      "relevance": 0.6451178789138794
    },
    {
      "chunk_id": "AAPL-10-K-chunk-0202",
      "text": "the Company’s products and services, and result in harm to the Company’s reputation, loss of competitive advantage, poor market acceptance, reduced demand for products and services, lost sales, and lo",
      "metadata": {
        "date": "2025-09-27",
        "doc_type": "10-K",
        "source": "sec",
        "section": "unknown",
        "company": "AAPL"
      },
      "relevance": 0.6184186935424805
    },
    {
      "chunk_id": "AAPL-10-K-chunk-0176",
      "text": " the Company’s cost of sales and operating expenses, materially adversely affecting the Company’s business, results of operations, financial condition and stock price. Additionally, such agreements ma",
      "metadata": {
        "date": "2025-09-27",
        "doc_type": "10-K",
        "section": "unknown",
        "company": "AAPL",
        "source": "sec"
      },
      "relevance": 0.590640664100647
    },
    {
      "chunk_id": "AAPL-10-K-chunk-0090",
      "text": "ther impacts can materially adversely affect the Company’s business, results of operations, financial condition and stock price.\nApple Inc. | 2025 Form 10-K | 5\nThe Company’s business can be impacted ",
      "metadata": {
        "source": "sec",
        "section": "unknown",
        "date": "2025-09-27",
        "doc_type": "10-K",
        "company": "AAPL"
      },
      "relevance": 0.5880309343338013
    },
    {
      "chunk_id": "AAPL-10-K-chunk-0083",
      "text": "10-K is not incorporated by reference into this filing. Further, the Company’s references to website URLs are intended to be inactive textual references only.\nApple Inc. | 2025 Form 10-K | 4\nItem 1A. ",
      "metadata": {
        "section": "unknown",
        "company": "AAPL",
        "date": "2025-09-27",
        "doc_type": "10-K",
        "source": "sec"
      },
      "relevance": 0.5772899389266968
    }
  ]
}
```

## what i learned.

I learned how to use embedding models such as all-MiniLM-L6-v2 to convert text into vector representations. I also understood how vectors are grouped based on similarity and how cosine similarity is used to measure the closeness between vectors, enabling effective filtering of relevant results.
One key insight from using a reranker is that some text chunks may appear similar at a surface level but do not actually provide meaningful context for the question. The reranker addresses this by reordering retrieved chunks based on their true relevance to the query, improving the quality of the final results.
The most challenging issue I faced was implementing complex filtering logic using $and conditions within the query, particularly when applying them through the where clause.