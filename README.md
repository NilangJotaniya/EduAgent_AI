# EduAgent AI

EduAgent AI is a college-focused student support system with:

- `Student portal`
  - student login with enrollment number
  - student details page
  - document center
  - separate AI chat page
  - fee reminders from admin

- `Admin portal`
  - FAQ management
  - escalation review
  - PDF upload and download tracking
  - exam management
  - student management with create, edit, delete, and bulk import
  - fee ledger and reminder actions

## Current Architecture

- `backend_api.py`
  - FastAPI backend for student/admin APIs
- `database/`
  - MongoDB access layer
- `agents/`
  - query, retrieval, response, and escalation agents
- `UI/`
  - student frontend
- `UI-admin/`
  - admin frontend

## Data Safety

This repository is intended to contain only:

- application code
- safe configuration templates
- synthetic or non-sensitive sample data

It does **not** include:

- `.env`
- uploaded institutional PDFs
- vector database files
- real student credential files

## Requirements

- Python `3.12+`
- Node `22.22.1` recommended
- MongoDB Atlas or MongoDB connection
- Ollama installed locally

## Environment Variables

Create a local `.env` file with values like:

```env
MONGO_URI=your-mongodb-uri
MONGO_DB_NAME=eduagent_db
ADMIN_PASSWORD=your-admin-password
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=phi3:mini
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173,http://localhost:5174,http://127.0.0.1:5174
ENABLE_DEMO_SEED=false
```

## Install

Backend:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

Student frontend:

```powershell
cd UI
npm install
```

Admin frontend:

```powershell
cd UI-admin
npm install
```

## Run

1. Start Ollama:

```powershell
ollama serve
```

2. Start backend:

```powershell
python -m uvicorn backend_api:app --reload --port 8000
```

3. Start student frontend:

```powershell
cd UI
npm run dev
```

4. Start admin frontend:

```powershell
cd UI-admin
npm run dev
```

## Notes

- Student and admin portals are separated.
- Student details and student chat are on different pages.
- Student passwords are stored hashed in MongoDB.
- Common FAQ-type chat queries use a fast path to reduce latency.
- PDF/vector search is only used when the query likely needs document context.

## Recommended Next Steps

- add first-login password reset flow
- import real institutional data only from sanitized files
- configure production domains in `CORS_ORIGINS`
- replace temporary sample students with approved operational data before deployment
