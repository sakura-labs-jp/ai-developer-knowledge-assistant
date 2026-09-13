# AI Developer Knowledge Assistant

Engineering knowledge is often scattered across incident tickets, monitoring
records, change logs, reports, architecture decisions, and individual
experience.

**AI Developer Knowledge Assistant** retrieves that evidence, reconstructs
position-relevant Knowledge Chains, and generates grounded answers with Google
Gemini.

> People move on. Knowledge shouldn't.

## What changed in v0.4.0

v0.4.0 adds a position-aware Knowledge Chain prototype on top of the existing
RAG pipeline.

- User-to-position context
- Position-specific knowledge mapping
- Knowledge-to-knowledge relations
- Multi-chain reconstruction
- Database Engineer, Cloud Architect, and AI Engineer perspectives
- Separation of confirmed facts, supported inferences, and unknowns
- Guardrails against presenting correlation as confirmed causation
- Reproducible SQL Server schema, migration, and seed scripts

## Architecture

The repository contains two complementary retrieval flows.

### Standard RAG

```text
Question
  -> Question Embedding
  -> Semantic Retrieval
  -> Top-K Knowledge
  -> RAG Context
  -> Gemini
  -> Answer + Source
```

The FastAPI `/chat` endpoint currently uses this flow.

### Position-aware Knowledge Chain

```text
User ID
  -> User Positions
  -> Question Embedding
  -> Start Knowledge
  -> Position-specific Relations
  -> Reconstructed Knowledge Chains
  -> Evidence Analysis
  -> Grounded Answer
```

For the included batch-processing example, the same incident produces different
evidence paths:

```text
Database Engineer:
Incident -> RESOLVED_BY -> Resolution -> RESULTED_IN -> Result

Cloud Architect:
Incident -> RESOLVED_BY -> Resolution -> RESULTED_IN -> Result

AI Engineer:
Incident -> ANALYZED_BY -> Analysis -> INFORMED -> Decision
```

## Grounding behavior

Knowledge Chain answer generation uses two LLM stages:

1. Evidence analysis classifies retrieved information as
   `CONFIRMED_FACTS`, `INFERENCES`, or `UNKNOWNS`.
2. Final answer generation may state confirmed facts directly, must qualify
   inferences, and must preserve evidence gaps.

The AI Engineer chain also carries an architecture decision requiring
time-window correlation to remain an inference unless direct causal evidence
exists.

## Tech stack

- Python 3.12
- FastAPI
- Google Gemini `gemini-3.6-flash`
- Gemini Embedding `gemini-embedding-2`
- SQL Server
- pyodbc
- HTML, CSS, and JavaScript

## Project structure

```text
backend/
├── database/
│   ├── connection.py
│   ├── schema.sql
│   ├── kc_schema.sql
│   ├── kc_seed_phase0.sql
│   ├── kc_migration_phase1.sql
│   └── kc_seed_phase1.sql
├── repositories/
│   ├── knowledge_repository.py
│   ├── knowledge_embedding_repository.py
│   ├── user_repository.py
│   ├── kc_knowledge_repository.py
│   ├── kc_knowledge_embedding_repository.py
│   └── knowledge_relation_repository.py
├── services/
│   ├── rag.py
│   ├── retrieval.py
│   ├── chain_builder.py
│   ├── kc_retrieval.py
│   ├── knowledge_chain.py
│   └── knowledge_chain_answer.py
└── tools/
    ├── generate_embeddings.py
    └── build_kc_embeddings.py
```

## Knowledge Chain tables

| Table | Responsibility |
| --- | --- |
| `KC_User` | Demo users |
| `KC_Position` | Engineering positions and descriptions |
| `KC_UserPosition` | User-to-position assignments |
| `KC_KnowledgeSource` | Ticket, CSV, PDF, monitoring, and ADR metadata |
| `KC_Knowledge` | Atomic knowledge units |
| `KC_KnowledgePosition` | Position relevance for each knowledge unit |
| `KC_KnowledgeRelation` | Directed, typed, confidence-scored relations |
| `KC_KnowledgeEmbedding` | Model-specific embedding vectors |

Supported knowledge types are:

```text
Incident, Analysis, Resolution, Decision, Result
```

## Setup

### Prerequisites

- Python 3.12
- SQL Server
- Microsoft ODBC Driver 18 for SQL Server
- Gemini API key

### Python environment

```bash
python -m venv .venv
```

Windows:

```bat
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

### Configuration

Copy `.env.example` to `.env` and set:

```text
GEMINI_API_KEY=YOUR_API_KEY
DB_SERVER=localhost
DB_NAME=KnowledgeDB
```

The `.env` file is excluded from Git.

## Database setup

### New environment

Run these scripts in order:

1. `backend/database/schema.sql` for the standard RAG tables.
2. `backend/database/kc_schema.sql` for the Knowledge Chain tables.
3. `backend/database/kc_seed_phase0.sql`.
4. `backend/database/kc_seed_phase1.sql`.

Then generate both embedding sets:

```bat
python -m backend.tools.generate_embeddings
python -m backend.tools.build_kc_embeddings
```

### Existing Phase 0 environment

Run:

1. `backend/database/kc_migration_phase1.sql`.
2. `backend/database/kc_seed_phase1.sql`.

Then rebuild Knowledge Chain embeddings:

```bat
python -m backend.tools.build_kc_embeddings
```

Seed scripts use natural-key lookups and `NOT EXISTS` checks rather than fixed
identity values. Embeddings use an UPSERT keyed by Knowledge ID and embedding
model.

## Run and verify

Start the API:

```bat
uvicorn backend.main:app --reload
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

Run Knowledge Chain reconstruction:

```bat
python -m backend.services.knowledge_chain
```

Run grounded answer generation:

```bat
python -m backend.services.knowledge_chain_answer
```

The included local test evaluates:

| User | Position context | Expected chain |
| --- | --- | --- |
| Alice | Database Engineer, Cloud Architect | Database and Cloud |
| Bob | Cloud Architect | Cloud only |
| Carol | AI Engineer | AI Analysis and Decision |

## Current limitations

- Knowledge relations and position mappings are manually curated.
- Semantic retrieval scans stored vectors in application memory.
- The Knowledge Chain flow is currently a local service test and is not yet
  exposed through a dedicated API endpoint or frontend.
- Automated evaluation and regression tests are not yet implemented.
- Demo sources are illustrative rather than connected enterprise systems.

## Roadmap

### Completed

- Phase 0: `Incident -> Resolution -> Result`
- Phase 1: `User -> Position -> Relevant Knowledge Chain`

### Next: Phase 2

- Chain-based reasoning
- Tool selection
- Controlled action execution
- Human approval boundaries
- Action result capture as new knowledge

### Later

- Automated evaluation
- Observability
- Security and guardrails
- Google Cloud deployment
- Scale and ANN/vector database evaluation

## Version

**v0.4.0 — Position-aware Knowledge Chain and Context Expansion**
