"""
Orbital Serializers
"""
from rest_framework import serializers
from .models import OrbitalElements, TrajectoryPoint


class OrbitalElementsSerializer(serializers.ModelSerializer):
    neo_name = serializers.CharField(source='neo.name', read_only=True)
    
    class Meta:
        model = OrbitalElements
        fields = '__all__'


class TrajectoryPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrajectoryPoint
        fields = [
            'julian_date',
            'position_x_au', 'position_y_au', 'position_z_au',
            'velocity_x_au_per_day', 'velocity_y_au_per_day', 'velocity_z_au_per_day',
            'earth_distance_au'
        ]

