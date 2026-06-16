# IMS Deployment Guide

This guide covers the deployment of the Incident Management System to Google Cloud using Terraform and Docker.

## 1. Prerequisites
- Google Cloud Platform Account
- Google Cloud CLI (`gcloud`) installed and authenticated
- Terraform installed
- Supabase account (for PostgreSQL)

## 2. Supabase Setup
1. Create a new project in Supabase.
2. Go to Project Settings -> Database.
3. Copy the Connection String (URI). Choose the `Transaction` connection pooler format if using asyncpg.
4. Replace `[YOUR-PASSWORD]` with your actual password.
5. The string should look like: `postgresql+asyncpg://postgres.[ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres`

## 3. GCP Setup & Terraform
1. Authenticate with GCP:
   ```bash
   gcloud auth login
   gcloud auth application-default login
   ```
2. Navigate to the `terraform` directory:
   ```bash
   cd terraform
   ```
3. Initialize Terraform:
   ```bash
   terraform init
   ```
4. Create a `terraform.tfvars` file based on `terraform.tfvars.example` and fill in your DB URL and a secure JWT secret key.
5. Apply the infrastructure:
   ```bash
   terraform apply
   ```
   *Note: This will create the GCS Bucket, Artifact Registry, and Cloud Run services (which might fail initially until we push the Docker images).*

## 4. Building and Pushing Docker Images
1. Configure Docker to use Artifact Registry:
   ```bash
   gcloud auth configure-docker asia-south1-docker.pkg.dev
   ```
2. Build and push the backend:
   ```bash
   cd ../backend
   docker build -t asia-south1-docker.pkg.dev/YOUR_PROJECT_ID/ims-repo/backend:latest .
   docker push asia-south1-docker.pkg.dev/YOUR_PROJECT_ID/ims-repo/backend:latest
   ```
3. Build and push the frontend:
   ```bash
   cd ../frontend
   docker build -t asia-south1-docker.pkg.dev/YOUR_PROJECT_ID/ims-repo/frontend:latest .
   docker push asia-south1-docker.pkg.dev/YOUR_PROJECT_ID/ims-repo/frontend:latest
   ```

## 5. Finalizing Deployment
1. Re-run `terraform apply` to ensure Cloud Run services start successfully with the new images.
2. After completion, Terraform will output the `frontend_url` and `backend_url`.

## 6. Database Migrations
1. Locally, configure your `.env` file in the `backend` directory with the Supabase connection string.
2. Run migrations to create tables:
   ```bash
   alembic upgrade head
   ```

## 7. Creating the First Admin
Since there's no registration endpoint for security reasons, create the first admin user manually in the Supabase SQL Editor:
```sql
INSERT INTO users (id, email, hashed_password, full_name, role, is_active, created_at)
VALUES (
    gen_random_uuid(),
    'admin@company.com',
    '$2b$12$YOUR_BCRYPT_HASH', -- Generate using python passlib locally
    'System Admin',
    'admin',
    true,
    now()
);
```
