"""
Impact Events Views
"""
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from .models import ImpactEvent, Earthquake
from .serializers import ImpactEventSerializer, EarthquakeSerializer


class ImpactEventViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for historical impact events
    """
    
    queryset = ImpactEvent.objects.all()
    serializer_class = ImpactEventSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['extinction_event', 'crater_preserved']
    search_fields = ['name', 'location_name', 'description']
    
    @action(detail=False, methods=['get'])
    def major_events(self, request):
        """Get major impact events (> 100 MT)"""
        events = self.queryset.filter(energy_megatons__gte=100)
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def recent_events(self, request):
        """Get recent impact events (< 200 years ago)"""
        events = self.queryset.filter(years_ago__lte=200)
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)


class EarthquakeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for historical earthquakes
    """
    
    queryset = Earthquake.objects.all()
    serializer_class = EarthquakeSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tsunami_generated']
    search_fields = ['name', 'location', 'country']
    
    @action(detail=False, methods=['get'])
    def major_earthquakes(self, request):
        """Get major earthquakes (M >= 7.0)"""
        earthquakes = self.queryset.filter(magnitude__gte=7.0)
        serializer = self.get_serializer(earthquakes, many=True)
        return Response(serializer.data)

