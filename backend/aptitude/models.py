from django.db import models
from django.conf import settings


class AptitudeQuestion(models.Model):
    """Model representing an aptitude question"""
    CATEGORY_CHOICES = [
        ('Time and Work', 'Time and Work'),
        ('Time and Distance', 'Time and Distance'),
        ('Probability', 'Probability'),
        ('Percentages', 'Percentages'),
        ('Logical Reasoning', 'Logical Reasoning'),
    ]

    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]

    question = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    solution = models.TextField(help_text="Step-by-step solution")
    explanation = models.TextField(help_text="Detailed explanation of the concept")
    formula_used = models.CharField(max_length=300, blank=True, help_text="Key formula used")
    youtube_link = models.URLField(blank=True, help_text="YouTube video explanation")
    options = models.JSONField(default=list, help_text="Multiple choice options as JSON array")
    correct_answer = models.CharField(max_length=200, help_text="Correct answer or option index")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'difficulty']
        verbose_name_plural = 'Aptitude Questions'

    def __str__(self):
        return f"{self.category} - {self.difficulty}: {self.question[:50]}"


class UserAttempt(models.Model):
    """Model to track user attempts on aptitude questions"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='aptitude_attempts')
    question = models.ForeignKey(AptitudeQuestion, on_delete=models.CASCADE, related_name='user_attempts')
    selected_answer = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    time_taken = models.PositiveIntegerField(help_text="Time taken in seconds", null=True, blank=True)
    attempted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-attempted_at']
        unique_together = ['user', 'question']

    def __str__(self):
        status = 'Correct' if self.is_correct else 'Incorrect'
        return f"{self.user.username} - {self.question.id} ({status})"
