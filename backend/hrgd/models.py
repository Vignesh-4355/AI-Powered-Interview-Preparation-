from django.db import models


class HRQuestion(models.Model):
    """Model representing an HR interview question"""
    
    CATEGORY_CHOICES = [
        ('General', 'General'),
        ('Behavioral', 'Behavioral'),
        ('Technical', 'Technical'),
        ('Situational', 'Situational'),
        ('Company Specific', 'Company Specific'),
    ]

    question = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='General')
    sample_answer = models.TextField(help_text="Sample answer or talking points")
    tips = models.TextField(blank=True, help_text="Additional tips for answering")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'id']
        verbose_name_plural = 'HR Questions'

    def __str__(self):
        return f"{self.category}: {self.question[:50]}"


class GDTopic(models.Model):
    """Model representing a Group Discussion topic"""
    
    TYPE_CHOICES = [
        ('Current Affairs', 'Current Affairs'),
        ('Social Issues', 'Social Issues'),
        ('Business & Economy', 'Business & Economy'),
        ('Technology', 'Technology'),
        ('Abstract', 'Abstract'),
        ('Controversial', 'Controversial'),
    ]

    topic = models.CharField(max_length=300)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='Current Affairs')
    introduction_points = models.TextField(help_text="Key points to introduce the topic")
    arguments_for = models.TextField(help_text="Arguments in favor of the topic")
    arguments_against = models.TextField(help_text="Arguments against the topic", blank=True)
    dos_and_donts = models.TextField(help_text="Do's and Don'ts for this GD")
    conclusion_points = models.TextField(help_text="How to conclude the discussion", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'GD Topics'

    def __str__(self):
        return f"{self.type}: {self.topic[:50]}"
