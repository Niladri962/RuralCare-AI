# 🏥 RuralCare AI — Agentic Healthcare Triage Assistant

An AI-powered multilingual healthcare triage assistant built using FastAPI, LangGraph, and LLM orchestration to improve healthcare accessibility in rural and semi-urban communities.

> **Live Demo:** https://your-render-url.onrender.com

---

## Features

- 🎤 Voice-to-Text symptom collection
- 🤖 Multi-Agent AI conversation
- ❤️ Emergency risk assessment
- 🌍 Multilingual-ready architecture
- 📊 Conversation memory
- 🔒 Security-focused prompt handling
- ☁️ One-click deployment on Render

---

## System Architecture

Whisper (Speech)

↓

Planner Agent

↓

Symptom Analysis

↓

Triage Agent

↓

Recommendation

↓

Text/Voice Response

---

## Tech Stack

| Layer | Technology |
|--------|------------|
| Backend | FastAPI |
| AI Orchestration | LangGraph |
| LLM | Groq (Llama 3) |
| Frontend | HTML/CSS/JavaScript |
| Testing | Pytest |
| Deployment | Render |
| Container | Docker |

---

## Project Structure

```text
app/
frontend/
tests/
Dockerfile
render.yaml
requirements.txt
