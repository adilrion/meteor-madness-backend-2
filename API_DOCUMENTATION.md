# API Documentation

## Meteor Madness Backend API Reference

Base URL: `http://localhost:8000/api/` (development)

## Authentication

The API uses JWT (JSON Web Token) authentication.

### Obtain Token

```http
POST /api/auth/token/
Content-Type: application/json

{
    "username": "your_username",
    "password": "your_password"
}
```

Response:

```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Use Token

Include the access token in the Authorization header:

```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

## NEOs API

### List NEOs

```http
GET /api/neos/objects/
GET /api/neos/objects/?is_potentially_hazardous_asteroid=true
GET /api/neos/objects/?page=2
```

### Get NEO Details

```http
GET /api/neos/objects/{id}/
```

### Get PHAs

```http
GET /api/neos/objects/potentially_hazardous/
```

### Filter by Size

```http
GET /api/neos/objects/by_size/?size=large
```

Sizes: `small`, `medium`, `large`, `very_large`

### Sync NASA Data

```http
POST /api/neos/objects/sync_nasa_data/
```

## Close Approaches API

### Upcoming Approaches

```http
GET /api/neos/close-approaches/upcoming/?days=7
```

### Close Encounters

```http
GET /api/neos/close-approaches/close_encounters/?threshold=10
```

## Statistics API

### Latest Statistics

```http
GET /api/neos/statistics/latest/
```

Response:

```json
{
    "id": 1,
    "date": "2025-10-03",
    "total_neos": 34520,
    "total_phas": 2347,
    "small_neos_count": 28000,
    "medium_neos_count": 5200,
    "large_neos_count": 980,
    "very_large_neos_count": 340,
    "close_approaches_next_7_days": 15,
    "close_approaches_next_30_days": 67
}
```

## Asteroids API

### List Threat Scenarios

```http
GET /api/asteroids/scenarios/
GET /api/asteroids/scenarios/?impact_type=ocean
```

### Get Scenario Details

```http
GET /api/asteroids/scenarios/{id}/
```

### Calculate Threat Assessment

```http
POST /api/asteroids/scenarios/{id}/calculate_assessment/
```

### Compare Scenarios

```http
POST /api/asteroids/scenarios/compare/
Content-Type: application/json

{
    "scenario_ids": [1, 2, 3]
}
```

### Threat Assessments

```http
GET /api/asteroids/assessments/
GET /api/asteroids/assessments/high_risk/
```

## Impacts API

### Historical Impact Events

```http
GET /api/impacts/events/
GET /api/impacts/events/major_events/
GET /api/impacts/events/recent_events/
```

### Earthquakes

```http
GET /api/impacts/earthquakes/
GET /api/impacts/earthquakes/major_earthquakes/
```

## Seismic API

### Calculate Seismic Impact

```http
POST /api/seismic/analyses/calculate/
Content-Type: application/json

{
    "threat_assessment_id": 1
}
```

Response includes:

-   Moment magnitude
-   Ground motion parameters
-   Damage zones
-   Comparable earthquakes
-   Shockwave models

## Safety API

### Emergency Checklists

```http
GET /api/safety/checklists/
GET /api/safety/checklists/?category=pre_impact
```

### Resource Calculator

```http
POST /api/safety/resources/calculate/
Content-Type: application/json

{
    "population_size": 10000,
    "shelter_duration_days": 30
}
```

Response:

```json
{
    "water_liters": 900000,
    "food_calories": 600000000,
    "medical_supplies_units": 42,
    "shelter_space_m2": 30000,
    "power_kwh": 150000,
    "personnel_required": 100,
    "vehicles_required": 20,
    "communication_devices": 200
}
```

### AI Chatbot

```http
POST /api/safety/chatbot/chat/
Content-Type: application/json

{
    "message": "How do I prepare for an asteroid impact?",
    "session_id": "optional-session-id"
}
```

### Climate Impact Modeling

```http
POST /api/safety/climate-models/calculate/
Content-Type: application/json

{
    "impact_energy_mt": 10000
}
```

### Mental Health Resources

