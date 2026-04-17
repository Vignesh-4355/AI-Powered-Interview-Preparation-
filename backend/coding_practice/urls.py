from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CodingQuestionViewSet, UserProgressViewSet

router = DefaultRouter()
router.register(r'coding-questions', CodingQuestionViewSet, basename='coding-question')
router.register(r'user-progress', UserProgressViewSet, basename='user-progress')

urlpatterns = [
    path('', include(router.urls)),
]
