from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .solar_calculator import SolarCalculator
from .models import SolarCalculation

# Create your tests here.

class SolarCalculatorUnitTests(TestCase):
    def setUp(self):
        self.calc = SolarCalculator()

    def test_optimal_tilt_equator(self):
        result = self.calc.calculate_optimal_angles(0, 0)
        self.assertAlmostEqual(float(result['optimal_pitch']), 0, delta=1)

    def test_optimal_tilt_northern_latitude(self):
        result = self.calc.calculate_optimal_angles(40, -74)
        pitch = float(result['optimal_pitch'])
        self.assertTrue(40 <= pitch <= 50)

    def test_optimal_azimuth_north(self):
        result = self.calc.calculate_optimal_angles(40, -74)
        self.assertEqual(float(result['optimal_azimuth']), 180.0)

    def test_optimal_azimuth_south(self):
        result = self.calc.calculate_optimal_angles(-33, 151)
        self.assertEqual(float(result['optimal_azimuth']), 0.0)

    def test_offset_angle_applied(self):
        result = self.calc.calculate_optimal_angles(30, 0, offset_angle=15)
        self.assertAlmostEqual(float(result['optimal_pitch']), 50, delta=1)

    def test_invalid_latitude(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_optimal_angles(100, 0)

    def test_invalid_longitude(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_optimal_angles(0, 200)

class SolarCalculationAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/solar/calculate/'

    def test_api_valid_request(self):
        data = {"latitude": 40.7128, "longitude": -74.0060}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('optimal_pitch', response.data)
        self.assertIn('optimal_azimuth', response.data)

    def test_api_with_offset_angle(self):
        data = {"latitude": 40.7128, "longitude": -74.0060, "offset_angle": 5}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('optimal_pitch', response.data)

    def test_api_missing_latitude(self):
        data = {"longitude": -74.0060}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_invalid_latitude(self):
        data = {"latitude": 100, "longitude": 0}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_invalid_offset_angle(self):
        data = {"latitude": 40, "longitude": 0, "offset_angle": 200}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_health_check(self):
        response = self.client.get('/api/health/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'healthy')
