# Cab Booking API

A full-featured ride-sharing system built with FastAPI, SQLAlchemy, and PostgreSQL.

## Features

- User authentication and authorization
- Driver management and availability
- Cab registration and management
- Booking system with fare estimation
- Payment processing
- Notification system
- Admin dashboard
- Rate limiting and logging

## Tech Stack

- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- JWT Authentication
- Docker
- Pytest

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd cab-booking
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run with Docker:
```bash
docker-compose up --build
```

Or run locally:
```bash
uvicorn app.main:app --reload
```

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

Run tests with pytest:
```bash
pytest
```

## Database Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "description"
```

Apply migrations:
```bash
alembic upgrade head
```

## Project Structure

```
cab-booking/
├── alembic/
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   └── services/
├── tests/
├── .env
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License. 