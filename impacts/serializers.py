"""
Impact Events Serializers
"""
from rest_framework import serializers
from .models import ImpactEvent, Earthquake


class ImpactEventSerializer(serializers.ModelSerializer):
    """Serializer for impact events"""
    
    severity_category = serializers.CharField(read_only=True)
    
    class Meta:
        model = ImpactEvent
        fields = '__all__'


class EarthquakeSerializer(serializers.ModelSerializer):
    """Serializer for earthquakes"""
    
    class Meta:
        model = Earthquake
        fields = '__all__'

