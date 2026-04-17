from django.db import models
from django.conf import settings


class CodingQuestion(models.Model):
    """Model representing a coding practice question"""
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]

    TOPIC_CHOICES = [
        ('Arrays', 'Arrays'),
        ('Strings', 'Strings'),
        ('Linked List', 'Linked List'),
        ('Trees', 'Trees'),
        ('Graphs', 'Graphs'),
        ('Dynamic Programming', 'Dynamic Programming'),
        ('Sorting & Searching', 'Sorting & Searching'),
        ('Stack & Queue', 'Stack & Queue'),
        ('Hash Table', 'Hash Table'),
        ('Recursion', 'Recursion'),
        ('Backtracking', 'Backtracking'),
        ('Divide & Conquer', 'Divide & Conquer'),
        ('Greedy', 'Greedy'),
        ('Bit Manipulation', 'Bit Manipulation'),
        ('Database', 'Database'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(help_text="Detailed problem description")
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    topic = models.CharField(max_length=50, choices=TOPIC_CHOICES)
    sample_input = models.TextField(help_text="Example input for the problem")
    sample_output = models.TextField(help_text="Expected output for the sample input")
    explanation = models.TextField(help_text="Detailed explanation of the solution approach")
    youtube_link = models.URLField(blank=True, null=True, help_text="YouTube video link for solution")
    constraints = models.TextField(blank=True, help_text="Problem constraints")
    test_cases = models.JSONField(default=list, blank=True, help_text="Additional test cases as JSON")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']
        verbose_name_plural = 'Coding Questions'

    def __str__(self):
        return f"{self.title} ({self.difficulty})"


class UserProgress(models.Model):
    """Model to track user progress on coding questions"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='coding_progress')
    question = models.ForeignKey(CodingQuestion, on_delete=models.CASCADE, related_name='user_progress')
    is_solved = models.BooleanField(default=False)
    is_bookmarked = models.BooleanField(default=False)
    attempts = models.PositiveIntegerField(default=0)
    last_attempted_at = models.DateTimeField(null=True, blank=True)
    solved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'question']
        ordering = ['-updated_at']

    def __str__(self):
        status = 'Solved' if self.is_solved else 'In Progress'
        return f"{self.user.username} - {self.question.title} ({status})"
