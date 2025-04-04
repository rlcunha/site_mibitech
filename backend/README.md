# MibiTech Backend API

This is the backend API for MibiTech website, built with FastAPI and PostgreSQL.

## Features

- RESTful API endpoints
- PostgreSQL database integration
- Docker containerization
- Social media endpoint (/api/social-media/)

## Setup

1. Copy .env.example to .env and configure:
   ```bash
   cp .env.example .env
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run with Docker:
   ```bash
   docker-compose up --build
   ```

4. Or run locally:
   ```bash
   python init_db.py
   uvicorn app.main:app --reload
   ```

## API Documentation

After starting the server, access API docs at:
- Swagger UI: http://localhost:8000/docs
- Redoc: http://localhost:8000/redoc

## Deployment

1. Build Docker image:
   ```bash
   docker-compose build
   ```

2. Start services:
   ```bash
   docker-compose up -d
   ```

## Database

The API uses PostgreSQL with the following default credentials:
- Database: mibitech
- User: postgres
- Password: postgres

Initial social media data is automatically seeded on first run.