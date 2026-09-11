# AI Career Skill Gap & Course Recommendation System — Backend

Stage 1 implements the backend foundation only.

## Included

- FastAPI application
- Pydantic settings and environment variables
- PostgreSQL + SQLAlchemy
- Alembic configuration
- Initial database models
- CORS configuration
- Health endpoint
- Swagger/OpenAPI
- Basic pytest tests

## Requirements

- Python 3.11+
- PostgreSQL 14+ recommended

## 1. Create virtual environment

Windows:

    python -m venv venv
    venv\Scripts\activate

macOS/Linux:

    python3 -m venv venv
    source venv/bin/activate

## 2. Install dependencies

    pip install -r requirements.txt

## 3. Create PostgreSQL database

Using psql:

    CREATE DATABASE career_skill_gap;

Or create it using pgAdmin.

## 4. Configure environment

Copy:

    .env.example

to:

    .env

Then change DATABASE_URL if your PostgreSQL username/password/host/port differ.

Example:

    DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/career_skill_gap

## 5. Create the initial migration

Run:

    alembic revision --autogenerate -m "create initial tables"

Then:

    alembic upgrade head

## 6. Run the API

    uvicorn app.main:app --reload

API:

    http://127.0.0.1:8000

Swagger:

    http://127.0.0.1:8000/docs

ReDoc:

    http://127.0.0.1:8000/redoc

Health:

    http://127.0.0.1:8000/api/health

## 7. Run tests

    pytest -q

## Example requests

Health:

    curl http://127.0.0.1:8000/api/health

Expected:

    {"status":"ok"}

Root:

    curl http://127.0.0.1:8000/

Expected:

    {
      "name": "AI Career Skill Gap API",
      "version": "0.1.0",
      "docs": "/docs",
      "health": "/api/health"
    }

## Important

This stage deliberately does NOT implement:

- resume processing
- NLP skill extraction
- job requirement analysis
- skill-gap calculation
- embeddings
- course recommendation
- course search
- React frontend

Those belong to later stages.
