# Project Structure

Complete overview of the Meteor Madness Backend codebase structure.

## Directory Structure

```
meteor-madness-backend/
├── meteor_madness/              # Main project configuration
│   ├── __init__.py
│   ├── settings.py             # Django settings
│   ├── urls.py                 # Main URL routing
│   ├── wsgi.py                 # WSGI configuration
│   ├── asgi.py                 # ASGI configuration (WebSockets)
│   └── celery.py               # Celery configuration
│
├── neos/                       # NEO (Near-Earth Objects) app
│   ├── models.py               # NEO, CloseApproach, NEOStatistics models
│   ├── views.py                # API endpoints
│   ├── serializers.py          # REST serializers
│   ├── services.py             # NASA API integration
│   ├── tasks.py                # Celery tasks
│   ├── urls.py                 # URL routing
│   └── admin.py                # Django admin configuration
│
├── asteroids/                  # Asteroid threat assessment app
│   ├── models.py               # ThreatScenario, ThreatAssessment, DestructionZone
│   ├── views.py                # Threat assessment endpoints
│   ├── serializers.py          # Serializers
│   ├── services.py             # Threat calculation service
│   ├── tasks.py                # Background tasks
│   ├── urls.py                 # URL routing
│   └── admin.py                # Admin configuration
│
├── impacts/                    # Historical impact events app
│   ├── models.py               # ImpactEvent, Earthquake models
│   ├── views.py                # Impact data endpoints
│   ├── serializers.py          # Serializers
│   ├── urls.py                 # URL routing
│   └── admin.py                # Admin configuration
│
├── seismic/                    # Seismic impact analysis app
│   ├── models.py               # SeismicImpactAnalysis, ShockwaveModel
│   ├── views.py                # Seismic calculation endpoints
│   ├── serializers.py          # Serializers
│   ├── services.py             # Seismic calculations
│   ├── urls.py                 # URL routing
│   └── admin.py                # Admin configuration
│
├── safety/                     # Safety center features app
│   ├── models.py               # EmergencyChecklist, SafetyPlan, ChatbotConversation, etc.
│   ├── views.py                # Safety feature endpoints
│   ├── serializers.py          # Serializers
│   ├── services.py             # Chatbot, resource calculator, climate modeling
│   ├── urls.py                 # URL routing
│   └── admin.py                # Admin configuration
│
├── tracking/                   # Live tracking app
│   ├── models.py               # MeteorShower, LiveTrackingSession, MeteorActivity
│   ├── views.py                # Tracking endpoints
│   ├── serializers.py          # Serializers
│   ├── consumers.py            # WebSocket consumers
│   ├── routing.py              # WebSocket routing
│   ├── tasks.py                # Background tasks
│   ├── urls.py                 # URL routing
│   └── admin.py                # Admin configuration
│
├── orbital/                    # Orbital mechanics app
│   ├── models.py               # OrbitalElements, TrajectoryPoint
│   ├── views.py                # Orbital calculation endpoints
│   ├── serializers.py          # Serializers
│   ├── services.py             # Orbital mechanics calculations
│   ├── urls.py                 # URL routing
│   └── admin.py                # Admin configuration
│
├── users/                      # User management app
│   ├── models.py               # UserProfile, UserActivity
│   ├── views.py                # User endpoints
│   ├── serializers.py          # Serializers
│   ├── urls.py                 # URL routing
│   └── admin.py                # Admin configuration
│
├── notifications/              # Notifications app
│   ├── models.py               # Notification, ThreatAlert, AlertSubscription
│   ├── views.py                # Notification endpoints
│   ├── serializers.py          # Serializers
│   ├── urls.py                 # URL routing
│   └── admin.py                # Admin configuration
│
├── logs/                       # Application logs (created at runtime)
├── media/                      # User-uploaded files (created at runtime)
├── staticfiles/                # Collected static files (created at runtime)
│
├── requirements.txt            # Python dependencies
├── manage.py                   # Django management script
├── env.example                 # Environment variables template
├── .gitignore                  # Git ignore rules
├── README.md                   # Project documentation
├── QUICKSTART.md              # Quick start guide
├── DEPLOYMENT.md              # Deployment instructions
├── API_DOCUMENTATION.md       # API reference
├── CONTRIBUTING.md            # Contribution guidelines
└── PROJECT_STRUCTURE.md       # This file
```

## App Descriptions

### 1. neos/

**Purpose**: NEO data management and NASA API integration

**Key Models**:

-   `NEO`: Near-Earth Object data (34,000+ objects)
-   `CloseApproach`: Close approach events
-   `NEOStatistics`: Aggregated statistics

**Key Features**:

-   NASA API integration
-   Real-time data synchronization
-   Close approach tracking
-   NEO statistics dashboard

