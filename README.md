# IT Staffing Sales Opportunity Assessment Backend

This is the backend service for the IT Staffing Sales Opportunity Assessment application. It provides APIs for managing sales opportunities, candidates, and sales representatives, along with AI-powered analysis and matching capabilities.

## Features

### Opportunity Management
- Create and track sales opportunities with detailed requirements
- Analyze opportunity potential and qualification
- Match opportunities with suitable candidates
- Track opportunity stages and probability
- Manage client company information and project details

### Candidate Management
- Store comprehensive candidate profiles
- Track skills, experience, and certifications
- Manage candidate availability and preferences
- Match candidates with opportunities
- Track candidate rates and location preferences

### Sales Representative Management
- Track sales performance metrics
- Manage territories and quotas
- Monitor win rates and YTD sales
- Track opportunity pipeline
- Analyze performance trends

### AI-Powered Analysis
- Opportunity scoring and qualification
- Candidate matching with skill analysis
- Rate matching and availability checking
- Sales performance predictions
- Automated candidate recommendations

## Technical Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT-based authentication
- **AI/ML**: OpenAI integration for analysis
- **Storage**: AWS S3 for file storage
- **Containerization**: Docker support

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

### Key API Endpoints

#### Opportunities
- `GET /api/opportunities` - List opportunities
- `POST /api/opportunities` - Create opportunity
- `GET /api/opportunities/{id}` - Get opportunity details
- `PUT /api/opportunities/{id}` - Update opportunity
- `GET /api/opportunities/{id}/analyze` - Analyze opportunity
- `GET /api/opportunities/{id}/candidates` - Get matching candidates

#### Candidates
- `GET /api/candidates` - List candidates
- `POST /api/candidates` - Create candidate
- `GET /api/candidates/{id}` - Get candidate details
- `PUT /api/candidates/{id}` - Update candidate
- `GET /api/candidates/{id}/opportunities` - Get matching opportunities

#### Sales Representatives
- `GET /api/sales-reps` - List sales reps
- `POST /api/sales-reps` - Create sales rep
- `GET /api/sales-reps/{id}` - Get sales rep details
- `PUT /api/sales-reps/{id}` - Update sales rep
- `GET /api/sales-reps/{id}/performance` - Get performance metrics

## Project Structure

```
app/backend/
├── models/                 # SQLAlchemy models
│   ├── opportunity.py     # Opportunity model
│   ├── candidate.py       # Candidate model
│   ├── candidate_match.py # Candidate matching model
│   └── sales_representative.py # Sales rep model
├── routes/                # API route handlers
│   ├── opportunity_api.py # Opportunity endpoints
│   ├── candidate_api.py   # Candidate endpoints
│   └── sales_rep_api.py   # Sales rep endpoints
├── services/             # Business logic
│   └── opportunity_analysis.py # AI analysis service
├── migrations/           # Database migrations
├── tests/               # Test suite
├── app.py              # Main application file
├── db_utils.py         # Database utilities
├── data_classes.py     # Pydantic models
└── requirements.txt    # Python dependencies
```

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

### Docker Deployment

Build and run using Docker:

```bash
docker build -t it-staffing-backend .
docker run -p 8000:8000 it-staffing-backend
```

### Environment Variables

Make sure to set all required environment variables in your deployment environment:

- Database connection string
- AWS credentials
- API keys for external services
- Security settings

## Security Considerations

- All API endpoints are protected with JWT authentication
- Sensitive data is encrypted at rest
- API keys and credentials are stored in environment variables
- Regular security audits are performed
- Input validation using Pydantic models
- SQL injection prevention with SQLAlchemy
- CORS protection enabled

## Monitoring and Logging

- Application logs are captured and can be forwarded to your preferred logging service
- Performance metrics are available through the API
- Error tracking and monitoring can be integrated

## Support

For support, please contact the development team or create an issue in the repository.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.