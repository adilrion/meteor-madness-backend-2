"""
Tracking Admin Configuration
"""
from django.contrib import admin
from .models import MeteorShower, LiveTrackingSession, MeteorActivity


@admin.register(MeteorShower)
class MeteorShowerAdmin(admin.ModelAdmin):
    list_display = ['name', 'peak_date', 'zhr', 'is_active']
    list_filter = ['is_active', 'hemisphere']
    date_hierarchy = 'peak_date'


@admin.register(LiveTrackingSession)
class LiveTrackingSessionAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'total_objects', 'last_active']
    readonly_fields = ['last_active']


@admin.register(MeteorActivity)
class MeteorActivityAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'activity_level', 'meteors_per_hour', 'detection_stations']
    list_filter = ['activity_level']
    date_hierarchy = 'timestamp'

