"""
Asteroid Threat Assessment Models
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from neos.models import NEO


class ThreatScenario(models.Model):
    """
    Pre-configured asteroid threat scenarios for simulation
    """
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    
    # Asteroid Properties
    diameter_km = models.FloatField(validators=[MinValueValidator(0.001)])
    mass_kg = models.FloatField(blank=True, null=True)
    velocity_kps = models.FloatField(help_text="Impact velocity in km/s")
    composition = models.CharField(max_length=50, default="rocky")
    density_kg_m3 = models.FloatField(default=2600, help_text="Density in kg/m³")
    
    # Impact Parameters
    impact_angle_degrees = models.FloatField(
        default=45,
        validators=[MinValueValidator(0), MaxValueValidator(90)]
    )
    impact_location_lat = models.FloatField(
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
        blank=True,
        null=True
    )
    impact_location_lon = models.FloatField(
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
        blank=True,
        null=True
    )
    impact_type = models.CharField(
        max_length=20,
        choices=[('land', 'Land'), ('ocean', 'Ocean')],
        default='land'
    )
    
    # Pre-calculated Results
    energy_megatons = models.FloatField(blank=True, null=True)
    crater_diameter_km = models.FloatField(blank=True, null=True)
    seismic_magnitude = models.FloatField(blank=True, null=True)
    
    # Metadata
    scenario_type = models.CharField(
        max_length=50,
        choices=[
            ('historical', 'Historical Event'),
            ('hypothetical', 'Hypothetical Scenario'),
            ('prediction', 'Predicted Event')
        ],
        default='hypothetical'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'threat_scenarios'
        ordering = ['-energy_megatons']
        verbose_name = 'Threat Scenario'
        verbose_name_plural = 'Threat Scenarios'
    
    def __str__(self):
        return f"{self.name} ({self.diameter_km}km)"


class ThreatAssessment(models.Model):
    """
    Calculated threat assessment for NEOs or scenarios
    """
    
    neo = models.OneToOneField(
        NEO,
        on_delete=models.CASCADE,
        related_name='threat_assessment',
        null=True,
        blank=True
    )
    scenario = models.ForeignKey(
        ThreatScenario,
        on_delete=models.CASCADE,
        related_name='assessments',
        null=True,
        blank=True
    )
    
    # Risk Levels
    RISK_CHOICES = [
        ('minimal', 'Minimal'),
        ('low', 'Low'),
        ('moderate', 'Moderate'),
        ('high', 'High'),
        ('critical', 'Critical')
    ]
    
    overall_risk_level = models.CharField(max_length=20, choices=RISK_CHOICES)
    impact_probability = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text="Probability between 0 and 1"
    )
    
    # Impact Calculations
    kinetic_energy_megatons = models.FloatField()
    crater_diameter_km = models.FloatField()
    destruction_radius_km = models.FloatField()
    
    # Casualty Estimates
    estimated_deaths = models.BigIntegerField(default=0)
    estimated_injuries = models.BigIntegerField(default=0)
    economic_loss_billions_usd = models.FloatField(default=0)
    
    # Environmental Impact
    seismic_magnitude = models.FloatField(blank=True, null=True)
    tsunami_risk = models.CharField(
        max_length=20,
        choices=[
            ('none', 'None'),
            ('low', 'Low'),
            ('moderate', 'Moderate'),
            ('high', 'High'),
            ('extreme', 'Extreme')
        ],
        default='none'
    )
    
    # Atmospheric Effects
    dust_cloud_duration_days = models.IntegerField(blank=True, null=True)
    global_temperature_change_c = models.FloatField(blank=True, null=True)
    
    # System fields
    calculated_at = models.DateTimeField(auto_now=True)
    calculation_version = models.CharField(max_length=20, default='1.0')
    
    class Meta:
        db_table = 'threat_assessments'
        ordering = ['-overall_risk_level', '-kinetic_energy_megatons']
        verbose_name = 'Threat Assessment'
        verbose_name_plural = 'Threat Assessments'
    
    def __str__(self):
        obj_name = self.neo.name if self.neo else self.scenario.name
        return f"Threat Assessment: {obj_name} - {self.overall_risk_level}"


class DestructionZone(models.Model):
    """
    Destruction zone calculations for threat assessments
    """
    
    assessment = models.ForeignKey(
        ThreatAssessment,
        on_delete=models.CASCADE,
        related_name='destruction_zones'
    )
    
    zone_type = models.CharField(
        max_length=50,
        choices=[
            ('total', 'Total Destruction'),
            ('severe', 'Severe Destruction'),
            ('moderate', 'Moderate Destruction'),
            ('light', 'Light Damage'),
            ('glass_breakage', 'Glass Breakage')
        ]
    )
    
    radius_km = models.FloatField()
    area_km2 = models.FloatField()
    overpressure_psi = models.FloatField(help_text="Peak overpressure in PSI")
    fatality_rate = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text="Expected fatality rate in this zone"
    )
    
    estimated_casualties = models.BigIntegerField(default=0)
    estimated_injuries = models.BigIntegerField(default=0)
    
    class Meta:
        db_table = 'destruction_zones'
        ordering = ['-radius_km']
        unique_together = [['assessment', 'zone_type']]
        verbose_name = 'Destruction Zone'
        verbose_name_plural = 'Destruction Zones'
    
    def __str__(self):
        return f"{self.zone_type} - {self.radius_km}km radius"

