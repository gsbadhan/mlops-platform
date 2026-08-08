## Backend Structure
```bash
.
├── alembic
├── alembic.ini
├── app
├── Dockerfile
├── mlops.db
├── pyproject.toml
├── README.md
└── tests
```

## Initialise/Setup Backend Locally
- uv init
- uv venv
- source .venv/bin/activate

## Execute Testcases
- uv run pytest

## Run API Server Standalone
- uv run uvicorn app.main:app --reload

## API Server Health checks url:
- http://127.0.0.1:8000/api/v1/health

## Open API docs:
- http://127.0.0.1:8000/docs

## Backend Folder Structure Overview 
- app/api/  → API endpoints
- app/core/ → configuration, logging, database, seesion
- app/enums/  → mappings
- app/exceptions/  → Application exceptions
- app/schema/ → API request/response models
- app/models/ → ORM entities
- app/repository/ → ORM repositories
- app/service/ → business logic
- app/middleware/ → request/response logging
- tests/ → test cases
- alembic/ → alembic configurations


## Deploy Backend Using Dockerisation
- docker build -t mlops-backend .
- docker run -d --rm -p 8000:8000 mlops-backend
