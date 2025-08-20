# 🐳 Docker Deployment Guide

## Quick Start (Local)

### 1. Build and Run Locally
```bash
# Build the Docker image
docker build -t college-practical-helper .

# Run the container
docker run -p 5000:5000 \
  -e SECRET_KEY=your-super-secure-secret-key \
  -e FLASK_ENV=production \
  college-practical-helper
```

### 2. Using Docker Compose (Recommended)
```bash
# Create .env file
echo "SECRET_KEY=your-super-secure-secret-key-here" > .env

# Start with docker-compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

Access your app at: http://localhost:5000

---

## 🌐 Cloud Deployment Options

### Option 1: DigitalOcean Droplet

#### 1. Create Droplet
- Create Ubuntu 22.04 droplet
- SSH into your server

#### 2. Install Docker
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

#### 3. Deploy Application
```bash
# Clone your repository
git clone <your-repo-url>
cd college_practical_helper

# Set environment variables
echo "SECRET_KEY=$(openssl rand -base64 32)" > .env

# Deploy
docker-compose up -d
```

#### 4. Set up Nginx (Optional but Recommended)
```bash
# Install Nginx
sudo apt install nginx -y

# Create Nginx config
sudo tee /etc/nginx/sites-available/college-helper << EOF
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/college-helper /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl reload nginx
```

---

### Option 2: AWS ECS (Elastic Container Service)

#### 1. Build and Push to ECR
```bash
# Create ECR repository
aws ecr create-repository --repository-name college-practical-helper

# Get login command
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Tag and push image
docker tag college-practical-helper:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/college-practical-helper:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/college-practical-helper:latest
```

#### 2. Create ECS Task Definition
```json
{
  "family": "college-practical-helper",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "executionRoleArn": "arn:aws:iam::<account>:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "college-helper",
      "image": "<account-id>.dkr.ecr.us-east-1.amazonaws.com/college-practical-helper:latest",
      "portMappings": [
        {
          "containerPort": 5000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "FLASK_ENV",
          "value": "production"
        },
        {
          "name": "SECRET_KEY",
          "value": "your-secret-key"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/college-practical-helper",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

---

### Option 3: Railway.app (Easiest)

#### 1. Deploy to Railway
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize and deploy
railway init
railway up
```

#### 2. Set Environment Variables
```bash
railway variables set SECRET_KEY=$(openssl rand -base64 32)
railway variables set FLASK_ENV=production
```

---

### Option 4: Google Cloud Run

#### 1. Build and Deploy
```bash
# Set project ID
export PROJECT_ID=your-project-id

# Build and push to Container Registry
gcloud builds submit --tag gcr.io/$PROJECT_ID/college-practical-helper

# Deploy to Cloud Run
gcloud run deploy college-practical-helper \
  --image gcr.io/$PROJECT_ID/college-practical-helper \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="FLASK_ENV=production,SECRET_KEY=your-secret-key"
```

---

### Option 5: Azure Container Instances

#### 1. Create Resource Group
```bash
az group create --name college-helper-rg --location eastus
```

#### 2. Deploy Container
```bash
az container create \
  --resource-group college-helper-rg \
  --name college-practical-helper \
  --image your-dockerhub-username/college-practical-helper \
  --cpu 1 \
  --memory 1 \
  --ports 5000 \
  --environment-variables FLASK_ENV=production SECRET_KEY=your-secret-key \
  --dns-name-label college-helper-unique
```

---

## 🔒 Production Security Checklist

### Environment Variables
Create `.env` file for production:
```bash
SECRET_KEY=your-super-secure-64-character-secret-key
FLASK_ENV=production
DATABASE_PATH=/app/instance/database.db
HOST=0.0.0.0
PORT=5000
```

### Security Best Practices
- [ ] Change default admin password (admin/admin123)
- [ ] Use strong SECRET_KEY
- [ ] Enable HTTPS with SSL certificates
- [ ] Set up firewall rules
- [ ] Regular security updates
- [ ] Use non-root user in container
- [ ] Implement rate limiting
- [ ] Add monitoring and logging

---

## 📊 Monitoring & Maintenance

### Docker Commands
```bash
# Check container status
docker ps

# View logs
docker logs college_practical_helper

# Update application
docker-compose pull
docker-compose up -d

# Backup database
docker exec college_practical_helper cp /app/instance/database.db /tmp/
docker cp college_practical_helper:/tmp/database.db ./backup-$(date +%Y%m%d).db

# Restore database
docker cp ./backup.db college_practical_helper:/app/instance/database.db
docker-compose restart
```

### Health Check
Your app includes a health check endpoint. Monitor it:
```bash
curl http://your-domain.com/
```

---

## 🚨 Troubleshooting

### Common Issues

#### Container Won't Start
```bash
# Check logs
docker logs college_practical_helper

# Debug by running interactively
docker run -it --entrypoint /bin/bash college-practical-helper
```

#### Database Issues
```bash
# Check if database file exists
docker exec college_practical_helper ls -la /app/instance/

# Reset database
docker exec college_practical_helper rm /app/instance/database.db
docker-compose restart
```

#### Permission Issues
```bash
# Fix permissions
docker exec -u root college_practical_helper chown -R appuser:appuser /app/instance/
```

---

## 🔄 CI/CD Pipeline (GitHub Actions)

Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Build Docker image
      run: docker build -t college-practical-helper .
    
    - name: Deploy to server
      run: |
        # Add your deployment commands here
        # e.g., push to registry, update server, etc.
```

---

## 📞 Support

If you encounter issues:
1. Check the logs: `docker-compose logs -f`
2. Verify environment variables are set correctly
3. Ensure database permissions are correct
4. Check firewall and port settings

**Default Admin Credentials:**
- Username: `admin`
- Password: `admin123` (⚠️ Change this immediately!)

Your Flask application will be available at the configured port (default: 5000).
