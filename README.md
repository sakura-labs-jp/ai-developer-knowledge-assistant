# AI Developer Knowledge Assistant

Engineering knowledge is often scattered across incident reports, architecture decisions, troubleshooting records, and individual experience.

**AI Developer Knowledge Assistant** turns that engineering experience into searchable, reusable knowledge.

It uses Retrieval-Augmented Generation (RAG) to retrieve relevant engineering knowledge from SQL Server and generate grounded answers using Google Gemini.

Instead of relying only on an LLM's general knowledge, the assistant retrieves relevant engineering knowledge first and uses it as context for the generated response.

---

# Architecture

![Architecture](architecture.png)

The system follows a Retrieval-Augmented Generation (RAG) architecture.

```text
User Question
      |
      v
Frontend
      |
      v
FastAPI Backend
      |
      v
Question Embedding
      |
      v
Semantic Retrieval
      |
      v
Cosine Similarity Search
      |
      v
Top-K Knowledge
      |
      v
Context Construction
      |
      v
Google Gemini
      |
      v
Generated Answer + Source
```

When a user submits a question:

1. The question is converted into an embedding vector.
2. The system compares it with stored knowledge embeddings.
3. The top relevant knowledge records are retrieved.
4. Retrieved knowledge is formatted into RAG context.
5. Gemini generates an answer using the retrieved engineering knowledge.
6. The API returns the generated answer together with source information.

---

# 🚀 Current Features

* ✅ FastAPI REST API
* ✅ Google Gemini integration
* ✅ Gemini Embedding integration
* ✅ SQL Server knowledge base
* ✅ Vector embedding storage
* ✅ Embedding-based semantic retrieval
* ✅ Cosine similarity search
* ✅ Top-K knowledge retrieval
* ✅ Retrieval-Augmented Generation (RAG)
* ✅ Context-grounded answer generation
* ✅ Source information with similarity score
* ✅ Idempotent embedding generation using UPSERT
* ✅ Environment-based configuration
* ✅ Layered backend architecture
* ✅ Simple web interface

---

# 🛠 Tech Stack

## Backend

* Python 3.12
* FastAPI
* Pydantic
* Uvicorn

## AI

* Google Gemini
* Gemini Embedding
* Retrieval-Augmented Generation (RAG)
* Semantic Similarity Search
* Cosine Similarity

## Database

* SQL Server
* pyodbc
* Vector embedding storage

## Frontend

* HTML
* CSS
* JavaScript

---

# 🗄 Database Design

The knowledge base is managed using SQL Server.

## Knowledge

The `Knowledge` table stores structured engineering experience used for AI retrieval.

Knowledge records include:

* Category
* Technology
* Title
* Problem
* Analysis
* Solution
* Result
* Lessons Learned
* Keywords
* Difficulty
* CreatedAt
* UpdatedAt

The schema is designed to preserve not only final solutions, but also the troubleshooting process and engineering decisions that led to them.

---

## KnowledgeEmbedding

The `KnowledgeEmbedding` table stores vector representations of knowledge records.

Each embedding contains:

* EmbeddingId
* KnowledgeId
* EmbeddingModel
* EmbeddingVector
* CreatedAt

`KnowledgeId` and `EmbeddingModel` are unique as a pair, preventing duplicate embeddings for the same knowledge record and embedding model.

Embedding generation uses UPSERT behavior, allowing the generation process to be safely rerun without creating duplicate records.

---

# 📂 Project Structure

```text
ai-knowledge-assistant/
│
├── .env.example
├── .gitignore
├── architecture.png
├── README.md
├── requirements.txt
│
├── backend/
│   ├── main.py
│   │
│   ├── database/
│   │   ├── connection.py
│   │   └── schema.sql
│   │
│   ├── models/
│   │   └── chat.py
│   │
│   ├── repositories/
│   │   ├── knowledge_embedding_repository.py
│   │   └── knowledge_repository.py
│   │
│   ├── services/
│   │   ├── embedding.py
│   │   ├── gemini.py
│   │   ├── knowledge_formatter.py
│   │   ├── rag.py
│   │   ├── retrieval.py
│   │   └── similarity.py
│   │
│   └── tools/
│       └── generate_embeddings.py
│
└── frontend/
    ├── app.js
    ├── index.html
    └── style.css
```

---

# Layer Responsibilities

| Layer | Responsibility |
| --- | --- |
| `main.py` | FastAPI endpoints and API error handling |
| `services` | AI processing, semantic retrieval, and RAG workflow |
| `repositories` | SQL Server data access and persistence |
| `models` | API request and response schemas |
| `database` | Database connection and schema management |
| `tools` | Embedding generation utilities |
| `frontend` | Simple browser-based user interface |

---

# 🧠 RAG Processing Flow

## 1. User Question

The user submits a technical question through the web interface or REST API.

Example:

