# Meteor Madness Backend

Django REST API backend for the Meteor Madness platform - NASA Space Apps Challenge 2025

## 🌟 Overview

Comprehensive backend system for tracking, analyzing, and understanding near-Earth objects (NEOs) and meteor threats using real-time NASA data and advanced calculations.

## 📋 Features

### Core Modules

-   **NEOs Module**: 34,000+ NEO database with real-time NASA API integration
-   **Asteroids Module**: Threat assessment and multi-scenario analysis
-   **Impacts Module**: Historical impact events and earthquake comparison database
-   **Seismic Module**: Seismic impact calculations and shockwave modeling
-   **Safety Module**: MeteorShield safety features including AI chatbot
-   **Tracking Module**: Live meteor tracking and activity monitoring
-   **Orbital Module**: Orbital mechanics and trajectory calculations
-   **Users Module**: User management and activity tracking
-   **Notifications Module**: Alert system and threat notifications

### Key Capabilities

-   Real-time NEO data synchronization from NASA APIs
-   Advanced threat assessment calculations
-   Seismic impact and shockwave modeling
-   Climate chain reaction modeling
-   Resource allocation calculator
-   AI-powered safety chatbot
-   WebSocket support for live tracking
-   Comprehensive REST API with authentication

## 🚀 Technology Stack

-   **Framework**: Django 5.0.1
-   **API**: Django REST Framework 3.14.0
-   **Database**: PostgreSQL with PostGIS support
-   **Caching**: Redis
-   **Task Queue**: Celery with Redis broker
-   **WebSockets**: Django Channels
-   **Authentication**: JWT (Simple JWT)
-   **Scientific Computing**: NumPy, SciPy, Pandas, Astropy
-   **API Documentation**: drf-spectacular, drf-yasg

## 📦 Installation

### Prerequisites

-   Python 3.10+
-   PostgreSQL 14+
-   Redis 6+

### Setup Steps

1. **Clone the repository**

```bash
git clone <repository-url>
cd meteor-madness-backend
```

2. **Create virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Setup database**

```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create superuser**

```bash
python manage.py createsuperuser
```

7. **Run development server**

```bash
python manage.py runserver
```

## 🔧 Configuration

### Environment Variables

Key environment variables (see `.env.example`):

-   `SECRET_KEY`: Django secret key
-   `DEBUG`: Debug mode (True/False)
-   `NASA_API_KEY`: Your NASA API key (get from https://api.nasa.gov/)
-   `DATABASE_URL`: PostgreSQL connection string
-   `REDIS_HOST`: Redis server host
-   `OPENAI_API_KEY`: OpenAI API key for chatbot

### NASA API Key

Get your free NASA API key at: https://api.nasa.gov/

## 🎯 API Endpoints

### NEOs

-   `GET /api/neos/objects/` - List all NEOs
-   `GET /api/neos/objects/{id}/` - NEO details
-   `GET /api/neos/objects/potentially_hazardous/` - PHAs only
-   `GET /api/neos/close-approaches/upcoming/` - Upcoming close approaches
-   `GET /api/neos/statistics/latest/` - Latest statistics

### Asteroids

-   `GET /api/asteroids/scenarios/` - Threat scenarios
-   `GET /api/asteroids/assessments/` - Threat assessments
-   `POST /api/asteroids/scenarios/{id}/calculate_assessment/` - Calculate threat

### Impacts

-   `GET /api/impacts/events/` - Historical impact events
-   `GET /api/impacts/earthquakes/` - Historical earthquakes
-   `GET /api/impacts/events/major_events/` - Major impacts (>100MT)

### Seismic

-   `GET /api/seismic/analyses/` - Seismic analyses
-   `POST /api/seismic/analyses/calculate/` - Calculate seismic impact

### Safety

-   `GET /api/safety/checklists/` - Emergency checklists
-   `POST /api/safety/resources/calculate/` - Resource calculator
-   `POST /api/safety/chatbot/chat/` - AI chatbot
-   `POST /api/safety/climate-models/calculate/` - Climate modeling

### Tracking

-   `GET /api/tracking/meteor-showers/` - Meteor showers
-   `GET /api/tracking/activity/current/` - Current meteor activity
-   `WS /ws/tracking/` - Real-time tracking WebSocket

### Orbital

-   `GET /api/orbital/elements/` - Orbital elements
-   `GET /api/orbital/trajectories/for_neo/` - Trajectory points
-   `POST /api/orbital/trajectories/calculate/` - Calculate trajectory

### Users

-   `GET /api/users/me/` - Current user
-   `GET /api/users/profiles/my_profile/` - User profile
-   `POST /api/users/activities/` - Log activity

### Notifications

-   `GET /api/notifications/` - User notifications
-   `GET /api/notifications/unread/` - Unread notifications
-   `GET /api/notifications/alerts/active/` - Active alerts
-   `POST /api/notifications/subscriptions/` - Create subscription

### Authentication

-   `POST /api/auth/token/` - Obtain JWT token
-   `POST /api/auth/token/refresh/` - Refresh token
-   `POST /api/auth/token/verify/` - Verify token

## 🔄 Background Tasks

Celery tasks for automated data processing:

-   **NEO Data Sync**: Fetches NEO data every 6 hours
-   **Close Approaches Update**: Updates every hour
-   **Threat Assessments**: Recalculates every 12 hours
-   **Statistics Calculation**: Updates NEO statistics

### Running Celery

```bash
# Start Celery worker
celery -A meteor_madness worker -l info

