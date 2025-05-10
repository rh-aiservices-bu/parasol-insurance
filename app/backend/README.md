# IT Staffing Sales Opportunity Assessment Backend

This is the backend service for the IT Staffing Sales Opportunity Assessment application. It provides APIs for managing sales opportunities, candidates, and sales representatives, along with AI-powered analysis and matching capabilities.

## Setup Instructions

### Prerequisites

- Python 3.8+
- PostgreSQL 12+
- AWS Account (for S3 storage)
- OpenAI API Key
- CRM and ATS API credentials

### Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the `app/backend` directory with the following variables:
```
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/it_staffing_db

# AWS Configuration
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1
S3_BUCKET_NAME=your-bucket-name

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# External Services
OPENAI_API_KEY=your-openai-api-key
CRM_API_KEY=your-crm-api-key
ATS_API_KEY=your-ats-api-key
```

4. Run database migrations:
```bash
python run_migration.py
```

5. Start the server:
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, you can access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
app/backend/
├── models/                 # SQLAlchemy models
├── routes/                # API route handlers
├── services/             # Business logic and services
├── migrations/           # Database migrations
├── config/              # Configuration files
├── app.py              # Main application file
├── db_utils.py         # Database utilities
├── data_classes.py     # Pydantic models
└── requirements.txt    # Python dependencies
```

## Features

- Opportunity Management
  - Create and track sales opportunities
  - Analyze opportunity potential
  - Match with suitable candidates

- Candidate Management
  - Store candidate profiles
  - Track skills and experience
  - Match with opportunities

- Sales Representative Management
  - Track sales performance
  - Manage territories and quotas
  - Monitor win rates

- AI-Powered Analysis
  - Opportunity scoring
  - Candidate matching
  - Sales performance predictions

## Development

### Running Tests

```bash
pytest
```

### Code Style

The project follows PEP 8 style guidelines. Use `black` for code formatting:

```bash
black .
```

### Database Migrations

To create a new migration:

1. Make changes to the models
2. Create a new migration file in `migrations/`
3. Run the migration script

## Deployment

The application can be deployed using Docker:

```bash
docker build -t it-staffing-backend .
docker run -p 8000:8000 it-staffing-backend
```

## Security Considerations

- All API endpoints are protected with JWT authentication
- Sensitive data is encrypted at rest
- API keys and credentials are stored in environment variables
- Regular security audits are performed

## Support

For support, please contact the development team or create an issue in the repository. 