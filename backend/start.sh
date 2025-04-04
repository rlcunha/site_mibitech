#!/bin/bash

# Wait for database to be ready
echo "Waiting for database..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "Database ready"

# Initialize database
python init_db.py

# Start FastAPI server
uvicorn app.main:app --host $APP_HOST --port $APP_PORT --reload