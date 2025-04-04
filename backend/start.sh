#!/bin/bash\r\n
\r\n
# Wait for database to be ready\r\n
echo "Waiting for database..."\r\n
while ! nc -z postgres 5432; do\r\n
  sleep 0.1\r\n
done\r\n
echo "Database ready"\r\n
\r\n
# Initialize database\r\n
python init_db.py\r\n
\r\n
# Start FastAPI server\r\n
uvicorn app.main:app --host $APP_HOST --port $APP_PORT --reload\r\n