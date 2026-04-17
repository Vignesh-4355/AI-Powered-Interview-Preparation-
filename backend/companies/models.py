from django.db import models
from django.core.validators import MinLengthValidator


class Company(models.Model):
    """Model representing a company"""
    DIFFICULTY_LEVELS = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]
    
    HIRING_FREQUENCY = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]
    
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    logo = models.URLField(blank=True, null=True, help_text="URL to company logo")
    website = models.URLField(blank=True, null=True)
    industry = models.CharField(max_length=100, blank=True)
    difficulty_level = models.CharField(
        max_length=20,
        choices=DIFFICULTY_LEVELS,
        default='Medium',
        help_text="Overall difficulty level of company interviews"
    )
    hiring_frequency = models.CharField(
        max_length=20,
        choices=HIRING_FREQUENCY,
        default='Medium',
        help_text="How frequently the company hires"
    )
    total_questions = models.PositiveIntegerField(default=0, help_text="Total number of questions")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.name


class CompanyInterviewPattern(models.Model):
    """Model representing interview pattern for a company"""
    ROUND_TYPES = [
        ('Aptitude', 'Aptitude Test'),
        ('Technical', 'Technical Interview'),
        ('HR', 'HR Interview'),
        ('Coding', 'Coding Round'),
        ('Group Discussion', 'Group Discussion'),
        ('Managerial', 'Managerial Round'),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='interview_patterns')
    round_name = models.CharField(max_length=100, choices=ROUND_TYPES)
    description = models.TextField(help_text="Description of this interview round")
    duration = models.CharField(max_length=50, blank=True, help_text="Duration (e.g., '60 minutes')")
    order = models.PositiveIntegerField(default=0, help_text="Order of the round in interview process")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Company Interview Patterns'

    def __str__(self):
        return f"{self.company.name} - {self.round_name}"


class CompanyQuestion(models.Model):
    """Model representing interview questions for companies"""
    QUESTION_TYPES = [
        ('HR', 'HR Question'),
        ('Technical', 'Technical Question'),
        ('Coding', 'Coding Question'),
        ('Aptitude', 'Aptitude Question'),
        ('Behavioral', 'Behavioral Question'),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='questions')
    question = models.TextField()
    question_type = models.CharField(max_length=50, choices=QUESTION_TYPES)
    answer = models.TextField(help_text="Detailed answer/explanation")
    youtube_link = models.URLField(blank=True, null=True, help_text="YouTube video link for explanation")
    difficulty = models.CharField(
        max_length=20,
        choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')],
        default='Medium'
    )
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated tags")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Company Questions'

    def __str__(self):
        return f"{self.company.name} - {self.question_type}: {self.question[:50]}"
