# AI Developer Knowledge Assistant
A personal AI assistant that helps me search my own technical knowledge and suggest relevant reference code through a conversational interface.

## Architecture

![Architecture](architecture.png)

This project is a personal learning project focused on modern AI application development using FastAPI and the Google Gemini API. It is the first step toward building a Retrieval-Augmented Generation (RAG) assistant.

---

## 🚀 Current Features

- ✅ FastAPI backend
- ✅ REST API
- ✅ Google Gemini API integration
- ✅ Interactive chat endpoint (`POST /chat`)
- ✅ Environment variable management (`.env`)
- ✅ Modular project structure (Services / Models)

---

## 🛠 Tech Stack

- Python 3.12
- FastAPI
- Google Gemini API
- Pydantic

### Planned

- ChromaDB
- React
- RAG (Retrieval-Augmented Generation)

---

## 📂 Project Structure

```
backend/
│
├── main.py
├── models/
│   └── chat.py
└── services/
    └── gemini.py
```

---

## 📖 API Example

### Request

**POST** `/chat`

```json
{
  "message": "What is FastAPI?"
}
```

### Response

```json
{
  "answer": "FastAPI is a modern Python web framework..."
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

Windows

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

- [x] FastAPI project
- [x] Gemini API integration
- [x] Chat API
- [ ] React frontend
- [ ] ChromaDB integration
- [ ] RAG implementation
- [ ] Authentication
- [ ] Docker support

---

## 📌 Version

**v0.1.0**

Initial release featuring a FastAPI backend with Google Gemini API integration.