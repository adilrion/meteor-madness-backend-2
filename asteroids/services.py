"""
Asteroid Threat Calculation Services
"""
import math
from .models import ThreatAssessment, DestructionZone
import logging

logger = logging.getLogger(__name__)


class ThreatCalculationService:
    """Service for calculating asteroid threat assessments"""
    
    def __init__(self):
        self.GRAVITATIONAL_CONSTANT = 6.67430e-11  # m³/kg/s²
        self.TNT_EQUIVALENT_JOULES = 4.184e15  # 1 megaton TNT in joules
    
    def calculate_scenario_threat(self, scenario):
        """Calculate complete threat assessment for a scenario"""
        
        # Calculate mass if not provided
        if not scenario.mass_kg:
            volume_m3 = (4/3) * math.pi * ((scenario.diameter_km * 1000 / 2) ** 3)
            mass_kg = volume_m3 * scenario.density_kg_m3
        else:
            mass_kg = scenario.mass_kg
        
        # Calculate kinetic energy
        velocity_mps = scenario.velocity_kps * 1000
        kinetic_energy_joules = 0.5 * mass_kg * (velocity_mps ** 2)
        energy_megatons = kinetic_energy_joules / self.TNT_EQUIVALENT_JOULES
        
        # Calculate crater diameter (Holsapple-Schmidt scaling)
        crater_diameter_km = self._calculate_crater_diameter(
            mass_kg,
            velocity_mps,
            scenario.density_kg_m3,
            scenario.impact_angle_degrees
        )
        
        # Calculate seismic magnitude
        seismic_magnitude = self._energy_to_magnitude(energy_megatons)
        
        # Determine risk level
        risk_level = self._determine_risk_level(
            energy_megatons,
            scenario.diameter_km
        )
        
        # Calculate tsunami risk
        tsunami_risk = self._calculate_tsunami_risk(
            energy_megatons,
            scenario.diameter_km,
            scenario.impact_type
        )
        
        # Calculate destruction radius
        destruction_radius_km = self._calculate_destruction_radius(energy_megatons)
        
        # Estimate casualties (simplified)
        estimated_deaths, estimated_injuries = self._estimate_casualties(
            destruction_radius_km,
            scenario.impact_location_lat,
            scenario.impact_location_lon
        )
        
        # Economic loss estimate
        economic_loss = self._estimate_economic_loss(
            destruction_radius_km,
            estimated_deaths
        )
        
        # Create or update threat assessment
        assessment, created = ThreatAssessment.objects.update_or_create(
            scenario=scenario,
            defaults={
                'overall_risk_level': risk_level,
                'impact_probability': 0.01,  # Default low probability
                'kinetic_energy_megatons': energy_megatons,
                'crater_diameter_km': crater_diameter_km,
                'destruction_radius_km': destruction_radius_km,
                'estimated_deaths': estimated_deaths,
                'estimated_injuries': estimated_injuries,
                'economic_loss_billions_usd': economic_loss,
                'seismic_magnitude': seismic_magnitude,
                'tsunami_risk': tsunami_risk,
                'dust_cloud_duration_days': self._estimate_dust_duration(energy_megatons),
                'global_temperature_change_c': self._estimate_temperature_change(energy_megatons),
            }
        )
        
        # Calculate destruction zones
        self._calculate_destruction_zones(assessment, energy_megatons)
        
        return assessment
    
    def _calculate_crater_diameter(self, mass_kg, velocity_mps, density, angle_deg):
        """Calculate crater diameter using scaling laws"""
        # Simplified Holsapple-Schmidt scaling
        energy_joules = 0.5 * mass_kg * (velocity_mps ** 2)
        
        # Convert to kilotons TNT equivalent
        energy_kt = energy_joules / (4.184e12)
        
        # Scaling law for crater diameter
        crater_diameter_m = 1.8 * (energy_kt ** 0.333) * math.sin(math.radians(angle_deg))
        
        return crater_diameter_m / 1000  # Convert to km
    
    def _energy_to_magnitude(self, energy_megatons):
        """Convert impact energy to seismic magnitude"""
        # Convert to ergs (1 MT = 4.184e22 ergs)
        energy_ergs = energy_megatons * 4.184e22
        
        # Seismic magnitude relationship
        magnitude = (2/3) * math.log10(energy_ergs) - 2.9
        
        return round(magnitude, 2)
    
    def _determine_risk_level(self, energy_megatons, diameter_km):
        """Determine overall risk level"""
        if energy_megatons > 100000 or diameter_km > 1:
            return 'critical'
        elif energy_megatons > 10000 or diameter_km > 0.5:
            return 'high'
        elif energy_megatons > 1000 or diameter_km > 0.2:
            return 'moderate'
        elif energy_megatons > 10 or diameter_km > 0.05:
            return 'low'
        else:
            return 'minimal'
    
    def _calculate_tsunami_risk(self, energy_megatons, diameter_km, impact_type):
        """Calculate tsunami risk for ocean impacts"""
        if impact_type != 'ocean':
            return 'none'
        
        if energy_megatons > 10000 or diameter_km > 1:
            return 'extreme'
        elif energy_megatons > 1000 or diameter_km > 0.5:
            return 'high'
        elif energy_megatons > 100 or diameter_km > 0.2:
            return 'moderate'
        elif energy_megatons > 10 or diameter_km > 0.05:
            return 'low'
        else:
            return 'none'
    
    def _calculate_destruction_radius(self, energy_megatons):
        """Calculate main destruction radius"""
        # Simplified scaling
        radius_km = 2.2 * (energy_megatons ** 0.33)
        return radius_km
    
    def _estimate_casualties(self, radius_km, lat, lon):
        """Estimate casualties based on destruction radius"""
        # Simplified population density model
        # Average: 50 people per km²
        area_km2 = math.pi * (radius_km ** 2)
        
        avg_population_density = 50  # people per km²
        affected_population = int(area_km2 * avg_population_density)
        
        # Assume 30% fatality rate, 50% injury rate
        deaths = int(affected_population * 0.3)
        injuries = int(affected_population * 0.5)
        
        return deaths, injuries
    
    def _estimate_economic_loss(self, radius_km, deaths):
        """Estimate economic loss in billions USD"""
        area_km2 = math.pi * (radius_km ** 2)
        
        # $1M per km² + $10M per death
        infrastructure_loss = area_km2 * 1
        human_capital_loss = deaths * 10
        
        total_loss = (infrastructure_loss + human_capital_loss) / 1000  # Convert to billions
        
        return round(total_loss, 2)
    
    def _estimate_dust_duration(self, energy_megatons):
        """Estimate dust cloud duration in days"""
        if energy_megatons > 100000:
            return 365 * 10  # 10 years
        elif energy_megatons > 10000:
            return 365 * 2  # 2 years
        elif energy_megatons > 1000:
            return 180  # 6 months
        elif energy_megatons > 100:
            return 30  # 1 month
        else:
            return 7  # 1 week
    
    def _estimate_temperature_change(self, energy_megatons):
        """Estimate global temperature change in Celsius"""
        if energy_megatons > 100000:
            return -15.0
        elif energy_megatons > 10000:
            return -5.0
        elif energy_megatons > 1000:
            return -2.0
        elif energy_megatons > 100:
            return -0.5
        else:
            return -0.1
    
    def _calculate_destruction_zones(self, assessment, energy_megatons):
        """Calculate multiple destruction zones"""
        zones = [
            {
                'zone_type': 'total',
                'overpressure_psi': 20,
                'fatality_rate': 0.95,
                'radius_multiplier': 0.5
            },
            {
                'zone_type': 'severe',
                'overpressure_psi': 10,
                'fatality_rate': 0.50,
                'radius_multiplier': 0.75
            },
            {
                'zone_type': 'moderate',
                'overpressure_psi': 5,
                'fatality_rate': 0.15,
                'radius_multiplier': 1.0
            },
            {
                'zone_type': 'light',
                'overpressure_psi': 2,
                'fatality_rate': 0.02,
                'radius_multiplier': 1.5
            },
            {
                'zone_type': 'glass_breakage',
                'overpressure_psi': 0.5,
                'fatality_rate': 0.001,
                'radius_multiplier': 2.5
            }
        ]
        
        base_radius = assessment.destruction_radius_km
        
        for zone_data in zones:
            radius = base_radius * zone_data['radius_multiplier']
            area = math.pi * (radius ** 2)
            
            # Simplified casualty estimation
            population = int(area * 50)  # 50 people per km²
            casualties = int(population * zone_data['fatality_rate'])
            injuries = int(population * zone_data['fatality_rate'] * 2)
            
            DestructionZone.objects.update_or_create(
                assessment=assessment,
                zone_type=zone_data['zone_type'],
                defaults={
                    'radius_km': radius,
                    'area_km2': area,
                    'overpressure_psi': zone_data['overpressure_psi'],
                    'fatality_rate': zone_data['fatality_rate'],
                    'estimated_casualties': casualties,
                    'estimated_injuries': injuries
                }
            )

