## Initialize the backend
- uv init
- uv venv
- source .venv/bin/activate

## Run backend
- uv run uvicorn app.main:app --reload

## Test backend
- uv run pytest


## Health checks url:
- http://127.0.0.1:8000/api/v1/health

## Open API docs:
- http://127.0.0.1:8000/docs

## Initialise the forntend
- ng new frontend

## Run frontend
- ng serve



## Backend Structure Overview 
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

## Frontend Structure Overview 

## Docker
- docker compose up -d