"""
Seismic Views
"""
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import SeismicImpactAnalysis
from .serializers import SeismicImpactAnalysisSerializer
from .services import SeismicCalculationService


class SeismicImpactAnalysisViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for seismic impact analyses
    """
    
    queryset = SeismicImpactAnalysis.objects.all()
    serializer_class = SeismicImpactAnalysisSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def calculate(self, request):
        """Calculate seismic impact for a threat assessment"""
        from asteroids.models import ThreatAssessment
        
        assessment_id = request.data.get('threat_assessment_id')
        
        try:
            assessment = ThreatAssessment.objects.get(id=assessment_id)
        except ThreatAssessment.DoesNotExist:
            return Response({'error': 'Threat assessment not found'}, status=404)
        
        service = SeismicCalculationService()
        analysis = service.calculate_seismic_impact(assessment)
        
        serializer = self.get_serializer(analysis)
        return Response(serializer.data)

