# 🎓 EduAgent AI — Multi-Agent Assistant for Academic Administration

<div align="center">

![EduAgent AI Banner](https://img.shields.io/badge/EduAgent_AI-Multi--Agent_Academic_Assistant-667eea?style=for-the-badge&logo=graduation-cap&logoColor=white)

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248?style=flat-square&logo=mongodb&logoColor=white)](https://mongodb.com/atlas)
[![Ollama](https://img.shields.io/badge/Ollama-phi3:mini-black?style=flat-square&logo=ollama&logoColor=white)](https://ollama.com)
[![LangChain](https://img.shields.io/badge/LangChain-0.1.12-1C3C3C?style=flat-square&logo=chainlink&logoColor=white)](https://langchain.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

**A GenAI-powered, multi-agent intelligent assistant that automates and simplifies academic administration tasks in colleges and universities.**

[Features](#-features) • [Architecture](#-system-architecture) • [Tech Stack](#-tech-stack) • [Getting Started](#-getting-started) • [Demo](#-demo) • [Author](#-author)

</div>

---

## 📌 Overview

**EduAgent AI** is a production-ready, multi-agent academic helpdesk built as part of the **SAP Internship Program** under **Edunet Foundation — Artificial Intern**. 

Instead of students manually visiting offices or searching through piles of documents, EduAgent AI serves as a **single intelligent point of interaction** — answering queries about exams, fees, attendance, scholarships, and more in real time.

> 💡 Built with a **100% local AI** (phi3:mini via Ollama) — no API keys, no internet dependency for AI inference, zero cost per query.

---

## ✨ Features

### 🤖 Student Chat Interface
- Natural language Q&A powered by **phi3:mini** (local LLM)
- Instant answers about exams, fees, attendance, scholarships, admissions, library
- **📥 PDF Document Downloads** — AI detects when a student is asking for a document and provides a one-click download button directly in the chat
- Smart escalation for sensitive queries (mental health, complaints, emergencies)
- Quick-question buttons for common queries
- Full chat history within session

### 🔧 Admin Panel
- 🔐 Password-protected admin dashboard
- 📊 Live statistics (FAQs, escalated queries, uploaded PDFs, exam entries)
- 🚨 View & manage escalated queries (update status, add admin notes, export CSV)
- 📝 Full FAQ management — Add, Edit, Delete with category filtering
- 📄 PDF document upload with AI knowledge base integration
- 📅 Exam schedule management
- 💰 Fee structure management

### 🧠 Multi-Agent Architecture
| Agent | Role |
|---|---|
| **Query Understanding Agent** | Classifies student questions into categories using NLP keyword matching |
| **Information Retrieval Agent** | Fetches relevant FAQs, schedules, and fees from MongoDB Atlas |
| **Response Generation Agent** | Generates human-like answers using phi3:mini (local LLM) |
| **Escalation Agent** | Detects sensitive queries and flags them for human review |
| **PDF Matcher** | Matches student queries to uploaded PDF documents for direct download |

---

## 🏗️ System Architecture

```
Student Query
      │
      ▼
┌─────────────────────────────────────────────┐
│              EduAgent AI Pipeline           │
│                                             │
│  1. Escalation Agent  ──► Sensitive? ──► Admin (MongoDB)
│         │ No                                │
│         ▼                                   │
│  2. PDF Matcher  ──► Documents found? ──► Download Button
│         │                                   │
│         ▼                                   │
│  3. Query Understanding Agent               │
│         │  (category + keywords)            │
│         ▼                                   │
│  4. Information Retrieval Agent             │
│         │  MongoDB Atlas + FAISS PDF Search │
│         ▼                                   │
│  5. Response Generation Agent               │
│         │  phi3:mini via Ollama             │
│         ▼                                   │
│      AI Response + Download Button          │
└─────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Frontend** | Streamlit 1.32 | Web UI, chat interface, admin panel |
| **AI / LLM** | phi3:mini via Ollama | Local response generation (no API key) |
| **Database** | MongoDB Atlas | Cloud storage for FAQs, exams, fees, escalations |
| **PDF Search** | FAISS + LangChain + HuggingFace | Semantic search over uploaded documents |
| **PDF Processing** | PyPDF + LangChain | Text extraction and chunking |
| **Embeddings** | all-MiniLM-L6-v2 | Local text-to-vector conversion |
| **Backend** | Python 3.12 | Core application logic |
| **Environment** | python-dotenv | Secure credential management |

---

## 📁 Project Structure

```
EduAgent-AI/
│
├── app.py                          ← Main student chat interface
├── start_llm.py                    ← Auto-starts Ollama on app launch
│
├── agents/
│   ├── query_agent.py              ← Understands & categorizes queries
│   ├── retrieval_agent.py          ← Fetches data from MongoDB + PDFs
│   ├── response_agent.py           ← Generates AI responses (phi3:mini)
│   └── escalation_agent.py        ← Flags sensitive queries
│
├── database/
│   ├── mongo_db.py                 ← MongoDB Atlas connection & all operations
│   └── seed_mongodb.py             ← Seeds initial academic data
│
├── pages/
│   └── admin_panel.py              ← Staff admin dashboard (Streamlit multi-page)
│
├── utils/
│   ├── pdf_processor.py            ← PDF upload, chunking, FAISS vector storage
│   └── pdf_matcher.py              ← Matches student queries to downloadable PDFs
│
├── uploaded_pdfs/                  ← Uploaded PDF documents (gitignored)
├── vector_db/                      ← FAISS vector index (gitignored)
├── .env                            ← Secrets — MongoDB URI, passwords (gitignored)
├── requirements.txt                ← Python dependencies
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- [Ollama](https://ollama.com/download) installed on your machine
- [MongoDB Atlas](https://cloud.mongodb.com) account (free tier works)

### 1. Clone the Repository
```bash
git clone https://github.com/NilangJotaniya/EduAgent-AI.git
cd EduAgent-AI
```

### 2. Create & Activate Virtual Environment
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Pull the Local AI Model
```bash
ollama pull phi3:mini
```

### 5. Configure Environment Variables
Create a `.env` file in the project root:
```env
# MongoDB Atlas connection string
MONGO_URI=mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
MONGO_DB_NAME=eduagent_db

# Ollama (no changes needed)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=phi3:mini

# Admin Panel password
ADMIN_PASSWORD=admin123
```

> 💡 Get your `MONGO_URI` from **MongoDB Atlas → Connect → Drivers → Python**

### 6. Seed the Database
```bash
python database/seed_mongodb.py
```

### 7. Run the Application
```bash
streamlit run app.py
```

The app will automatically start Ollama and open at **http://localhost:8501** 🎉

---

## 🎯 Usage

### For Students
1. Open the app in your browser
2. Type your academic question or click a quick-question button
3. Get an instant AI-powered answer
4. If a related PDF is available, a **Download button** appears right in the chat

### For Admin Staff
1. Click **"Admin Panel"** in the sidebar navigation
2. Login with the admin password
3. Manage FAQs, exam schedules, fee structure
4. Upload PDF documents (timetables, handbooks, forms)
5. Review and respond to escalated student queries

---

## 📸 Demo

```
Student: "Can I get the exam timetable?"

EduAgent AI: "Here is the upcoming exam schedule for Semester 2:
  • Mathematics  : March 10 at 10:00 AM — Hall A
  • Physics      : March 12 at 10:00 AM — Hall B
  • Computer Sci : March 14 at 02:00 PM — Lab 1
  ...
  📥 A downloadable timetable document is also available below!
  Is there anything else I can help you with?"

  ┌──────────────────────────────────────┐
  │ 📄 Exam Timetable Sem 2              │
  │ Click below to download.             │
  └──────────────────────────────────────┘
  [ ⬇️ Download Exam Timetable Sem 2 ]
```

---

## 📦 Requirements

```
streamlit==1.32.0
requests==2.31.0
python-dotenv==1.0.0
pandas==2.2.0
pymongo==4.6.1
dnspython==2.6.1
langchain==0.1.12
langchain-community==0.0.28
pypdf==4.1.0
faiss-cpu==1.7.4
sentence-transformers==2.5.1
```

---

## 🔮 Future Enhancements

- [ ] Voice input support (speech-to-text)
- [ ] Email notification system for escalated queries
- [ ] Student login portal with personalized query history
- [ ] Multi-language support (Hindi, Gujarati)
- [ ] Integration with college ERP/SIS systems
- [ ] Mobile app version
- [ ] Analytics dashboard for admin (query trends, peak hours)

---

## 🏫 About This Project

This project was built as part of the **SAP Internship Program** under **Edunet Foundation — Artificial Intern**, with the goal of applying GenAI and multi-agent systems to solve a real-world problem in academic administration.

---

## 👨‍💻 Author

<div align="center">

### Nilang Jotaniya

[![GitHub](https://img.shields.io/badge/GitHub-NilangJotaniya-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/NilangJotaniya)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-nilangjotaniya-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/nilangjotaniya/)
[![Email](https://img.shields.io/badge/Email-nilangjotaniya@gmail.com-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:nilangjotaniya@gmail.com)



</div>

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

*If you found this project helpful, please consider giving it a ⭐ on GitHub!*

</div>
