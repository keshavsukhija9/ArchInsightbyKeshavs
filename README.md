# ArchInsight - AI-Powered Code Dependency Analyzer

ArchInsight is a production-ready SaaS application that analyzes code dependencies, predicts risks, and provides AI-powered refactoring recommendations using advanced Graph Neural Networks and OpenAI integration.

## 🚀 Features

### Core Capabilities
- **Code Analysis Engine**: Parse code files, extract dependencies, build comprehensive graphs
- **Risk Prediction**: ML model to score modules based on complexity, changes, and dependencies
- **AI Recommendations**: OpenAI integration for intelligent refactoring suggestions
- **Interactive Dependency Graph**: D3.js/Cytoscape.js visualization of code relationships
- **Real-time Processing**: WebSocket support for live analysis updates
- **GitHub Integration**: OAuth, webhook handling, repository cloning

### Technology Stack
- **Frontend**: React 18+ with TypeScript, Vite, Material-UI (MUI)
- **Backend**: FastAPI with Python 3.11+, async/await patterns
- **Database**: Neo4j (graph database) + PostgreSQL (relational data)
- **ML/AI**: PyTorch Geometric for Graph Neural Networks, OpenAI API integration
- **DevOps**: Docker containers, Docker Compose for development
- **Platform**: macOS M4 compatible (ARM64 architecture)

## 🛠 Quick Start (macOS M4)

### Prerequisites
- macOS with Apple Silicon (M1/M2/M3/M4)
- Docker Desktop for Mac
- Git

### Automated Setup
```bash
# Clone the repository
git clone <repository-url>
cd ArchInsight

# Run the automated setup script
./scripts/setup.sh
```

The setup script will:
- Install Homebrew (if not present)
- Install required tools (Node.js, Python 3.11, Docker, etc.)
- Install Neo4j Desktop
- Set up Python virtual environment with ARM64 optimized packages
- Install all dependencies
- Build Docker images
- Start database services
- Create necessary directories and configuration files

### Manual Setup

#### 1. Install Dependencies
```bash
# Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install required tools
brew install git node python@3.11 docker docker-compose
brew install --cask neo4j docker
```

#### 2. Setup Backend
```bash
cd backend
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install -r requirements-ml.txt
```

#### 3. Setup Frontend
```bash
cd frontend
npm install
```

#### 4. Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your API keys and configuration
# Required: OPENAI_API_KEY, GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET
```

#### 5. Start Services
```bash
# Start databases
docker-compose up -d postgres neo4j redis

# Start backend (in new terminal)
cd backend
source venv/bin/activate
uvicorn app.main:app --reload

# Start frontend (in new terminal)
cd frontend
npm run dev
```

## 🐳 Docker Development

### Start All Services
```bash
docker-compose up -d
```

### View Logs
```bash
docker-compose logs -f
```

### Stop All Services
```bash
docker-compose down
```

### Rebuild Images
```bash
docker-compose build --no-cache
```

## 📊 Database Access

### PostgreSQL
- **Host**: localhost:5432
- **Database**: archinsight
- **Username**: archinsight
- **Password**: archinsight_dev_password

### Neo4j
- **Browser**: http://localhost:7474
- **Bolt**: bolt://localhost:7687
- **Username**: neo4j
- **Password**: archinsight_dev_password

### Redis
- **Host**: localhost:6379

## 🔧 Development

### Backend Development
```bash
cd backend
source venv/bin/activate

# Run tests
pytest

# Code formatting
black .
isort .

# Type checking
mypy .

# Linting
flake8 .
```

### Frontend Development
```bash
cd frontend

# Run tests
npm test

# Build for production
npm run build

# Lint code
npm run lint
```

### API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🧪 Testing

### Backend Tests
```bash
cd backend
source venv/bin/activate
pytest --cov=app tests/
```

### Frontend Tests
```bash
cd frontend
npm test
npm run test:coverage
```

## 🚀 Production Deployment

### Environment Variables
Set the following environment variables for production:

```bash
# Security
JWT_SECRET_KEY=your_production_secret_key
ENVIRONMENT=production

# External APIs
OPENAI_API_KEY=your_openai_api_key
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret

# Database URLs (update for production)
DATABASE_URL=postgresql://user:password@host:port/database
NEO4J_URI=bolt://host:port
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_neo4j_password
REDIS_URL=redis://host:port

# Monitoring
SENTRY_DSN=your_sentry_dsn
```

### Docker Production Build
```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Deploy
docker-compose -f docker-compose.prod.yml up -d
```

## 📁 Project Structure

```
ArchInsight/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Core functionality
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic
│   │   ├── ml/             # ML models and training
│   │   └── utils/          # Utilities
│   ├── tests/              # Backend tests
│   └── requirements*.txt   # Python dependencies
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   ├── store/          # State management
│   │   └── utils/          # Utilities
│   └── public/             # Static assets
├── scripts/                # Setup and utility scripts
├── docs/                   # Documentation
├── tests/                  # Integration tests
├── data/                   # Data storage
│   ├── uploads/            # Uploaded files
│   ├── cache/              # Cache storage
│   └── models/             # ML models
└── docker-compose.yml      # Development services
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: [docs/](docs/)
- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions

## 🔮 Roadmap

- [ ] Advanced ML risk prediction models
- [ ] Real-time collaboration features
- [ ] CI/CD pipeline integration
- [ ] Multi-language support expansion
- [ ] Enterprise SSO integration
- [ ] Advanced visualization options
- [ ] API rate limiting and quotas
- [ ] Webhook integrations

---

**Built with ❤️ for developers who care about code quality and architecture.**