"""
Notification Models
"""
from django.db import models
from django.contrib.auth.models import User


class Notification(models.Model):
    """
    System notifications
    """
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications',
        null=True,
        blank=True
    )
    
    notification_type = models.CharField(
        max_length=50,
        choices=[
            ('info', 'Information'),
            ('warning', 'Warning'),
            ('alert', 'Alert'),
            ('critical', 'Critical')
        ]
    )
    
    title = models.CharField(max_length=200)
    message = models.TextField()
    
    # Related Objects
    related_object_type = models.CharField(max_length=50, blank=True)
    related_object_id = models.IntegerField(blank=True, null=True)
    
    # Metadata
    action_url = models.URLField(blank=True)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['notification_type']),
        ]
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
    
    def __str__(self):
        user_str = f"{self.user.username}" if self.user else "System"
        return f"{user_str} - {self.title}"


class ThreatAlert(models.Model):
    """
    Automated threat alerts
    """
    
    alert_level = models.CharField(
        max_length=20,
        choices=[
            ('low', 'Low'),
            ('moderate', 'Moderate'),
            ('high', 'High'),
            ('critical', 'Critical')
        ]
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Threat Details
    threat_object_name = models.CharField(max_length=200)
    threat_object_id = models.IntegerField(blank=True, null=True)
    estimated_impact_date = models.DateTimeField(blank=True, null=True)
    impact_probability = models.FloatField(blank=True, null=True)
    
    # Geographic Area
    affected_regions = models.JSONField(default=list)
    
    # Status
    is_active = models.BooleanField(default=True)
    resolved_at = models.DateTimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'threat_alerts'
        ordering = ['-alert_level', '-created_at']
        indexes = [
            models.Index(fields=['alert_level', 'is_active']),
        ]
        verbose_name = 'Threat Alert'
        verbose_name_plural = 'Threat Alerts'
    
    def __str__(self):
        return f"{self.alert_level.upper()}: {self.title}"


class AlertSubscription(models.Model):
    """
    User alert subscriptions
    """
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alert_subscriptions')
    
    subscription_type = models.CharField(
        max_length=50,
        choices=[
            ('all_threats', 'All Threats'),
            ('high_threats', 'High & Critical Only'),
            ('local_only', 'Local Region Only'),
            ('custom', 'Custom')
        ]
    )
    
    # Filters
    min_alert_level = models.CharField(max_length=20, default='low')
    regions_of_interest = models.JSONField(default=list)
    min_diameter_km = models.FloatField(default=0.0)
    
    # Delivery Channels
    email_enabled = models.BooleanField(default=True)
    sms_enabled = models.BooleanField(default=False)
    push_enabled = models.BooleanField(default=True)
    
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'alert_subscriptions'
        verbose_name = 'Alert Subscription'
        verbose_name_plural = 'Alert Subscriptions'
    
    def __str__(self):
        return f"{self.user.username} - {self.subscription_type}"

