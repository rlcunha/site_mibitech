#!/bin/bash

# Skip waiting for postgres since we're connecting to an external database
echo "Connecting to external database..."

# Initialize database
python init_db.py

# Start FastAPI server
uvicorn app.main:app --host $APP_HOST --port $APP_PORT --reload