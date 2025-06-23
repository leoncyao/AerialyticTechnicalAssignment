import React, { useState } from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { Container, Box, Typography, Paper } from '@mui/material';
import SolarPanelCalculator from './components/SolarPanelCalculator';
import './App.css';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="lg">
        <Box sx={{ my: 4 }}>
          <Typography variant="h3" component="h1" gutterBottom align="center" color="primary">
            🌞 Solar Panel Optimizer
          </Typography>
          <Typography variant="h6" component="h2" gutterBottom align="center" color="text.secondary">
            Calculate optimal pitch and azimuth for solar panels based on your location
          </Typography>
          
          <Paper elevation={3} sx={{ p: 3, mt: 3 }}>
            <SolarPanelCalculator />
          </Paper>
        </Box>
      </Container>
    </ThemeProvider>
  );
}

export default App;
