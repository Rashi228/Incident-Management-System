# Incident Management System (IMS)

An enterprise-grade Incident Management System featuring a modern Angular frontend, scalable FastAPI backend, Supabase (PostgreSQL) database, and Terraform scripts for Google Cloud deployment.

## Architecture
- **Frontend**: Angular, Angular Material, RxJS.
- **Backend**: FastAPI, SQLAlchemy, Pydantic, Alembic.
- **Database**: PostgreSQL (Supabase).
- **Storage**: Google Cloud Storage Bucket.
- **Infrastructure**: Docker, Terraform.

## Prerequisites
- Docker & Docker Compose
- Node.js (for local frontend development)
- Python 3.10+ (for local backend development)
- Terraform CLI (for deployment)
- Google Cloud SDK (for GCP deployment)

## Local Setup (Docker)
1. Copy `.env.example` to `.env` in the `backend` and `frontend` directories.
2. Run `docker-compose up --build` from the root directory.
3. Access Frontend at `http://localhost:80`
4. Access Backend API Docs at `http://localhost:8000/docs`

## Deployment
See `deployment/DEPLOYMENT_GUIDE.md` for full instructions.
