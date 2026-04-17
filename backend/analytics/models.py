from django.db import models
from django.conf import settings


class UserProgress(models.Model):
    """Model to track overall user progress across all modules"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='progress')
    
    # Coding Practice Stats
    coding_attempted = models.PositiveIntegerField(default=0)
    coding_solved = models.PositiveIntegerField(default=0)
    
    # Mock Interview Stats
    mock_interviews_completed = models.PositiveIntegerField(default=0)
    mock_interviews_average_score = models.FloatField(default=0)
    
    # Aptitude Stats
    aptitude_attempted = models.PositiveIntegerField(default=0)
    aptitude_correct = models.PositiveIntegerField(default=0)
    
    # Overall Stats
    total_activity_hours = models.FloatField(default=0)
    current_streak = models.PositiveIntegerField(default=0)
    longest_streak = models.PositiveIntegerField(default=0)
    
    # Timestamps
    last_coding_activity = models.DateTimeField(null=True, blank=True)
    last_mock_activity = models.DateTimeField(null=True, blank=True)
    last_aptitude_activity = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'User Progress'

    def __str__(self):
        return f"{self.user.username} - Progress Tracker"
    
    @property
    def coding_accuracy(self):
        if self.coding_attempted == 0:
            return 0
        return (self.coding_solved / self.coding_attempted) * 100
    
    @property
    def aptitude_accuracy(self):
        if self.aptitude_attempted == 0:
            return 0
        return (self.aptitude_correct / self.aptitude_attempted) * 100
