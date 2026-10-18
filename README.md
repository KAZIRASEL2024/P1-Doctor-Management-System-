# Human Doctor Management System

Containerized portal for patients to ask medical questions, doctors to answer assigned questions, and administrators to create doctor accounts.

## Stack

- **Frontend:** Next.js App Router, TypeScript, Tailwind CSS
- **API:** FastAPI, SQLAlchemy 2, Pydantic, Alembic, JWT bearer authentication
- **Database:** PostgreSQL 16
- **Runtime:** Docker Compose

## Start locally with Docker

Requirements: Docker Desktop with Compose enabled.

1. Copy `.env.example` to `.env`.
2. In `.env`, replace the database password, JWT secret, and admin password with unique random values. Keep the database password identical in `POSTGRES_PASSWORD` and `DATABASE_URL`. `ADMIN_PASSWORD` must be at least 12 characters.
3. Start the services from the project root:

   ```powershell
   docker compose up --build
   ```

   Migrations run automatically before the backend starts. On first startup, the backend creates the administrator specified by `ADMIN_EMAIL` and `ADMIN_PASSWORD` if both are set. No demo accounts or credentials are enabled by default.

4. Open the frontend at <http://localhost:3000>, sign in with the configured administrator credentials, and create doctor accounts. Patients can create their own accounts from the sign-in page.

To stop the services, use `Ctrl+C`, or run `docker compose down`. Persistent PostgreSQL data remains in the `postgres_data` volume. To remove it and all stored records, run `docker compose down --volumes`.

## Workflow

- **Admin:** creates doctor accounts and reviews the doctor list.
- **Doctor:** signs in with admin-provided credentials, reviews assigned patient queries, filters by status, and submits answers.
- **Patient:** registers with contact details, selects a doctor, submits a query, and reviews query status and doctor answers.

## API

OpenAPI documentation: <http://localhost:8000/api/docs>

Workflow routes are under `/api/v1`:

| Method | Route | Access |
| --- | --- | --- |
| `POST` | `/auth/login` | Public; JSON email/password login |
| `POST` | `/auth/token` | Public; OAuth2 password form (`username`, `password`) |
| `POST` | `/patient/register` | Public |
| `POST` | `/admin/doctors` | Admin |
| `GET` | `/admin/doctors` | Admin |
| `GET` | `/admin/stats` | Admin |
| `GET` | `/patient/doctors` | Patient |
| `POST` / `GET` | `/patient/queries` | Patient; own queries only |
| `GET` | `/doctor/queries` | Doctor; assigned queries only |
| `PUT` | `/doctor/queries/{query_id}/answer` | Owning doctor only |

The older `/api` routes and veterinary consultation tables are retained for compatibility with existing deployments; the new human patient workflow stores profiles in `patient_profiles` and queries in `medical_queries`. Alembic revision `0003_medical_queries` creates those tables without deleting existing data.

## Local development

The optional development Compose override enables backend reload and mounts source files:

```powershell
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build
```

Backend tests (from `backend/`):

```powershell
pytest
```

Frontend production build (from `frontend/`):

```powershell
npm ci
npm run build
```

## Configuration notes

- `ADMIN_EMAIL` and `ADMIN_PASSWORD` bootstrap the first admin account; existing admin passwords are not reset on subsequent starts.
- `SECRET_KEY` signs JWTs. Use a high-entropy value and keep it private.
- `BACKEND_CORS_ORIGINS` accepts a comma-separated list.
- `SEED_DEMO_DATA` is disabled by default. Do not enable the legacy demonstration seeder outside disposable development environments.
