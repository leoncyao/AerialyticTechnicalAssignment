import React, { useState, useEffect } from 'react';
import {
  Box,
  TextField,
  Button,
  Typography,
  Paper,
  CircularProgress,
  Alert
} from '@mui/material';
import { LocationOn } from '@mui/icons-material';

interface CoordinateFormProps {
  coordinates: { lat: number; lng: number } | null;
  onCalculate: (lat: number, lng: number, offsetAngle?: number) => void;
  loading: boolean;
}

const CoordinateForm: React.FC<CoordinateFormProps> = ({ 
  coordinates, 
  onCalculate, 
  loading 
}) => {
  const [latitude, setLatitude] = useState<string>('');
  const [longitude, setLongitude] = useState<string>('');
  const [offsetAngle, setOffsetAngle] = useState<string>('');
  const [errors, setErrors] = useState<{ [key: string]: string }>({});

  useEffect(() => {
    if (coordinates) {
      setLatitude(coordinates.lat.toString());
      setLongitude(coordinates.lng.toString());
      setErrors({});
    }
  }, [coordinates]);

  const validateForm = (): boolean => {
    const newErrors: { [key: string]: string } = {};

    // Validate latitude
    if (!latitude.trim()) {
      newErrors.latitude = 'Latitude is required';
    } else {
      const lat = parseFloat(latitude);
      if (isNaN(lat) || lat < -90 || lat > 90) {
        newErrors.latitude = 'Latitude must be between -90 and 90 degrees';
      }
    }

    // Validate longitude
    if (!longitude.trim()) {
      newErrors.longitude = 'Longitude is required';
    } else {
      const lng = parseFloat(longitude);
      if (isNaN(lng) || lng < -180 || lng > 180) {
        newErrors.longitude = 'Longitude must be between -180 and 180 degrees';
      }
    }

    // Validate offset angle (optional)
    if (offsetAngle.trim()) {
      const offset = parseFloat(offsetAngle);
      if (isNaN(offset) || offset < -90 || offset > 90) {
        newErrors.offsetAngle = 'Offset angle must be between -90 and 90 degrees';
      }
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (validateForm()) {
      const lat = parseFloat(latitude);
      const lng = parseFloat(longitude);
      const offset = offsetAngle.trim() ? parseFloat(offsetAngle) : undefined;
      
      onCalculate(lat, lng, offset);
    }
  };

  const handleClear = () => {
    setLatitude('');
    setLongitude('');
    setOffsetAngle('');
    setErrors({});
  };

  const handleGetCurrentLocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const lat = position.coords.latitude;
          const lng = position.coords.longitude;
          setLatitude(lat.toString());
          setLongitude(lng.toString());
          setErrors({});
        },
        (error) => {
          console.error('Error getting location:', error);
        }
      );
    }
  };

  return (
    <Paper elevation={2} sx={{ p: 3 }}>
      <Typography variant="h6" gutterBottom>
        Location Details
      </Typography>
      
      <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
        <TextField
          fullWidth
          label="Latitude"
          value={latitude}
          onChange={(e) => setLatitude(e.target.value)}
          error={!!errors.latitude}
          helperText={errors.latitude || 'Enter latitude (-90 to 90 degrees)'}
          margin="normal"
          type="number"
          inputProps={{ step: 'any' }}
          placeholder="e.g., 40.7128"
        />

        <TextField
          fullWidth
          label="Longitude"
          value={longitude}
          onChange={(e) => setLongitude(e.target.value)}
          error={!!errors.longitude}
          helperText={errors.longitude || 'Enter longitude (-180 to 180 degrees)'}
          margin="normal"
          type="number"
          inputProps={{ step: 'any' }}
          placeholder="e.g., -74.0060"
        />

        <TextField
          fullWidth
          label="Offset Angle (Optional)"
          value={offsetAngle}
          onChange={(e) => setOffsetAngle(e.target.value)}
          error={!!errors.offsetAngle}
          helperText={
            errors.offsetAngle || 
            'Angle between ground surface and horizontal line (-90 to 90 degrees)'
          }
          margin="normal"
          type="number"
          inputProps={{ step: 'any' }}
          placeholder="e.g., 5 (for 5° slope)"
        />

        <Box sx={{ mt: 3, display: 'flex', gap: 2 }}>
          <Button
            type="submit"
            variant="contained"
            disabled={loading || !latitude.trim() || !longitude.trim()}
            sx={{ flex: 1 }}
          >
            {loading ? (
              <>
                <CircularProgress size={20} sx={{ mr: 1 }} />
                Calculating...
              </>
            ) : (
              'Calculate Optimal Angles'
            )}
          </Button>
          
          <Button
            variant="outlined"
            onClick={handleClear}
            disabled={loading}
          >
            Clear
          </Button>
        </Box>

        {coordinates && (
          <Alert severity="info" sx={{ mt: 2 }}>
            Location selected from map: {coordinates.lat.toFixed(6)}, {coordinates.lng.toFixed(6)}
          </Alert>
        )}
      </Box>
      
      <Box sx={{ mt: 2 }}>
        <Button
          variant="outlined"
          onClick={handleGetCurrentLocation}
          startIcon={<LocationOn />}
          fullWidth
        >
          Use Current Location
        </Button>
      </Box>
    </Paper>
  );
};

export default CoordinateForm; 