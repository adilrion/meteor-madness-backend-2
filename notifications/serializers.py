"""
Notifications Serializers
"""
from rest_framework import serializers
from .models import Notification, ThreatAlert, AlertSubscription


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ['created_at']


class ThreatAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThreatAlert
        fields = '__all__'


class AlertSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertSubscription
        fields = '__all__'
        read_only_fields = ['user', 'created_at']

