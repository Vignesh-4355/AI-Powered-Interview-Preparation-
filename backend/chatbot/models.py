from django.db import models
from django.conf import settings


class ChatMessage(models.Model):
    """Model representing a chat message between user and AI chatbot"""
    
    CATEGORY_CHOICES = [
        ('General', 'General'),
        ('Interview Prep', 'Interview Preparation'),
        ('Coding', 'Coding Guidance'),
        ('Company', 'Company Preparation'),
        ('Resume', 'Resume Tips'),
        ('Other', 'Other'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_messages', null=True, blank=True)
    message = models.TextField(help_text="User's message")
    response = models.TextField(help_text="Chatbot's response")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='General')
    timestamp = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=100, blank=True, help_text="Session identifier for anonymous users")

    class Meta:
        ordering = ['timestamp']
        verbose_name_plural = 'Chat Messages'

    def __str__(self):
        return f"{self.message[:50]} - {self.timestamp}"
