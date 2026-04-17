from django.urls import path
from .views import AnalyticsView, UpdateProgressView

urlpatterns = [
    path('', AnalyticsView.as_view(), name='analytics'),
    path('update/', UpdateProgressView.as_view(), name='update-progress'),
]
