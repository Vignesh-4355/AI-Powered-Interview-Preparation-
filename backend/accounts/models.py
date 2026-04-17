from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom User model with email as username"""
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Email is already required by default
    
    def __str__(self):
        return self.email


class UserProfile(models.Model):
    """Extended user profile for additional information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)
    target_job_role = models.CharField(max_length=200, blank=True)
    experience_level = models.CharField(
        max_length=50,
        choices=[
            ('fresher', 'Fresher'),
            ('entry', 'Entry Level (0-2 years)'),
            ('mid', 'Mid Level (3-5 years)'),
            ('senior', 'Senior Level (5+ years)'),
        ],
        blank=True
    )
    preferred_locations = models.CharField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.email}'s Profile"
