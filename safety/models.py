"""
Safety Center Models - MeteorShield Features
"""
from django.db import models
from django.contrib.auth.models import User


class EmergencyChecklist(models.Model):
    """
    Emergency preparedness checklists
    """
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(
        max_length=50,
        choices=[
            ('pre_impact', 'Pre-Impact Preparation'),
            ('during_impact', 'During Impact'),
            ('post_impact', 'Post-Impact Recovery'),
            ('evacuation', 'Evacuation'),
            ('shelter', 'Shelter-in-Place')
        ]
    )
    
    priority = models.IntegerField(default=1)
    items = models.JSONField(default=list)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'emergency_checklists'
        ordering = ['priority', 'title']
        verbose_name = 'Emergency Checklist'
        verbose_name_plural = 'Emergency Checklists'
    
    def __str__(self):
        return self.title


class ResourceAllocation(models.Model):
    """
    Resource allocation calculator data
    """
    
    scenario_name = models.CharField(max_length=200)
    population_size = models.IntegerField()
    shelter_duration_days = models.IntegerField()
    
    # Calculated Resources
    water_liters = models.FloatField()
    food_calories = models.FloatField()
    medical_supplies_units = models.IntegerField()
    shelter_space_m2 = models.FloatField()
    power_kwh = models.FloatField()
    
    # Additional Resources
    personnel_required = models.IntegerField()
    vehicles_required = models.IntegerField()
    communication_devices = models.IntegerField()
    
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    class Meta:
        db_table = 'resource_allocations'
        ordering = ['-created_at']
        verbose_name = 'Resource Allocation'
        verbose_name_plural = 'Resource Allocations'
    
    def __str__(self):
        return f"{self.scenario_name} - {self.population_size} people"


class SafetyPlan(models.Model):
    """
    Family/Community safety plans
    """
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='safety_plans')
    name = models.CharField(max_length=200)
    plan_type = models.CharField(
        max_length=50,
        choices=[
            ('family', 'Family Plan'),
            ('community', 'Community Plan'),
            ('workplace', 'Workplace Plan')
        ]
    )
    
    # Members
    members = models.JSONField(default=list, help_text="List of people in the plan")
    
    # Emergency Contacts
    emergency_contacts = models.JSONField(default=list)
    
    # Meeting Points
    primary_meetup_location = models.TextField()
    secondary_meetup_location = models.TextField()
    evacuation_route = models.TextField()
    
    # Supplies
    emergency_kit_location = models.CharField(max_length=200)
    supplies_checklist = models.JSONField(default=list)
    
    # Communication Plan
    communication_plan = models.TextField()
    out_of_area_contact = models.CharField(max_length=200, blank=True)
    
    # Special Needs
    special_needs_notes = models.TextField(blank=True)
    pet_care_plan = models.TextField(blank=True)
    
    is_active = models.BooleanField(default=True)
    last_reviewed = models.DateField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'safety_plans'
        ordering = ['-updated_at']
        verbose_name = 'Safety Plan'
        verbose_name_plural = 'Safety Plans'
    
    def __str__(self):
        return f"{self.name} ({self.user.username})"


class MentalHealthResource(models.Model):
    """
    Mental health and psychological support resources
    """
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    resource_type = models.CharField(
        max_length=50,
        choices=[
            ('hotline', 'Crisis Hotline'),
            ('article', 'Educational Article'),
            ('video', 'Video Resource'),
            ('technique', 'Coping Technique'),
            ('support_group', 'Support Group')
        ]
    )
    
    content = models.TextField()
    phone_number = models.CharField(max_length=50, blank=True)
    url = models.URLField(blank=True)
    availability = models.CharField(max_length=100, default="24/7")
    
    languages_available = models.JSONField(default=list)
    target_audience = models.CharField(max_length=100, blank=True)
    
    is_active = models.BooleanField(default=True)
    priority = models.IntegerField(default=1)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'mental_health_resources'
        ordering = ['priority', 'title']
        verbose_name = 'Mental Health Resource'
        verbose_name_plural = 'Mental Health Resources'
    
    def __str__(self):
        return self.title


class ChatbotConversation(models.Model):
    """
    AI Chatbot conversation history
    """
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='chatbot_conversations',
        null=True,
        blank=True
    )
    session_id = models.CharField(max_length=100, db_index=True)
    
    messages = models.JSONField(default=list)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'chatbot_conversations'
        ordering = ['-updated_at']
        verbose_name = 'Chatbot Conversation'
        verbose_name_plural = 'Chatbot Conversations'
    
    def __str__(self):
        return f"Conversation {self.session_id}"


class ClimateImpactModel(models.Model):
    """
    Climate chain reaction modeling
    """
    
    impact_energy_mt = models.FloatField(help_text="Impact energy in megatons")
    
    # Immediate Effects
    dust_ejected_gigatons = models.FloatField()
    water_vapor_gigatons = models.FloatField()
    sulfur_dioxide_gigatons = models.FloatField()
    
    # Temperature Effects
    initial_temperature_drop_c = models.FloatField()
    recovery_time_years = models.FloatField()
    
    # Agricultural Impact
    growing_season_reduction_percent = models.FloatField()
    crop_yield_reduction_percent = models.FloatField()
    
    # Ocean Effects
    ocean_temperature_drop_c = models.FloatField()
    phytoplankton_reduction_percent = models.FloatField()
    
    # Ecological Cascade
    species_extinction_percent = models.FloatField()
    ecosystem_recovery_years = models.FloatField()
    
    # Human Impact
    food_security_risk = models.CharField(max_length=20)
    water_security_risk = models.CharField(max_length=20)
    health_impact_severity = models.CharField(max_length=20)
    
    calculated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'climate_impact_models'
        ordering = ['-impact_energy_mt']
        verbose_name = 'Climate Impact Model'
        verbose_name_plural = 'Climate Impact Models'
    
    def __str__(self):
        return f"Climate Model - {self.impact_energy_mt} MT"

