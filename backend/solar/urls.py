from django.urls import path
from . import views

app_name = 'solar'

urlpatterns = [
    path('api/solar/calculate/', views.calculate_solar_angles, name='calculate_solar_angles'),
    path('api/health/', views.health_check, name='health_check'),
] 