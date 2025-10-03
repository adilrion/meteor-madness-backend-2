"""
NEO Models - Database models for Near-Earth Objects
"""
from django.db import models
from django.utils import timezone


class NEO(models.Model):
    """
    Near-Earth Object Model
    Stores data from NASA's NEO Web Service
    """
    
    # NASA Identifiers
    neo_reference_id = models.CharField(max_length=20, unique=True, db_index=True)
    name = models.CharField(max_length=200)
    designation = models.CharField(max_length=100, blank=True, null=True)
    
    # Classification
    is_potentially_hazardous_asteroid = models.BooleanField(default=False, db_index=True)
    is_sentry_object = models.BooleanField(default=False)
    
    # Physical Characteristics
    absolute_magnitude_h = models.FloatField(help_text="Absolute magnitude")
    estimated_diameter_min_km = models.FloatField(null=True, blank=True)
    estimated_diameter_max_km = models.FloatField(null=True, blank=True)
    estimated_diameter_min_m = models.FloatField(null=True, blank=True)
    estimated_diameter_max_m = models.FloatField(null=True, blank=True)
    
    # Orbital Data
    orbital_data = models.JSONField(default=dict, blank=True)
    
    # Additional Information
    nasa_jpl_url = models.URLField(max_length=500, blank=True, null=True)
    orbital_period_days = models.FloatField(null=True, blank=True)
    perihelion_distance = models.FloatField(null=True, blank=True, help_text="AU")
    aphelion_distance = models.FloatField(null=True, blank=True, help_text="AU")
    semi_major_axis = models.FloatField(null=True, blank=True, help_text="AU")
    eccentricity = models.FloatField(null=True, blank=True)
    inclination = models.FloatField(null=True, blank=True, help_text="degrees")
    
    # Metadata
    first_observation_date = models.DateField(null=True, blank=True)
    last_observation_date = models.DateField(null=True, blank=True)
    observations_used = models.IntegerField(null=True, blank=True)
    
    # System fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_synced_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'neos'
        ordering = ['-absolute_magnitude_h']
        indexes = [
            models.Index(fields=['neo_reference_id']),
            models.Index(fields=['is_potentially_hazardous_asteroid']),
            models.Index(fields=['estimated_diameter_max_km']),
        ]
        verbose_name = 'Near-Earth Object'
        verbose_name_plural = 'Near-Earth Objects'
    
    def __str__(self):
        return f"{self.name} ({self.neo_reference_id})"
    
    @property
    def estimated_diameter_avg_km(self):
        """Calculate average estimated diameter in kilometers"""
        if self.estimated_diameter_min_km and self.estimated_diameter_max_km:
            return (self.estimated_diameter_min_km + self.estimated_diameter_max_km) / 2
        return None
    
    @property
    def size_category(self):
        """Categorize NEO by size"""
        avg_diameter = self.estimated_diameter_avg_km
        if not avg_diameter:
            return "Unknown"
        
        if avg_diameter < 0.1:
            return "Small"
        elif avg_diameter < 0.5:
            return "Medium"
        elif avg_diameter < 1.0:
            return "Large"
        else:
            return "Very Large"


class CloseApproach(models.Model):
    """
    Close Approach Data for NEOs
    Stores predicted and historical close approaches to Earth
    """
    
    neo = models.ForeignKey(NEO, on_delete=models.CASCADE, related_name='close_approaches')
    
    # Approach Details
    close_approach_date = models.DateField(db_index=True)
    close_approach_date_full = models.DateTimeField()
    epoch_date_close_approach = models.BigIntegerField()
    
    # Distance Data
    relative_velocity_kps = models.FloatField(help_text="km/s")
    relative_velocity_kmph = models.FloatField(help_text="km/h")
    relative_velocity_mph = models.FloatField(help_text="mph")
    
    miss_distance_astronomical = models.FloatField(help_text="AU")
    miss_distance_lunar = models.FloatField(help_text="Lunar Distance")
    miss_distance_kilometers = models.FloatField(help_text="km")
    miss_distance_miles = models.FloatField(help_text="miles")
    
    # Orbiting Body
    orbiting_body = models.CharField(max_length=50, default="Earth")
    
    # System fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'close_approaches'
        ordering = ['close_approach_date']
        unique_together = [['neo', 'close_approach_date_full']]
        indexes = [
            models.Index(fields=['close_approach_date']),
            models.Index(fields=['miss_distance_lunar']),
        ]
        verbose_name = 'Close Approach'
        verbose_name_plural = 'Close Approaches'
    
    def __str__(self):
        return f"{self.neo.name} - {self.close_approach_date}"
    
    @property
    def is_close(self):
        """Check if approach is within 10 lunar distances"""
        return self.miss_distance_lunar < 10


class NEOStatistics(models.Model):
    """
    Aggregated NEO Statistics
    Cached statistics for dashboard display
    """
    
    date = models.DateField(unique=True, db_index=True)
    
    # Counts
    total_neos = models.IntegerField(default=0)
    total_phas = models.IntegerField(default=0, help_text="Potentially Hazardous Asteroids")
    
    # Size Distribution
    small_neos_count = models.IntegerField(default=0, help_text="< 0.1 km")
    medium_neos_count = models.IntegerField(default=0, help_text="0.1 - 0.5 km")
    large_neos_count = models.IntegerField(default=0, help_text="0.5 - 1.0 km")
    very_large_neos_count = models.IntegerField(default=0, help_text="> 1.0 km")
    
    # Close Approaches
    close_approaches_next_7_days = models.IntegerField(default=0)
    close_approaches_next_30_days = models.IntegerField(default=0)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'neo_statistics'
        ordering = ['-date']
        verbose_name = 'NEO Statistics'
        verbose_name_plural = 'NEO Statistics'
    
    def __str__(self):
        return f"NEO Statistics - {self.date}"

