## Project Structure
```bash
.
├── backend
├── docker-compose.yml
├── docs
├── frontend
└── README.md
```

## [Backend](./backend/README.md)

## [Frontend](./frontend/README.md)

## [Documentation](./Docs/README.md)


## Deployment
```bash
Docker Compose
├── Frontend (Angular + Nginx)
│   └── :4200
│
└── Backend (FastAPI + uv)
    └── :8000
```
### Deploy Backend/Frontend Both Using Dockerisation
- docker compose build --no-cache --progress=plain
- docker compose up -d
- docker compose down
- docker ps