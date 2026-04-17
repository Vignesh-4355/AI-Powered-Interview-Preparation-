from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AptitudeQuestionViewSet, UserAttemptViewSet

router= DefaultRouter()
router.register(r'aptitude', AptitudeQuestionViewSet, basename='aptitude')
router.register(r'user-attempts', UserAttemptViewSet, basename='user-attempts')

urlpatterns = [
   path('', include(router.urls)),
]
