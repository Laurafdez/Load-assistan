# Load Assistant API

A comprehensive FastAPI-based load management system with carrier verification, call analytics, and real-time dashboard. Built for freight brokers to manage loads, verify carriers through FMCSA integration, and track negotiation analytics.

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Poetry
- Docker & Docker Compose
- ngrok (optional, for testing webhooks)

### Installation

```bash
# Clone the repository
git clone https://github.com/Laurafdez/Load-assistant
cd load_assistant

# Install dependencies
make install
```

### Environment Setup

Create a `.env` file based on `env.template`:

```env
# API Authentication
AUTH_HEADER_KEY=X-API-Key
AUTH_API_KEY=my-secret-api-key-123

# External APIs
FMCSA_API_KEY=your-fmcsa-api-key

# CORS
BACKEND_CORS_ORIGINS=http://localhost:3000,http://localhost:8080

# Project Config
PROJECT_NAME=Load Assistant API
API_V1_STR=/api/v1
ENVIRONMENT=development
TESTING=false

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/loads_db

# Server
HOST=0.0.0.0
PORT=8000
```

## 🐳 Docker Setup (Recommended)

The application runs as a multi-container setup with PostgreSQL database and Streamlit dashboard.

### Services Overview

- **PostgreSQL Database** (`db`): Data persistence with automatic initialization
- **FastAPI Application** (`api`): Main REST API service
- **Streamlit Dashboard** (`dashboard`): Real-time analytics and metrics

### Quick Start with Docker

```bash
# Start all services
make dc-up

# Access the services:
# - API: http://localhost:8000
# - Dashboard: http://localhost:8501
# - Database: localhost:5432
```

### Docker Commands

```bash
# Full Stack Management
make dc-up              # Start all services
make dc-down            # Stop all services
make dc-logs            # View logs from all services
make dc-restart         # Restart with rebuild
make dc-shell           # Access API container shell

# Individual Container Management
make docker-build       # Build API image only
make docker-run         # Run API container only
```

## 🛠️ Development Commands

### Local Development (without Docker)

```bash
# Setup & Dependencies
make install               # Install with poetry
make update               # Update dependencies
make dev                  # Full dev setup (install + lint + test)

# Code Quality
make lint                 # Check code quality with ruff
make lint-fix            # Auto-fix linting issues
make test                # Run pytest test suite
make coverage           # Test with coverage report

# Running Locally
make run                # Start server (localhost:8000)
make serve              # Alias for run

# For Demo/Testing with External Access
make run-ngrok          # Start server + ngrok tunnel
```


## 🌐 API Endpoints

### Core Load Management
- `GET /api/v1/health` - API health status
- `GET /api/v1/loads` - List available loads with filtering
- `POST /api/v1/loads/search` - Advanced load search

### Call Analytics
- `GET /api/v1/call-summary` - Retrieve all call summaries
- `POST /api/v1/call-summary` - Log new call interactions

### Carrier Management
- `GET /api/v1/carriers/authorization/{mc_number}` - Verify carrier authorization via FMCSA

### Negotiation System
- `POST /api/v1/counteroffer` - Process carrier counteroffers with business rules

### Metrics & Analytics
- `GET /api/v1/metrics` - Dashboard metrics and KPIs

### Authentication
All protected endpoints require API key authentication:
```bash
curl -H "X-API-Key: my-secret-api-key-123" http://localhost:8000/api/v1/loads
```

## 📊 Key Features

### Load Management
- Advanced search and filtering capabilities
- Real-time load availability tracking
- Geographic and route-based matching

### Carrier Verification
- FMCSA MC number validation
- Real-time authorization status checking
- Carrier safety rating integration

### Call Analytics
- Comprehensive call outcome tracking
- Sentiment analysis and satisfaction metrics
- Negotiation round counting and success rates

### Intelligent Negotiations
- Automated counteroffer processing
- Business rule-based decision making
- Multi-round negotiation support (up to 3 rounds)

### Real-time Dashboard
- Live metrics and KPIs visualization
- Call success rate monitoring
- Load distribution analytics
- Carrier performance tracking


## 🏗️ Project Structure

```
load_assistant/
├── app/
│   ├── api/                    # API layer
│   │   ├── dependencies.py     # Dependency injection
│   │   ├── main.py            # API router setup
│   │   └── v1/routes/         # API endpoints
│   │       ├── healthcheck.py # Health monitoring
│   │       ├── load.py        # Load management
│   │       ├── call_summary.py# Call analytics
│   │       ├── metrics.py     # Dashboard metrics
│   │       ├── carrier.py     # Carrier verification
│   │       └── negotations.py # Negotiation logic
│   ├── business/              # Business logic layer
│   │   ├── healthcheck.py     # Health check logic
│   │   ├── load.py           # Load business rules
│   │   ├── metrics.py        # Metrics calculations
│   │   └── negotiation.py    # Negotiation algorithms
│   ├── crud/                  # Database operations
│   │   ├── call_summary.py   # Call CRUD operations
│   │   └── load.py           # Load CRUD operations
│   ├── models/                # SQLAlchemy models
│   │   ├── call_summary.py   # Call summary model
│   │   └── load.py           # Load model
│   ├── schemas/               # Pydantic schemas
│   │   ├── call_summary.py   # Call summary schemas
│   │   ├── carrier.py        # Carrier schemas
│   │   ├── load.py           # Load schemas
│   │   ├── metrics.py        # Metrics schemas
│   │   └── negotiations.py   # Negotiation schemas
│   ├── core/                  # Core configuration
│   │   └── config.py         # Application settings
│   ├── database_engine/       # Database setup
│   │   ├── base_class.py     # Base model class
│   │   └── session.py        # Database session
│   ├── middlewares/           # Custom middlewares
│   │   └── api_log_request.py# Request logging
│   └── utils/                 # Utility functions
│       ├── normalization.py  # Data normalization
│       └── parsing.py        # Data parsing helpers
├── streamlit/                 # Dashboard application
│   ├── dashboard.py          # Streamlit dashboard
│   ├── Dockerfile           # Dashboard container
│   └── requirements.txt     # Dashboard dependencies
├── tests/                    # Test suite
│   └── unit/
│       └── test_loads.py    # Load endpoint tests
├── docker-compose.yml       # Multi-container setup
├── Dockerfile              # API container
├── init.sql               # Database initialization
├── Makefile              # Development commands
└── pyproject.toml        # Poetry configuration
```
