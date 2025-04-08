# MibiTech Website

A modern website for MibiTech company with a Django backend API and a JavaScript frontend.

## Project Structure

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
│   ├── Dockerfile       # Nginx Docker configuration
│   └── nginx.conf       # Nginx configuration file
├── docker-compose.yml   # Docker Compose configuration
├── deploy.sh            # Deployment script for Linux/Mac
└── deploy.bat           # Deployment script for Windows
```

## Local Development Setup

### Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Git](https://git-scm.com/downloads)

### Running Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/mibitech.git
   cd mibitech
   ```

2. Build and start the containers:
   ```bash
   # Linux/Mac
   ./deploy.sh --build --up
   
   # Windows
   deploy.bat --build --up
   ```

3. Access the application:
   - Frontend: http://localhost:3000 (configurável via FRONTEND_PORT)
   - Backend API: Configurável via API_BASE_URL
   - Admin panel: Configurável via BACKEND_ADMIN_URL

## Deployment to a VPS

### Prerequisites

- A VPS with Ubuntu 20.04 or later
- Docker and Docker Compose installed on the VPS
- Domain name (optional)

### Step 1: Set Up Your VPS

1. Connect to your VPS via SSH:
   ```bash
   ssh username@your-vps-ip
   ```

2. Update the system:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

3. Install Docker:
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   ```

4. Install Docker Compose:
   ```bash
   sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.3/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   ```

5. Add your user to the docker group:
   ```bash
   sudo usermod -aG docker $USER
   ```

6. Log out and log back in for the changes to take effect.

### Step 2: Deploy the Application

1. Clone the repository on your VPS:
   ```bash
   git clone https://github.com/rlcunha/mibitech.git
   cd mibitech
   ```

2. Create a `.env` file for environment variables (optional):
   ```bash
   touch .env
   ```

3. Edit the `.env` file with your configuration:
   ```
   DEBUG=False
   ALLOWED_HOSTS=your-domain.com,www.your-domain.com
   ```

4. Build and start the containers:
   ```bash
   ./deploy.sh --build --up
   ```

5. Access your application at your VPS IP address or domain name.

### Step 3: Set Up Domain Name (Optional)

1. Configure your domain's DNS settings to point to your VPS IP address.

2. Update the nginx configuration in `nginx/nginx.conf`:
   ```
   server_name your-domain.com www.your-domain.com;
   ```

3. Restart the nginx container:
   ```bash
   ./deploy.sh --restart --nginx
   ```

### Step 4: Set Up SSL with Let's Encrypt (Optional)

1. Install Certbot:
   ```bash
   sudo apt install certbot python3-certbot-nginx -y
   ```

2. Obtain SSL certificate:
   ```bash
   sudo certbot --nginx -d your-domain.com -d www.your-domain.com
   ```

3. Follow the prompts to complete the SSL setup.

## Docker Container Management

### Using the Deployment Scripts

The project includes deployment scripts for both Linux/Mac (`deploy.sh`) and Windows (`deploy.bat`) to simplify Docker container management.

#### Available Commands

- Build containers:
  ```bash
  # Linux/Mac
  ./deploy.sh --build
  
  # Windows
  deploy.bat --build
  ```

- Start containers:
  ```bash
  # Linux/Mac
  ./deploy.sh --up
  
  # Windows
  deploy.bat --up
  ```

- Stop containers:
  ```bash
  # Linux/Mac
  ./deploy.sh --down
  
  # Windows
  deploy.bat --down
  ```

- Restart containers:
  ```bash
  # Linux/Mac
  ./deploy.sh --restart
  
  # Windows
  deploy.bat --restart
  ```

- View logs:
  ```bash
  # Linux/Mac
  ./deploy.sh --logs
  
  # Windows
  deploy.bat --logs
  ```

#### Managing Individual Containers

You can also manage individual containers by specifying the service name:

- Frontend:
  ```bash
  # Linux/Mac
  ./deploy.sh --frontend --restart
  
  # Windows
  deploy.bat --frontend --restart
  ```

- Backend:
  ```bash
  # Linux/Mac
  ./deploy.sh --backend --logs
  
  # Windows
  deploy.bat --backend --logs
  ```

- Nginx:
  ```bash
  # Linux/Mac
  ./deploy.sh --nginx --build
  
  # Windows
  deploy.bat --nginx --build
  ```

## Updating the Application

### Pulling Changes from Git

1. Navigate to your project directory:
   ```bash
   cd mibitech
   ```

2. Pull the latest changes:
   ```bash
   git pull origin main
   ```

3. Rebuild and restart the containers:
   ```bash
   # Linux/Mac
   ./deploy.sh --build --restart
   
   # Windows
   deploy.bat --build --restart
   ```

### Making Individual Service Updates

If you only need to update a specific service:

1. Pull the latest changes:
   ```bash
   git pull origin main
   ```

2. Rebuild and restart only the affected service:
   ```bash
   # For frontend updates (Linux/Mac)
   ./deploy.sh --frontend --build --restart
   
   # For backend updates (Windows)
   deploy.bat --backend --build --restart
   ```

## Troubleshooting

### Common Issues

1. **Container fails to start**:
   - Check the logs: `./deploy.sh --logs`
   - Verify environment variables in `.env` file
   - Ensure ports are not already in use

2. **Cannot connect to the application**:
   - Verify containers are running: `docker-compose ps`
   - Check firewall settings on your VPS
   - Ensure correct ports are exposed in `docker-compose.yml`

3. **Database connection issues**:
   - Check database credentials in environment variables
   - Verify database container is running

### Getting Help

If you encounter any issues not covered in this documentation, please:

1. Check the logs for error messages
2. Consult the Docker and Docker Compose documentation
3. Open an issue on the GitHub repository

## License

This project is licensed under the MIT License - see the LICENSE file for details.