# Trading Agent API

Trading Agent API is a backend service designed for an AI-powered trading assistant.
It enables users to query their trading history, ask questions about market news, explore strategies, and interact with an intelligent financial agent.

---

## Features

* AI-powered trading assistant
* Query trading history and portfolio insights
* Ask questions about news, markets, and trading strategies

---

## Tech Stack

* **FastAPI** — modern async Python web framework
* **PostgreSQL** — primary database
* **SQLAlchemy + Alembic** — ORM + migrations
* **Celery** — background job processing
* **Redis** — message broker / cache
* **Docker** — full environment containerization
* **Google ADK** — Agent Development Kit

---

## Running the Project

### **1. Docker (Recommended)**

For Linux and macOS:

```bash
./startapp.sh
```

This script will:

* build images
* start PostgreSQL, Redis, the API server, and Celery workers
* run health checks
* prepare the environment

After startup, API is available at:

```
http://localhost:7000
```

---

### **2. Manual Installation (Without Docker)**

#### **Create and activate a virtual environment**

```bash
python3 -m venv venv
source venv/bin/activate
```

#### **Install dependencies**

```bash
pip install -r requirements.txt
```

#### **Start the required services**

You must run these individually:

* PostgreSQL (database)
* Redis (Celery broker)
* Celery worker
* FastAPI app

Example:

```bash
uvicorn app.main:app --reload --port 7000
celery -A app.core.celery_worker.celery_app worker --loglevel=info
```

Make sure PostgreSQL credentials match your `.env` file.

---

## Google Account Connection
- Make a new google cloud project retrieve project name
- Get started with google cloud cli and generate service-account-key.json
- keep the service-account-key.json in root folder

## Database Migrations (Alembic)

Alembic is already set up in the project.

To apply all migrations:

```bash
alembic upgrade head
```

To create a new migration after updating models:

```bash
alembic revision --autogenerate -m "your message"
```

---

## Environment Variables

Create a `.env` file at the root following `.env.example`

---

## Project Structure

```
app/
│── api/              # API routes
│── base/             # Base models and schema
│── core/             # config, celery, logging
│── db/               # database session, models
│── middleware/       # Middlewares and Exception Handlers
│── main.py           # FastAPI entrypoint
alembic/              # migration directory
.env
docker-compose.yml
Dockerfile
startapp.sh
README.md
```

---

## API Documentation

FastAPI automatically generates docs:

Swagger UI:

```
http://localhost:7000/api/v1/docs
```

ReDoc:

```
http://localhost:7000/api/v1/redoc
```

---


# delete cache in alembic/versions:
```
sudo find . -type d -name "__pycache__" -exec rm -rf {} +
```