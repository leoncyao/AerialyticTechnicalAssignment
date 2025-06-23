from django.db import models
from django.utils import timezone

class SolarCalculation(models.Model):
    """
    Model to store solar panel calculation requests and results.
    This can be used for analytics, caching, and tracking usage patterns.
    """
    latitude = models.FloatField(help_text="Latitude coordinate")
    longitude = models.FloatField(help_text="Longitude coordinate")
    offset_angle = models.FloatField(
        null=True, 
        blank=True, 
        help_text="Optional offset angle between ground surface and horizontal line"
    )
    
    # Calculated results
    optimal_pitch = models.FloatField(help_text="Optimal tilt angle in degrees")
    optimal_azimuth = models.FloatField(help_text="Optimal azimuth angle in degrees")
    annual_solar_radiation = models.FloatField(
        help_text="Annual solar radiation in kWh/m²/day"
    )
    efficiency_factor = models.FloatField(
        help_text="System efficiency factor (0-1)"
    )
    estimated_annual_output = models.FloatField(
        help_text="Estimated annual energy output in kWh"
    )
    
    # Metadata
    created_at = models.DateTimeField(default=timezone.now)
    calculation_date = models.DateField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['latitude', 'longitude']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Solar calculation for ({self.latitude}, {self.longitude}) - {self.created_at}"
