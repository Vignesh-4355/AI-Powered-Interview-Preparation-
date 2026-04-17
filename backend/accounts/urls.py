from django.urls import path
from .views import (
    register,
    login,
    logout,
    profile,
    dashboard_data,
    api_test
)

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('dashboard/', dashboard_data, name='dashboard_data'),
    path('api-test/', api_test, name='api_test'),
]
