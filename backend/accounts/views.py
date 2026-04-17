from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth import login as django_login
from django.views.decorators.csrf import csrf_exempt
from .models import UserProfile
from .serializers import (
    UserSerializer, 
    UserProfileSerializer, 
    RegisterSerializer,
    CustomTokenObtainPairSerializer
)
import json

User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Register a new user"""
    try:
        serializer = RegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'message': 'Registration successful',
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                },
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        import traceback
        print(f"Registration error: {str(e)}")
        print(traceback.format_exc())
        return Response(
            {'error': f'Registration failed: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """Login user and return JWT token"""
    try:
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response(
                {'error': 'Email and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = authenticate(email=email, password=password)
        
        if user:
            # Use custom serializer to get tokens with user data
            serializer = CustomTokenObtainPairSerializer(context={'request': request}, data={
                'email': user.email,
                'password': password
            })
            
            if serializer.is_valid():
                return Response({
                    'message': 'Login successful',
                    'user': serializer.validated_data['user'],
                    'access_token': serializer.validated_data['access'],
                    'refresh_token': serializer.validated_data['refresh'],
                })
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {'error': 'Invalid email or password'},
                status=status.HTTP_401_UNAUTHORIZED
            )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """Logout user and blacklist token"""
    try:
        refresh_token = request.data.get('refresh_token')
        
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        
        return Response({
            'message': 'Logout successful'
        })
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    """Get current user profile"""
    try:
        user = request.user
        profile, created = UserProfile.objects.get_or_create(user=user)
        
        return Response({
            'user': UserSerializer(user).data,
            'profile': UserProfileSerializer(profile).data if not created else None
        })
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_data(request):
    """Dashboard data for authenticated users"""
    user = request.user
    
    # Get or create user profile
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    return Response({
        'user': {
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        },
        'profile': {
            'target_job_role': profile.target_job_role,
            'experience_level': profile.experience_level,
            'bio': profile.bio,
        } if not created else None
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def api_test(request):
    """Basic API test endpoint"""
    return Response({
        'message': 'AI Powered Interview Preparation Portal API is running!',
        'version': '1.0.0',
        'status': 'healthy'
    })
