Initialize the backend
- uv init
- uv venv
- source .venv/bin/activate

Run backend
- uv run uvicorn app.main:app --reload

Test backend
- uv run pytest


Health checks
- http://127.0.0.1:8000/api/v1/health

Docs
- http://127.0.0.1:8000/docs

Alembic
- uv run alembic init alembic
- uv run alembic revision --autogenerate -m "create tables"
- uv run alembic upgrade head

Structure Overview 
core/ → configuration, logging, security
db/ → engine, session, base model
models/ → ORM entities


Docker
- docker compose up -d