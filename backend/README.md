# PROPER - Backend API

This directory contains the FastAPI backend for the PROPER application. It handles user authentication, agent interactions, and database operations.

## 📖 API Documentation

Once the server is running, you can access the interactive API documentation (Swagger UI) at [http://localhost:8080/docs](http://localhost:8080/docs). This interface allows you to explore and test all available endpoints directly from your browser.

## 📋 Prerequisites

-   Python 3.9+
-   A running PostgreSQL instance.
-   Google AI API key (for Gemini 2.0 Pro)

## ⚙️ Local Development Setup

### 1. Navigate to the Backend Directory

```bash
cd backend
```

### 2. Create a Virtual Environment

It's highly recommended to use a virtual environment to manage dependencies.

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in this directory by copying the `.env.example` file.

Edit the `.env` file and set the `DATABASE_URL` to point to your local or cloud PostgreSQL instance.

**Example `DATABASE_URL`:**
`postgresql://user:password@localhost:5432/proper_db`

### 5. Run the Development Server

The application uses `uvicorn` to run. The `--reload` flag enables hot-reloading for development.

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

## ✅ Running Tests

The backend includes a suite of unit tests using `pytest`. These tests mock database and external service dependencies to ensure isolated and fast execution.

To run the tests, execute the following command from the `backend/` directory:

```bash
pytest
```
