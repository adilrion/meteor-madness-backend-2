"""
Orbital Mechanics Services
"""
import math
import numpy as np
from .models import OrbitalElements, TrajectoryPoint
import logging

logger = logging.getLogger(__name__)


class OrbitalMechanicsService:
    """Service for orbital mechanics calculations"""
    
    def __init__(self):
        self.AU = 1.496e11  # meters
        self.G = 6.67430e-11  # gravitational constant
        self.M_SUN = 1.989e30  # kg
        self.EARTH_ORBIT_RADIUS = 1.0  # AU
    
    def calculate_orbital_elements(self, neo):
        """Calculate detailed orbital elements"""
        
        # Get basic orbital data
        a = neo.semi_major_axis or 1.0
        e = neo.eccentricity or 0.0
        i = neo.inclination or 0.0
        
        # Calculate derived parameters
        period_days = self._calculate_period(a)
        perihelion = a * (1 - e)
        aphelion = a * (1 + e)
        mean_motion = 360.0 / period_days if period_days > 0 else 0
        
        # Calculate MOID (simplified)
        moid = self._calculate_moid(a, e)
        
        # Determine orbit class
        orbit_class = self._classify_orbit(a, e, perihelion, aphelion)
        
        # Create or update orbital elements
        elements, created = OrbitalElements.objects.update_or_create(
            neo=neo,
            defaults={
                'semi_major_axis_au': a,
                'eccentricity': e,
                'inclination_deg': i,
                'longitude_ascending_node_deg': 0,  # Placeholder
                'argument_perihelion_deg': 0,  # Placeholder
                'mean_anomaly_deg': 0,  # Placeholder
                'epoch_jd': 2459000.5,  # Placeholder epoch
                'orbital_period_days': period_days,
                'perihelion_distance_au': perihelion,
                'aphelion_distance_au': aphelion,
                'mean_motion_deg_per_day': mean_motion,
                'moid_au': moid,
                'orbit_class': orbit_class
            }
        )
        
        return elements
    
    def calculate_trajectory(self, neo, num_points=100):
        """Calculate trajectory points for visualization"""
        
        elements = self.calculate_orbital_elements(neo)
        
        # Clear old trajectory points
        TrajectoryPoint.objects.filter(neo=neo).delete()
        
        # Calculate points along orbit
        trajectory_points = []
        
        for i in range(num_points):
            # Mean anomaly from 0 to 360 degrees
            mean_anomaly = (i / num_points) * 360
            
            # Calculate position (simplified 2D circular orbit)
            theta = math.radians(mean_anomaly)
            r = elements.semi_major_axis_au * (1 - elements.eccentricity ** 2) / \
                (1 + elements.eccentricity * math.cos(theta))
            
            x = r * math.cos(theta)
            y = r * math.sin(theta)
            z = 0  # Simplified - ignore inclination
            
            # Simplified velocity
            v_mag = math.sqrt(self.G * self.M_SUN / (r * self.AU))
            v_x = -v_mag * math.sin(theta) / self.AU * 86400  # AU/day
            v_y = v_mag * math.cos(theta) / self.AU * 86400
            v_z = 0
            
            # Earth distance (simplified)
            earth_dist = math.sqrt(x**2 + y**2 + z**2)
            
            # Julian date (simplified)
            jd = elements.epoch_jd + (i / num_points) * elements.orbital_period_days
            
            point = TrajectoryPoint(
                neo=neo,
                julian_date=jd,
                position_x_au=x,
                position_y_au=y,
                position_z_au=z,
                velocity_x_au_per_day=v_x,
                velocity_y_au_per_day=v_y,
                velocity_z_au_per_day=v_z,
                earth_distance_au=earth_dist
            )
            
            trajectory_points.append(point)
        
        # Bulk create
        TrajectoryPoint.objects.bulk_create(trajectory_points)
        
        return len(trajectory_points)
    
    def _calculate_period(self, semi_major_axis_au):
        """Calculate orbital period using Kepler's third law"""
        # P² = a³ (when a is in AU and P is in years)
        period_years = semi_major_axis_au ** 1.5
        period_days = period_years * 365.25
        return period_days
    
    def _calculate_moid(self, a, e):
        """Calculate Minimum Orbit Intersection Distance (simplified)"""
        perihelion = a * (1 - e)
        aphelion = a * (1 + e)
        
        # Simplified MOID calculation
        if perihelion > self.EARTH_ORBIT_RADIUS:
            moid = perihelion - self.EARTH_ORBIT_RADIUS
        elif aphelion < self.EARTH_ORBIT_RADIUS:
            moid = self.EARTH_ORBIT_RADIUS - aphelion
        else:
            moid = 0.0
        
        return abs(moid)
    
    def _classify_orbit(self, a, e, q, Q):
        """Classify orbit type"""
        # q = perihelion, Q = aphelion
        
        if Q < 1.0:
            return 'atira'
        elif a < 1.0 and Q >= 1.0:
            return 'aten'
        elif a >= 1.0 and q < 1.017 and q >= 0.983:
            return 'apollo'
        elif a >= 1.0 and q > 1.017 and q < 1.3:
            return 'amor'
        elif a > 2.0 and a < 3.2:
            return 'main_belt'
        else:
            return 'other'

