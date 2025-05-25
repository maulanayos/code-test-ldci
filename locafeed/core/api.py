from django.contrib.auth import login
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from .serializers import (
    UserSerializer, RegisterSerializer, LoginSerializer, 
    UserProfileSerializer, PostSerializer, LocationSerializer
)
from .models import UserProfile, Post, Location


class RegisterAPI(generics.GenericAPIView):
    """API endpoint for user registration"""
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Create token for the new user
        _, token = AuthToken.objects.create(user)
        
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token
        })


class LoginAPI(KnoxLoginView):
    """API endpoint for user login"""
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super().post(request, format=format)


class UserAPI(generics.RetrieveAPIView):
    """API endpoint for retrieving user data"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class UserProfileAPI(generics.RetrieveUpdateAPIView):
    """API endpoint for retrieving and updating user profile"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user.profile


class LocationListCreateAPI(generics.ListCreateAPIView):
    """API endpoint for listing and creating locations"""
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [permissions.IsAuthenticated]


class LocationDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    """API endpoint for retrieving, updating and deleting a location"""
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [permissions.IsAuthenticated]


class PostListCreateAPI(generics.ListCreateAPIView):
    """API endpoint for listing and creating posts"""
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Post.objects.all().order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    """API endpoint for retrieving, updating and deleting a post"""
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Users can only modify their own posts
        if self.request.method != 'GET':
            return Post.objects.filter(author=self.request.user)
        return Post.objects.all()
