# Backend

Django REST API for solar calculations.

## Setup with uv

This project uses [uv](https://github.com/astral-sh/uv) for fast Python package management.

### Prerequisites
- Python 3.10+
- uv (install with: `curl -LsSf https://astral.sh/uv/install.sh | sh`)

### Installation
1. Clone the repository and navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

3. Run Django migrations:
   ```bash
   uv run python manage.py migrate
   ```

4. Create a superuser (optional):
   ```bash
   uv run python manage.py createsuperuser
   ```

### Development

Start the development server:
```bash
uv run python manage.py runserver
```

The API will be available at `http://localhost:8000/`

### Testing

Run tests:
```bash
uv run pytest
```

### Code Quality

Format code:
```bash
uv run black .
uv run isort .
```

Lint code:
```bash
uv run flake8
```

### Production

For production deployment, see the `k8s/` directory for Kubernetes manifests.

## Project Structure

- `solar/` - Main Django app with solar calculation models and views
- `solar_backend/` - Django project settings and configuration
- `manage.py` - Django management script
- `pyproject.toml` - Project dependencies and configuration 