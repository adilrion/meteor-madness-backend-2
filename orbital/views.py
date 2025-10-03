"""
Orbital Views
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import OrbitalElements, TrajectoryPoint
from .serializers import OrbitalElementsSerializer, TrajectoryPointSerializer
from .services import OrbitalMechanicsService
from neos.models import NEO


class OrbitalElementsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for orbital elements
    """
    
    queryset = OrbitalElements.objects.all()
    serializer_class = OrbitalElementsSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def calculate(self, request):
        """Calculate orbital elements for a NEO"""
        neo_id = request.data.get('neo_id')
        
        try:
            neo = NEO.objects.get(id=neo_id)
        except NEO.DoesNotExist:
            return Response({'error': 'NEO not found'}, status=status.HTTP_404_NOT_FOUND)
        
        service = OrbitalMechanicsService()
        elements = service.calculate_orbital_elements(neo)
        
        serializer = self.get_serializer(elements)
        return Response(serializer.data)


class TrajectoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for trajectory points
    """
    
    queryset = TrajectoryPoint.objects.all()
    serializer_class = TrajectoryPointSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'])
    def for_neo(self, request):
        """Get trajectory points for a specific NEO"""
        neo_id = request.query_params.get('neo_id')
        
        if not neo_id:
            return Response(
                {'error': 'neo_id required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        points = self.queryset.filter(neo_id=neo_id)
        serializer = self.get_serializer(points, many=True)
        
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def calculate(self, request):
        """Calculate trajectory for a NEO"""
        neo_id = request.data.get('neo_id')
        num_points = request.data.get('num_points', 100)
        
        try:
            neo = NEO.objects.get(id=neo_id)
        except NEO.DoesNotExist:
            return Response({'error': 'NEO not found'}, status=status.HTTP_404_NOT_FOUND)
        
        service = OrbitalMechanicsService()
        count = service.calculate_trajectory(neo, num_points)
        
        return Response({
            'neo_id': neo_id,
            'points_calculated': count
        })

