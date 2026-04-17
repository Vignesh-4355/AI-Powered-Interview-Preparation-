from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'mock', views.MockInterviewViewSet, basename='mock-interview')
router.register(r'mock/questions', views.InterviewQuestionViewSet, basename='interview-questions')

urlpatterns = [
    path('', include(router.urls)),
]