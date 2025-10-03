"""
Asteroid Threat Assessment Views
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from .models import ThreatScenario, ThreatAssessment, DestructionZone
from .serializers import (
    ThreatScenarioSerializer,
    ThreatScenarioListSerializer,
    ThreatAssessmentSerializer,
    DestructionZoneSerializer
)
from .services import ThreatCalculationService


class ThreatScenarioViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Threat Scenarios
    
    Provides pre-configured asteroid threat scenarios
    """
    
    queryset = ThreatScenario.objects.filter(is_active=True)
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['scenario_type', 'impact_type']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ThreatScenarioSerializer
        return ThreatScenarioListSerializer
    
    @action(detail=True, methods=['post'])
    def calculate_assessment(self, request, pk=None):
        """Calculate threat assessment for a scenario"""
        scenario = self.get_object()
        
        service = ThreatCalculationService()
        assessment = service.calculate_scenario_threat(scenario)
        
        serializer = ThreatAssessmentSerializer(assessment)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_severity(self, request):
        """Get scenarios ordered by severity (energy)"""
        scenarios = self.queryset.order_by('-energy_megatons')
        page = self.paginate_queryset(scenarios)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(scenarios, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def compare(self, request):
        """Compare multiple scenarios"""
        scenario_ids = request.data.get('scenario_ids', [])
        
        if not scenario_ids:
            return Response(
                {'error': 'scenario_ids required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        scenarios = self.queryset.filter(id__in=scenario_ids)
        serializer = ThreatScenarioSerializer(scenarios, many=True)
        
        return Response(serializer.data)


class ThreatAssessmentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Threat Assessments
    
    Provides calculated threat assessments
    """
    
    queryset = ThreatAssessment.objects.all()
    serializer_class = ThreatAssessmentSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['overall_risk_level', 'tsunami_risk']
    
    @action(detail=False, methods=['get'])
    def high_risk(self, request):
        """Get high and critical risk assessments"""
        assessments = self.queryset.filter(
            overall_risk_level__in=['high', 'critical']
        )
        
        serializer = self.get_serializer(assessments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def destruction_analysis(self, request, pk=None):
        """Get detailed destruction zone analysis"""
        assessment = self.get_object()
        zones = assessment.destruction_zones.all()
        
        serializer = DestructionZoneSerializer(zones, many=True)
        return Response(serializer.data)

