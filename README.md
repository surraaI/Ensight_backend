# Ensight Backend

Lightweight backend for Ensight — a FastAPI service powering users, profiles, articles, resources, subscriptions and admin workflows.

This repository contains the API, database models, migrations and services used by Ensight's backend.

## Tech stack
- Python 3.10+
- FastAPI
- SQLAlchemy (via `app.database`)
- Alembic for migrations
- Uvicorn for ASGI server

## Features
- JWT-based authentication and authorization
- User, Profile, Article, Resource, Subscription and Admin endpoints
- Database migrations with Alembic
- Cloudinary integration for uploads (config in `app/core/cloudinary_config.py`)

## Quick start
Prerequisites:

- Python 3.10+ installed
- A running PostgreSQL (or other SQL) database

1. Create a virtual environment and install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Configure environment variables

Create a `.env` file in the project root (or export variables in your shell). Minimum recommended variables:

```env
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/ensight
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=1440
CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=
```

3. Run database migrations

Ensure `DATABASE_URL` points to your DB, then:

```bash
alembic upgrade head
```

4. Seed a superadmin account (optional)

```bash
python seed_superadmin.py
```

5. Run the application

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open interactive docs at `http://localhost:8000/docs` (Swagger) or `http://localhost:8000/redoc`.

## Tests
This repository does not include a test suite by default. Add tests under a `tests/` folder and run them with `pytest`.

## Project structure (high level)
- `app/` — application package
	- `main.py` — FastAPI app entrypoint
	- `database.py` — SQLAlchemy setup
	- `models/` — ORM models
	- `schemas/` — Pydantic request/response schemas
	- `routers/` — API route modules
	- `services/` — business logic services
	- `core/` — config and security helpers
- `alembic/` — Alembic migration config and versions
- `requirements.txt` — pinned Python dependencies
- `seed_superadmin.py` — helper to create initial admin user

## Environment & Deployment notes
- Use a production-ready server (e.g., Uvicorn/Gunicorn combination) behind a reverse proxy for production.
- Keep `SECRET_KEY` secure and do not commit `.env` to source control.
- Configure allowed hosts, CORS origins and logging according to your deployment environment.

## Contributing
Contributions are welcome. Please open an issue to discuss larger changes and submit PRs for bug fixes or features. Follow the existing code style, and add tests for new functionality.

## License
Specify your project license here (e.g., MIT). If you don't have one yet, add a `LICENSE` file.

---
If you'd like, I can also:
- add a sample `.env.example` file
- add a `Procfile` / systemd unit for production
- scaffold tests and CI workflow
Tell me which you'd like next.
