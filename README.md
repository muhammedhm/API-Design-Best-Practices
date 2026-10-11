# Task Management API

A FastAPI-based task management application for user lifecycle management and task operations, designed with a clean modular structure that follows common microservice-friendly API principles. The project separates concerns across domain modules (`users`, `tasks`, and shared utilities), uses JWT-based authentication, and exposes a contract-first style API for secure communication.

## Architecture Overview

This service is structured to align with microservice best practices when evolved into independent deployment units:

- Clear domain boundaries: `users` and `tasks` are separated into independent modules
- Stateless API design: each request contains the required authentication and context
- Shared utilities for cross-cutting concerns such as database access and settings
- Validation-first request handling with Pydantic DTOs
- API-first contracts via explicit schemas and OpenAPI generation
- Separation of business logic from routing and persistence code

![Authentication Workflow](./authentication_workflow.jpeg)

## Features

- User registration and login
- JWT-based authentication
- Task creation, listing, updating, and deletion
- PostgreSQL-backed database
- Auto-generated OpenAPI documentation via FastAPI

## Microservice Design Best Practices Applied

This API follows a microservice-oriented design mindset in the following ways:

- Bounded context separation: user management and task management are logically isolated
- Small reusable modules: each domain has its own router, controller, DTOs, and models
- Explicit contracts: request and response validation is enforced through schemas
- Security by default: protected routes require authentication tokens
- Externalized configuration: environment variables keep runtime settings decoupled from code
- Observability readiness: the project can easily integrate logging, tracing, and metrics when scaled out

## Tech Stack

- Python 3.10+
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- JWT (PyJWT)
- Alembic (migration support)

## Project Structure

```text
.
├── .env                     # Environment configuration
├── .gitignore               # Git ignore rules
├── alembic.ini              # Alembic config
├── authentication_workflow.jpeg
├── main.py                  # FastAPI app entry point
├── migrations/              # Database migrations
├── src/
│   ├── tasks/
│   │   ├── controller.py
│   │   ├── dtos.py
│   │   ├── models.py
│   │   └── router.py
│   ├── users/
│   │   ├── controller.py
│   │   ├── dtos.py
│   │   ├── models.py
│   │   └── router.py
│   └── utils/
│       ├── db.py
│       ├── helpers.py
│       ├── mail.py
│       ├── settings.py
│       └── __init__.py
├── requirement.txt          # Dependency list
├── README.md                # Project documentation
└── .venv/                   # Local virtual environment (optional)
```

## Prerequisites

Before running the application, ensure you have:

- Python 3.10 or later installed
- PostgreSQL running and accessible
- A database created for the application

## Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd task_management_app
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install fastapi "uvicorn[standard]" sqlalchemy pydantic pydantic-settings python-dotenv PyJWT psycopg2-binary alembic
```

If you prefer to use a requirements file, make sure the project has all required packages listed in `requirement.txt` before running the install command.

4. Configure environment variables:

Create a `.env` file in the project root with values like:

```env
DB_CONNECTION = "postgresql://username:password@localhost:5432/task_management"
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
EXP_TIME_MINUTES = 30
```

> Replace the database URL and secret key with your own values.

## Running the Application

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

The API will be available at:

- http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## API Endpoints

### User Routes

- `POST /user/register` — Register a new user
- `POST /user/login` — Log in and receive authentication token
- `GET /user/is_auth` — Validate authentication state

### Task Routes

- `POST /tasks/create` — Create a new task
- `GET /tasks/list` — Retrieve all tasks for the authenticated user
- `GET /tasks/listbyID/{task_id}` — Retrieve a specific task by ID
- `PUT /tasks/update/{task_id}` — Update a task
- `DELETE /tasks/delete/{task_id}` — Delete a task

## Authentication

Protected task routes require a valid JWT token. The token is usually sent in the `Authorization` header:

```http
Authorization: Bearer <token>
```

## Database Initialization

The application creates database tables automatically at startup through:

```python
Base.metadata.create_all(bind=engine)
```

This happens in `main.py`, so the required tables are created when the app starts.

## Notes

- The project is structured around a modular FastAPI design with separate `users` and `tasks` modules.
- Authentication logic and database configuration are centralized in the `src/utils` package.
- If you are using Alembic for migrations, you can add new schema changes under the `migrations` folder.

## License

This project does not currently include a license file. If you plan to distribute or publish it, add a license that matches your intended usage.