```http
GET /api/safety/mental-health/
GET /api/safety/mental-health/crisis_hotlines/
```

## Tracking API

### Meteor Showers

```http
GET /api/tracking/meteor-showers/
GET /api/tracking/meteor-showers/upcoming/
GET /api/tracking/meteor-showers/active/
```

### Current Meteor Activity

```http
GET /api/tracking/activity/current/
```

### Activity History

```http
GET /api/tracking/activity/history/?hours=24
```

## Orbital API

### Calculate Orbital Elements

```http
POST /api/orbital/elements/calculate/
Content-Type: application/json

{
    "neo_id": 1
}
```

### Get Trajectory

```http
GET /api/orbital/trajectories/for_neo/?neo_id=1
```

### Calculate Trajectory

```http
POST /api/orbital/trajectories/calculate/
Content-Type: application/json

{
    "neo_id": 1,
    "num_points": 100
}
```

## Notifications API

### Get Notifications

```http
GET /api/notifications/
GET /api/notifications/unread/
```

### Mark as Read

```http
POST /api/notifications/{id}/mark_read/
```

### Mark All Read

```http
POST /api/notifications/mark_all_read/
```

### Threat Alerts

```http
GET /api/notifications/alerts/active/
GET /api/notifications/alerts/critical/
```

### Alert Subscriptions

```http
GET /api/notifications/subscriptions/
POST /api/notifications/subscriptions/
```

Subscription body:

```json
{
    "subscription_type": "high_threats",
    "min_alert_level": "high",
    "email_enabled": true,
    "push_enabled": true
}
```

## WebSocket API

### Live Tracking WebSocket

```javascript
const ws = new WebSocket("ws://localhost:8000/ws/tracking/");

ws.onopen = () => {
    ws.send(
        JSON.stringify({
            type: "subscribe",
            objects: ["neo_id_1", "neo_id_2"],
        })
    );
};

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log("Tracking update:", data);
};
```

## Error Responses

### 400 Bad Request

```json
{
    "error": "Invalid parameters"
}
```

### 401 Unauthorized

```json
{
    "detail": "Authentication credentials were not provided."
}
```

### 404 Not Found

```json
{
    "detail": "Not found."
}
```

### 500 Internal Server Error

```json
{
    "error": "Internal server error"
}
```

## Rate Limiting

-   Anonymous: 100 requests/hour
-   Authenticated: 1000 requests/hour

Rate limit headers:

```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 995
X-RateLimit-Reset: 1633536000
```

## Pagination

List endpoints support pagination:

```http
GET /api/neos/objects/?page=2&page_size=50
```

Response includes:

```json
{
    "count": 34520,
    "next": "http://localhost:8000/api/neos/objects/?page=3",
    "previous": "http://localhost:8000/api/neos/objects/?page=1",
    "results": [...]
}
```

## Filtering & Searching

Most list endpoints support filtering:

```http
GET /api/neos/objects/?search=apophis
GET /api/asteroids/scenarios/?scenario_type=historical
GET /api/impacts/events/?extinction_event=true
```

## Interactive Documentation

Visit these URLs for interactive API documentation:

-   Swagger UI: http://localhost:8000/api/docs/
-   ReDoc: http://localhost:8000/api/redoc/
-   OpenAPI Schema: http://localhost:8000/api/schema/

## Examples

### Complete Threat Assessment Flow

1. Get a threat scenario:

```http
GET /api/asteroids/scenarios/1/
```

2. Calculate threat assessment:

```http
POST /api/asteroids/scenarios/1/calculate_assessment/
```

3. Calculate seismic impact:

```http
POST /api/seismic/analyses/calculate/
{
    "threat_assessment_id": 1
}
```

4. Calculate climate impact:

```http
POST /api/safety/climate-models/calculate/
{
    "impact_energy_mt": 10000
}
```

5. Calculate resource needs:

```http
POST /api/safety/resources/calculate/
{
    "population_size": 100000,
    "shelter_duration_days": 90
}
```

For more examples and detailed documentation, visit the interactive docs.
