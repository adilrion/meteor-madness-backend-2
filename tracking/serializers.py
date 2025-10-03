"""
Tracking Serializers
"""
from rest_framework import serializers
from .models import MeteorShower, LiveTrackingSession, MeteorActivity


class MeteorShowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeteorShower
        fields = '__all__'


class LiveTrackingSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiveTrackingSession
        fields = '__all__'


class MeteorActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = MeteorActivity
        fields = '__all__'

