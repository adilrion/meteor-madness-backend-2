"""
Seismic Admin Configuration
"""
from django.contrib import admin
from .models import SeismicImpactAnalysis, ShockwaveModel


@admin.register(SeismicImpactAnalysis)
class SeismicImpactAnalysisAdmin(admin.ModelAdmin):
    list_display = [
        'threat_assessment', 'moment_magnitude', 'richter_scale_equivalent',
        'modified_mercalli_intensity', 'calculated_at'
    ]
    readonly_fields = ['calculated_at']


@admin.register(ShockwaveModel)
class ShockwaveModelAdmin(admin.ModelAdmin):
    list_display = [
        'seismic_analysis', 'wave_type', 'distance_from_impact_km',
        'peak_overpressure_psi', 'structural_damage_level'
    ]
    list_filter = ['wave_type', 'structural_damage_level']

