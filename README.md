# Load Assistant API

FastAPI-based load management system with carrier verification and call analytics.

## 🚀 Quick Setup

### Prerequisites
- Python 3.12+ (using pyenv)
- Poetry
- Docker & Docker Compose

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Poetry
- Docker & Docker Compose
- ngrok (optional, for testing)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd load-agent-api

# Install dependencies
make install

# Install pre-commit hooks
make pre-commit-install
```

### Environment Setup

Create a `.env` file:

```env
# API Authentication
AUTH_HEADER_KEY=
AUTH_API_KEY=

# External APIs
FMCSA_API_KEY=

# CORS
BACKEND_CORS_ORIGINS=

# Project Config
PROJECT_NAME=
API_V1_STR=
ENVIRONMENT=
TESTING=

# Database
DATABASE_URL=

# Server
HOST=
PORT=
```

## 🛠️ Development Commands

```bash
# Setup & Dependencies
make install               # Install with poetry
make update               # Update dependencies
make dev                  # Full dev setup (install + lint + test)

# Code Quality
make lint                 # Check code quality
make lint-fix            # Auto-fix issues
make test                # Run tests
make coverage           # Test with coverage report

# Running Locally
make run                # Start server (localhost:8000)
make serve              # Alias for run

# For Demo/Testing
make run-ngrok          # Start server + ngrok tunnel
```

## 🐳 Docker Commands

```bash
# Single Container
make docker-build       # Build image
make docker-run         # Run container

# Docker Compose (Full Stack)
make dc-up              # Start all services
make dc-down            # Stop services
make dc-logs            # View logs
make dc-restart         # Restart with rebuild
make dc-shell           # Access container shell
```

## 📡 Demo Setup with ngrok

For external access (perfect for webhooks and demos):

```bash
# Terminal 1: Start the API with ngrok
make run-ngrok

# This will:
# 1. Start FastAPI server on localhost:8000
# 2. Create ngrok tunnel
# 3. Show public URL (e.g., https://abc123.ngrok.io)
```

Your API will be accessible at the ngrok URL for external services.

## 🏗️ Project Structure

```
load_assistant/
├── app/
│   ├── api/v1/routes/          # API endpoints
│   │   ├── health.py           # Health checks
│   │   ├── load.py            # Load management
│   │   ├── call_summary.py    # Call analytics
│   │   ├── metrics.py         # Dashboard metrics
│   │   └── mock_fmcsa.py      # FMCSA integration
│   ├── business/              # Business logic
│   ├── crud/                  # Database operations
│   ├── models/                # SQLAlchemy models
│   ├── schemas/               # Pydantic schemas
│   └── core/                  # Configuration
├── tests/                     # Test suite
├── docker-compose.yml         # Multi-container setup
├── Dockerfile                 # Container definition
└── init.sql                  # Database initialization
```

## 🌐 API Endpoints

### Core Routes
- `GET /health` - Health check
- `GET /api/v1/loads` - List loads
- `POST /api/v1/loads/search` - Search loads
- `POST /api/v1/call-summary` - Create call summary
- `GET /api/v1/metrics` - Dashboard metrics
- `POST /api/v1/verify-mc` - Verify MC number

### Authentication
All protected endpoints require:
```bash
curl -H "X-API-Key: my-secret-api-key-123" http://localhost:8000/api/v1/loads
```

## 📊 Features

- **Load Management**: Search and manage freight loads
- **Carrier Verification**: FMCSA MC number validation
- **Call Analytics**: Track call outcomes and metrics
- **Dashboard**: Real-time metrics and reporting
- **Health Monitoring**: System health endpoints

## 🧪 Testing

```bash
make test                   # Run all tests
make coverage              # Run with coverage report
poetry run pytest tests/unit/test_loads.py -v  # Run specific test
```

## 🔧 Python Environment

```bash
# Set Python version
pyenv shell 3.12.0

# Install dependencies
make install

# Check current version
make version  # Shows: 1.0.0
```

---

**Quick Start Summary:**
1. `pyenv shell 3.12.0`
2. `make install`
3. Create `.env` file
4. `make run` or `make run-ngrok` for demo
5. API available at `http://localhost:8000`ent

### Deployment Steps

1. **Build**: `make docker-build`
2. **Push**: Push image to your registry
3. **Deploy**: Use your cloud provider's deployment tools
4. **Configure**: Set environment variables
5. **Test**: Verify all endpoints are working

## 📱 HappyRobot Integration

### Webhook Configuration

Configure your HappyRobot webhook to point to:
```
https://your-domain.com/api/v1/calls/webhook
```

### Call Flow

1. Carrier calls the HappyRobot number
2. AI assistant engages and collects MC number
3. System verifies carrier with FMCSA API
4. Load search and presentation
5. Negotiation handling (up to 3 rounds)
6. Call transfer or conclusion
7. Analytics and reporting

## 🧪 Testing

### Running Tests

```bash
# Run all tests
make test

# Run with coverage
make coverage

```

### Test Data

The system includes test data for:
- Sample loads
- Mock carrier information
- Test scenarios for negotiations

## 📄 License

This project is part of the FDE Technical Challenge.


**Project Version**: 1.0.0  
**Last Updated**: 2025  
**Python Version**: 3.8+  
**Framework**: FastAPI