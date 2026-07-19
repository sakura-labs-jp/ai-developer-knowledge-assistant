# AI Developer Knowledge Assistant

A Retrieval-Augmented Generation (RAG) based AI assistant that retrieves technical knowledge from a SQL Server knowledge base and generates contextual answers using the Google Gemini API.

This project demonstrates modern AI application development using FastAPI, SQL Server, and Large Language Models (LLMs).

---

## Architecture

![Architecture](architecture.png)

The system follows a RAG architecture:

```
User Question
      |
      v
FastAPI Backend
      |
      v
Knowledge Retrieval
      |
      v
SQL Server Knowledge Base
      |
      v
Context Augmentation
      |
      v
Google Gemini API
      |
      v
Generated Answer
```

Technical knowledge is stored in SQL Server.
When a user submits a question, relevant knowledge records are retrieved and injected into the prompt.
Google Gemini then generates an answer based on the retrieved context.

---

## 🚀 Current Features

* ✅ FastAPI backend
* ✅ REST API
* ✅ Google Gemini API integration
* ✅ SQL Server knowledge base integration
* ✅ Knowledge retrieval using SQL keyword matching
* ✅ RAG-based contextual response generation
* ✅ Environment variable management (`.env`)
* ✅ Modular project structure (Services / Repository / Models)

---

## 🛠 Tech Stack

### Backend

- Python 3.12
- FastAPI
- Pydantic

### AI

- Google Gemini API
- Retrieval-Augmented Generation (RAG)

### Database

- SQL Server
- pyodbc
---

## 🗄 Database Schema

The knowledge base is managed using SQL Server.

The `Knowledge` table stores structured technical knowledge used for RAG-based answer generation.

Knowledge records include:

- Category
- Technology
- Title
- Problem
- Analysis
- Solution
- Result
- Lessons Learned
- Keywords
- Difficulty

The schema definition is available here:

```text
database/schema.sql

The knowledge structure is designed to store not only answers, but also troubleshooting processes and engineering decision history, enabling future expansion to more advanced retrieval methods such as embedding-based semantic search.

---

## 📂 Project Structure

```
backend/
│
├── main.py
│
├── models/
│   └── chat.py
│
├── services/
│   ├── gemini.py
│   └── knowledge.py
│
├── repositories/
│   └── knowledge_repository.py
│
└── database/
    ├── connection.py
    └── schema.sql
```

### Responsibility

| Layer        | Responsibility                      |
| ------------ | ----------------------------------- |
| main.py      | FastAPI API endpoints               |
| services     | Application logic and AI processing |
| repositories | Database access                     |
| models       | Request / Response schema           |
| database     | Database connection management      |

---

## 🧠 RAG Flow

The assistant generates answers through the following process:

1. User submits a technical question.
2. The backend searches the SQL Server knowledge database.
3. Relevant knowledge records are retrieved.
4. Retrieved information is formatted as additional context.
5. The context and user question are sent to Gemini.
6. Gemini generates a context-aware response.

Example knowledge fields:

```
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

## 📖 API Example

### Request

**POST** `/chat`

```json
{
  "message": "How can I improve SQL Server performance?"
}
```

### Response

```json
{
  "answer": "Based on the stored knowledge, the recommended approach is..."
}
```

---

## ⚙️ Setup

Clone this repository.

Create a virtual environment.

```bash
python -m venv .venv
```

Activate the environment.

### Windows

```bash
.venv\Scripts\activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

Create a `.env` file.

```text
GEMINI_API_KEY=YOUR_API_KEY
```

Configure the SQL Server connection in:

```text
backend/database/connection.py

Run the application.

```bash
uvicorn backend.main:app --reload
```

Open Swagger UI.

```
http://127.0.0.1:8000/docs
```

---

## 🗺 Roadmap

* [x] FastAPI project
* [x] Gemini API integration
* [x] Chat API
* [x] SQL Server knowledge retrieval
* [x] Basic RAG implementation
* [ ] Embedding-based semantic search
* [ ] Vector Database integration
* [ ] React frontend
* [ ] Authentication
* [ ] Docker support
* [ ] Cloud deployment (Google Cloud Run)

---

## 📌 Version

**v0.2.0**

Added SQL Server based knowledge retrieval and RAG-powered response generation using Google Gemini API.

---

## 🎯 Future Vision

The goal of this project is to evolve into a developer knowledge assistant that can:

* Retrieve internal technical knowledge
* Provide architecture and troubleshooting suggestions
* Support engineering decision making
* Integrate with cloud-native AI platforms
