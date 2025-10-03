"""
Seismic Impact Calculation Services
"""
import math
from .models import SeismicImpactAnalysis, ShockwaveModel
import logging

logger = logging.getLogger(__name__)


class SeismicCalculationService:
    """Service for calculating seismic impacts of asteroid strikes"""
    
    def calculate_seismic_impact(self, threat_assessment):
        """Calculate complete seismic impact analysis"""
        
        energy_mt = threat_assessment.kinetic_energy_megatons
        
        # Convert energy to different units
        energy_joules = energy_mt * 4.184e15
        energy_ergs = energy_joules * 1e7
        
        # Calculate moment magnitude
        moment_magnitude = self._energy_to_magnitude(energy_ergs)
        richter_equivalent = moment_magnitude  # Simplified
        
        # Calculate ground motion parameters
        pga = self._calculate_pga(energy_mt)
        pgv = self._calculate_pgv(energy_mt)
        pgd = self._calculate_pgd(energy_mt)
        
        # Calculate intensity
        mmi = self._calculate_mmi(moment_magnitude)
        felt_radius = self._calculate_felt_radius(energy_mt)
        
        # Calculate damage radii
        severe_radius = threat_assessment.destruction_radius_km * 0.5
        moderate_radius = threat_assessment.destruction_radius_km * 1.0
        light_radius = threat_assessment.destruction_radius_km * 2.0
        
        # Find comparable earthquake
        comparable_eq, comparable_mag = self._find_comparable_earthquake(moment_magnitude)
        
        # Create or update analysis
        analysis, created = SeismicImpactAnalysis.objects.update_or_create(
            threat_assessment=threat_assessment,
            defaults={
                'moment_magnitude': moment_magnitude,
                'richter_scale_equivalent': richter_equivalent,
                'energy_ergs': energy_ergs,
                'energy_joules': energy_joules,
                'peak_ground_acceleration_g': pga,
                'peak_ground_velocity_mps': pgv,
                'peak_ground_displacement_m': pgd,
                'modified_mercalli_intensity': mmi,
                'felt_radius_km': felt_radius,
                'severe_damage_radius_km': severe_radius,
                'moderate_damage_radius_km': moderate_radius,
                'light_damage_radius_km': light_radius,
                'comparable_earthquake_name': comparable_eq,
                'comparable_earthquake_magnitude': comparable_mag
            }
        )
        
        # Calculate shockwave models
        self._calculate_shockwave_models(analysis, energy_mt)
        
        return analysis
    
    def _energy_to_magnitude(self, energy_ergs):
        """Convert energy to seismic magnitude"""
        # M = (2/3) * log10(E) - 2.9
        magnitude = (2/3) * math.log10(energy_ergs) - 2.9
        return round(magnitude, 2)
    
    def _calculate_pga(self, energy_mt):
        """Calculate peak ground acceleration in g"""
        # Empirical scaling
        pga = 0.1 * (energy_mt ** 0.33)
        return min(pga, 2.0)  # Cap at 2g
    
    def _calculate_pgv(self, energy_mt):
        """Calculate peak ground velocity in m/s"""
        pgv = 1.0 * (energy_mt ** 0.33)
        return pgv
    
    def _calculate_pgd(self, energy_mt):
        """Calculate peak ground displacement in meters"""
        pgd = 0.5 * (energy_mt ** 0.33)
        return pgd
    
    def _calculate_mmi(self, magnitude):
        """Calculate Modified Mercalli Intensity"""
        # Simplified correlation
        mmi = int(1.5 * magnitude - 1)
        return min(max(mmi, 1), 12)  # MMI ranges from I to XII
    
    def _calculate_felt_radius(self, energy_mt):
        """Calculate radius where impact is felt"""
        radius = 100 * (energy_mt ** 0.33)
        return radius
    
    def _find_comparable_earthquake(self, magnitude):
        """Find a historical earthquake with similar magnitude"""
        from impacts.models import Earthquake
        
        earthquake = Earthquake.objects.filter(
            magnitude__gte=magnitude - 0.5,
            magnitude__lte=magnitude + 0.5
        ).first()
        
        if earthquake:
            return earthquake.name, earthquake.magnitude
        
        return "No comparable event", None
    
    def _calculate_shockwave_models(self, analysis, energy_mt):
        """Calculate shockwave models at various distances"""
        distances = [1, 5, 10, 25, 50, 100, 200, 500]
        
        for distance in distances:
            # Atmospheric shockwave
            overpressure = self._calculate_overpressure(energy_mt, distance)
            
            if overpressure < 0.01:  # Too small to matter
                continue
            
            dynamic_pressure = 0.5 * overpressure
            arrival_time = distance / 0.34  # Speed of sound ~340 m/s
            duration = 1 + (energy_mt ** 0.33) / distance
            
            damage_level, damage_desc = self._determine_damage(overpressure)
            
            ShockwaveModel.objects.update_or_create(
                seismic_analysis=analysis,
                wave_type='atmospheric',
                distance_from_impact_km=distance,
                defaults={
                    'peak_overpressure_psi': overpressure,
                    'dynamic_pressure_psi': dynamic_pressure,
                    'arrival_time_seconds': arrival_time,
                    'duration_seconds': duration,
                    'damage_description': damage_desc,
                    'structural_damage_level': damage_level
                }
            )
    
    def _calculate_overpressure(self, energy_mt, distance_km):
        """Calculate overpressure at distance"""
        # Scaling law for overpressure
        scaled_distance = distance_km / (energy_mt ** 0.33)
        
        if scaled_distance < 0.1:
            overpressure = 100
        elif scaled_distance < 1:
            overpressure = 20 / scaled_distance
        elif scaled_distance < 10:
            overpressure = 5 / (scaled_distance ** 2)
        else:
            overpressure = 0.5 / (scaled_distance ** 3)
        
        return overpressure
    
    def _determine_damage(self, overpressure_psi):
        """Determine damage level from overpressure"""
        if overpressure_psi >= 20:
            return 'total', 'Complete destruction of all structures'
        elif overpressure_psi >= 10:
            return 'severe', 'Severe structural damage, few buildings remain standing'
        elif overpressure_psi >= 5:
            return 'moderate', 'Moderate structural damage, buildings partially collapse'
        elif overpressure_psi >= 2:
            return 'light', 'Light structural damage, window breakage'
        elif overpressure_psi >= 0.5:
            return 'cosmetic', 'Minor damage, glass breakage'
        else:
            return 'none', 'No significant damage'

