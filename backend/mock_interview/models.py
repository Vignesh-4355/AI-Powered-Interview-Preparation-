from django.db import models
from django.conf import settings


class InterviewQuestion(models.Model):
    """Model representing interview questions"""
    QUESTION_TYPE_CHOICES = [
        ('HR', 'HR'),
        ('Technical', 'Technical'),
        ('Coding', 'Coding'),
    ]

    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]

    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    expected_keywords = models.JSONField(
        default=list,
        help_text="List of keywords to look for in answers"
    )
    model_answer = models.TextField(
        blank=True,
        help_text="Ideal answer or key points"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['question_type', 'difficulty']

    def __str__(self):
        return f"{self.question_type} - {self.difficulty}: {self.question_text[:50]}"


class MockInterviewSession(models.Model):
    """Model representing a mock interview session"""
    INTERVIEW_TYPE_CHOICES = [
        ('HR', 'HR'),
        ('Technical', 'Technical'),
        ('Mixed', 'Mixed'),
    ]

    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mock_interviews'
    )
    interview_type = models.CharField(max_length=20, choices=INTERVIEW_TYPE_CHOICES)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    total_questions = models.PositiveIntegerField(default=5)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    score = models.FloatField(null=True, blank=True, help_text="Overall score 0-100")
    feedback = models.TextField(blank=True)

    class Meta:
        ordering = ['-start_time']

    def __str__(self):
        return f"{self.user.username} - {self.interview_type} ({self.difficulty})"


class UserAnswer(models.Model):
    """Model representing user's answer to an interview question"""
    session = models.ForeignKey(
        MockInterviewSession,
        on_delete=models.CASCADE,
        related_name='answers'
    )
    question = models.ForeignKey(InterviewQuestion, on_delete=models.CASCADE)
    answer_text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    keyword_score = models.FloatField(
        default=0,
        help_text="Score based on keyword matching (0-100)"
    )
    feedback = models.TextField(blank=True)

    class Meta:
        ordering = ['timestamp']
        unique_together = ['session', 'question']

    def __str__(self):
        return f"{self.session.user.username} - Q{self.id}"
