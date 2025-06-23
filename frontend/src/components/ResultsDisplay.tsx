import React from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Card,
  CardContent,
  Divider
} from '@mui/material';
import {
  TrendingUp,
  CompassCalibration,
  WbSunny,
  ElectricBolt
} from '@mui/icons-material';
import { SolarCalculation } from '../types/solar';

interface ResultsDisplayProps {
  results: SolarCalculation;
}

const ResultsDisplay: React.FC<ResultsDisplayProps> = ({ results }) => {
  const formatNumber = (num: number, decimals: number = 2) => {
    return num.toFixed(decimals);
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString();
  };

  return (
    <Paper elevation={3} sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom color="primary">
        🌞 Solar Panel Optimization Results
      </Typography>
      
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Calculated on {formatDate(results.calculation_date)} for coordinates: {results.latitude.toFixed(6)}, {results.longitude.toFixed(6)}
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} sm={6} md={3}>
          <Card elevation={2}>
            <CardContent sx={{ textAlign: 'center' }}>
              <TrendingUp sx={{ fontSize: 40, color: 'primary.main', mb: 1 }} />
              <Typography variant="h6" gutterBottom>
                Optimal Pitch
              </Typography>
              <Typography variant="h4" color="primary">
                {formatNumber(results.optimal_pitch)}°
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Tilt angle from horizontal
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card elevation={2}>
            <CardContent sx={{ textAlign: 'center' }}>
              <CompassCalibration sx={{ fontSize: 40, color: 'primary.main', mb: 1 }} />
              <Typography variant="h6" gutterBottom>
                Optimal Azimuth
              </Typography>
              <Typography variant="h4" color="primary">
                {formatNumber(results.optimal_azimuth)}°
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Direction from true north
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card elevation={2}>
            <CardContent sx={{ textAlign: 'center' }}>
              <WbSunny sx={{ fontSize: 40, color: 'primary.main', mb: 1 }} />
              <Typography variant="h6" gutterBottom>
                Solar Radiation
              </Typography>
              <Typography variant="h4" color="primary">
                {formatNumber(results.annual_solar_radiation)} kWh/m²
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Annual solar radiation
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card elevation={2}>
            <CardContent sx={{ textAlign: 'center' }}>
              <ElectricBolt sx={{ fontSize: 40, color: 'primary.main', mb: 1 }} />
              <Typography variant="h6" gutterBottom>
                Annual Output
              </Typography>
              <Typography variant="h4" color="primary">
                {formatNumber(results.estimated_annual_output)} kWh
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Estimated per kW installed
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Divider sx={{ my: 3 }} />

      <Box sx={{ mt: 2 }}>
        <Typography variant="h6" gutterBottom>
          Additional Information
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={6}>
            <Typography variant="body2">
              <strong>Efficiency Factor:</strong> {formatNumber(results.efficiency_factor * 100)}%
            </Typography>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Typography variant="body2">
              <strong>Location:</strong> {results.latitude > 0 ? 'Northern' : 'Southern'} Hemisphere
            </Typography>
          </Grid>
        </Grid>
      </Box>

      <Box sx={{ mt: 3, p: 2, bgcolor: 'grey.50', borderRadius: 1 }}>
        <Typography variant="body2" color="text.secondary">
          <strong>Note:</strong> These calculations are estimates based on solar modeling algorithms. 
          Actual performance may vary due to local weather conditions, shading, and panel quality. 
          Consult with a solar professional for detailed site assessment.
        </Typography>
      </Box>
    </Paper>
  );
};

export default ResultsDisplay; 