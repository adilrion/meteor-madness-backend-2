"""
Asteroid Threat Assessment Serializers
"""
from rest_framework import serializers
from .models import ThreatScenario, ThreatAssessment, DestructionZone


class DestructionZoneSerializer(serializers.ModelSerializer):
    """Serializer for destruction zones"""
    
    class Meta:
        model = DestructionZone
        fields = [
            'id', 'zone_type', 'radius_km', 'area_km2',
            'overpressure_psi', 'fatality_rate',
            'estimated_casualties', 'estimated_injuries'
        ]


class ThreatAssessmentSerializer(serializers.ModelSerializer):
    """Serializer for threat assessments"""
    
    destruction_zones = DestructionZoneSerializer(many=True, read_only=True)
    neo_name = serializers.CharField(source='neo.name', read_only=True)
    scenario_name = serializers.CharField(source='scenario.name', read_only=True)
    
    class Meta:
        model = ThreatAssessment
        fields = [
            'id', 'neo', 'neo_name', 'scenario', 'scenario_name',
            'overall_risk_level', 'impact_probability',
            'kinetic_energy_megatons', 'crater_diameter_km', 'destruction_radius_km',
            'estimated_deaths', 'estimated_injuries', 'economic_loss_billions_usd',
            'seismic_magnitude', 'tsunami_risk',
            'dust_cloud_duration_days', 'global_temperature_change_c',
            'destruction_zones', 'calculated_at', 'calculation_version'
        ]


class ThreatScenarioSerializer(serializers.ModelSerializer):
    """Serializer for threat scenarios"""
    
    assessments = ThreatAssessmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = ThreatScenario
        fields = '__all__'


class ThreatScenarioListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for scenario list views"""
    
    class Meta:
        model = ThreatScenario
        fields = [
            'id', 'name', 'description', 'diameter_km', 'velocity_kps',
            'energy_megatons', 'crater_diameter_km', 'seismic_magnitude',
            'impact_type', 'scenario_type'
        ]

