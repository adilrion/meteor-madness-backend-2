"""
Celery Tasks for Asteroid Threat Assessments
"""
from celery import shared_task
from .models import ThreatScenario
from .services import ThreatCalculationService
import logging

logger = logging.getLogger(__name__)


@shared_task
def calculate_threat_assessments():
    """
    Calculate threat assessments for all active scenarios
    """
    logger.info("Starting threat assessment calculations")
    
    service = ThreatCalculationService()
    scenarios = ThreatScenario.objects.filter(is_active=True)
    
    processed = 0
    for scenario in scenarios:
        try:
            service.calculate_scenario_threat(scenario)
            processed += 1
        except Exception as e:
            logger.error(f"Error calculating threat for {scenario.name}: {e}")
    
    logger.info(f"Processed {processed} threat assessments")
    
    return {'processed': processed}

