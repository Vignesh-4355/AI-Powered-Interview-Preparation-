from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet, CompanyQuestionViewSet

router = DefaultRouter()
router.register(r'companies', CompanyViewSet, basename='company')
router.register(r'questions', CompanyQuestionViewSet, basename='company-questions')

urlpatterns = [
    path('', include(router.urls)),
]
