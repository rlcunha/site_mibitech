# Local Environment Setup: MibiTech

This is a simplified guide for setting up and running the MibiTech project locally.

## Project Structure

The MibiTech project is divided into two main parts:

1. **Backend (Django)**: REST API that provides data to the frontend
2. **Frontend (JavaScript)**: User interface that consumes the API

## Quick Setup

### Prerequisites

- Python 3.9+
- Node.js 18+
- Git
- Docker and Docker Compose (optional)

### Using Setup Scripts

To facilitate the setup, use the provided scripts:

**On Windows:**
```
local_dev_setup.bat
```

**On Linux/Mac:**
```
chmod +x local_dev_setup.sh
./local_dev_setup.sh
```

### Manual Setup

If you prefer to set up manually:

#### Backend (Django)

1. Navigate to the backend folder:
   ```
   cd backend
   ```

2. Create a Python virtual environment:
   ```
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run database migrations:
   ```
   python manage.py migrate
   ```

5. Start the server:
   ```
   python manage.py runserver
   ```

The backend will be available at: http://localhost:8000/api/

#### Frontend (JavaScript)

1. Navigate to the frontend folder:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the server:
   ```
   node server.js
   ```

The frontend will be available at: http://localhost:3000

## Using Docker

If you prefer to use Docker:

1. Build and start the containers:
   ```
   # Windows
   deploy.bat --build --up

   # Linux/Mac
   ./deploy.sh --build --up
   ```

2. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/api/

## Available Pages

- **Home**: http://localhost:3000/
- **About**: http://localhost:3000/sobre.html
- **Portfolio**: http://localhost:3000/portfolio.html
- **Blog**: http://localhost:3000/blog.html
- **Contact**: http://localhost:3000/contato.html

## Development

### Basic Workflow

1. Make changes to the code
2. Test locally
3. Commit and push to GitHub (see `criar_repositorio_github.md`)
4. Deploy to the server (see `VPS_DEPLOYMENT.md`)

### Useful Commands

**Restart Docker services:**
```
# Windows
deploy.bat --restart

# Linux/Mac
./deploy.sh --restart
```

**View logs:**
```
# Windows
deploy.bat --logs

# Linux/Mac
./deploy.sh --logs
```

## Troubleshooting

### Common Issues

1. **Ports already in use**:
   - Check if another process is using ports 3000 or 8000
   - Terminate the process or change the ports in the configuration files

2. **API connection error**:
   - Check if the backend is running
   - Verify that the API URLs are correct

3. **Dependency errors**:
   - Update dependencies:
     ```
     # Backend
     pip install -r requirements.txt

     # Frontend
     npm install
     ```

## Additional Documentation

For more detailed information, see:

- `README.md`: Project overview
- `LOCAL_DEVELOPMENT.md`: Detailed local development guide
- `VPS_DEPLOYMENT.md`: Instructions for deploying to a VPS server
- `criar_repositorio_github.md`: How to set up the GitHub repository

## Support

If you encounter issues not covered in this guide, refer to the complete documentation or open an issue in the GitHub repository.