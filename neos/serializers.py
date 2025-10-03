"""
NEO Serializers - REST API serializers for NEO data
"""
from rest_framework import serializers
from .models import NEO, CloseApproach, NEOStatistics


class CloseApproachSerializer(serializers.ModelSerializer):
    """Serializer for Close Approach data"""
    
    neo_name = serializers.CharField(source='neo.name', read_only=True)
    is_close = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = CloseApproach
        fields = [
            'id', 'neo', 'neo_name',
            'close_approach_date', 'close_approach_date_full',
            'relative_velocity_kps', 'relative_velocity_kmph', 'relative_velocity_mph',
            'miss_distance_astronomical', 'miss_distance_lunar',
            'miss_distance_kilometers', 'miss_distance_miles',
            'orbiting_body', 'is_close',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class NEOListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for NEO list views"""
    
    size_category = serializers.CharField(read_only=True)
    estimated_diameter_avg_km = serializers.FloatField(read_only=True)
    next_close_approach = serializers.SerializerMethodField()
    
    class Meta:
        model = NEO
        fields = [
            'id', 'neo_reference_id', 'name', 'designation',
            'is_potentially_hazardous_asteroid', 'is_sentry_object',
            'absolute_magnitude_h',
            'estimated_diameter_min_km', 'estimated_diameter_max_km',
            'estimated_diameter_avg_km', 'size_category',
            'next_close_approach',
        ]
    
    def get_next_close_approach(self, obj):
        """Get the next upcoming close approach"""
        from django.utils import timezone
        next_approach = obj.close_approaches.filter(
            close_approach_date__gte=timezone.now().date()
        ).first()
        
        if next_approach:
            return {
                'date': next_approach.close_approach_date,
                'miss_distance_lunar': next_approach.miss_distance_lunar,
                'velocity_kps': next_approach.relative_velocity_kps
            }
        return None


class NEODetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for NEO detail views"""
    
    size_category = serializers.CharField(read_only=True)
    estimated_diameter_avg_km = serializers.FloatField(read_only=True)
    close_approaches = CloseApproachSerializer(many=True, read_only=True)
    
    class Meta:
        model = NEO
        fields = '__all__'


class NEOStatisticsSerializer(serializers.ModelSerializer):
    """Serializer for NEO statistics"""
    
    class Meta:
        model = NEOStatistics
        fields = '__all__'

