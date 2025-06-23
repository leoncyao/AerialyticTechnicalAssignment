# Solar Panel Optimizer

A full-stack web application that calculates optimal pitch and azimuth angles for solar panel installation based on geographic coordinates. This tool simulates how an intelligent solar design assistant might behave when assessing a building site.

## Features

- **Geographic Input**: Input latitude and longitude coordinates manually or via map selection
- **Offset Angle Support**: Optional input for ground surface angle adjustments
- **Solar Calculations**: Optimal tilt (pitch) and azimuth calculations using the Liu-Jordan model
- **Solar Radiation Estimates**: Annual solar radiation and energy output estimates
- **Modern UI**: React-based frontend with Material-UI components
- **RESTful API**: Django backend with comprehensive validation
- **Containerized**: Docker support for easy deployment
- **Kubernetes Ready**: Complete K8s manifests and Helm chart
- **Scalable**: Designed for horizontal scaling and cloud deployment

## Architecture

### Frontend (React/TypeScript)
- **Framework**: React 18 with TypeScript
- **UI Library**: Material-UI (MUI) for consistent design
- **State Management**: React hooks for local state
- **HTTP Client**: Fetch API for backend communication
- **Build Tool**: Create React App with TypeScript template

### Backend (Django/Python)
- **Framework**: Django 5.2 with Django REST Framework
- **Solar Calculations**: pvlib library for solar geometry
- **Database**: SQLite (development) / PostgreSQL (production)
- **CORS**: django-cors-headers for frontend communication
- **Validation**: Comprehensive input validation and error handling

### Infrastructure
- **Containerization**: Docker with multi-stage builds
- **Orchestration**: Docker Compose for local development
- **Kubernetes**: Complete K8s manifests with services and ingress
- **Helm**: Chart for easy deployment and configuration
- **Monitoring**: Health checks and readiness probes

## Solar Modeling Logic

### Optimal Tilt Calculation (Liu-Jordan Model)
The application uses the Liu-Jordan model for calculating optimal tilt angles:

1. **Base Tilt**: Approximately equal to the absolute latitude
2. **Seasonal Adjustment**: Higher latitudes receive seasonal adjustments
   - Northern Hemisphere: +5° for better winter performance
   - Southern Hemisphere: -5° for better summer performance
3. **Offset Integration**: User-provided offset angle is added to the calculation
4. **Constraints**: Tilt is constrained between 0° and 90°

### Optimal Azimuth Calculation
- **Northern Hemisphere**: 180° (south-facing) for maximum solar exposure
- **Southern Hemisphere**: 0° (north-facing) for maximum solar exposure

### Solar Radiation Estimation
The application uses pvlib's solar position algorithms:

1. **Solar Position**: Calculates solar zenith angles throughout the year
2. **Clear Sky Model**: Estimates radiation under clear sky conditions
3. **Tilted Surface**: Calculates radiation on tilted panels
4. **Fallback Model**: Empirical relationships when pvlib calculations fail

### References
- Liu, B.Y.H. and Jordan, R.C., 1960. The interrelationship and characteristic distribution of direct, diffuse and total solar radiation. Solar Energy, 4(3), pp.1-19.
- Duffie, J.A. and Beckman, W.A., 2013. Solar engineering of thermal processes. John Wiley & Sons.
- NREL (National Renewable Energy Laboratory) solar position algorithms

## Setup Instructions

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.10+ (for local development)
- Kubernetes cluster (for production deployment)

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AerialyticTechnicalAssignment
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm start
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Health Check: http://localhost:8000/api/health/

### Docker Deployment

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

### Kubernetes Deployment

1. **Build Docker images**
   ```bash
   docker build -t solar-backend:latest ./backend
   docker build -t solar-frontend:latest ./frontend
   ```

2. **Deploy to Kubernetes**
   ```bash
   kubectl apply -f k8s/
   ```

3. **Deploy with Helm**
   ```bash
   helm install solar-panel-calculator ./helm
   ```

## API Documentation

### Calculate Solar Angles
**Endpoint**: `POST /api/solar/calculate/`

**Request Body**:
```json
{
  "latitude": 40.7128,
  "longitude": -74.0060,
  "offset_angle": 5.0  // optional
}
```

**Response**:
```json
{
  "optimal_pitch": 45.0,
  "optimal_azimuth": 180.0,
  "annual_solar_radiation": 4.5,
  "efficiency_factor": 0.75,
  "estimated_annual_output": 1230.5,
  "calculation_date": "2024-01-15"
}
```

### Health Check
**Endpoint**: `GET /api/health/`

**Response**:
```json
{
  "status": "healthy",
  "service": "solar-panel-calculator",
  "version": "1.0.0"
}
```

## Configuration

### Environment Variables

**Backend**:
- `DEBUG`: Enable/disable debug mode
- `SECRET_KEY`: Django secret key
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts

**Frontend**:
- `REACT_APP_API_URL`: Backend API URL

### Kubernetes Configuration

The application uses ConfigMaps and Secrets for configuration:

```bash
# Create ConfigMap
kubectl apply -f k8s/configmap.yaml

# Create Secret (update the secret key)
kubectl apply -f k8s/configmap.yaml
```

## Assumptions and Limitations

### Current Limitations
1. **Simplified Solar Model**: Uses clear sky model instead of actual weather data
2. **No Shading Analysis**: Does not consider surrounding structures or terrain
3. **Fixed Efficiency**: Uses a constant system efficiency factor
4. **No Terrain Data**: Does not account for elevation or complex terrain
5. **Limited Validation**: Basic coordinate validation only

### Future Enhancements
1. **Weather Integration**: Real-time weather data for more accurate calculations
2. **Shading Analysis**: 3D modeling of surrounding structures
3. **Terrain Modeling**: Elevation data integration
4. **Dynamic Horizon**: Complex terrain horizon modeling
5. **PV Simulation**: Detailed system modeling with specific panel types
6. **Historical Data**: Solar radiation historical analysis
7. **Economic Analysis**: ROI calculations and payback periods

## Production Considerations

### Security
- Change default secret keys
- Enable HTTPS/TLS
- Implement proper authentication
- Use environment-specific configurations

### Performance
- Enable database connection pooling
- Implement caching for calculations
- Use CDN for static assets
- Monitor resource usage

### Monitoring
- Implement application metrics
- Set up logging aggregation
- Configure alerting
- Monitor solar calculation accuracy

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- NREL for solar position algorithms
- pvlib community for solar calculation libraries
- Material-UI for the component library
- Django and React communities for excellent frameworks 