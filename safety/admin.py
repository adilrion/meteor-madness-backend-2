"""
Safety Admin Configuration
"""
from django.contrib import admin
from .models import (
    EmergencyChecklist,
    ResourceAllocation,
    SafetyPlan,
    MentalHealthResource,
    ChatbotConversation,
    ClimateImpactModel
)


@admin.register(EmergencyChecklist)
class EmergencyChecklistAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'priority']
    list_filter = ['category']


@admin.register(ResourceAllocation)
class ResourceAllocationAdmin(admin.ModelAdmin):
    list_display = ['scenario_name', 'population_size', 'shelter_duration_days', 'created_at']


@admin.register(SafetyPlan)
class SafetyPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'plan_type', 'is_active', 'last_reviewed']
    list_filter = ['plan_type', 'is_active']


@admin.register(MentalHealthResource)
class MentalHealthResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'resource_type', 'is_active', 'priority']
    list_filter = ['resource_type', 'is_active']


@admin.register(ChatbotConversation)
class ChatbotConversationAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'user', 'created_at', 'updated_at']


@admin.register(ClimateImpactModel)
class ClimateImpactModelAdmin(admin.ModelAdmin):
    list_display = [
        'impact_energy_mt', 'initial_temperature_drop_c',
        'food_security_risk', 'calculated_at'
    ]

