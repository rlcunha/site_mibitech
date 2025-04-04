# MibiTech Local Development Guide

This guide provides detailed instructions for setting up and running the MibiTech application in a local development environment.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Project Structure](#project-structure)
3. [Backend Setup](#backend-setup)
4. [Frontend Setup](#frontend-setup)
5. [Running with Docker](#running-with-docker)
6. [Running without Docker](#running-without-docker)
7. [Development Workflow](#development-workflow)
8. [Testing](#testing)
9. [Troubleshooting](#troubleshooting)

## Prerequisites

Before you begin, ensure you have the following installed:

- [Git](https://git-scm.com/downloads)
- [Python 3.9+](https://www.python.org/downloads/)
- [Node.js 18+](https://nodejs.org/)
- [Docker](https://www.docker.com/get-started) (optional, for containerized development)
- [Docker Compose](https://docs.docker.com/compose/install/) (optional, for containerized development)

## Project Structure

The MibiTech project is organized as follows:

```
mibitech/
├── backend/             # Django backend API
│   ├── api/             # API app
│   ├── backend/         # Django project settings
│   ├── Dockerfile       # Backend Docker configuration
│   └── requirements.txt # Python dependencies
├── frontend/            # JavaScript frontend
│   ├── controllers/     # Frontend controllers
│   ├── models/          # Frontend models
│   ├── public/          # Static assets
│   ├── views/           # HTML views
│   ├── Dockerfile       # Frontend Docker configuration
│   └── server.js        # Node.js server
├── nginx/               # Nginx configuration
├── docker-compose.yml   # Docker Compose configuration
└── deploy.sh/bat        # Deployment scripts
```

## Backend Setup

### Setting Up a Python Virtual Environment

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   # Linux/Mac
   python3 -m venv venv
   
   # Windows
   python -m venv venv
   ```

3. Activate the virtual environment:
   ```bash
   # Linux/Mac
   source venv/bin/activate
   
   # Windows
   venv\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Database Setup

1. Apply migrations:
   ```bash
   python manage.py migrate
   ```

2. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

3. Load initial data (if available):
   ```bash
   python manage.py loaddata api/fixtures/initial_data.json
   ```

### Running the Backend Server

Start the Django development server:

```bash
python manage.py runserver
```

The backend API will be available at http://localhost:8000/api/

## Frontend Setup

### Installing Dependencies

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

### Running the Frontend Server

Start the Node.js server:

```bash
node server.js
```

The frontend will be available at http://localhost:3000

## Running with Docker

If you prefer to use Docker for development, you can use the provided Docker Compose configuration.

### Starting All Services

1. Build and start all containers:
   ```bash
   # Linux/Mac
   ./deploy.sh --build --up
   
   # Windows
   deploy.bat --build --up
   ```

2. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/api/
   - Admin panel: http://localhost:8000/admin/

### Starting Individual Services

You can also start individual services:

```bash
# Linux/Mac
./deploy.sh --frontend --build --up
./deploy.sh --backend --build --up

# Windows
deploy.bat --frontend --build --up
deploy.bat --backend --build --up
```

### Viewing Logs

View logs from all containers:

```bash
# Linux/Mac
./deploy.sh --logs

# Windows
deploy.bat --logs
```

Or view logs from a specific container:

```bash
# Linux/Mac
./deploy.sh --frontend --logs
./deploy.sh --backend --logs

# Windows
deploy.bat --frontend --logs
deploy.bat --backend --logs
```

## Running without Docker

If you prefer not to use Docker, you can run the frontend and backend servers directly.

1. Start the backend server:
   ```bash
   cd backend
   # Activate virtual environment
   python manage.py runserver
   ```

2. In a separate terminal, start the frontend server:
   ```bash
   cd frontend
   node server.js
   ```

## Development Workflow

### Backend Development

1. Make changes to the Django code
2. Run migrations if needed:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
3. Restart the Django server if needed

### Frontend Development

1. Make changes to the frontend code
2. The changes will be reflected when you refresh the browser
3. For JavaScript changes, you may need to restart the Node.js server

### API Testing

You can test the API endpoints using tools like:
- [Postman](https://www.postman.com/)
- [Insomnia](https://insomnia.rest/)
- [curl](https://curl.se/)

Example API request:

```bash
curl http://localhost:8000/api/contacts/
```

## Testing

### Backend Tests

Run Django tests:

```bash
cd backend
python manage.py test
```

### Frontend Tests

If you have frontend tests set up, you can run them with:

```bash
cd frontend
npm test
```

## Troubleshooting

### Common Issues

1. **Port already in use**:
   - Check if another process is using the required ports (8000 for backend, 3000 for frontend)
   - Kill the process or change the port in the configuration

2. **Database migration issues**:
   - Try resetting migrations:
     ```bash
     python manage.py migrate api zero
     python manage.py makemigrations
     python manage.py migrate
     ```

3. **Node.js dependency issues**:
   - Try clearing the npm cache:
     ```bash
     npm cache clean --force
     rm -rf node_modules
     npm install
     ```

4. **Docker issues**:
   - Check Docker logs:
     ```bash
     docker-compose logs
     ```
   - Restart Docker:
     ```bash
     docker-compose down
     docker-compose up -d
     ```

### Getting Help

If you encounter any issues not covered in this guide:

1. Check the project documentation
2. Consult the Django and Node.js documentation
3. Open an issue on the GitHub repository

## Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework Documentation](https://www.django-rest-framework.org/)
- [Node.js Documentation](https://nodejs.org/en/docs/)
- [Docker Documentation](https://docs.docker.com/)