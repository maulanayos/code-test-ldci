from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import UserProfile, Post, Location

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model"""
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data.get('email', ''),
            validated_data['password']
        )
        
        if 'first_name' in validated_data:
            user.first_name = validated_data['first_name']
        
        if 'last_name' in validated_data:
            user.last_name = validated_data['last_name']
            
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=username,
            password=password
        )

        if not user:
            msg = 'Unable to authenticate with provided credentials'
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for the UserProfile model"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ('id', 'user', 'bio', 'profile_picture', 'location', 'date_of_birth', 'is_private')
        read_only_fields = ('id',)


class LocationSerializer(serializers.ModelSerializer):
    """Serializer for the Location model"""
    class Meta:
        model = Location
        fields = ('id', 'name', 'latitude', 'longitude')


class PostSerializer(serializers.ModelSerializer):
    """Serializer for the Post model"""
    author = UserSerializer(read_only=True)
    location = LocationSerializer(read_only=True)
    location_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = Post
        fields = ('id', 'author', 'text', 'location', 'location_id', 'created_at')
        read_only_fields = ('id', 'created_at', 'author')
    
    def create(self, validated_data):
        location_id = validated_data.pop('location_id', None)
        location = None
        
        if location_id:
            try:
                location = Location.objects.get(id=location_id)
            except Location.DoesNotExist:
                raise serializers.ValidationError({"location_id": "Location does not exist"})
        
        user = self.context['request'].user
        post = Post.objects.create(
            author=user,
            location=location,
            **validated_data
        )
        return post
