# 🩺 RuralCare AI — Agentic Healthcare Triage Assistant

<div align="center">

### **An AI-powered multilingual healthcare triage assistant for rural and semi-urban communities**

*Built with FastAPI · LangGraph · Groq Llama 3.1 · Whisper · AI Safety Guardrails*

![Status](https://img.shields.io/badge/Status-65%25%20Complete-0F766E)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688)
![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-blue)
![Render](https://img.shields.io/badge/Deployment-Render-purple)

</div>

---

## 🌍 Problem Statement

Millions of people in rural and semi-urban India face delays in receiving medical care because they:

* Cannot easily describe symptoms in English.
* Have limited access to healthcare professionals.
* Struggle with telemedicine platforms.
* Need quick guidance before reaching a hospital.

**RuralCare AI** addresses this gap with a multilingual, voice-first AI assistant that performs safe symptom triage and recommends appropriate next actions.

> **Disclaimer:** RuralCare AI is a triage assistant, not a diagnostic system. It does not replace licensed healthcare professionals.

---

## ✨ Key Highlights

* 🤖 **Agentic AI workflow** using LangGraph
* 🩺 **Healthcare triage pipeline** with multiple specialized agents
* 🔒 **Deterministic emergency safety guardrails**
* 💬 **Conversation memory** across patient sessions
* 🌐 **Multilingual-ready architecture** (English, Hindi, Punjabi)
* 🎨 **Professional healthcare UI**
* ⚡ **FastAPI backend** with interactive API documentation
* 🎙️ **Voice architecture prepared** for Whisper STT
* 🚀 **Render deployment-ready structure**

---

## 🏗️ Architecture

```text
                    Patient
                       │
          ┌────────────┴────────────┐
          │                         │
       Voice Input             Text Input
          │                         │
          └────────────┬────────────┘
                       ▼
                  FastAPI Backend
                       │
                Session Management
                       │
                       ▼
                LangGraph Workflow
                       │
      ┌────────┬────────┬────────┐
      ▼        ▼        ▼        ▼
 Planner   Extractor  Triage  Safety
      │                 │        │
      └────────┬────────┴────────┘
               ▼
      Emergency Guardrails
               │
     ┌─────────┼─────────┐
     ▼         ▼         ▼
Emergency   Urgent    Routine
               │
               ▼
        Patient Response
```

---

## 🧠 Multi-Agent Workflow

RuralCare AI uses specialized AI agents instead of a single chatbot.

| Agent                     | Responsibility                                               |
| ------------------------- | ------------------------------------------------------------ |
| **Planner Agent**         | Understands symptoms and asks the next best question         |
| **Information Extractor** | Converts conversation into structured patient information    |
| **Triage Agent**          | Determines urgency level                                     |
| **Safety Agent**          | Applies healthcare safety validation                         |
| **Emergency Guardrail**   | Overrides unsafe AI outputs for critical symptoms            |
| **Response Handlers**     | Generates emergency, urgent, routine, or follow-up responses |

Example workflow:

```text
Patient:
"I have severe chest pain."

        │
        ▼
Planner
        │
        ▼
Extractor
        │
        ▼
Triage
        │
        ▼
Emergency Guardrail
        │
        ▼
EMERGENCY RESPONSE
```

---

## 🚨 AI Safety Guardrails

One of the strongest features of RuralCare AI is its deterministic safety layer.

Even if the language model requests more information, dangerous symptoms automatically trigger emergency guidance.

### Example

**Input**

> "I have severe chest pain and difficulty breathing."

**LLM**

```text
Need More Information
```

**Guardrail**

```text
EMERGENCY
```

This ensures potentially life-threatening symptoms are never downgraded.

---

## 💬 Conversation Memory

Each patient receives a unique session.

```text
patient-001

User:
"I have fever."

Assistant:
"How old are you?"

User:
"I am 25."

Assistant remembers previous context.
```

This creates a natural multi-turn conversation instead of isolated API calls.

---

## 📋 Structured Patient Information Extraction

Instead of repeatedly asking the same questions, the system builds structured patient information.

Example:

```json
{
  "age": 25,
  "symptoms": [
    "fever"
  ],
  "temperature": "102°F",
  "symptom_duration": "2 days"
}
```

This structured information improves future triage decisions.

---

## 🎨 Professional Patient Interface

The application includes a modern healthcare-inspired interface featuring:

* Minimal medical dashboard
* Soft glassmorphism design
* Mobile responsiveness
* Chat-style conversation
* Emergency alert cards
* Large microphone interface
* Language selector

Designed for accessibility and ease of use.

---

## 🛠️ Tech Stack

### Backend

* Python 3.10+
* FastAPI
* LangGraph
* Groq Llama 3.1
* Pydantic
* Uvicorn

### AI

* LangGraph Multi-Agent
* Groq API
* Whisper (planned integration)
* Safety Guardrails

### Frontend

* HTML5
* CSS3
* Vanilla JavaScript
* Browser Voice APIs

### Deployment

* Render (target platform)

---

## 📂 Project Structure

```text
rural-healthcare-triage/

├── app/
│   ├── agents/
│   ├── api/
│   ├── graph/
│   ├── services/
│   ├── security/
│   ├── models/
│   ├── config.py
│   └── main.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── tests/
├── .env
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### Clone

```bash
git clone https://github.com/yourusername/rural-healthcare-triage.git
cd rural-healthcare-triage
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate

Windows

```powershell
.venv\Scripts\activate
```

Linux/macOS

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment

Create `.env`

```env
GROQ_API_KEY=your_api_key
GROQ_MODEL=llama-3.1-8b-instant
```

### Run

```bash
python -m uvicorn app.main:app --reload
```

Visit

```text
http://127.0.0.1:8000/
```

---

## 🔌 API Endpoints

| Method | Endpoint        | Purpose                            |
| ------ | --------------- | ---------------------------------- |
| GET    | `/`             | Patient UI                         |
| GET    | `/health`       | Health check                       |
| POST   | `/chat`         | AI triage                          |
| DELETE | `/session/{id}` | Clear conversation                 |
| POST   | `/voice`        | Voice upload (planned integration) |

---

## 🧪 Example

Request

```json
{
  "session_id": "patient-001",
  "message": "I have fever since yesterday."
}
```

Response

```json
{
  "next_action": "NEED_MORE_INFORMATION",
  "message": "How old are you and what is your temperature?"
}
```

---

## 📈 Development Progress

Current completion: **≈65%**

| Feature                           | Status |
| --------------------------------- | ------ |
| Project Structure                 | ✅      |
| FastAPI Backend                   | ✅      |
| Planner Agent                     | ✅      |
| Triage Agent                      | ✅      |
| LangGraph Workflow                | ✅      |
| Session Memory                    | ✅      |
| Safety Guardrails                 | ✅      |
| Emergency Routing                 | ✅      |
| Structured Information Extraction | ✅      |
| Professional UI                   | ✅      |
| API Documentation                 | ✅      |
| Whisper Integration               | 🚧     |
| Voice Response (TTS)              | 🚧     |
| Regional Language Support         | 🚧     |
| Appointment Scheduling            | 🚧     |
| PostgreSQL Persistence            | ⏳      |
| Redis Sessions                    | ⏳      |
| Authentication                    | ⏳      |
| Docker                            | ⏳      |
| Render Production Deployment      | ⏳      |

Legend:

* ✅ Complete
* 🚧 In Progress
* ⏳ Planned

---

## 🎯 Roadmap

### Phase 1 — Foundation

* [x] FastAPI backend
* [x] LangGraph workflow
* [x] Multi-agent architecture
* [x] Safety guardrails

### Phase 2 — Intelligence

* [x] Conversation memory
* [x] Patient information extraction
* [ ] Adaptive questioning
* [ ] Better symptom reasoning

### Phase 3 — Voice

* [ ] Whisper STT
* [ ] Coqui TTS
* [ ] Hindi support
* [ ] Punjabi support

### Phase 4 — Production

* [ ] PostgreSQL
* [ ] Redis
* [ ] Authentication
* [ ] Docker
* [ ] Render deployment

---

## 🎓 Learning Outcomes

This project demonstrates practical experience with:

* Multi-Agent AI Systems
* AI Safety Guardrails
* LangGraph Orchestration
* FastAPI Backend Development
* Healthcare AI Design
* Conversation State Management
* API Development
* Production-ready Project Architecture

---

## 🌟 Why This Project Matters

RuralCare AI combines **Generative AI**, **AI Governance**, **Healthcare Safety**, and **Agentic Systems** into a practical real-world application aimed at improving access to healthcare guidance for underserved communities.

It showcases modern AI engineering practices rather than building a simple chatbot.

---

## 📄 License

This project is released under the **MIT License**.

---

<div align="center">

### ⭐ If you find this project interesting, consider giving it a star!

*Building AI for safer and more accessible healthcare.*

</div>
