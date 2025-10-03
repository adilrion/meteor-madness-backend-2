"""
Celery Tasks for NEO Data Processing
"""
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import NEO, NEOStatistics
from .services import NEODataService
import logging

logger = logging.getLogger(__name__)


@shared_task
def fetch_neo_data():
    """
    Periodic task to fetch NEO data from NASA
    Runs every 6 hours
    """
    logger.info("Starting NEO data fetch")
    
    service = NEODataService()
    result = service.sync_neo_data()
    
    logger.info(f"NEO data fetch completed: {result}")
    
    # Trigger statistics calculation
    calculate_neo_statistics.delay()
    
    return result


@shared_task
def calculate_neo_statistics():
    """
    Calculate and store NEO statistics
    """
    logger.info("Calculating NEO statistics")
    
    today = timezone.now().date()
    
    # Count total NEOs
    total_neos = NEO.objects.count()
    total_phas = NEO.objects.filter(is_potentially_hazardous_asteroid=True).count()
    
    # Size distribution
    small_count = NEO.objects.filter(
        estimated_diameter_max_km__lt=0.1
    ).count()
    
    medium_count = NEO.objects.filter(
        estimated_diameter_max_km__gte=0.1,
        estimated_diameter_max_km__lt=0.5
    ).count()
    
    large_count = NEO.objects.filter(
        estimated_diameter_max_km__gte=0.5,
        estimated_diameter_max_km__lt=1.0
    ).count()
    
    very_large_count = NEO.objects.filter(
        estimated_diameter_max_km__gte=1.0
    ).count()
    
    # Close approaches
    from .models import CloseApproach
    
    close_approaches_7_days = CloseApproach.objects.filter(
        close_approach_date__gte=today,
        close_approach_date__lte=today + timedelta(days=7)
    ).count()
    
    close_approaches_30_days = CloseApproach.objects.filter(
        close_approach_date__gte=today,
        close_approach_date__lte=today + timedelta(days=30)
    ).count()
    
    # Create or update statistics
    stats, created = NEOStatistics.objects.update_or_create(
        date=today,
        defaults={
            'total_neos': total_neos,
            'total_phas': total_phas,
            'small_neos_count': small_count,
            'medium_neos_count': medium_count,
            'large_neos_count': large_count,
            'very_large_neos_count': very_large_count,
            'close_approaches_next_7_days': close_approaches_7_days,
            'close_approaches_next_30_days': close_approaches_30_days,
        }
    )
    
    logger.info(f"Statistics {'created' if created else 'updated'} for {today}")
    
    return {
        'date': str(today),
        'total_neos': total_neos,
        'total_phas': total_phas
    }


@shared_task
def cleanup_old_statistics():
    """
    Clean up old statistics records (keep last 90 days)
    """
    cutoff_date = timezone.now().date() - timedelta(days=90)
    deleted_count, _ = NEOStatistics.objects.filter(date__lt=cutoff_date).delete()
    
    logger.info(f"Cleaned up {deleted_count} old statistics records")
    
    return {'deleted_count': deleted_count}

