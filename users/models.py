"""
User Models
"""
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    Extended user profile
    """
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Location
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    timezone = models.CharField(max_length=50, default='UTC')
    
    # Preferences
    notification_preferences = models.JSONField(default=dict)
    measurement_units = models.CharField(
        max_length=20,
        choices=[
            ('metric', 'Metric'),
            ('imperial', 'Imperial')
        ],
        default='metric'
    )
    
    # Interests
    interests = models.JSONField(default=list)
    subscribed_alerts = models.JSONField(default=list)
    
    # Privacy
    profile_public = models.BooleanField(default=False)
    show_location = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_profiles'
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
    
    def __str__(self):
        return f"Profile: {self.user.username}"


class UserActivity(models.Model):
    """
    Track user activity
    """
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    
    activity_type = models.CharField(
        max_length=50,
        choices=[
            ('view_neo', 'Viewed NEO'),
            ('view_scenario', 'Viewed Scenario'),
            ('create_plan', 'Created Safety Plan'),
            ('chat', 'Used Chatbot'),
            ('calculate', 'Used Calculator')
        ]
    )
    
    activity_data = models.JSONField(default=dict)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.CharField(max_length=500, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_activities'
        ordering = ['-created_at']
        verbose_name = 'User Activity'
        verbose_name_plural = 'User Activities'
    
    def __str__(self):
        return f"{self.user.username} - {self.activity_type}"