**API Endpoints**:

-   `/api/neos/objects/` - List/filter NEOs
-   `/api/neos/close-approaches/` - Approach data
-   `/api/neos/statistics/` - Statistics

### 2. asteroids/

**Purpose**: Threat assessment and scenario analysis

**Key Models**:

-   `ThreatScenario`: Pre-configured scenarios
-   `ThreatAssessment`: Calculated threats
-   `DestructionZone`: Impact zones

**Key Features**:

-   6 pre-configured scenarios
-   Multi-scenario comparison
-   Threat level calculation
-   Casualty estimation
-   Economic impact analysis

**API Endpoints**:

-   `/api/asteroids/scenarios/` - Scenarios
-   `/api/asteroids/assessments/` - Assessments

### 3. impacts/

**Purpose**: Historical impact events database

**Key Models**:

-   `ImpactEvent`: Historical impacts (7 major events)
-   `Earthquake`: Historical earthquakes (8 events)

**Key Features**:

-   Impact event catalog
-   Earthquake comparison
-   Energy calculations
-   Historical analysis

**API Endpoints**:

-   `/api/impacts/events/` - Impact events
-   `/api/impacts/earthquakes/` - Earthquakes

### 4. seismic/

**Purpose**: Seismic impact analysis

**Key Models**:

-   `SeismicImpactAnalysis`: Seismic calculations
-   `ShockwaveModel`: Shockwave propagation

**Key Features**:

-   Moment magnitude calculation
-   Ground motion modeling
-   Damage zone estimation
-   Earthquake comparison
-   Shockwave modeling

**API Endpoints**:

-   `/api/seismic/analyses/` - Analyses
-   `/api/seismic/analyses/calculate/` - Calculate

### 5. safety/

**Purpose**: MeteorShield safety features

**Key Models**:

-   `EmergencyChecklist`: Safety checklists
-   `ResourceAllocation`: Resource calculations
-   `SafetyPlan`: User safety plans
-   `MentalHealthResource`: Support resources
-   `ChatbotConversation`: AI chatbot
-   `ClimateImpactModel`: Climate modeling

**Key Features**:

-   AI-powered chatbot (8 implemented features)
-   Resource allocation calculator
-   Climate chain reaction modeling
-   Emergency planning tools
-   Mental health support
-   Psychological preparedness

**API Endpoints**:

-   `/api/safety/checklists/` - Checklists
-   `/api/safety/resources/` - Resources
-   `/api/safety/chatbot/` - Chatbot
-   `/api/safety/climate-models/` - Climate

### 6. tracking/

**Purpose**: Live meteor and NEO tracking

**Key Models**:

-   `MeteorShower`: Meteor shower data
-   `LiveTrackingSession`: Tracking sessions
-   `MeteorActivity`: Real-time activity

**Key Features**:

-   Real-time tracking
-   WebSocket support
-   Meteor shower catalog
-   Activity monitoring

**API Endpoints**:

-   `/api/tracking/meteor-showers/` - Showers
-   `/api/tracking/activity/` - Activity
-   `/ws/tracking/` - WebSocket

### 7. orbital/

**Purpose**: Orbital mechanics calculations

**Key Models**:

-   `OrbitalElements`: Keplerian elements
-   `TrajectoryPoint`: 3D trajectory points

**Key Features**:

-   Orbital element calculation
-   Trajectory propagation
-   3D visualization data
-   MOID calculation

**API Endpoints**:

-   `/api/orbital/elements/` - Elements
-   `/api/orbital/trajectories/` - Trajectories

### 8. users/

**Purpose**: User management

**Key Models**:

-   `UserProfile`: Extended profiles
-   `UserActivity`: Activity tracking

**Key Features**:

-   User profiles
-   Preferences management
-   Activity logging

**API Endpoints**:

-   `/api/users/` - Users
-   `/api/users/profiles/` - Profiles

### 9. notifications/

**Purpose**: Alert and notification system

**Key Models**:

-   `Notification`: User notifications
-   `ThreatAlert`: System alerts
-   `AlertSubscription`: User subscriptions

**Key Features**:

-   Real-time notifications
-   Threat alerts
-   Custom subscriptions
-   Multi-channel delivery

**API Endpoints**:

-   `/api/notifications/` - Notifications
-   `/api/notifications/alerts/` - Alerts

## Key Technologies

### Backend Framework

-   **Django 5.0.1**: Web framework
-   **Django REST Framework**: API framework
-   **Channels**: WebSocket support

### Database

-   **PostgreSQL**: Primary database
-   **Redis**: Caching and message broker

### Task Queue

-   **Celery**: Asynchronous tasks
-   **Redis**: Message broker

### Scientific Computing

