#!/bin/bash

# ArchInsight Development Environment Setup for macOS M4
# This script sets up the complete development environment

set -e

echo "🚀 Setting up ArchInsight development environment for macOS M4..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    print_error "This script is designed for macOS. Detected OS: $OSTYPE"
    exit 1
fi

# Check if running on Apple Silicon
if [[ $(uname -m) != "arm64" ]]; then
    print_warning "This script is optimized for Apple Silicon (M1/M2/M3/M4). Detected: $(uname -m)"
fi

# Check prerequisites
print_status "Checking prerequisites..."

# Check for Homebrew
if ! command -v brew &> /dev/null; then
    print_status "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    print_status "Homebrew already installed"
fi

# Update Homebrew
print_status "Updating Homebrew..."
brew update

# Install required tools
print_status "Installing required tools..."
brew install --quiet git node python@3.11 docker docker-compose

# Install GitHub CLI if not present
if ! command -v gh &> /dev/null; then
    print_status "Installing GitHub CLI..."
    brew install --quiet gh
fi

# Check Docker Desktop
if ! docker info &> /dev/null; then
    print_warning "Docker Desktop is not running. Please start Docker Desktop and run this script again."
    print_status "You can download Docker Desktop from: https://www.docker.com/products/docker-desktop/"
    exit 1
fi

# Install Neo4j Desktop
print_status "Checking Neo4j Desktop..."
if ! ls /Applications/Neo4j\ Desktop.app &> /dev/null; then
    print_status "Installing Neo4j Desktop..."
    brew install --cask neo4j
else
    print_status "Neo4j Desktop already installed"
fi

# Setup Python virtual environment
print_status "Setting up Python virtual environment..."
cd backend
python3.11 -m venv venv
source venv/bin/activate

# Upgrade pip and install ARM64 compatible wheels
print_status "Installing Python dependencies (ARM64 optimized)..."
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install ML dependencies separately to handle ARM64 compatibility
print_status "Installing ML dependencies..."
pip install -r requirements-ml.txt

deactivate
cd ..

# Setup Node.js environment
print_status "Setting up Node.js environment..."
cd frontend

# Install dependencies
print_status "Installing Node.js dependencies..."
npm install

cd ..

# Create environment file
print_status "Creating environment configuration..."
if [ ! -f .env ]; then
    cp .env.example .env
    print_status "Created .env file from .env.example"
    print_warning "Please update .env file with your API keys and configuration"
else
    print_status ".env file already exists"
fi

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p data/uploads data/cache data/models logs

# Set up Git hooks (if in a git repository)
if [ -d .git ]; then
    print_status "Setting up Git hooks..."
    # Install pre-commit hooks
    cd backend
    source venv/bin/activate
    pre-commit install
    deactivate
    cd ..
fi

# Build Docker images
print_status "Building Docker images..."
docker-compose build

# Start services
print_status "Starting services..."
docker-compose up -d postgres neo4j redis

# Wait for services to be ready
print_status "Waiting for services to start..."
sleep 30

# Run database migrations
print_status "Running database setup..."
cd backend
source venv/bin/activate
# Add migration commands here when implemented
deactivate
cd ..

# Test the setup
print_status "Testing the setup..."
if curl -f http://localhost:8000/health &> /dev/null; then
    print_status "Backend health check passed"
else
    print_warning "Backend not responding. You may need to start it manually."
fi

print_status "✅ Setup completed successfully!"
echo ""
echo "🎉 ArchInsight development environment is ready!"
echo ""
echo "Next steps:"
echo "1. Update .env file with your API keys"
echo "2. Start the development servers:"
echo "   - Backend: cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
echo "   - Frontend: cd frontend && npm run dev"
echo "3. Open http://localhost:3000 in your browser"
echo ""
echo "Useful commands:"
echo "- Start all services: docker-compose up -d"
echo "- Stop all services: docker-compose down"
echo "- View logs: docker-compose logs -f"
echo "- Access Neo4j browser: http://localhost:7474"
echo ""
print_status "Happy coding! 🚀"