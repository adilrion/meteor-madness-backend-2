"""
NEO Admin Configuration
"""
from django.contrib import admin
from .models import NEO, CloseApproach, NEOStatistics


@admin.register(NEO)
class NEOAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'neo_reference_id', 'is_potentially_hazardous_asteroid',
        'estimated_diameter_avg_km', 'size_category', 'last_synced_at'
    ]
    list_filter = ['is_potentially_hazardous_asteroid', 'is_sentry_object']
    search_fields = ['name', 'neo_reference_id', 'designation']
    readonly_fields = ['created_at', 'updated_at', 'last_synced_at']
    
    fieldsets = (
        ('Identification', {
            'fields': ('neo_reference_id', 'name', 'designation')
        }),
        ('Classification', {
            'fields': ('is_potentially_hazardous_asteroid', 'is_sentry_object')
        }),
        ('Physical Properties', {
            'fields': (
                'absolute_magnitude_h',
                'estimated_diameter_min_km', 'estimated_diameter_max_km',
                'estimated_diameter_min_m', 'estimated_diameter_max_m'
            )
        }),
        ('Orbital Data', {
            'fields': (
                'orbital_period_days', 'perihelion_distance', 'aphelion_distance',
                'semi_major_axis', 'eccentricity', 'inclination', 'orbital_data'
            )
        }),
        ('Metadata', {
            'fields': (
                'first_observation_date', 'last_observation_date',
                'observations_used', 'nasa_jpl_url',
                'created_at', 'updated_at', 'last_synced_at'
            )
        }),
    )


@admin.register(CloseApproach)
class CloseApproachAdmin(admin.ModelAdmin):
    list_display = [
        'neo', 'close_approach_date', 'miss_distance_lunar',
        'relative_velocity_kps', 'is_close'
    ]
    list_filter = ['orbiting_body', 'close_approach_date']
    search_fields = ['neo__name']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'close_approach_date'


@admin.register(NEOStatistics)
class NEOStatisticsAdmin(admin.ModelAdmin):
    list_display = [
        'date', 'total_neos', 'total_phas',
        'close_approaches_next_7_days', 'updated_at'
    ]
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'date'

