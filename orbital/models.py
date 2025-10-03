"""
Orbital Mechanics Models
"""
from django.db import models
from neos.models import NEO


class OrbitalElements(models.Model):
    """
    Detailed Keplerian orbital elements
    """
    
    neo = models.OneToOneField(NEO, on_delete=models.CASCADE, related_name='orbital_elements')
    
    # Keplerian Elements
    semi_major_axis_au = models.FloatField(help_text="Semi-major axis in AU")
    eccentricity = models.FloatField()
    inclination_deg = models.FloatField(help_text="Inclination in degrees")
    longitude_ascending_node_deg = models.FloatField(help_text="Longitude of ascending node")
    argument_perihelion_deg = models.FloatField(help_text="Argument of perihelion")
    mean_anomaly_deg = models.FloatField(help_text="Mean anomaly at epoch")
    epoch_jd = models.FloatField(help_text="Epoch in Julian Date")
    
    # Derived Parameters
    orbital_period_days = models.FloatField()
    perihelion_distance_au = models.FloatField()
    aphelion_distance_au = models.FloatField()
    mean_motion_deg_per_day = models.FloatField()
    
    # MOID (Minimum Orbit Intersection Distance)
    moid_au = models.FloatField(blank=True, null=True, help_text="MOID with Earth")
    moid_jupiter_au = models.FloatField(blank=True, null=True)
    
    # Tisserand Parameter
    tisserand_parameter = models.FloatField(blank=True, null=True)
    
    # Orbital Class
    orbit_class = models.CharField(
        max_length=50,
        choices=[
            ('atira', 'Atira (inside Earth)'),
            ('aten', 'Aten'),
            ('apollo', 'Apollo'),
            ('amor', 'Amor'),
            ('main_belt', 'Main Belt'),
            ('jupiter_trojan', 'Jupiter Trojan')
        ],
        blank=True
    )
    
    calculated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'orbital_elements'
        verbose_name = 'Orbital Elements'
        verbose_name_plural = 'Orbital Elements'
    
    def __str__(self):
        return f"Orbital Elements: {self.neo.name}"


class TrajectoryPoint(models.Model):
    """
    Calculated trajectory points for visualization
    """
    
    neo = models.ForeignKey(NEO, on_delete=models.CASCADE, related_name='trajectory_points')
    
    # Julian Date
    julian_date = models.FloatField(db_index=True)
    
    # 3D Position (Heliocentric)
    position_x_au = models.FloatField()
    position_y_au = models.FloatField()
    position_z_au = models.FloatField()
    
    # 3D Velocity
    velocity_x_au_per_day = models.FloatField()
    velocity_y_au_per_day = models.FloatField()
    velocity_z_au_per_day = models.FloatField()
    
    # Distance from Earth
    earth_distance_au = models.FloatField()
    
    calculated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'trajectory_points'
        ordering = ['julian_date']
        indexes = [
            models.Index(fields=['neo', 'julian_date']),
        ]
        verbose_name = 'Trajectory Point'
        verbose_name_plural = 'Trajectory Points'
    
    def __str__(self):
        return f"{self.neo.name} @ JD {self.julian_date}"

