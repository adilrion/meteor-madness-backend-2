"""
Notifications Admin Configuration
"""
from django.contrib import admin
from .models import Notification, ThreatAlert, AlertSubscription


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'notification_type', 'title', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read']
    search_fields = ['title', 'message']
    date_hierarchy = 'created_at'


@admin.register(ThreatAlert)
class ThreatAlertAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'alert_level', 'threat_object_name',
        'is_active', 'created_at'
    ]
    list_filter = ['alert_level', 'is_active']
    search_fields = ['title', 'threat_object_name']


@admin.register(AlertSubscription)
class AlertSubscriptionAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'subscription_type', 'email_enabled',
        'sms_enabled', 'is_active'
    ]
    list_filter = ['subscription_type', 'is_active']

