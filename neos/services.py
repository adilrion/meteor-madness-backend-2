"""
NEO Data Services - Integration with NASA APIs
"""
import requests
from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta
import logging

from .models import NEO, CloseApproach

logger = logging.getLogger(__name__)


class NEODataService:
    """Service for fetching and processing NEO data from NASA"""
    
    def __init__(self):
        self.api_key = settings.NASA_API_KEY
        self.neo_api_url = settings.NASA_NEO_API_URL
        self.sbdb_api_url = settings.NASA_SBDB_API_URL
    
    def fetch_neo_feed(self, start_date=None, end_date=None):
        """
        Fetch NEO feed data for a date range
        Maximum range is 7 days
        """
        if not start_date:
            start_date = timezone.now().date()
        
        if not end_date:
            end_date = start_date + timedelta(days=7)
        
        url = f"{self.neo_api_url}/feed"
        params = {
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'api_key': self.api_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching NEO feed: {e}")
            return None
    
    def fetch_neo_by_id(self, neo_id):
        """Fetch detailed NEO data by ID"""
        url = f"{self.neo_api_url}/neo/{neo_id}"
        params = {'api_key': self.api_key}
        
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching NEO {neo_id}: {e}")
            return None
    
    def sync_neo_data(self):
        """Sync NEO data from NASA API to database"""
        start_date = timezone.now().date()
        end_date = start_date + timedelta(days=7)
        
        data = self.fetch_neo_feed(start_date, end_date)
        
        if not data:
            return {'success': False, 'message': 'Failed to fetch data'}
        
        neos_created = 0
        neos_updated = 0
        approaches_created = 0
        
        near_earth_objects = data.get('near_earth_objects', {})
        
        for date_str, neos_list in near_earth_objects.items():
            for neo_data in neos_list:
                neo, created = self._sync_neo(neo_data)
                
                if created:
                    neos_created += 1
                else:
                    neos_updated += 1
                
                # Sync close approach data
                for approach_data in neo_data.get('close_approach_data', []):
                    if self._sync_close_approach(neo, approach_data):
                        approaches_created += 1
        
        return {
            'success': True,
            'neos_created': neos_created,
            'neos_updated': neos_updated,
            'approaches_created': approaches_created
        }
    
    def _sync_neo(self, neo_data):
        """Sync individual NEO to database"""
        neo_id = neo_data['neo_reference_id']
        
        # Extract diameter data
        estimated_diameter = neo_data.get('estimated_diameter', {})
        km_data = estimated_diameter.get('kilometers', {})
        m_data = estimated_diameter.get('meters', {})
        
        # Extract orbital data if available
        orbital_data = neo_data.get('orbital_data', {})
        
        neo, created = NEO.objects.update_or_create(
            neo_reference_id=neo_id,
            defaults={
                'name': neo_data['name'],
                'designation': neo_data.get('designation', ''),
                'is_potentially_hazardous_asteroid': neo_data['is_potentially_hazardous_asteroid'],
                'is_sentry_object': neo_data.get('is_sentry_object', False),
                'absolute_magnitude_h': neo_data['absolute_magnitude_h'],
                'estimated_diameter_min_km': km_data.get('estimated_diameter_min'),
                'estimated_diameter_max_km': km_data.get('estimated_diameter_max'),
                'estimated_diameter_min_m': m_data.get('estimated_diameter_min'),
                'estimated_diameter_max_m': m_data.get('estimated_diameter_max'),
                'nasa_jpl_url': neo_data.get('nasa_jpl_url', ''),
                'orbital_data': orbital_data,
                'orbital_period_days': self._safe_float(orbital_data.get('orbital_period')),
                'perihelion_distance': self._safe_float(orbital_data.get('perihelion_distance')),
                'aphelion_distance': self._safe_float(orbital_data.get('aphelion_distance')),
                'semi_major_axis': self._safe_float(orbital_data.get('semi_major_axis')),
                'eccentricity': self._safe_float(orbital_data.get('eccentricity')),
                'inclination': self._safe_float(orbital_data.get('inclination')),
                'first_observation_date': self._parse_date(orbital_data.get('first_observation_date')),
                'last_observation_date': self._parse_date(orbital_data.get('last_observation_date')),
                'observations_used': self._safe_int(orbital_data.get('observations_used')),
                'last_synced_at': timezone.now()
            }
        )
        
        return neo, created
    
    def _sync_close_approach(self, neo, approach_data):
        """Sync close approach data"""
        close_approach_date = datetime.strptime(
            approach_data['close_approach_date'],
            '%Y-%m-%d'
        ).date()
        
        close_approach_datetime = datetime.fromisoformat(
            approach_data['close_approach_date_full'].replace('Z', '+00:00')
        )
        
        relative_velocity = approach_data['relative_velocity']
        miss_distance = approach_data['miss_distance']
        
        _, created = CloseApproach.objects.update_or_create(
            neo=neo,
            close_approach_date_full=close_approach_datetime,
            defaults={
                'close_approach_date': close_approach_date,
                'epoch_date_close_approach': approach_data['epoch_date_close_approach'],
                'relative_velocity_kps': float(relative_velocity['kilometers_per_second']),
                'relative_velocity_kmph': float(relative_velocity['kilometers_per_hour']),
                'relative_velocity_mph': float(relative_velocity['miles_per_hour']),
                'miss_distance_astronomical': float(miss_distance['astronomical']),
                'miss_distance_lunar': float(miss_distance['lunar']),
                'miss_distance_kilometers': float(miss_distance['kilometers']),
                'miss_distance_miles': float(miss_distance['miles']),
                'orbiting_body': approach_data['orbiting_body']
            }
        )
        
        return created
    
    def _safe_float(self, value):
        """Safely convert to float"""
        try:
            return float(value) if value else None
        except (ValueError, TypeError):
            return None
    
    def _safe_int(self, value):
        """Safely convert to int"""
        try:
            return int(value) if value else None
        except (ValueError, TypeError):
            return None
    
    def _parse_date(self, date_str):
        """Parse date string"""
        if not date_str:
            return None
        try:
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return None

