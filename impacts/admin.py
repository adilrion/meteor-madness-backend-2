"""
Impacts Admin Configuration
"""
from django.contrib import admin
from .models import ImpactEvent, Earthquake


@admin.register(ImpactEvent)
class ImpactEventAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'date_description', 'location_name',
        'energy_megatons', 'severity_category', 'casualties'
    ]
    list_filter = ['extinction_event', 'crater_preserved', 'evidence_type']
    search_fields = ['name', 'location_name', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Earthquake)
class EarthquakeAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'date', 'location', 'magnitude',
        'casualties', 'tsunami_generated'
    ]
    list_filter = ['tsunami_generated']
    search_fields = ['name', 'location', 'country']
    readonly_fields = ['energy_joules', 'energy_megatons', 'created_at', 'updated_at']
    date_hierarchy = 'date'

