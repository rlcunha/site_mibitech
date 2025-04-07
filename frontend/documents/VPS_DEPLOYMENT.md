# MibiTech VPS Deployment Guide

This guide provides detailed instructions for deploying the MibiTech application on a Virtual Private Server (VPS).

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Initial Server Setup](#initial-server-setup)
3. [Installing Docker and Docker Compose](#installing-docker-and-docker-compose)
4. [Deploying the Application](#deploying-the-application)
5. [Setting Up Domain and SSL](#setting-up-domain-and-ssl)
6. [Maintenance and Updates](#maintenance-and-updates)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

Before you begin, you'll need:

- A VPS with at least 1GB RAM and 20GB storage (recommended providers: DigitalOcean, Linode, AWS, or GCP)
- A domain name (optional, but recommended for production)
- SSH access to your VPS
- Basic knowledge of Linux command line

## Initial Server Setup

### Step 1: Connect to Your VPS

Connect to your VPS using SSH:

```bash
ssh username@your-vps-ip
```

Replace `username` with your server username and `your-vps-ip` with your server's IP address.

### Step 2: Update System Packages

Update the package lists and upgrade installed packages:

```bash
sudo apt update
sudo apt upgrade -y
```

### Step 3: Create a Non-Root User (Optional)

If you're logged in as root, it's recommended to create a non-root user with sudo privileges:

```bash
# Create a new user
adduser mibitech

# Add user to sudo group
usermod -aG sudo mibitech

# Switch to the new user
su - mibitech
```

### Step 4: Set Up Firewall

Configure the firewall to allow SSH, HTTP, and HTTPS traffic:

```bash
sudo ufw allow OpenSSH
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

Verify the firewall status:

```bash
sudo ufw status
```

## Installing Docker and Docker Compose

### Step 1: Install Docker

Install Docker using the official installation script:

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

### Step 2: Install Docker Compose

Install Docker Compose:

```bash
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.3/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

Verify the installation:

```bash
docker --version
docker-compose --version
```

### Step 3: Add Your User to the Docker Group

This allows you to run Docker commands without sudo:

```bash
sudo usermod -aG docker $USER
```

Log out and log back in for the changes to take effect:

```bash
exit
# Log back in
ssh username@your-vps-ip
```

## Deploying the Application

### Step 1: Clone the Repository

Create a directory for the application and clone the repository:

```bash
mkdir -p /var/www
cd /var/www
mkdir -p /var/www
cd mibitech
```

### Step 2: Configure Environment Variables

Create a `.env` file for environment variables:

```bash
touch .env
```

Edit the `.env` file with your configuration:

```
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com,your-vps-ip
SECRET_KEY=your-secret-key
```

Replace `your-domain.com` with your actual domain name and `your-vps-ip` with your server's IP address.

### Step 3: Build and Start the Containers

Make the deployment script executable:

```bash
chmod +x deploy.sh
```

Build and start the containers:

```bash
./deploy.sh --build --up
```

### Step 4: Verify the Deployment

Check if the containers are running:

```bash
docker-compose ps
```

You should see all containers in the "Up" state.

Access your application:
- Using IP address: http://your-vps-ip
- Using domain (if configured): http://your-domain.com

## Setting Up Domain and SSL

### Step 1: Configure DNS

In your domain registrar's DNS settings, add an A record pointing to your VPS IP address:

```
Type: A
Name: @
Value: your-vps-ip
TTL: 3600 (or automatic)
```

If you want to include the www subdomain, add a CNAME record:

```
Type: CNAME
Name: www
Value: your-domain.com
TTL: 3600 (or automatic)
```

### Step 2: Update Nginx Configuration

Edit the nginx configuration file:

```bash
nano nginx/nginx.conf
```

Update the server_name directive:

```
server_name your-domain.com www.your-domain.com;
```

Rebuild and restart the nginx container:

```bash
./deploy.sh --nginx --build --restart
```

### Step 3: Set Up SSL with Let's Encrypt

Install Certbot:

```bash
sudo apt install certbot python3-certbot-nginx -y
```

Obtain SSL certificate:

```bash
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

Follow the prompts to complete the SSL setup.

Certbot will automatically update your nginx configuration to use SSL.

### Step 4: Set Up Auto-Renewal for SSL Certificates

Let's Encrypt certificates expire after 90 days. Set up auto-renewal:

```bash
sudo systemctl status certbot.timer
```

This should show that the certbot timer is active and enabled.

## Maintenance and Updates

### Updating the Application

To update the application with the latest changes:

1. Navigate to your project directory:
   ```bash
   cd /var/www/mibitech
   ```

2. Pull the latest changes:
   ```bash
   git pull origin main
   ```

3. Rebuild and restart the containers:
   ```bash
   ./deploy.sh --build --restart
   ```

### Backing Up the Application

It's important to regularly back up your application data:

1. Back up the database (if applicable):
   ```bash
   docker-compose exec backend python manage.py dumpdata > backup_$(date +%Y%m%d).json
   ```

2. Back up environment variables:
   ```bash
   cp .env .env.backup_$(date +%Y%m%d)
   ```

3. Consider setting up automated backups using a cron job.

### Monitoring the Application

Monitor your application logs:

```bash
./deploy.sh --logs
```

For specific service logs:

```bash
./deploy.sh --frontend --logs
./deploy.sh --backend --logs
./deploy.sh --nginx --logs
```

## Troubleshooting

### Common Issues

1. **Container fails to start**:
   - Check the logs: `./deploy.sh --logs`
   - Verify environment variables in `.env` file
   - Ensure ports are not already in use

2. **Cannot connect to the application**:
   - Verify containers are running: `docker-compose ps`
   - Check firewall settings: `sudo ufw status`
   - Ensure correct ports are exposed in `docker-compose.yml`

3. **SSL certificate issues**:
   - Verify DNS settings have propagated: `nslookup your-domain.com`
   - Check Certbot logs: `sudo certbot certificates`
   - Manually renew certificate: `sudo certbot renew --dry-run`

### Restarting Services

If a specific service is having issues, you can restart it:

```bash
./deploy.sh --frontend --restart
./deploy.sh --backend --restart
./deploy.sh --nginx --restart
```

To restart all services:

```bash
./deploy.sh --restart
```

### Checking Container Status

View detailed information about containers:

```bash
docker-compose ps
docker stats
```

### Accessing Container Shell

To access a shell inside a container:

```bash
docker-compose exec frontend sh
docker-compose exec backend bash
docker-compose exec nginx sh
```

This can be useful for debugging or running commands inside the container.

## Conclusion

You have successfully deployed the MibiTech application on your VPS. The application is now accessible via your domain name with HTTPS enabled.

For additional help or to report issues, please refer to the project's GitHub repository or contact the development team.