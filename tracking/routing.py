"""
WebSocket routing for live tracking
"""
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/tracking/', consumers.TrackingConsumer.as_asgi()),
]

