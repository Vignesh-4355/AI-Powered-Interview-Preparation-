from django.db import models
from django.conf import settings


class RoadmapItem(models.Model):
    """Model representing a personalized roadmap item for user"""
    
    STATUS_CHOICES = [
        ('Not Started', 'Not Started'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]

    CATEGORY_CHOICES = [
        ('Data Structures', 'Data Structures'),
        ('Algorithms', 'Algorithms'),
        ('Coding Practice', 'Coding Practice'),
        ('HR Preparation', 'HR Preparation'),
        ('Company Research', 'Company Research'),
        ('Aptitude', 'Aptitude'),
        ('Resume Building', 'Resume Building'),
        ('Mock Interviews', 'Mock Interviews'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='roadmap_items')
    topic = models.CharField(max_length=200, help_text="Topic or skill to master")
    description = models.TextField(help_text="Detailed description and resources")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Not Started')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='Medium')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    estimated_hours = models.PositiveIntegerField(default=5, help_text="Estimated hours to complete")
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order = models.PositiveIntegerField(default=0, help_text="Display order")

    class Meta:
        ordering = ['priority', 'order', 'created_at']
        verbose_name_plural = 'Roadmap Items'

    def __str__(self):
        return f"{self.user.username} - {self.topic} ({self.priority})"
