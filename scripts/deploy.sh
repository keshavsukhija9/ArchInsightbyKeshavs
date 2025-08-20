#!/bin/bash

# ArchInsight Production Deployment Script
# This script deploys the complete ArchInsight application to production

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="archinsight"
ENV_FILE=".env.production"
COMPOSE_FILE="docker-compose.prod.yml"

echo -e "${BLUE}🚀 ArchInsight Production Deployment${NC}"
echo "=================================="

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo -e "${RED}❌ This script should not be run as root${NC}"
   exit 1
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running. Please start Docker and try again.${NC}"
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed. Please install it and try again.${NC}"
    exit 1
fi

# Check if environment file exists
if [[ ! -f "$ENV_FILE" ]]; then
    echo -e "${RED}❌ Environment file $ENV_FILE not found.${NC}"
    echo -e "${YELLOW}Please copy env.production.example to $ENV_FILE and configure it.${NC}"
    exit 1
fi

# Load environment variables
echo -e "${BLUE}📋 Loading environment variables...${NC}"
source "$ENV_FILE"

# Validate required environment variables
required_vars=(
    "POSTGRES_PASSWORD"
    "NEO4J_PASSWORD"
    "REDIS_PASSWORD"
    "JWT_SECRET_KEY"
    "OPENAI_API_KEY"
    "GITHUB_CLIENT_ID"
    "GITHUB_CLIENT_SECRET"
    "CORS_ORIGINS"
    "API_BASE_URL"
)

for var in "${required_vars[@]}"; do
    if [[ -z "${!var}" ]]; then
        echo -e "${RED}❌ Required environment variable $var is not set${NC}"
        exit 1
    fi
done

echo -e "${GREEN}✅ Environment variables loaded successfully${NC}"

# Create necessary directories
echo -e "${BLUE}📁 Creating necessary directories...${NC}"
mkdir -p data/{uploads,cache,models,postgres/init}
mkdir -p logs
mkdir -p nginx/{ssl,conf}

echo -e "${GREEN}✅ Directories created successfully${NC}"

# Set proper permissions
echo -e "${BLUE}🔐 Setting proper permissions...${NC}"
chmod 755 data logs nginx
chmod 700 data/postgres/init

echo -e "${GREEN}✅ Permissions set successfully${NC}"

# Stop existing containers if running
echo -e "${BLUE}🛑 Stopping existing containers...${NC}"
docker-compose -f "$COMPOSE_FILE" down --remove-orphans || true

echo -e "${GREEN}✅ Existing containers stopped${NC}"

# Pull latest images
echo -e "${BLUE}📥 Pulling latest Docker images...${NC}"
docker-compose -f "$COMPOSE_FILE" pull

echo -e "${GREEN}✅ Images pulled successfully${NC}"

# Build images
echo -e "${BLUE}🔨 Building Docker images...${NC}"
docker-compose -f "$COMPOSE_FILE" build --no-cache

echo -e "${GREEN}✅ Images built successfully${NC}"

# Start services
echo -e "${BLUE}🚀 Starting services...${NC}"
docker-compose -f "$COMPOSE_FILE" up -d

echo -e "${GREEN}✅ Services started successfully${NC}"

# Wait for services to be healthy
echo -e "${BLUE}⏳ Waiting for services to be healthy...${NC}"
timeout=300  # 5 minutes timeout
elapsed=0

while [[ $elapsed -lt $timeout ]]; do
    if docker-compose -f "$COMPOSE_FILE" ps | grep -q "healthy"; then
        echo -e "${GREEN}✅ All services are healthy${NC}"
        break
    fi
    
    echo -e "${YELLOW}⏳ Waiting for services to be healthy... (${elapsed}s/${timeout}s)${NC}"
    sleep 10
    elapsed=$((elapsed + 10))
done

if [[ $elapsed -ge $timeout ]]; then
    echo -e "${RED}❌ Timeout waiting for services to be healthy${NC}"
    echo -e "${YELLOW}Checking service status...${NC}"
    docker-compose -f "$COMPOSE_FILE" ps
    exit 1
fi

# Run database migrations
echo -e "${BLUE}🗄️ Running database migrations...${NC}"
docker-compose -f "$COMPOSE_FILE" exec -T backend alembic upgrade head || {
    echo -e "${RED}❌ Database migration failed${NC}"
    exit 1
}

echo -e "${GREEN}✅ Database migrations completed${NC}"

# Check service status
echo -e "${BLUE}📊 Checking service status...${NC}"
docker-compose -f "$COMPOSE_FILE" ps

# Display access information
echo -e "${GREEN}🎉 Deployment completed successfully!${NC}"
echo ""
echo -e "${BLUE}📱 Access Information:${NC}"
echo -e "   Frontend: ${GREEN}http://localhost${NC}"
echo -e "   Backend API: ${GREEN}http://localhost:8000${NC}"
echo -e "   API Documentation: ${GREEN}http://localhost:8000/docs${NC}"
echo -e "   Neo4j Browser: ${GREEN}http://localhost:7474${NC}"
echo ""
echo -e "${BLUE}🔧 Useful Commands:${NC}"
echo -e "   View logs: ${YELLOW}docker-compose -f $COMPOSE_FILE logs -f${NC}"
echo -e "   Stop services: ${YELLOW}docker-compose -f $COMPOSE_FILE down${NC}"
echo -e "   Restart services: ${YELLOW}docker-compose -f $COMPOSE_FILE restart${NC}"
echo -e "   Update services: ${YELLOW}docker-compose -f $COMPOSE_FILE pull && docker-compose -f $COMPOSE_FILE up -d${NC}"
echo ""

# Check if services are accessible
echo -e "${BLUE}🔍 Testing service accessibility...${NC}"

# Test backend health
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Backend API is accessible${NC}"
else
    echo -e "${RED}❌ Backend API is not accessible${NC}"
fi

# Test frontend
if curl -f http://localhost > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Frontend is accessible${NC}"
else
    echo -e "${RED}❌ Frontend is not accessible${NC}"
fi

echo ""
echo -e "${GREEN}🎯 Deployment script completed!${NC}"
echo -e "${YELLOW}Remember to:${NC}"
echo -e "   1. Configure your domain and SSL certificates"
echo -e "   2. Set up monitoring and alerting"
echo -e "   3. Configure backups"
echo -e "   4. Set up CI/CD pipeline"
echo -e "   5. Monitor application performance"
