import React, { useState } from 'react';
import { Grid, Box, Typography, Alert } from '@mui/material';
import LocationMap from './LocationMap';
import CoordinateForm from './CoordinateForm';
import ResultsDisplay from './ResultsDisplay';
import { SolarCalculation } from '../types/solar';

const SolarPanelCalculator: React.FC = () => {
  const [coordinates, setCoordinates] = useState<{ lat: number; lng: number } | null>(null);
  const [results, setResults] = useState<SolarCalculation | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleLocationSelect = (lat: number, lng: number) => {
    setCoordinates({ lat, lng });
    setError(null);
  };

  const handleCalculate = async (lat: number, lng: number, offsetAngle?: number) => {
    setLoading(true);
    setError(null);
    
    try {
      const requestBody: any = {
        latitude: lat,
        longitude: lng,
      };
      
      // Add offset angle if provided
      if (offsetAngle !== undefined) {
        requestBody.offset_angle = offsetAngle;
      }

      const response = await fetch(`http://localhost:8000/api/solar/calculate/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || 'Failed to calculate solar panel parameters');
      }

      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Select Your Location
      </Typography>
      
      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <LocationMap 
            onLocationSelect={handleLocationSelect}
            selectedLocation={coordinates}
          />
        </Grid>
        
        <Grid item xs={12} md={4}>
          <CoordinateForm 
            coordinates={coordinates}
            onCalculate={handleCalculate}
            loading={loading}
          />
        </Grid>
      </Grid>

      {results && (
        <Box sx={{ mt: 3 }}>
          <ResultsDisplay results={results} />
        </Box>
      )}
    </Box>
  );
};

export default SolarPanelCalculator; 