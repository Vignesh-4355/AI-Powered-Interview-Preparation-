from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserProfile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone']
        read_only_fields = ['id']


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for UserProfile model"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['user', 'avatar', 'bio', 'target_job_role', 
                  'experience_level', 'preferred_locations', 
                  'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, min_length=8, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, min_length=8, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = ['email', 'password', 'password_confirm', 'first_name', 'last_name']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        
        # Check if email already exists
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "Email is already registered"})
        
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        try:
            # Generate a unique username from email (optional, but required by Django)
            email = validated_data['email']
            username = email.split('@')[0] + '_' + str(User.objects.count() + 1)
            
            user = User.objects.create_user(
                username=username,
                email=email,
                password=validated_data['password'],
                first_name=validated_data.get('first_name', ''),
                last_name=validated_data.get('last_name', '')
            )
            
            # Create user profile
            UserProfile.objects.get_or_create(user=user)
            
            return user
        except Exception as e:
            print(f"Error creating user: {str(e)}")
            raise


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom token serializer to include user data"""
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add custom claims
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Add user data to response
        data['user'] = {
            'id': self.user.id,
            'email': self.user.email,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
        }
        
        return data
