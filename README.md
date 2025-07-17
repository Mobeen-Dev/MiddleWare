# 🚀 MiddleWare - E-commerce Integration Service

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-brightgreen.svg)](https://www.docker.com/)
[![RabbitMQ](https://img.shields.io/badge/RabbitMQ-Integrated-orange.svg)](https://www.rabbitmq.com/)
[![Shopify](https://img.shields.io/badge/Shopify-API-green.svg)](https://shopify.dev/api)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A robust middleware service that bridges e-commerce platforms with internal systems, featuring real-time data synchronization, message queuing, and comprehensive product management capabilities.

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Testing](#testing)
- [Docker Support](#docker-support)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## ✨ Features

- **Shopify Integration**: Seamless product and order synchronization with Shopify stores
- **Message Queue Processing**: RabbitMQ integration for reliable async operations
- **Data Feed Management**: Automated product feed processing and updates
- **Real-time Synchronization**: Bi-directional sync between Shopify and internal database
- **Schema Validation**: Comprehensive validation for orders and products
- **Stress Testing**: Built-in performance testing capabilities
- **Logging & Monitoring**: Detailed logging system for debugging and monitoring
- **Docker Ready**: Fully containerized application with Docker Compose support
- **Web Interface**: Simple web UI for monitoring and management

## 🏗️ Architecture

```
┌─────────────────┐
│                 │
│  Shopify Store  │◄──────────────┐               
│      Child      │               |
│                 │               |
└─────────────────┘               |
┌─────────────────┐     ┌─────────|───────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Shopify Store  │◄────┤   MiddleWare    ├────►│   Database      │
│     Parent      │     │                 │     │                 │
│                 │     └────────┬────────┘     └─────────────────┘
└─────────────────┘              │
                                 │
                        ┌────────▼────────┐
                        │                 │
                        │    RabbitMQ     │
                        │                 │
                        └─────────────────┘
```

## 🛠️ Tech Stack

- **Language**: Python 3.8+
- **Web Framework**: FastAPI
- **Message Queue**: RabbitMQ
- **Database**: SQLAlchemy ORM compatible
- **API Integration**: Shopify API
- **Containerization**: Docker & Docker Compose
- **Testing**: Pytest
- **Logging**: Python logging module

## 📚 Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8 or higher
- Docker and Docker Compose (optional, for containerized deployment)
- RabbitMQ server (or use Docker)
- Git

## 🚀 Installation

### Local Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Mobeen-Dev/MiddleWare.git
   cd middleware
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp credentials/.env.example credentials/.env
   # Edit credentials/.env with your configuration
   ```

### Docker Installation

```bash
docker-compose up -d
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the `credentials/` directory with the following variables:

```env
# Shopify Configuration
SHOPIFY_API_KEY=your_api_key_here
SHOPIFY_API_SECRET=your_api_secret_here
SHOPIFY_STORE_URL=your-store.myshopify.com
SHOPIFY_ACCESS_TOKEN=your_access_token_here

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/middleware_db

# RabbitMQ Configuration
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
RABBITMQ_USER=guest
RABBITMQ_PASSWORD=guest
RABBITMQ_VHOST=/

# Application Configuration
APP_ENV=development
LOG_LEVEL=INFO
SERVER_PORT=5000
```

### Configuration File

Additional settings can be configured in `config.py`:

```python
# Example configuration structure
class Config:
    DEBUG = False
    TESTING = False
    SYNC_INTERVAL = 300  # seconds
    MAX_RETRY_ATTEMPTS = 3
    BATCH_SIZE = 100
```

## 💻 Usage

### Starting the Application

#### Local Development
```bash
# Start the workers 
taskiq worker broker:broker -fsd -w 1

# Start the Scheduler
taskiq scheduler broker:scheduler

# Start the main application
python app.py

# Or use the custom server
python custom_server.py
```

#### Using Docker
```bash
docker-compose up
```

### Running Individual Services

```bash
# Start the data feed service
python dataFeed.py

# Start the product feed service
python productFeed.py

# Start the sync service
python sync_service.py
```

### Command Line Interface

```bash
# Process a product feed
python productFeed.py --file bucket/product_feed.csv

# Sync products from Shopify
python shopify.py sync-products

# Run stress tests
python StressTester.py --concurrent 10 --duration 60
```

## 📡 API Reference

### Product Endpoints

#### Get All Products
```http
GET /api/products
```

#### Get Product by ID
```http
GET /api/products/{product_id}
```

#### Create Product
```http
POST /api/products
Content-Type: application/json

{
  "title": "Product Name",
  "description": "Product Description",
  "price": 29.99,
  "sku": "PROD-001"
}
```

#### Update Product
```http
PUT /api/products/{product_id}
```

### Order Endpoints

#### Get Orders
```http
GET /api/orders
```

#### Process Order
```http
POST /api/orders/process
```

### Webhook Endpoints

#### Shopify Webhook Handler
```http
POST /webhooks/shopify/{event_type}
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test1.py

# Run with coverage
pytest --cov=. --cov-report=html

# Run schema validation tests
pytest tests/schem_vaidation/

# Run RabbitMQ tests
pytest tests/rabbitmq_tests/
```

### Test Categories

- **Unit Tests**: Individual component testing
- **Integration Tests**: Service interaction testing
- **Schema Validation**: Order and product schema tests
- **RabbitMQ Tests**: Message queue functionality
- **Stress Tests**: Performance and load testing

## 🐳 Docker Support

### Building the Image

```bash
docker build -t middleware:latest .
```

### Docker Compose Services

```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - APP_ENV=production
    depends_on:
      - rabbitmq
      - db
  
  rabbitmq:
    image: rabbitmq:3-management
    ports:
      - "5672:5672"
      - "15672:15672"
  
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: middleware_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
```

### Running with Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 📁 Project Structure

```
MiddleWare/
├── app.py                    # Main application entry point
├── broker.py                 # Message broker functionality
├── database.py               # Database operations
├── models.py                 # Data models
├── config.py                 # Configuration settings
├── logger.py                 # Logging configuration
├── shopify.py                # Shopify API integration
├── dataFeed.py               # Data feed processing
├── productFeed.py            # Product feed handler
├── sync_service.py           # Synchronization service
├── tasks.py                  # Async task definitions
├── custom_server.py          # Custom server implementation
├── requirements.txt          # Python dependencies
├── docker-compose.yaml       # Docker Compose config
├── Dockerfile                # Docker build instructions
├── entrypoint.sh             # Docker entry point
├── credentials/              # Environment variables
│   └── .env                  # Environment configuration
├── bucket/                   # Data storage
│   ├── app.log              # Application logs
│   ├── product_feed.csv     # Product data
│   └── product_titles.pkl   # Cached product titles
├── templates/                # Web templates
│   └── index.html           # Web interface
├── tests/                    # Test suite
│   ├── rabbitmq_tests/      # RabbitMQ tests
│   └── schem_vaidation/     # Schema validation
└── RnD/                      # Research & Development
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Write tests for new features
- Update documentation
- Use meaningful commit messages
- Ensure all tests pass before submitting PR

## 🔧 Troubleshooting

### Common Issues

#### RabbitMQ Connection Error
```bash
# Check if RabbitMQ is running
docker ps | grep rabbitmq

# Restart RabbitMQ
docker-compose restart rabbitmq
```

#### Database Connection Issues
```bash
# Check database connectivity
python -c "from database import test_connection; test_connection()"
```

#### Shopify API Rate Limiting
- Implement exponential backoff
- Check `shopify.py` for rate limit handling

### Logs

Check logs in the following locations:
- Application logs: `bucket/app.log`
- Docker logs: `docker-compose logs -f app`
- RnD logs: `RnD/ServerLogs.json`

## 📝 TODO

See [TODO.txt](TODO.txt) for upcoming features and improvements.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Your Name** - *Initial work* - [YourGitHub](https://github.com/yourusername)

## 🙏 Acknowledgments

- Shopify API documentation
- RabbitMQ community
- All contributors who have helped shape this project

---

**Note**: This is a middleware service designed for internal use. Ensure proper security measures are in place before deploying to production.
