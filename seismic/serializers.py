"""
Seismic Serializers
"""
from rest_framework import serializers
from .models import SeismicImpactAnalysis, ShockwaveModel


class ShockwaveModelSerializer(serializers.ModelSerializer):
    """Serializer for shockwave models"""
    
    class Meta:
        model = ShockwaveModel
        fields = '__all__'


class SeismicImpactAnalysisSerializer(serializers.ModelSerializer):
    """Serializer for seismic impact analysis"""
    
    shockwave_models = ShockwaveModelSerializer(many=True, read_only=True)
    
    class Meta:
        model = SeismicImpactAnalysis
        fields = '__all__'

