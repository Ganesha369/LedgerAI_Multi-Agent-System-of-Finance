---
title: LedgerAI Multi-Agent Finance
emoji: 💰
colorFrom: green
colorTo: blue
sdk: docker
app_port: 7860
---

# 💰 LedgerAI: Multi-Agent Financial Analysis System

LedgerAI is a sophisticated AI-driven financial analysis platform built with LangGraph and Llama-Index. It utilizes a multi-agent architecture to process complex financial queries, analyze risk, and provide structured insights.

[attachment_0](attachment)

## 🤖 The Agentic Workflow
The system operates on a "Plan-Execute-Verify" cycle, utilizing three distinct agents:

1.  The Planner: Deconstructs the user's financial query into actionable tasks.
2.  The Researcher: Performs RAG (Retrieval-Augmented Generation) using Pinecone and Llama-Index to find specific financial data or tax regulations.
3.  The Auditor: Cross-checks the findings for accuracy and formats the final report for the user.

## 🛠️ Tech Stack
* Backend: FastAPI, Python 3.11
* Intelligence: Google Gemini (Generative AI)
* Orchestration: LangGraph (Stateful Multi-Agent workflows)
* Vector Database: Pinecone
* Frontend: Streamlit (Deployed on Hugging Face)
* Memory/Cache: Redis

## 🚀 Deployment Instructions

### 1. Backend (Railway)
The backend is containerized using Docker and optimized for CPU-only inference to maintain a small footprint.
* Port: 8000
* Optimization: Uses torch-cpu and .dockerignore to reduce image size from 5.7GB to <1GB.

### 2. Frontend (Hugging Face Spaces)
The frontend is built with Streamlit and served via Docker.
* Port: 7860 (Hugging Face standard)
* Communication: Connects to the Railway API via secure REST requests.

## 📦 Local Setup
1. Clone the repo.
2. Create a .env file with your GEMINI_API_KEY, PINECONE_API_KEY, and REDIS_URL.
3. Install dependencies:
   `bash
   pip install -r requirements.txt