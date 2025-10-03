"""
Users Admin Configuration
"""
from django.contrib import admin
from .models import UserProfile, UserActivity


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'city', 'country', 'measurement_units', 'profile_public']
    list_filter = ['profile_public', 'measurement_units']
    search_fields = ['user__username', 'city', 'country']


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity_type', 'created_at']
    list_filter = ['activity_type']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']

