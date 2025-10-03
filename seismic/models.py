"""
Seismic Impact Analysis Models
"""
from django.db import models
from asteroids.models import ThreatAssessment


class SeismicImpactAnalysis(models.Model):
    """
    Seismic analysis for asteroid impacts
    """
    
    threat_assessment = models.OneToOneField(
        ThreatAssessment,
        on_delete=models.CASCADE,
        related_name='seismic_analysis'
    )
    
    # Seismic Parameters
    moment_magnitude = models.FloatField(help_text="Moment magnitude (Mw)")
    richter_scale_equivalent = models.FloatField()
    energy_ergs = models.FloatField()
    energy_joules = models.FloatField()
    
    # Wave Propagation
    p_wave_velocity_kmps = models.FloatField(default=6.0)
    s_wave_velocity_kmps = models.FloatField(default=3.5)
    surface_wave_velocity_kmps = models.FloatField(default=3.0)
    
    # Ground Motion
    peak_ground_acceleration_g = models.FloatField(help_text="Peak ground acceleration in g")
    peak_ground_velocity_mps = models.FloatField(help_text="Peak ground velocity in m/s")
    peak_ground_displacement_m = models.FloatField(help_text="Peak ground displacement in meters")
    
    # Intensity
    modified_mercalli_intensity = models.IntegerField()
    felt_radius_km = models.FloatField()
    
    # Damage Zones
    severe_damage_radius_km = models.FloatField()
    moderate_damage_radius_km = models.FloatField()
    light_damage_radius_km = models.FloatField()
    
    # Comparison Data
    comparable_earthquake_name = models.CharField(max_length=200, blank=True)
    comparable_earthquake_magnitude = models.FloatField(blank=True, null=True)
    
    # System fields
    calculated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'seismic_impact_analyses'
        verbose_name = 'Seismic Impact Analysis'
        verbose_name_plural = 'Seismic Impact Analyses'
    
    def __str__(self):
        return f"Seismic Analysis - M{self.moment_magnitude}"


class ShockwaveModel(models.Model):
    """
    Atmospheric and ground shockwave modeling
    """
    
    seismic_analysis = models.ForeignKey(
        SeismicImpactAnalysis,
        on_delete=models.CASCADE,
        related_name='shockwave_models'
    )
    
    wave_type = models.CharField(
        max_length=20,
        choices=[
            ('atmospheric', 'Atmospheric Shockwave'),
            ('ground', 'Ground Shockwave'),
            ('seismic', 'Seismic Wave')
        ]
    )
    
    # Wave Parameters
    peak_overpressure_psi = models.FloatField()
    dynamic_pressure_psi = models.FloatField()
    arrival_time_seconds = models.FloatField()
    duration_seconds = models.FloatField()
    
    # Effects at Distance
    distance_from_impact_km = models.FloatField()
    
    # Damage Description
    damage_description = models.TextField()
    structural_damage_level = models.CharField(
        max_length=20,
        choices=[
            ('none', 'No Damage'),
            ('cosmetic', 'Cosmetic Damage'),
            ('light', 'Light Damage'),
            ('moderate', 'Moderate Damage'),
            ('severe', 'Severe Damage'),
            ('total', 'Total Destruction')
        ]
    )
    
    class Meta:
        db_table = 'shockwave_models'
        ordering = ['distance_from_impact_km']
        verbose_name = 'Shockwave Model'
        verbose_name_plural = 'Shockwave Models'
    
    def __str__(self):
        return f"{self.wave_type} at {self.distance_from_impact_km}km"

