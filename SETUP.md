# SETUP.md

## Local development prerequisites
- Python 3.12+
- PostgreSQL 16+ or containerized Postgres
- Node.js only if Tailwind build process requires it
- Docker and Docker Compose for containerized workflow

## Suggested local setup
1. Copy `.env.example` to `.env`
2. Create and activate virtual environment
3. Install Python requirements
4. Use `USE_SQLITE=1` for quick local run or configure PostgreSQL env vars
5. Run migrations
6. Create superuser
7. Start Tailwind watcher/build
8. Run Django server

## Docker-first setup
- `docker compose up --build`
- run migrations inside container
- create admin user

## Initial seed users
- admin user
- one reception user
- one doctor user

Use:
- `python manage.py seed_users` (local)
- `docker compose run --rm web python manage.py seed_users` (Docker)

## Static/media notes
- keep static and media paths explicit
- ensure Caddy serves static/media correctly in production
