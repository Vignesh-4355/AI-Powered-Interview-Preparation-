from django.urls import path
from .views import ResumeAnalyzerView, ResumeHistoryView, ResumeDetailView

urlpatterns = [
    path('analyze/', ResumeAnalyzerView.as_view(), name='resume-analyze'),
    path('history/', ResumeHistoryView.as_view(), name='resume-history'),
    path('<int:resume_id>/', ResumeDetailView.as_view(), name='resume-detail'),
]
