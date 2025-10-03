"""
Safety Serializers
"""
from rest_framework import serializers
from .models import (
    EmergencyChecklist,
    ResourceAllocation,
    SafetyPlan,
    MentalHealthResource,
    ChatbotConversation,
    ClimateImpactModel
)


class EmergencyChecklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyChecklist
        fields = '__all__'


class ResourceAllocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceAllocation
        fields = '__all__'


class SafetyPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SafetyPlan
        fields = '__all__'
        read_only_fields = ['user']


class MentalHealthResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentalHealthResource
        fields = '__all__'


class ChatbotConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatbotConversation
        fields = '__all__'


class ClimateImpactModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClimateImpactModel
        fields = '__all__'