-   **NumPy**: Numerical calculations
-   **SciPy**: Scientific computations
-   **Pandas**: Data manipulation
-   **Astropy**: Astronomy calculations
-   **Skyfield**: Orbital mechanics

### Authentication

-   **Simple JWT**: Token authentication
-   **Django Allauth**: User authentication

### API Documentation

-   **drf-spectacular**: OpenAPI 3.0
-   **drf-yasg**: Swagger/ReDoc

## Data Flow

### NEO Data Flow

```
NASA API → NEODataService → NEO Model → REST API → Frontend
                ↓
         Celery Tasks (periodic sync)
                ↓
         NEOStatistics
```

### Threat Assessment Flow

```
ThreatScenario → ThreatCalculationService → ThreatAssessment
                         ↓
                 SeismicCalculationService → SeismicImpactAnalysis
                         ↓
                 ClimateModelingService → ClimateImpactModel
```

### Real-time Tracking Flow

```
NASA API → TrackingService → WebSocket Consumer → Frontend
     ↓
Celery Tasks → MeteorActivity → WebSocket Broadcast
```

## Background Tasks (Celery)

### Scheduled Tasks

1. **fetch_neo_data** (every 6 hours)

    - Syncs NEO data from NASA
    - Updates close approaches

2. **update_close_approaches** (every hour)

    - Updates close approach data

3. **calculate_threat_assessments** (every 12 hours)

    - Recalculates threat assessments

4. **calculate_neo_statistics** (triggered)
    - Updates NEO statistics

## Configuration Files

### settings.py

Main Django configuration:

-   Database settings
-   Installed apps
-   Middleware
-   Authentication
-   REST Framework
-   Celery
-   NASA API configuration

### urls.py

URL routing:

-   API endpoints
-   Admin interface
-   Authentication
-   Documentation

### celery.py

Celery configuration:

-   Task discovery
-   Beat schedule
-   Result backend

### wsgi.py / asgi.py

Server configurations:

-   WSGI for traditional deployment
-   ASGI for WebSocket support

## Database Schema Overview

### Core Tables

-   `neos` - 34,000+ NEO records
-   `close_approaches` - Approach events
-   `threat_scenarios` - 6 scenarios
-   `threat_assessments` - Calculated threats
-   `impact_events` - 7 historical impacts
-   `earthquakes` - 8 historical earthquakes
-   `meteor_showers` - Meteor shower catalog

### Relationships

```
NEO ←→ CloseApproach (1:M)
NEO ←→ ThreatAssessment (1:1)
ThreatAssessment ←→ DestructionZone (1:M)
ThreatAssessment ←→ SeismicImpactAnalysis (1:1)
User ←→ UserProfile (1:1)
User ←→ SafetyPlan (1:M)
User ←→ Notification (1:M)
```

## API Architecture

### RESTful Design

-   Resource-based URLs
-   Standard HTTP methods
-   JSON responses
-   Pagination support
-   Filtering and search

### Authentication

-   JWT token-based
-   Bearer token in headers
-   Token refresh mechanism

### Rate Limiting

-   100 requests/hour (anonymous)
-   1000 requests/hour (authenticated)

### WebSocket

-   Real-time tracking updates
-   Channel-based subscriptions
-   JSON message format

## Development Workflow

1. **Local Development**

    ```bash
    python manage.py runserver
    celery -A meteor_madness worker -l info
    celery -A meteor_madness beat -l info
    ```

2. **Database Migrations**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

3. **Testing**

    ```bash
    pytest
    python manage.py check
    ```

4. **Code Quality**
    ```bash
    black .
    flake8
    isort .
    ```

## Deployment Architecture

```
Internet → Nginx → Gunicorn → Django Application
                      ↓
                 PostgreSQL Database
                      ↓
                  Redis Cache/Queue
                      ↓
                 Celery Workers
```

## Monitoring & Logs

### Log Files

-   `gunicorn-access.log` - Access logs
-   `gunicorn-error.log` - Error logs
-   `celery.log` - Celery worker logs
-   `meteor_madness.log` - Application logs

### Monitoring

-   Health check endpoint: `/health/`
-   Admin interface: `/admin/`
-   API documentation: `/api/docs/`

## Security Considerations

-   JWT authentication
-   CORS configuration
-   Rate limiting
-   Input validation
-   SQL injection protection (ORM)
-   XSS protection
-   CSRF protection
-   Secure headers in production

## Performance Optimization

-   Database indexing
-   Redis caching
-   Query optimization
-   Celery for background tasks
-   Connection pooling
-   Static file serving via CDN

---

For more detailed information, see:

-   [README.md](README.md) - General documentation
-   [QUICKSTART.md](QUICKSTART.md) - Quick start guide
-   [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - API reference
-   [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment guide
