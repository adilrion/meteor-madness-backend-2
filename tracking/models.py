"""
Live Tracking Models
"""
from django.db import models


class MeteorShower(models.Model):
    """
    Meteor shower data
    """
    
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    
    # Activity Period
    start_date = models.DateField()
    end_date = models.DateField()
    peak_date = models.DateField()
    
    # Characteristics
    zhr = models.IntegerField(help_text="Zenith Hourly Rate")
    velocity_kps = models.FloatField(help_text="Velocity in km/s")
    radiant_ra = models.FloatField(help_text="Right Ascension in degrees")
    radiant_dec = models.FloatField(help_text="Declination in degrees")
    parent_body = models.CharField(max_length=200, blank=True)
    
    # Visibility
    best_viewing_time = models.CharField(max_length=100)
    hemisphere = models.CharField(
        max_length=20,
        choices=[
            ('northern', 'Northern'),
            ('southern', 'Southern'),
            ('both', 'Both')
        ]
    )
    
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'meteor_showers'
        ordering = ['peak_date']
        verbose_name = 'Meteor Shower'
        verbose_name_plural = 'Meteor Showers'
    
    def __str__(self):
        return self.name


class LiveTrackingSession(models.Model):
    """
    Live tracking session data
    """
    
    session_id = models.CharField(max_length=100, unique=True, db_index=True)
    
    # Tracking Data
    objects_tracked = models.JSONField(default=list)
    filters_applied = models.JSONField(default=dict)
    
    # Settings
    playback_speed = models.FloatField(default=1.0)
    simulation_date = models.DateTimeField()
    
    # Statistics
    total_objects = models.IntegerField(default=0)
    filtered_objects = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'live_tracking_sessions'
        ordering = ['-last_active']
        verbose_name = 'Live Tracking Session'
        verbose_name_plural = 'Live Tracking Sessions'
    
    def __str__(self):
        return f"Session {self.session_id}"


class MeteorActivity(models.Model):
    """
    Real-time meteor activity metrics
    """
    
    timestamp = models.DateTimeField(db_index=True)
    
    # Activity Metrics
    meteors_per_hour = models.IntegerField()
    activity_level = models.CharField(
        max_length=20,
        choices=[
            ('quiet', 'Quiet'),
            ('normal', 'Normal'),
            ('active', 'Active'),
            ('high', 'High'),
            ('extreme', 'Extreme')
        ]
    )
    
    # Detection
    detection_stations = models.IntegerField(default=0)
    confirmed_detections = models.IntegerField(default=0)
    
    # Active Showers
    active_showers = models.JSONField(default=list)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'meteor_activity'
        ordering = ['-timestamp']
        verbose_name = 'Meteor Activity'
        verbose_name_plural = 'Meteor Activities'
    
    def __str__(self):
        return f"{self.activity_level} - {self.timestamp}"

