export interface SolarCalculation {
  latitude: number;
  longitude: number;
  optimal_pitch: number;
  optimal_azimuth: number;
  annual_solar_radiation: number;
  efficiency_factor: number;
  estimated_annual_output: number;
  calculation_date: string;
}

export interface CoordinateInput {
  latitude: number;
  longitude: number;
}

export interface MapLocation {
  lat: number;
  lng: number;
} 