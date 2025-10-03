"""
Users Views
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User

from .models import UserProfile, UserActivity
from .serializers import UserSerializer, UserProfileSerializer, UserActivitySerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for users
    """
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for user profiles
    """
    
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
    @action(detail=False, methods=['get', 'patch'])
    def my_profile(self, request):
        """Get or update current user's profile"""
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        
        if request.method == 'GET':
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        
        elif request.method == 'PATCH':
            serializer = self.get_serializer(profile, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class UserActivityViewSet(viewsets.ModelViewSet):
    """
    ViewSet for user activities
    """
    
    queryset = UserActivity.objects.all()
    serializer_class = UserActivitySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # Get client IP
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        
        serializer.save(
            user=self.request.user,
            ip_address=ip,
            user_agent=self.request.META.get('HTTP_USER_AGENT', '')
        )

