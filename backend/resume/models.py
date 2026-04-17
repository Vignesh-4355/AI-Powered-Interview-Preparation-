from django.db import models
from django.conf import settings


class Resume(models.Model):
    """Model representing an uploaded resume"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resumes')
    file = models.FileField(upload_to='resumes/%Y/%m/%d/', help_text="PDF resume file")
    original_filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_size = models.PositiveIntegerField(help_text="File size in bytes")
    
    # Extracted data
    extracted_text = models.TextField(blank=True, help_text="Extracted text from PDF")
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name_plural = 'Resumes'

    def __str__(self):
        return f"{self.user.username} - {self.original_filename}"


class ResumeAnalysis(models.Model):
    """Model representing resume analysis results"""
    resume = models.OneToOneField(Resume, on_delete=models.CASCADE, related_name='analysis')
    analyzed_at = models.DateTimeField(auto_now_add=True)
    
    # Skills analysis
    detected_skills = models.JSONField(default=list, help_text="List of detected skills")
    missing_skills = models.JSONField(default=list, help_text="List of missing important skills")
    keywords_found = models.JSONField(default=list, help_text="Keywords found in resume")
    
    # Analysis metrics
    skill_score = models.FloatField(default=0, help_text="Overall skill score 0-100")
    keyword_density = models.FloatField(default=0, help_text="Keyword density percentage")
    formatting_score = models.FloatField(default=0, help_text="Formatting quality score 0-100")
    
    # Detailed feedback
    strengths = models.JSONField(default=list, help_text="Resume strengths")
    weaknesses = models.JSONField(default=list, help_text="Areas for improvement")
    suggestions = models.JSONField(default=list, help_text="Specific suggestions")
    
    # ATS compatibility
    ats_score = models.FloatField(default=0, help_text="ATS compatibility score 0-100")
    ats_issues = models.JSONField(default=list, help_text="ATS compatibility issues")
    
    class Meta:
        ordering = ['-analyzed_at']
        verbose_name_plural = 'Resume Analyses'

    def __str__(self):
        return f"Analysis for {self.resume.original_filename}"