# Start Celery beat (scheduler)
celery -A meteor_madness beat -l info
```

## 📚 API Documentation

Interactive API documentation available at:

-   **Swagger UI**: http://localhost:8000/api/docs/
-   **ReDoc**: http://localhost:8000/api/redoc/
-   **OpenAPI Schema**: http://localhost:8000/api/schema/

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test file
pytest neos/tests/test_models.py
```

## 🚢 Deployment

### Production Checklist

1. Set `DEBUG=False` in environment
2. Configure `SECRET_KEY` with strong random value
3. Set up PostgreSQL database
4. Configure Redis for caching and Celery
5. Set up proper `ALLOWED_HOSTS`
6. Configure CORS origins
7. Set up HTTPS/SSL certificates
8. Configure static file serving
9. Set up Celery worker and beat
10. Configure monitoring (Sentry)

### Docker Deployment (Optional)

```bash
# Build image
docker build -t meteor-madness-backend .

# Run container
docker run -p 8000:8000 meteor-madness-backend
```

## 📊 Database Models

### Main Models

-   **NEO**: Near-Earth Object data
-   **CloseApproach**: Close approach events
-   **ThreatScenario**: Threat scenarios
-   **ThreatAssessment**: Calculated threats
-   **ImpactEvent**: Historical impacts
-   **Earthquake**: Historical earthquakes
-   **SeismicImpactAnalysis**: Seismic calculations
-   **EmergencyChecklist**: Safety checklists
-   **SafetyPlan**: User safety plans
-   **MeteorShower**: Meteor shower data
-   **OrbitalElements**: Orbital mechanics
-   **Notification**: User notifications
-   **ThreatAlert**: System alerts

## 🔐 Security

-   JWT-based authentication
-   CORS protection
-   Rate limiting (100 req/hour for anonymous, 1000 req/hour for authenticated)
-   HTTPS enforcement in production
-   Secure cookie handling
-   CSRF protection

## 📝 License

This project is licensed under the MIT License.

## 👥 Contributors

Created for NASA Space Apps Challenge 2025

## 🆘 Support

For issues and questions:

-   Open an issue on GitHub
-   Contact: [Your contact information]

## 🙏 Acknowledgments

-   NASA Open APIs
-   USGS Earthquake Data
-   CNEOS (Center for Near-Earth Object Studies)
-   Canadian Space Agency NEOSSAT

## 📈 Version

Current Version: 0.1.0

## 🔮 Future Features

-   Machine learning predictions
-   Enhanced visualization data
-   Real-time impact simulations
-   Multi-language support
-   Mobile app integration
-   Blockchain-secured alerts
-   Gamified education modules
