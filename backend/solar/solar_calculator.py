"""
Solar Panel Calculator Module

This module implements solar panel optimization calculations using pvlib and
the Liu and Jordan model for determining optimal tilt and azimuth angles.

References:
- Liu, B.Y.H. and Jordan, R.C., 1960. The interrelationship and characteristic 
  distribution of direct, diffuse and total solar radiation. Solar Energy, 4(3), pp.1-19.
- NREL (National Renewable Energy Laboratory) solar position algorithms
- Duffie, J.A. and Beckman, W.A., 2013. Solar engineering of thermal processes. 
  John Wiley & Sons.

Future enhancements planned:
- Dynamic horizon modeling for complex terrain
- PV simulation with detailed system modeling
- Terrain adjustment using elevation data
- Weather data integration for more accurate predictions
- Shading analysis from surrounding structures
"""

import pvlib
import numpy as np
import pandas as pd
from datetime import datetime, date
from typing import Dict, Optional, Tuple, Union
import logging

logger = logging.getLogger(__name__)

class SolarCalculator:
    """
    Solar panel optimization calculator using pvlib and Liu-Jordan model.
    
    This class provides methods to calculate optimal tilt (pitch) and azimuth
    angles for solar panel installation based on geographic coordinates.
    """
    
    def __init__(self):
        self.system_efficiency = 0.75  # Typical system efficiency factor
        self.panel_area = 1.0  # m², normalized for calculations
        
    def calculate_optimal_angles(self, latitude: float, longitude: float, 
                                offset_angle: Optional[float] = None) -> Dict[str, Union[float, str]]:
        """
        Calculate optimal tilt and azimuth angles for solar panel installation.
        
        Args:
            latitude: Latitude coordinate in decimal degrees
            longitude: Longitude coordinate in decimal degrees
            offset_angle: Optional offset angle between ground surface and horizontal (degrees)
            
        Returns:
            Dictionary containing optimal angles and solar radiation data
        """
        try:
            # Validate inputs
            if not (-90 <= latitude <= 90):
                raise ValueError("Latitude must be between -90 and 90 degrees")
            if not (-180 <= longitude <= 180):
                raise ValueError("Longitude must be between -180 and 180 degrees")
            if offset_angle is not None and not (-90 <= offset_angle <= 90):
                raise ValueError("Offset angle must be between -90 and 90 degrees")
            
            # Calculate optimal tilt using Liu-Jordan model
            optimal_tilt = self._calculate_optimal_tilt(latitude, offset_angle)
            
            # Calculate optimal azimuth (south-facing is optimal in Northern Hemisphere)
            optimal_azimuth = self._calculate_optimal_azimuth(latitude)
            
            # Calculate annual solar radiation
            annual_radiation = self._calculate_annual_radiation(latitude, longitude, optimal_tilt)
            
            # Calculate estimated annual output
            estimated_output = self._calculate_annual_output(annual_radiation)
            
            return {
                'optimal_pitch': round(optimal_tilt, 2),
                'optimal_azimuth': round(optimal_azimuth, 2),
                'annual_solar_radiation': round(annual_radiation, 2),
                'efficiency_factor': self.system_efficiency,
                'estimated_annual_output': round(estimated_output, 2),
                'calculation_date': date.today().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error calculating solar angles: {str(e)}")
            raise
    
    def _calculate_optimal_tilt(self, latitude: float, offset_angle: Optional[float] = None) -> float:
        """
        Calculate optimal tilt angle using the Liu-Jordan model.
        
        The Liu-Jordan model provides a good approximation for optimal tilt
        based on latitude. For most locations, the optimal tilt is approximately
        equal to the latitude.
        
        Args:
            latitude: Latitude coordinate in decimal degrees
            offset_angle: Optional offset angle from horizontal
            
        Returns:
            Optimal tilt angle in degrees
        """
        # Base optimal tilt is approximately equal to latitude
        base_tilt = abs(latitude)
        
        # Adjust for seasonal optimization (slightly higher for winter, lower for summer)
        # This is a simplified approach; more sophisticated models consider seasonal variations
        seasonal_adjustment = 0
        
        if abs(latitude) > 25:  # Higher latitudes benefit from seasonal adjustments
            if latitude > 0:  # Northern hemisphere
                seasonal_adjustment = 5  # Slightly higher tilt for better winter performance
            else:  # Southern hemisphere
                seasonal_adjustment = -5  # Slightly lower tilt
        
        optimal_tilt = base_tilt + seasonal_adjustment
        
        # Apply offset angle if provided
        if offset_angle is not None:
            optimal_tilt += offset_angle
        
        # Constrain to reasonable limits
        optimal_tilt = max(0, min(90, optimal_tilt))
        
        return optimal_tilt
    
    def _calculate_optimal_azimuth(self, latitude: float) -> float:
        """
        Calculate optimal azimuth angle.
        
        In the Northern Hemisphere, south-facing (180°) is optimal.
        In the Southern Hemisphere, north-facing (0°) is optimal.
        
        Args:
            latitude: Latitude coordinate in decimal degrees
            
        Returns:
            Optimal azimuth angle in degrees
        """
        if latitude >= 0:  # Northern Hemisphere
            return 180.0  # South-facing
        else:  # Southern Hemisphere
            return 0.0  # North-facing
    
    def _calculate_annual_radiation(self, latitude: float, longitude: float, 
                                   tilt: float) -> float:
        """
        Calculate annual solar radiation using pvlib.
        
        This method uses pvlib's solar position algorithms and clear sky models
        to estimate annual solar radiation for the given location and tilt.
        
        Args:
            latitude: Latitude coordinate in decimal degrees
            longitude: Longitude coordinate in decimal degrees
            tilt: Panel tilt angle in degrees
            
        Returns:
            Annual solar radiation in kWh/m²/day
        """
        try:
            # Create location object
            location = pvlib.location.Location(latitude, longitude)
            
            # Generate dates for a full year
            start_date = datetime(2024, 1, 1)
            end_date = datetime(2024, 12, 31)
            dates = pd.date_range(start_date, end_date, freq='D')
            
            # Calculate solar position for each day
            solar_position = location.get_solarposition(dates)
            
            # Calculate clear sky radiation (simplified model)
            # In production, this should use actual weather data or more sophisticated models
            clear_sky = location.get_clearsky(dates)
            
            # Calculate radiation on tilted surface
            # This is a simplified calculation; more accurate models consider
            # diffuse radiation, ground reflection, and shading
            ghi = clear_sky['ghi']
            zenith = solar_position['zenith']
            if hasattr(ghi, 'to_numpy'):
                ghi = ghi.to_numpy()
            if hasattr(zenith, 'to_numpy'):
                zenith = zenith.to_numpy()
            radiation_on_tilt = self._calculate_tilted_radiation(
                ghi,  # Global horizontal irradiance as numpy array
                zenith,  # Solar zenith as numpy array
                tilt
            )
            
            # Calculate annual average
            annual_radiation = float(np.mean(radiation_on_tilt) * 365 / 1000)  # Convert to kWh/m²/day
            
            return annual_radiation
            
        except Exception as e:
            logger.warning(f"Error calculating radiation with pvlib: {str(e)}")
            # Fallback to simplified calculation
            return self._fallback_radiation_calculation(latitude, tilt)
    
    def _calculate_tilted_radiation(self, ghi: np.ndarray, zenith: np.ndarray, 
                                   tilt: float) -> np.ndarray:
        """
        Calculate radiation on tilted surface using simplified model.
        
        This is a simplified calculation that could be enhanced with:
        - Diffuse radiation modeling
        - Ground reflection calculations
        - Shading analysis
        
        Args:
            ghi: Global horizontal irradiance
            zenith: Solar zenith angle
            tilt: Panel tilt angle in degrees
            
        Returns:
            Radiation on tilted surface
        """
        # Convert angles to radians
        tilt_rad = np.radians(tilt)
        zenith_rad = np.radians(zenith)
        
        # Calculate angle of incidence
        # This is a simplified calculation assuming south-facing panels
        # More accurate models consider actual azimuth orientation
        cos_incidence = (np.cos(zenith_rad) * np.cos(tilt_rad) + 
                        np.sin(zenith_rad) * np.sin(tilt_rad))
        
        # Ensure cos_incidence is within valid range
        cos_incidence = np.clip(cos_incidence, 0, 1)
        
        # Calculate radiation on tilted surface
        # This assumes direct radiation only; diffuse and reflected components
        # should be included for more accurate results
        radiation_tilted = ghi * cos_incidence
        
        return radiation_tilted
    
    def _fallback_radiation_calculation(self, latitude: float, tilt: float) -> float:
        """
        Fallback radiation calculation using simplified empirical model.
        
        This method provides a rough estimate when pvlib calculations fail.
        It's based on empirical relationships between latitude and solar radiation.
        
        Args:
            latitude: Latitude coordinate in decimal degrees
            tilt: Panel tilt angle in degrees
            
        Returns:
            Estimated annual solar radiation in kWh/m²/day
        """
        # Base radiation varies with latitude
        # Higher latitudes generally receive less solar radiation
        abs_lat = abs(latitude)
        
        if abs_lat < 23.5:  # Tropical regions
            base_radiation = 5.5
        elif abs_lat < 45:  # Temperate regions
            base_radiation = 4.5
        elif abs_lat < 60:  # High latitude regions
            base_radiation = 3.5
        else:  # Polar regions
            base_radiation = 2.5
        
        # Adjust for tilt optimization
        # Optimal tilt generally improves radiation capture
        tilt_factor = 1.0 + 0.1 * (1 - abs(tilt - abs_lat) / 90)
        
        return base_radiation * tilt_factor
    
    def _calculate_annual_output(self, annual_radiation: float) -> float:
        """
        Calculate estimated annual energy output.
        
        Args:
            annual_radiation: Annual solar radiation in kWh/m²/day
            
        Returns:
            Estimated annual energy output in kWh
        """
        # Convert daily radiation to annual
        annual_radiation_total = annual_radiation * 365
        
        # Calculate output considering system efficiency
        annual_output = annual_radiation_total * self.panel_area * self.system_efficiency
        
        return annual_output 