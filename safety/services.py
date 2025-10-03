"""
Safety Services
"""
import uuid
from django.conf import settings
from .models import ChatbotConversation, ResourceAllocation, ClimateImpactModel
import logging

logger = logging.getLogger(__name__)


class ChatbotService:
    """AI Chatbot service using OpenAI"""
    
    def process_message(self, message, session_id=None):
        """Process a chatbot message"""
        if not session_id:
            session_id = str(uuid.uuid4())
        
        # Get or create conversation
        conversation, created = ChatbotConversation.objects.get_or_create(
            session_id=session_id,
            defaults={'messages': []}
        )
        
        # Add user message
        conversation.messages.append({
            'role': 'user',
            'content': message
        })
        
        # Generate response (simplified - integrate with OpenAI API)
        bot_response = self._generate_response(message, conversation.messages)
        
        # Add bot response
        conversation.messages.append({
            'role': 'assistant',
            'content': bot_response
        })
        
        conversation.save()
        
        return {
            'session_id': session_id,
            'response': bot_response
        }
    
    def _generate_response(self, message, history):
        """Generate chatbot response (integrate with OpenAI)"""
        # Placeholder - integrate with OpenAI API
        message_lower = message.lower()
        
        if 'asteroid' in message_lower or 'meteor' in message_lower:
            return "I can help you understand asteroid threats and safety measures. What would you like to know?"
        elif 'prepare' in message_lower or 'safety' in message_lower:
            return "For impact preparedness, I recommend: 1) Create an emergency plan, 2) Stockpile supplies, 3) Identify shelter locations, 4) Stay informed about threats."
        else:
            return "I'm here to help with meteor safety and preparedness. How can I assist you today?"


class ResourceCalculationService:
    """Calculate resource requirements for shelters"""
    
    def calculate_resources(self, population, duration_days):
        """Calculate required resources"""
        
        # Water: 3 liters per person per day
        water_liters = population * 3 * duration_days
        
        # Food: 2000 calories per person per day
        food_calories = population * 2000 * duration_days
        
        # Medical supplies: 1 unit per 50 people per week
        weeks = duration_days / 7
        medical_supplies = int((population / 50) * weeks)
        
        # Shelter: 3 m² per person
        shelter_space = population * 3
        
        # Power: 0.5 kWh per person per day
        power_kwh = population * 0.5 * duration_days
        
        # Personnel: 1 staff per 100 people
        personnel = max(int(population / 100), 1)
        
        # Vehicles: 1 per 500 people
        vehicles = max(int(population / 500), 1)
        
        # Communication: 1 device per 50 people
        comm_devices = max(int(population / 50), 1)
        
        # Save calculation
        allocation = ResourceAllocation.objects.create(
            scenario_name=f"Population {population} for {duration_days} days",
            population_size=population,
            shelter_duration_days=duration_days,
            water_liters=water_liters,
            food_calories=food_calories,
            medical_supplies_units=medical_supplies,
            shelter_space_m2=shelter_space,
            power_kwh=power_kwh,
            personnel_required=personnel,
            vehicles_required=vehicles,
            communication_devices=comm_devices
        )
        
        return {
            'water_liters': water_liters,
            'food_calories': food_calories,
            'medical_supplies_units': medical_supplies,
            'shelter_space_m2': shelter_space,
            'power_kwh': power_kwh,
            'personnel_required': personnel,
            'vehicles_required': vehicles,
            'communication_devices': comm_devices
        }


class ClimateModelingService:
    """Climate impact modeling service"""
    
    def calculate_climate_impact(self, energy_mt):
        """Calculate climate chain reaction effects"""
        
        # Dust ejection (simplified model)
        dust_gigatons = energy_mt ** 0.5 * 0.1
        
        # Water vapor
        water_vapor_gigatons = energy_mt ** 0.4 * 0.05
        
        # Sulfur dioxide
        so2_gigatons = energy_mt ** 0.3 * 0.02
        
        # Temperature drop (based on dust)
        if energy_mt > 100000:
            temp_drop = -15.0
            recovery_years = 100
        elif energy_mt > 10000:
            temp_drop = -5.0
            recovery_years = 20
        elif energy_mt > 1000:
            temp_drop = -2.0
            recovery_years = 5
        else:
            temp_drop = -0.5
            recovery_years = 1
        
        # Agricultural impact
        growing_season_reduction = abs(temp_drop) * 10
        crop_yield_reduction = abs(temp_drop) * 15
        
        # Ocean effects
        ocean_temp_drop = temp_drop * 0.3
        phytoplankton_reduction = abs(temp_drop) * 5
        
        # Ecological cascade
        if energy_mt > 100000:
            extinction_percent = 75
            ecosystem_recovery = 1000000
        elif energy_mt > 10000:
            extinction_percent = 30
            ecosystem_recovery = 100000
        else:
            extinction_percent = 5
            ecosystem_recovery = 10000
        
        # Risk levels
        if energy_mt > 10000:
            food_risk = 'extreme'
            water_risk = 'extreme'
            health_risk = 'extreme'
        elif energy_mt > 1000:
            food_risk = 'high'
            water_risk = 'high'
            health_risk = 'high'
        else:
            food_risk = 'moderate'
            water_risk = 'moderate'
            health_risk = 'moderate'
        
        # Save model
        model = ClimateImpactModel.objects.create(
            impact_energy_mt=energy_mt,
            dust_ejected_gigatons=dust_gigatons,
            water_vapor_gigatons=water_vapor_gigatons,
            sulfur_dioxide_gigatons=so2_gigatons,
            initial_temperature_drop_c=temp_drop,
            recovery_time_years=recovery_years,
            growing_season_reduction_percent=growing_season_reduction,
            crop_yield_reduction_percent=crop_yield_reduction,
            ocean_temperature_drop_c=ocean_temp_drop,
            phytoplankton_reduction_percent=phytoplankton_reduction,
            species_extinction_percent=extinction_percent,
            ecosystem_recovery_years=ecosystem_recovery,
            food_security_risk=food_risk,
            water_security_risk=water_risk,
            health_impact_severity=health_risk
        )
        
        return model

