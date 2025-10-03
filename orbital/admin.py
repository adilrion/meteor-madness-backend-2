"""
Orbital Admin Configuration
"""
from django.contrib import admin
from .models import OrbitalElements, TrajectoryPoint


@admin.register(OrbitalElements)
class OrbitalElementsAdmin(admin.ModelAdmin):
    list_display = [
        'neo', 'semi_major_axis_au', 'eccentricity',
        'orbital_period_days', 'orbit_class'
    ]
    list_filter = ['orbit_class']
    readonly_fields = ['calculated_at']


@admin.register(TrajectoryPoint)
class TrajectoryPointAdmin(admin.ModelAdmin):
    list_display = [
        'neo', 'julian_date', 'earth_distance_au'
    ]
    list_filter = ['neo']

