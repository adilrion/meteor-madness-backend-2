"""
Safety Views
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import (
    EmergencyChecklist,
    ResourceAllocation,
    SafetyPlan,
    MentalHealthResource,
    ChatbotConversation,
    ClimateImpactModel
)
from .serializers import (
    EmergencyChecklistSerializer,
    ResourceAllocationSerializer,
    SafetyPlanSerializer,
    MentalHealthResourceSerializer,
    ChatbotConversationSerializer,
    ClimateImpactModelSerializer
)
from .services import ChatbotService, ResourceCalculationService, ClimateModelingService


class EmergencyChecklistViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EmergencyChecklist.objects.all()
    serializer_class = EmergencyChecklistSerializer
    permission_classes = [AllowAny]
    filterset_fields = ['category']


class ResourceAllocationViewSet(viewsets.ModelViewSet):
    queryset = ResourceAllocation.objects.all()
    serializer_class = ResourceAllocationSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def calculate(self, request):
        """Calculate resource requirements"""
        service = ResourceCalculationService()
        
        population = request.data.get('population_size')
        duration = request.data.get('shelter_duration_days')
        
        if not population or not duration:
            return Response(
                {'error': 'population_size and shelter_duration_days required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        result = service.calculate_resources(int(population), int(duration))
        
        return Response(result)


class SafetyPlanViewSet(viewsets.ModelViewSet):
    queryset = SafetyPlan.objects.all()
    serializer_class = SafetyPlanSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MentalHealthResourceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MentalHealthResource.objects.filter(is_active=True)
    serializer_class = MentalHealthResourceSerializer
    permission_classes = [AllowAny]
    filterset_fields = ['resource_type']
    
    @action(detail=False, methods=['get'])
    def crisis_hotlines(self, request):
        """Get crisis hotlines"""
        hotlines = self.queryset.filter(resource_type='hotline')
        serializer = self.get_serializer(hotlines, many=True)
        return Response(serializer.data)


class ChatbotViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def chat(self, request):
        """Send a message to the chatbot"""
        service = ChatbotService()
        
        message = request.data.get('message')
        session_id = request.data.get('session_id')
        
        if not message:
            return Response(
                {'error': 'message required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        response = service.process_message(message, session_id)
        
        return Response(response)


class ClimateImpactModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ClimateImpactModel.objects.all()
    serializer_class = ClimateImpactModelSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def calculate(self, request):
        """Calculate climate impact"""
        service = ClimateModelingService()
        
        energy_mt = request.data.get('impact_energy_mt')
        
        if not energy_mt:
            return Response(
                {'error': 'impact_energy_mt required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        result = service.calculate_climate_impact(float(energy_mt))
        serializer = self.get_serializer(result)
        
        return Response(serializer.data)

