"""
Historical Impact Events Models
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class ImpactEvent(models.Model):
    """
    Historical meteor/asteroid impact events
    """
    
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    
    # Date Information
    date = models.DateField(null=True, blank=True)
    date_description = models.CharField(max_length=200, help_text="e.g., '65 million years ago'")
    years_ago = models.BigIntegerField(help_text="Approximate years before present")
    
    # Location
    location_name = models.CharField(max_length=200)
    latitude = models.FloatField(
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
        null=True,
        blank=True
    )
    longitude = models.FloatField(
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
        null=True,
        blank=True
    )
    country = models.CharField(max_length=100, blank=True)
    
    # Impact Characteristics
    estimated_diameter_km = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text="Estimated impactor diameter in km"
    )
    crater_diameter_km = models.FloatField(
        validators=[MinValueValidator(0)],
        null=True,
        blank=True
    )
    energy_megatons = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text="Estimated energy in megatons TNT"
    )
    
    # Effects
    casualties = models.BigIntegerField(default=0)
    injuries = models.BigIntegerField(default=0)
    extinction_event = models.BooleanField(default=False)
    global_effects = models.TextField(blank=True)
    local_effects = models.TextField(blank=True)
    
    # Evidence
    crater_preserved = models.BooleanField(default=True)
    evidence_type = models.CharField(
        max_length=100,
        choices=[
            ('crater', 'Impact Crater'),
            ('eyewitness', 'Eyewitness Accounts'),
            ('geological', 'Geological Evidence'),
            ('meteorites', 'Meteorite Fragments'),
            ('combined', 'Multiple Evidence Types')
        ],
        default='crater'
    )
    
    # Reference Data
    discovery_year = models.IntegerField(null=True, blank=True)
    references = models.JSONField(default=list, blank=True)
    wikipedia_url = models.URLField(blank=True)
    
    # System fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'impact_events'
        ordering = ['-years_ago']
        verbose_name = 'Impact Event'
        verbose_name_plural = 'Impact Events'
    
    def __str__(self):
        return f"{self.name} ({self.date_description})"
    
    @property
    def severity_category(self):
        """Categorize impact by energy"""
        if self.energy_megatons > 1000000:
            return "Extinction Level"
        elif self.energy_megatons > 10000:
            return "Global Catastrophe"
        elif self.energy_megatons > 100:
            return "Regional Disaster"
        elif self.energy_megatons > 1:
            return "Local Event"
        else:
            return "Minor Event"


class Earthquake(models.Model):
    """
    Historical earthquake data for comparison with impact events
    """
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Date and Location
    date = models.DateField()
    location = models.CharField(max_length=200)
    latitude = models.FloatField(
        validators=[MinValueValidator(-90), MaxValueValidator(90)]
    )
    longitude = models.FloatField(
        validators=[MinValueValidator(-180), MaxValueValidator(180)]
    )
    country = models.CharField(max_length=100)
    
    # Magnitude
    magnitude = models.FloatField(help_text="Moment magnitude (Mw)")
    magnitude_type = models.CharField(max_length=20, default="Mw")
    depth_km = models.FloatField(help_text="Focal depth in km")
    
    # Energy
    energy_joules = models.FloatField(null=True, blank=True)
    energy_megatons = models.FloatField(null=True, blank=True)
    
    # Impact
    casualties = models.BigIntegerField(default=0)
    injuries = models.BigIntegerField(default=0)
    displaced = models.BigIntegerField(default=0)
    economic_loss_billions_usd = models.FloatField(default=0)
    
    # Additional Info
    tsunami_generated = models.BooleanField(default=False)
    max_intensity = models.CharField(max_length=10, blank=True, help_text="Modified Mercalli Intensity")
    
    # System fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'earthquakes'
        ordering = ['-magnitude', '-date']
        verbose_name = 'Earthquake'
        verbose_name_plural = 'Earthquakes'
    
    def __str__(self):
        return f"{self.name} ({self.date.year}) - M{self.magnitude}"
    
    def save(self, *args, **kwargs):
        """Calculate energy when saving"""
        if not self.energy_joules:
            # Energy-magnitude relationship
            # log10(E) = 1.5 * M + 4.8 (E in Joules)
            import math
            self.energy_joules = 10 ** (1.5 * self.magnitude + 4.8)
            self.energy_megatons = self.energy_joules / 4.184e15
        
        super().save(*args, **kwargs)

