# ⚖️ Legal GraphRAG — AI-Powered Contract Review

Legal GraphRAG is an application for exploring and reviewing legal contracts with retrieval-augmented generation (RAG), hybrid search, and a Neo4j knowledge graph. It extracts text from PDF contracts, retrieves relevant evidence, and uses an agent-based workflow to produce answers grounded in the available contract content.

The project supports two main workflows: asking questions about contracts from the CUAD dataset, and uploading a PDF to ask questions about that document. The upload workflow includes human-review checkpoints for evidence and the generated answer.

> **Important:** This is a legal-research and contract-review aid, not a substitute for advice from a qualified legal professional. Always verify outputs against the original contract.

---

## 🌐 Live Demo & API Documentation

- **Live application:** [Open Legal GraphRAG](https://legalassistantwitheval-vj49.onrender.com)
- **API documentation (Swagger):** [Explore API endpoints](https://legalassistantwitheval-vj49.onrender.com/docs)
- 
The service is hosted on Render. The first request after a period of inactivity may take longer while the service starts. The application also relies on a Neo4j database, which must be running for graph-backed operations to work.

## 👩‍💻 Contributor

- **Sowmya Bhupatiraju**

---

## ✨ Features

- **Contract question answering:** Ask questions about contracts and retrieve relevant supporting text.
- **CUAD dataset workflow:** Select a contract from the CUAD collection and ask questions about its provisions.
- **Upload and Ask:** Upload a PDF contract and query the document.
- **Hybrid retrieval:** Combines semantic retrieval from ChromaDB with lexical search to help find relevant contract passages.
- **Knowledge graph integration:** Uses Neo4j to represent and query relationships relevant to the GraphRAG workflow.
- **PDF text extraction:** Extracts text from PDFs and includes an OCR fallback for scanned or low-text pages.
- **Agent-based pipeline:** Uses LangGraph to route questions, review retrieved evidence, and synthesize an answer.
- **Human-in-the-loop review:** The upload workflow provides an evidence checkpoint and an answer checkpoint. Depending on the workflow state, reviewers can approve, revise, or reject the answer.
- **API access:** FastAPI exposes the application's endpoints and provides interactive API documentation through Swagger UI.
- **Evaluation utilities:** The repository includes CUAD/RAGAS evaluation tooling for offline evaluation and experimentation.

---

## 🧭 Application Workflows

### 1. Ask CUAD

1. Open the live application and select a contract from the available CUAD contracts.
2. Enter a question about the selected contract.
3. The application retrieves relevant passages and generates an answer based on the contract evidence.
4. Review the answer and its evaluation information when provided.

Contract data may be ingested when it is first needed. An un-ingested contract can therefore require additional time on its first request.

### 2. Upload and Ask

1. Upload a PDF contract.
2. Enter a question about the uploaded document.
3. Review the retrieved evidence at the evidence checkpoint.
4. Review the proposed answer at the answer checkpoint. The workflow supports approval, revision, or rejection according to the available controls.

---

## 🏗️ Architecture Overview

```text
PDF Contract / CUAD Contract
            │
            ▼
    PDF Text Extraction
 (OCR fallback when needed)
            │
            ▼
       Chunking & Metadata
            │
      ┌─────┴───────────┐
      ▼                 ▼
 ChromaDB           Neo4j Graph
 Semantic Search    Relationships
      │                 │
      └──────┬──────────┘
             ▼
     Hybrid Retrieval
 (semantic + lexical search)
             │
             ▼
   LangGraph Agent Pipeline
  routing → evidence review
  → answer synthesis/review
             │
             ▼
        Final Response
```

The diagram is a high-level overview. The exact path used for a question depends on the selected workflow and routing decisions in the application.

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|---|---|---|
| API and web server | FastAPI, Uvicorn | Serves the API and web console. |
| Agent workflow | LangGraph | Coordinates routing, retrieval, auditing, and answer synthesis. |
| Language model | `openai/gpt-oss-20b` through the configured model API | Generates and synthesizes answers from retrieved evidence. |
| Vector database | ChromaDB | Stores document chunks and their embeddings for semantic retrieval. |
| Embeddings | FastEmbed, `sentence-transformers/all-MiniLM-L6-v2` model family | Encodes text for semantic retrieval. |
| Lexical retrieval | BM25 | Helps retrieve passages using exact terms and keywords. |
| Knowledge graph | Neo4j | Stores and queries relationships used by the graph-backed workflow. |
| PDF processing | pdfplumber, Tesseract OCR, pdf2image/Poppler | Extracts PDF text and supports OCR for scanned pages. |
| Evaluation tooling | CUAD utilities, RAGAS | Supports dataset-based evaluation and experimentation. |
| Packaging | Docker, Docker Compose | Builds and runs the application and local Neo4j service. |
| Hosting | Render | Hosts the live application. |

The model API and database credentials are configured through environment variables. Use the repository's `.env.example` as the source of truth for the variables required by the current checkout.

---

## 📂 Project Structure

```text
LegalAssistantWithEval/
├── .env.example                 # Template for local environment variables
├── .gitignore
├── Dockerfile                   # Container build and runtime configuration
├── docker-compose.yml           # App + local Neo4j services
├── requirements.txt             # Python dependencies
├── pyproject.toml               # Package and test configuration
├── frontend/
│   └── index.html               # Web console
├── src/legal_graphrag/
│   ├── api/
│   │   ├── main.py              # FastAPI application entry point
│   │   └── cuad_routes.py       # CUAD-related API routes
│   ├── agents/
│   │   ├── legal_pipeline.py    # Main LangGraph query workflow
│   │   └── prompts.py            # Agent prompts
│   ├── ingestion/
│   │   ├── pdf_pipeline.py      # PDF extraction, chunking, and vector storage
│   │   └── langgraph_agent.py   # Ingestion workflow
│   ├── retrieval/
│   │   ├── contract_metadata.py # Contract metadata extraction
│   │   └── hybrid_search.py     # Semantic and lexical retrieval
│   ├── graphrag/
│   │   ├── neo4j_store.py       # Neo4j operations
│   │   ├── extraction.py        # Graph extraction and query utilities
│   │   └── langgraph_agent.py   # GraphRAG workflow components
│   ├── evaluation/              # Evaluation utilities
│   ├── config.py                # Application configuration
│   ├── llm_client.py            # Language-model API client
│   └── resources.py              # Shared database and embedding resources
├── scripts/
│   ├── run_demo.py              # CLI demo utilities
│   └── run_cuad_eval.py         # CUAD evaluation entry point
├── tests/                       # Automated tests
└── data/
    ├── uploads/                 # Local uploaded PDFs (not committed)
    ├── metadata/                # Local metadata and evaluation output
    └── chroma_db/               # Local ChromaDB data (not committed)
```

> This tree highlights the main application components; small differences may exist between branches or revisions.

---

## 🚀 Run Locally with Docker Compose

### Prerequisites

- Git
- Docker Desktop with Docker Compose
- A model-provider API key configured for the application
- A Neo4j password for the local database, or credentials for a separately managed Neo4j instance

### 1. Clone the repository

```bash
git clone https://github.com/almabetter-school-ds/LegalAssistantWithEval.git
cd LegalAssistantWithEval
```

### 2. Create the environment file

```bash
cp .env.example .env
```

Open `.env` and fill in the required values. In particular, use a strong value for `NEO4J_PASSWORD` and provide the model-provider credentials required by `.env.example`. Keep `.env` private; do not commit API keys or database passwords to GitHub.

### 3. Build and start the services

```bash
docker compose up --build
```

On the first run, Docker may need time to build the image and download model files.

### 4. Open the application

- **Web console:** [http://localhost:8000](http://localhost:8000)
- **Swagger API docs:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Health endpoint:** [http://localhost:8000/api/health](http://localhost:8000/api/health)
- **Neo4j Browser:** [http://localhost:7474](http://localhost:7474)

To stop the services, press `Ctrl+C`, or run `docker compose down` in another terminal. The named Docker volumes are used for local Neo4j data and the model cache; the `./data` bind mount stores the application's local data.

### Run the API without Docker (advanced)

If you already have the required Python dependencies and a reachable Neo4j instance configured, activate your virtual environment, install the requirements, and start Uvicorn:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=src uvicorn legal_graphrag.api.main:app --host 0.0.0.0 --port 8000
```

The PDF pipeline may also require the operating-system packages `tesseract-ocr` and `poppler-utils` for OCR support. On macOS, install the equivalent packages with your preferred package manager if needed.

---

## 🔌 API Documentation

The interactive Swagger documentation lists the routes, request schemas, and response formats exposed by the running version of the API:

- **Production:** [https://legalassistantwitheval-vj49.onrender.com/docs](https://legalassistantwitheval-vj49.onrender.com/docs)
- **Local:** [http://localhost:8000/docs](http://localhost:8000/docs)

A simple health check can be run with:

```bash
curl -i https://legalassistantwitheval-vj49.onrender.com/api/health
```

For a complete and current list of endpoints, use Swagger rather than relying on a manually maintained endpoint list in this README.

---

## 📊 Evaluation

The repository includes scripts for running CUAD-oriented evaluation and RAGAS-based experiments. These are intended to help compare generated answers with reference annotations and inspect retrieval/answer quality.

Example command from the repository's evaluation workflow:

```bash
python -m scripts.run_cuad_eval --n-contracts 20 --seed 42 --out data/metadata/cuad_eval_results.json
```

Check the script's available arguments and configure its required dependencies and environment variables before running it. Evaluation can consume additional API usage and compute resources.

**Current live API note:** background RAGAS scoring is not currently enabled in the deployed request workflow. Consequently, an API response may report `metrics_status` as `pending` and may not include metrics. This does not necessarily mean that answer retrieval failed; use the answer, evidence, and HTTP status to inspect the request, and run the evaluation utilities separately when needed.

---

## 🖼️ Interface Preview

The repository's interface supports CUAD contract questions and the upload-and-ask workflow with review checkpoints.

![Legal GraphRAG interface — CUAD workflow](https://github.com/user-attachments/assets/097c2908-9bec-46c4-835e-eabebb2d8140)

![Legal GraphRAG interface — upload and review workflow](https://github.com/user-attachments/assets/daee557f-211b-4bd8-b6c6-46237920df65)

---

## 🧪 Tests

Run the automated tests from the repository root in the configured Python environment:

```bash
pytest
```

If a test needs a live model provider or Neo4j database, configure those dependencies before running that test. Unit tests and live integration checks may have different environment requirements.

---

## 🛠️ Troubleshooting

### The first request is slow

The first request may trigger service startup, model initialization, or on-demand ingestion of a contract. Allow the request to finish before retrying.

### Neo4j connection or DNS error

Confirm that the Neo4j instance is running and that the configured URI, username, and password are correct. For Neo4j Aura, check the Aura console and resume the instance if it has paused. Restart the app after correcting its database configuration if necessary.

### The answer works but `metrics_status` is `pending`

The deployed API currently does not run background RAGAS scoring as part of the request workflow. Use the standalone evaluation script for evaluation instead.

### The local container cannot read or write data

Check that the local `data/` directory and Docker volumes are writable by the container. Do not delete persistent database directories unless you intend to rebuild the local indexes.

---

## 🔐 Security & Responsible Use

- Store API keys and database credentials in environment variables or a private `.env` file.
- Never commit `.env`, access tokens, passwords, or other secrets.
- Review retrieved source passages before relying on an answer, particularly for deadlines, exceptions, amounts, renewal terms, governing law, and party names.
- Treat generated answers as research assistance, not legal advice or a definitive interpretation of a contract.
- Use only documents you are authorized to upload and process.

---

## 📚 Project Deliverables & Documentation

- [Project presentation / overview](https://gamma.app/docs/Legal-Contract-Intelligence-Platform-swcgtvc4mi86m71?mode=doc)
- [Detailed technical documentation](https://docs.google.com/document/d/1u1ATQ1UbCB7MGS4LKG_hHCQiHUTk2tam8LGX71UEXOc/edit?usp=sharing)
- [Live application](https://legalassistantwitheval-vj49.onrender.com)
- [API documentation](https://legalassistantwitheval-vj49.onrender.com/docs)

---

**Legal GraphRAG** — contract exploration and evidence-grounded question answering with hybrid retrieval and graph-backed workflows.
