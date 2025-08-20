# ArchInsight Deployment Guide

This guide covers deploying ArchInsight to production environments.

## 🚀 Quick Start

### 1. Prerequisites

- **Docker & Docker Compose**: Version 20.10+ and 2.0+
- **Git**: For cloning the repository
- **Domain**: For production deployment
- **SSL Certificate**: For HTTPS (Let's Encrypt recommended)
- **API Keys**: OpenAI, GitHub OAuth (optional)

### 2. Clone and Setup

```bash
git clone <your-repo-url>
cd ArchInsight
cp env.production.example .env.production
# Edit .env.production with your actual values
```

### 3. Deploy

```bash
./scripts/deploy.sh
```

## 📋 Environment Configuration

### Required Environment Variables

Create a `.env.production` file with the following variables:

```bash
# Application Settings
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO

# Security
JWT_SECRET_KEY=your_super_secret_jwt_key_here
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=30

# Database Configuration
POSTGRES_PASSWORD=your_secure_postgres_password
NEO4J_PASSWORD=your_secure_neo4j_password
REDIS_PASSWORD=your_secure_redis_password

# External API Keys
OPENAI_API_KEY=your_openai_api_key
GITHUB_CLIENT_ID=your_github_oauth_client_id
GITHUB_CLIENT_SECRET=your_github_oauth_client_secret

# CORS Settings
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# API Base URL
API_BASE_URL=https://api.yourdomain.com
```

### Security Considerations

- **JWT Secret**: Use a strong, random 64+ character string
- **Database Passwords**: Use strong, unique passwords
- **API Keys**: Store securely and rotate regularly
- **CORS Origins**: Restrict to your actual domains

## 🐳 Docker Deployment

### Production Docker Compose

The `docker-compose.prod.yml` file includes:

- **PostgreSQL**: Primary database
- **Neo4j**: Graph database for dependency analysis
- **Redis**: Caching and session storage
- **Backend**: FastAPI application
- **Frontend**: React application
- **Nginx**: Reverse proxy and SSL termination
- **ML Service**: Optional GPU-enabled ML processing

### Deploy with Docker Compose

```bash
# Start all services
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Stop services
docker-compose -f docker-compose.prod.yml down

# Update services
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d
```

## 🌐 Domain and SSL Configuration

### 1. Domain Setup

Configure your domain's DNS to point to your server:
- **A Record**: `@` → Your server IP
- **A Record**: `api` → Your server IP (for API subdomain)

### 2. SSL Certificate

#### Option A: Let's Encrypt (Recommended)

```bash
# Install Certbot
sudo apt-get update
sudo apt-get install certbot

# Get certificate
sudo certbot certonly --standalone -d yourdomain.com -d api.yourdomain.com

# Certificates will be in /etc/letsencrypt/live/yourdomain.com/
```

#### Option B: Self-Signed (Development Only)

```bash
# Generate self-signed certificate
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx/ssl/key.pem \
  -out nginx/ssl/cert.pem
```

### 3. Nginx Configuration

Create `nginx/nginx.conf`:

```nginx
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend:8000;
    }

    upstream frontend {
        server frontend:80;
    }

    server {
        listen 80;
        server_name yourdomain.com www.yourdomain.com;
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name yourdomain.com www.yourdomain.com;

        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;

        # Frontend
        location / {
            proxy_pass http://frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        # Backend API
        location /api/ {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
}
```

## 🗄️ Database Setup

### PostgreSQL

```bash
# Connect to PostgreSQL
docker-compose -f docker-compose.prod.yml exec postgres psql -U archinsight_prod -d archinsight

# Run migrations
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head
```

### Neo4j

```bash
# Access Neo4j Browser
# Open http://yourdomain.com:7474 in your browser
# Login with neo4j/your_password
# Change password on first login
```

## 📊 Monitoring and Health Checks

### Health Check Endpoints

- **Backend**: `http://yourdomain.com/api/v1/health`
- **Detailed Health**: `http://yourdomain.com/api/v1/health/detailed`

### Log Monitoring

```bash
# View all logs
docker-compose -f docker-compose.prod.yml logs -f

# View specific service logs
docker-compose -f docker-compose.prod.yml logs -f backend
docker-compose -f docker-compose.prod.yml logs -f frontend
```

### Performance Monitoring

- **Application Metrics**: Available at `/api/v1/metrics`
- **Database Monitoring**: Use PostgreSQL and Neo4j built-in tools
- **System Monitoring**: Consider Prometheus + Grafana

## 🔒 Security Hardening

### 1. Firewall Configuration

```bash
# UFW (Ubuntu)
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable

# iptables (CentOS/RHEL)
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT
```

### 2. Database Security

- Change default passwords
- Restrict network access
- Enable SSL connections
- Regular security updates

### 3. Application Security

- Enable rate limiting
- Input validation
- SQL injection prevention
- XSS protection
- CORS configuration

## 💾 Backup Strategy

### Automated Backups

```bash
# Create backup script
cat > scripts/backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/archinsight_$DATE"

mkdir -p "$BACKUP_DIR"

# PostgreSQL backup
docker-compose -f docker-compose.prod.yml exec -T postgres \
  pg_dump -U archinsight_prod archinsight > "$BACKUP_DIR/postgres.sql"

# Neo4j backup
docker-compose -f docker-compose.prod.yml exec -T neo4j \
  neo4j-admin database backup neo4j --to-path=/backups/neo4j

# Application data backup
tar -czf "$BACKUP_DIR/app_data.tar.gz" data/ logs/

echo "Backup completed: $BACKUP_DIR"
EOF

chmod +x scripts/backup.sh
```

### Backup Schedule

```bash
# Add to crontab
0 2 * * * /path/to/ArchInsight/scripts/backup.sh
```

## 🚀 CI/CD Pipeline

### GitHub Actions Example

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to server
        uses: appleboy/ssh-action@v0.1.5
        with:
          host: ${{ secrets.HOST }}
          username: ${{ secrets.USERNAME }}
          key: ${{ secrets.KEY }}
          script: |
            cd /path/to/ArchInsight
            git pull origin main
            docker-compose -f docker-compose.prod.yml pull
            docker-compose -f docker-compose.prod.yml up -d
            docker-compose -f docker-compose.prod.yml exec -T backend alembic upgrade head
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Services Not Starting

```bash
# Check service status
docker-compose -f docker-compose.prod.yml ps

# Check logs
docker-compose -f docker-compose.prod.yml logs service_name

# Check resource usage
docker stats
```

#### 2. Database Connection Issues

```bash
# Test PostgreSQL connection
docker-compose -f docker-compose.prod.yml exec postgres pg_isready -U archinsight_prod

# Test Neo4j connection
docker-compose -f docker-compose.prod.yml exec neo4j neo4j status
```

#### 3. Port Conflicts

```bash
# Check port usage
sudo netstat -tulpn | grep :80
sudo netstat -tulpn | grep :443
sudo netstat -tulpn | grep :8000
```

### Performance Issues

- **Memory**: Increase container memory limits
- **CPU**: Monitor CPU usage and scale accordingly
- **Disk I/O**: Use SSD storage for databases
- **Network**: Optimize network configuration

## 📈 Scaling

### Horizontal Scaling

```yaml
# docker-compose.prod.yml
services:
  backend:
    deploy:
      replicas: 3
    environment:
      - REDIS_URL=redis://redis:6379
```

### Load Balancing

- Use Nginx as load balancer
- Implement health checks
- Configure sticky sessions if needed

### Database Scaling

- **PostgreSQL**: Read replicas, connection pooling
- **Neo4j**: Cluster deployment
- **Redis**: Redis Cluster for high availability

## 🆘 Support

- **Documentation**: Check the main README.md
- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Security**: Report security issues privately

## 📝 Maintenance

### Regular Tasks

- **Daily**: Monitor logs and metrics
- **Weekly**: Review performance and security
- **Monthly**: Update dependencies and security patches
- **Quarterly**: Review backup and disaster recovery

### Updates

```bash
# Update application
git pull origin main
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d

# Update system packages
sudo apt-get update && sudo apt-get upgrade
```

---

**Remember**: Always test deployments in a staging environment first!
