"""
Asteroid Admin Configuration
"""
from django.contrib import admin
from .models import ThreatScenario, ThreatAssessment, DestructionZone


@admin.register(ThreatScenario)
class ThreatScenarioAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'diameter_km', 'velocity_kps', 'energy_megatons',
        'impact_type', 'scenario_type', 'is_active'
    ]
    list_filter = ['scenario_type', 'impact_type', 'is_active']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ThreatAssessment)
class ThreatAssessmentAdmin(admin.ModelAdmin):
    list_display = [
        'neo', 'scenario', 'overall_risk_level',
        'kinetic_energy_megatons', 'estimated_deaths',
        'calculated_at'
    ]
    list_filter = ['overall_risk_level', 'tsunami_risk']
    readonly_fields = ['calculated_at']


@admin.register(DestructionZone)
class DestructionZoneAdmin(admin.ModelAdmin):
    list_display = [
        'assessment', 'zone_type', 'radius_km',
        'fatality_rate', 'estimated_casualties'
    ]
    list_filter = ['zone_type']

