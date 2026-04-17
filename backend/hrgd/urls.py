from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HRQuestionViewSet, GDTopicViewSet

router = DefaultRouter()
router.register(r'hr-questions', HRQuestionViewSet, basename='hr-questions')
router.register(r'gd-topics', GDTopicViewSet, basename='gd-topics')

urlpatterns = [
    path('', include(router.urls)),
]
