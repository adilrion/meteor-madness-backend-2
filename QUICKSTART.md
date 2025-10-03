# Quick Start Guide

Get the Meteor Madness backend up and running in 5 minutes!

## Prerequisites

Ensure you have installed:

-   Python 3.10 or higher
-   PostgreSQL 14 or higher
-   Redis 6 or higher

## Installation Steps

### 1. Clone & Setup

```bash
# Clone the repository
git clone <repository-url>
cd meteor-madness-backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Setup

```bash
# Create PostgreSQL database
createdb meteor_madness

# Or using psql:
psql -U postgres
CREATE DATABASE meteor_madness;
\q
```

### 3. Configuration

```bash
# Copy environment file
cp env.example .env

# Edit .env with your settings (minimum required):
# - SECRET_KEY (generate one)
# - DATABASE settings
# - NASA_API_KEY (get from https://api.nasa.gov/)
```

Generate SECRET_KEY:

```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
```

### 6. Start Development Server

```bash
# Terminal 1: Django server
python manage.py runserver

# Terminal 2: Redis (if not running as service)
redis-server

# Terminal 3: Celery worker
celery -A meteor_madness worker -l info

# Terminal 4: Celery beat
celery -A meteor_madness beat -l info
```

## Access the Application

-   **API**: http://localhost:8000/api/
-   **Admin Panel**: http://localhost:8000/admin/
-   **API Docs**: http://localhost:8000/api/docs/
-   **ReDoc**: http://localhost:8000/api/redoc/

## Initial Data Load

### Sync NEO Data

```bash
python manage.py shell
```

```python
from neos.services import NEODataService
service = NEODataService()
result = service.sync_neo_data()
print(result)
exit()
```

Or use the API endpoint:

```bash
curl -X POST http://localhost:8000/api/neos/objects/sync_nasa_data/
```

## Quick API Test

### Get JWT Token

```bash
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"your_username","password":"your_password"}'
```

### List NEOs

```bash
curl http://localhost:8000/api/neos/objects/
```

### Get NEO Statistics

```bash
curl http://localhost:8000/api/neos/statistics/latest/
```

## Common Issues & Solutions

### Issue: "No module named 'psycopg2'"

**Solution**: `pip install psycopg2-binary`

### Issue: "Redis connection refused"

**Solution**: Start Redis server: `redis-server`

### Issue: "Database does not exist"

**Solution**: Create database: `createdb meteor_madness`

### Issue: "NASA API rate limit exceeded"

**Solution**: Get your own API key at https://api.nasa.gov/

## Next Steps

1. **Load Sample Data**: Run initial NEO data sync
2. **Explore API**: Visit http://localhost:8000/api/docs/
3. **Setup Threat Scenarios**: Create scenarios in admin panel
4. **Configure Celery**: Set up periodic tasks
5. **Test Features**: Try different API endpoints

## Development Workflow

```bash
# Make changes to code

# Run migrations if models changed
python manage.py makemigrations
python manage.py migrate

# Restart server
# Ctrl+C and run: python manage.py runserver

# Run tests
pytest

# Check code
python manage.py check
```

## Production Deployment

For production deployment, see [DEPLOYMENT.md](DEPLOYMENT.md)

## Need Help?

-   Check [README.md](README.md) for detailed documentation
-   Review [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for API reference
-   Open an issue on GitHub
-   Contact the development team

Happy coding! 🚀
