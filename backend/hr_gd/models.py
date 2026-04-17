from django.db import models


class HRQuestion(models.Model):
    """Model representing HR interview questions"""
    CATEGORY_CHOICES = [
        ('Personal', 'Personal Questions'),
        ('Behavioral', 'Behavioral Questions'),
        ('Situational', 'Situational Questions'),
        ('Career', 'Career Questions'),
        ('Company', 'Company Questions'),
        ('Strengths Weaknesses', 'Strengths & Weaknesses'),
        ('Goals', 'Goals & Aspirations'),
        ('Teamwork', 'Teamwork & Leadership'),
        ('Conflict', 'Conflict Resolution'),
        ('Motivation', 'Motivation'),
    ]

  question = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    sample_answer= models.TextField(help_text="Sample answer or talking points")
   tips = models.TextField(blank=True, help_text="Additional tips for answering")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'question']
        verbose_name_plural = 'HR Questions'

  def __str__(self):
      return f"{self.category}: {self.question[:50]}"


class GDTopic(models.Model):
    """Model representing Group Discussion topics"""
    TYPE_CHOICES = [
        ('Current Affairs', 'Current Affairs'),
        ('Social Issues', 'Social Issues'),
        ('Economic', 'Economic Issues'),
        ('Political', 'Political Topics'),
        ('Technology', 'Technology'),
        ('Education', 'Education'),
        ('Environment', 'Environment'),
        ('Business', 'Business & Management'),
        ('Abstract', 'Abstract Topics'),
        ('Ethical', 'Ethical Dilemmas'),
    ]

  topic = models.CharField(max_length=200)
  topic_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
   introduction_points = models.TextField(help_text="Key points to introduce the topic")
   arguments_for = models.TextField(help_text="Arguments in favor/positive aspects")
   arguments_against = models.TextField(help_text="Arguments against/negative aspects", blank=True)
  conclusion_points = models.TextField(help_text="How to conclude the discussion")
   dos_and_donts = models.TextField(help_text="Do's and Don'ts for this topic")
   key_facts = models.JSONField(default=list, blank=True, help_text="Important facts and statistics as JSON array")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['topic_type', 'topic']
        verbose_name_plural = 'GD Topics'

  def __str__(self):
      return f"{self.topic_type}: {self.topic}"