```text
How can I improve SQL Server batch performance?
```

---

## 2. Question Embedding

The question is converted into an embedding vector using Gemini Embedding.

The application currently uses:

```text
gemini-embedding-2
```

---

## 3. Semantic Retrieval

The question vector is compared against stored knowledge embeddings using cosine similarity.

Only embeddings generated with the currently configured embedding model are considered.

---

## 4. Top-K Retrieval

Results are ranked by similarity score.

The current implementation retrieves the top 3 most relevant knowledge records.

---

## 5. Context Construction

Retrieved knowledge is transformed into structured context containing information such as:

```text
Title
Category
Technology
Problem
Analysis
Solution
Result
Lessons Learned
```

---

## 6. Gemini Generation

The retrieved context and user question are sent to Gemini.

Gemini generates an answer using the retrieved engineering knowledge whenever it is relevant.

If the available knowledge is insufficient, the model is instructed to state that clearly.

---

## 7. Source Information

The API returns information about the top retrieved source together with the generated answer.

Source information includes:

* Knowledge ID
* Title
* Category
* Technology
* Similarity score

---

# 🔄 Embedding Generation Flow

Knowledge embeddings are generated through:

```text
backend/tools/generate_embeddings.py
```

Processing flow:

```text
Knowledge
    |
    v
Knowledge Formatter
    |
    v
Gemini Embedding
    |
    v
Embedding Vector
    |
    v
UPSERT
    |
    v
KnowledgeEmbedding
```

Embeddings can be generated or regenerated with:

```bash
python -m backend.tools.generate_embeddings
```

The combination of `KnowledgeId` and `EmbeddingModel` is unique, making the process safe to rerun.

---

# 📖 API Example

## Request

`POST /chat`

```json
{
  "message": "How can I improve SQL Server performance?"
}
```

## Response

```json
{
  "answer": "Based on the retrieved engineering knowledge, ...",
  "source": {
    "knowledge_id": 1,
    "title": "SQL Server Batch Performance Improvement",
    "category": "Database",
    "technology": "SQL Server",
    "similarity": 0.91
  }
}
```

---

# ⚙️ Setup

## Prerequisites

* Python 3.12
* SQL Server
* Microsoft ODBC Driver 18 for SQL Server
* Gemini API key

---

## 1. Create Virtual Environment

```bash
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

---

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3. Configure Environment Variables

Copy `.env.example` to `.env`.

Example:

```text
GEMINI_API_KEY=YOUR_API_KEY

DB_SERVER=localhost
DB_NAME=KnowledgeDB
```

The `.env` file is excluded from Git.

---

## 4. Create Database Schema

Create the `KnowledgeDB` database in SQL Server.

Then execute:

```text
backend/database/schema.sql
```

This creates the `Knowledge` and `KnowledgeEmbedding` tables and their required constraints.

---

## 5. Add Knowledge

Add engineering knowledge records to the `Knowledge` table.

The knowledge can represent technical incidents, troubleshooting experience, architecture decisions, or engineering best practices.

---

## 6. Generate Embeddings

From the project root:

```bash
python -m backend.tools.generate_embeddings
```

---

## 7. Run Application

Run the FastAPI application from the project root:

```bash
uvicorn backend.main:app --reload
```

---

## 8. Open Swagger UI

```text
http://127.0.0.1:8000/docs
```

---

# 🗺 Roadmap

## Completed

* [x] FastAPI backend
* [x] Gemini API integration
* [x] SQL Server knowledge management
* [x] Gemini Embedding integration
* [x] Vector embedding storage
* [x] Embedding-based semantic retrieval
* [x] Cosine similarity search
* [x] Top-K retrieval
* [x] Retrieval-Augmented Generation
* [x] Source attribution
* [x] Idempotent embedding generation
* [x] Layered backend architecture
* [x] Simple web interface

## Future Improvements

* [ ] Similarity score threshold filtering
* [ ] Vector database / ANN search for larger datasets
* [ ] Hybrid search (keyword + vector)
* [ ] RAG evaluation framework
* [ ] Feedback-based retrieval improvement
* [ ] React frontend
* [ ] Authentication and authorization
* [ ] Automated tests
* [ ] Docker support
* [ ] CI/CD pipeline
* [ ] Observability and monitoring
* [ ] Google Cloud deployment

---

# 📌 Version

## v0.3.0

Implemented an embedding-based semantic retrieval pipeline and Retrieval-Augmented Generation architecture using Google Gemini and SQL Server.

---

# 🎯 Future Vision

The goal is to evolve this project into an AI-powered engineering knowledge platform that can:

* Preserve engineering experience
* Retrieve relevant incident and troubleshooting knowledge
* Support architecture decision making
* Reduce dependency on individual experts
* Improve developer productivity
* Turn engineering experience into reusable organizational knowledge

**People move on. Knowledge shouldn't.**