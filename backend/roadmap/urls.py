from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoadmapViewSet

router = DefaultRouter()
router.register(r'roadmap', RoadmapViewSet, basename='roadmap')

urlpatterns = [
    path('', include(router.urls)),
]
