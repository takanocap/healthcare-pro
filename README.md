# Patient Reported Outcomes Multi-Agent System
A sophisticated multi-agent system for collecting and analyzing Patient Reported Outcomes (PROs) using Google AI SDK, Gemini 2.0 Pro, FastAPI, and SQLite. The system provides a patient-centered, clinician-ready feedback loop through three coordinated AI agents.

## 🏥 System Overview
This system addresses healthcare challenges in capturing high-quality PROs for chronic care patients by providing:

* Conversational check-ins with emotional intelligence
* Adaptive questionnaires that personalize based on patient responses
* Trend monitoring with real-time clinical insights and alerts
* Multilingual and accessibility support
* Compliance with data privacy standards

## 🤖 Multi-Agent Architecture
1. Companion Agent
    * Purpose: Initiates conversational check-ins and builds rapport
    * Capabilities:
        * Emotional state detection and response adaptation
        * Multilingual communication support
        * Accessibility-aware interactions
        * Trust-building through empathetic communication

2. Adaptive Questionnaire Agent
    * Purpose: Delivers personalized PRO collection
    * Capabilities:
        * Dynamic question complexity adjustment
        * Comprehension monitoring and clarification
        * Response quality assessment
        * Condition-specific question templates

3. Trend Monitoring Agent
    * Purpose: Analyzes patterns and generates clinical insights
    * Capabilities:
        * Time-series pattern recognition
        * Risk assessment and alert generation
        * Clinical recommendation generation
        * Predictive analysis for early intervention

## ✨ Features

-   **Intelligent Agent Interaction**: Engages with patients for check-ins, questionnaires, and trend analysis.
-   **Secure User Authentication**: Simple and secure user login/registration.
-   **RESTful API**: A robust backend built with FastAPI providing clear and interactive API documentation.
-   **Scalable Database**: Utilizes PostgreSQL for reliable data storage.
-   **Cloud-Ready**: Designed for easy deployment to Google Cloud services like Cloud Run and Cloud SQL.

## 🛠️ Tech Stack

-   **Backend**: Python, FastAPI, SQLAlchemy, `asyncpg`, `psycopg2`
-   **Frontend**: (Assumed) React / Next.js, TypeScript
-   **Database**: PostgreSQL
-   **Deployment**: Docker, Google Cloud (Cloud Run, Cloud SQL)
-   **Testing**: Pytest

## 📂 Project Structure

```
healthcare-pro/
├── backend/
│   ├── app/
│   ├── tests/
│   ├── .env.example
│   └── requirements.txt
├── frontend/
│   ├── src/
│   ├── .env.local.example
│   └── package.json
├── .gitignore
└── README.md
```

## Getting Started

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd proper
```

### 2. Configure Environment Variables

This project uses `.env` files for managing environment variables. You will find `.env.example` files in both the `backend/` and `frontend/` directories. Copy them to `.env` (for backend) and `.env.local` (for frontend) and fill in the required values, especially the `DATABASE_URL`.

### 3. Running the Application

The easiest way to get started is with Docker Compose (if a `docker-compose.yml` file is configured), which can build and run all services.

-   The backend API will be available at `http://localhost:8000`.
-   The interactive API documentation (Swagger UI) will be at `http://localhost:8000/docs`.
-   The frontend application will be available at `http://localhost:3000`.

