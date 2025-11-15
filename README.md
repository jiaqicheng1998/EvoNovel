# Project Template

A full-stack application with FastAPI backend and React frontend, fully dockerized for easy development on any machine.

## Prerequisites

- Docker Desktop (or Docker Engine + Docker Compose)
- Git

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-org/project-template.git
   cd project-template
   ```
2. (Optional) Copy any `.env.example` files to `.env` if you decide to customize environment variables. The repository ships with sensible defaults baked into `docker-compose.yml`, so you can skip this step for local experimentation.

## Getting Started

### Start the Application

```bash
docker-compose up --build
```

This will:
- Build the FastAPI, React, and PostgreSQL images (if they are not cached)
- Start the services with hot reload enabled
- Expose the services on:
  - FastAPI: http://localhost:8000
  - React: http://localhost:5173
  - PostgreSQL: localhost:5432 (user/password: `postgres`/`postgres`)

Prefer detached mode?

```bash
docker-compose up --build -d
```

Check that all services are running:

```bash
docker ps
```

### Access the Application

- **Frontend**: Open http://localhost:5173 in your browser
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs (FastAPI auto-generated docs)

### Development Workflow

Both app services support hot reload:
- Changes to Python files in `fastApiServer/` automatically restart the FastAPI server
- Changes to React files in `reactClient/` automatically reload in the browser

Restart only one service if needed:

```bash
docker-compose restart fastapi
docker-compose restart react
```

### Stop the Application

```bash
docker-compose down
```

To also remove volumes (including the PostgreSQL data volume):

```bash
docker-compose down -v
```

## Exec Into PostgreSQL

Open a `psql` session inside the running PostgreSQL container (container name: `postgres-db`):

```bash
docker exec -it postgres-db psql -U postgres -d postgres
```

Need a full shell? Swap `psql` for `bash`:

```bash
docker exec -it postgres-db bash
```

Once in `psql`, list databases with `\l`, switch with `\c <database>`, and inspect tables with `\dt`.

## Project Structure

```
project-template/
├── docker-compose.yml          # Orchestrates FastAPI, React, and PostgreSQL
├── fastApiServer/
│   ├── Dockerfile              # FastAPI container definition
│   ├── requirements.txt        # Python dependencies
│   └── app/
│       ├── main.py             # FastAPI entrypoint
│       └── model.py            # Pydantic models and database entities
└── reactClient/
    ├── Dockerfile              # React container definition
    ├── package.json            # Node dependencies
    └── src/                    # React source code
```

## Troubleshooting

### Port Already in Use

If ports 8000, 5173, or 5432 are already in use, modify the host port mappings in `docker-compose.yml`:

```yaml
ports:
  - "8001:8000"  # Change host port (left side)
```

### Rebuild After Dependency Changes

If you add new dependencies:

```bash
# For Python dependencies
docker-compose build fastapi

# For Node dependencies
docker-compose build react

# Rebuild everything
docker-compose up --build
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f fastapi
docker-compose logs -f react
docker-compose logs -f postgres
```

