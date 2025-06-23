from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
import logging

from .solar_calculator import SolarCalculator
from .models import SolarCalculation

logger = logging.getLogger(__name__)

@api_view(['POST'])
def calculate_solar_angles(request):
    """
    API endpoint to calculate optimal solar panel angles.
    
    Expected JSON payload:
    {
        "latitude": float,
        "longitude": float,
        "offset_angle": float (optional)
    }
    
    Returns:
    {
        "optimal_pitch": float,
        "optimal_azimuth": float,
        "annual_solar_radiation": float,
        "efficiency_factor": float,
        "estimated_annual_output": float,
        "calculation_date": string
    }
    """
    try:
        # Parse request data
        data = request.data
        
        # Validate required fields
        if 'latitude' not in data or 'longitude' not in data:
            return Response(
                {'error': 'latitude and longitude are required fields'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Extract and validate coordinates
        try:
            latitude = float(data['latitude'])
            longitude = float(data['longitude'])
        except (ValueError, TypeError):
            return Response(
                {'error': 'latitude and longitude must be valid numbers'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Extract optional offset angle
        offset_angle = None
        if 'offset_angle' in data:
            try:
                offset_angle = float(data['offset_angle'])
            except (ValueError, TypeError):
                return Response(
                    {'error': 'offset_angle must be a valid number'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Perform solar calculations
        calculator = SolarCalculator()
        result = calculator.calculate_optimal_angles(latitude, longitude, offset_angle)
        
        # Store calculation in database for analytics (optional)
        try:
            SolarCalculation.objects.create(
                latitude=latitude,
                longitude=longitude,
                offset_angle=offset_angle,
                optimal_pitch=result['optimal_pitch'],
                optimal_azimuth=result['optimal_azimuth'],
                annual_solar_radiation=result['annual_solar_radiation'],
                efficiency_factor=result['efficiency_factor'],
                estimated_annual_output=result['estimated_annual_output']
            )
        except Exception as e:
            # Log the error but don't fail the request
            logger.warning(f"Failed to store calculation in database: {str(e)}")
        
        return Response(result, status=status.HTTP_200_OK)
        
    except ValueError as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        logger.error(f"Unexpected error in solar calculation: {str(e)}")
        return Response(
            {'error': 'Internal server error'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def health_check(request):
    """
    Health check endpoint for monitoring and deployment verification.
    """
    return Response(
        {
            'status': 'healthy',
            'service': 'solar-panel-calculator',
            'version': '1.0.0'
        },
        status=status.HTTP_200_OK
    )
