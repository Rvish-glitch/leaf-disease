# Docker Deployment Guide

This project now supports Docker deployment for both development and production environments.

## Project Structure

```
leaf-image-detec/
├── backend/
│   ├── Dockerfile              # Backend Docker configuration
│   ├── .dockerignore          # Backend Docker ignore file
│   ├── app.py                 # Main Flask application
│   ├── requirements.txt       # Python dependencies
│   └── ...
├── frontend/
│   ├── Dockerfile             # Frontend Docker configuration
│   ├── .dockerignore         # Frontend Docker ignore file
│   ├── nginx.conf            # Nginx configuration
│   ├── package.json          # Node.js dependencies
│   └── ...
├── docker-compose.yml         # Multi-container setup
└── README_DOCKER.md          # This file
```

## Quick Start

### Using Docker Compose (Recommended)

1. **Build and run both services:**
   ```bash
   docker-compose up --build
   ```

2. **Access the application:**
   - Frontend: http://localhost:80
   - Backend API: http://localhost:5000

3. **Run in detached mode:**
   ```bash
   docker-compose up -d --build
   ```

4. **Stop the services:**
   ```bash
   docker-compose down
   ```

### Individual Container Deployment

#### Backend Only

1. **Build the backend image:**
   ```bash
   cd backend
   docker build -t leaf-disease-backend .
   ```

2. **Run the backend container:**
   ```bash
   docker run -p 5000:5000 \
     -e HF_REPO_ID=rishabh914/leaf-disease-detection \
     -v $(pwd)/uploads:/app/uploads \
     leaf-disease-backend
   ```

#### Frontend Only

1. **Build the frontend image:**
   ```bash
   cd frontend
   docker build -t leaf-disease-frontend .
   ```

2. **Run the frontend container:**
   ```bash
   docker run -p 80:80 leaf-disease-frontend
   ```

## Railway Deployment

The project is configured to deploy on Railway using Docker:

1. **Push your code to GitHub**

2. **Connect to Railway:**
   - The `railway.toml` and `backend/railway.json` files are configured for Docker deployment
   - Railway will automatically use the Dockerfile instead of Nixpacks

3. **Environment Variables:**
   Set these in Railway dashboard:
   - `HF_REPO_ID=rishabh914/leaf-disease-detection`
   - `PORT=5000` (usually auto-set by Railway)

## Vercel Deployment (Frontend)

For frontend deployment on Vercel:

1. **Build command:** `npm run build`
2. **Output directory:** `build`
3. **Install command:** `npm install`

## Docker Configuration Details

### Backend Dockerfile Features:
- Python 3.10 slim base image
- System dependencies for OpenCV and ML libraries
- Optimized layer caching with requirements.txt
- Gunicorn production server
- Health checks support
- Volume mounts for uploads and predictions

### Frontend Dockerfile Features:
- Multi-stage build (Node.js build + Nginx serve)
- Node.js 18 for React compatibility
- Nginx with custom configuration
- Gzip compression enabled
- Client-side routing support
- Security headers
- Static asset caching

### Docker Compose Features:
- Automatic service dependencies
- Health checks for both services
- Volume persistence
- Network isolation
- Restart policies

## Development vs Production

### Development:
```bash
# Use Docker Compose for local development
docker-compose up --build
```

### Production:
- **Backend:** Deploy to Railway using Docker
- **Frontend:** Deploy to Vercel or use the Docker image
- **Full Stack:** Use Docker Compose on VPS/cloud provider

## Troubleshooting

### Common Issues:

1. **Port conflicts:**
   ```bash
   # Change ports in docker-compose.yml if needed
   ports:
     - "3001:80"  # Instead of "80:80"
   ```

2. **Permission issues:**
   ```bash
   # Make sure start.sh is executable
   chmod +x backend/start.sh
   ```

3. **Memory issues:**
   ```bash
   # Increase Docker memory allocation in Docker Desktop settings
   # Or use single worker in production
   ```

4. **Build failures:**
   ```bash
   # Clean Docker cache
   docker system prune -a
   docker-compose build --no-cache
   ```

### Logs and Debugging:

```bash
# View logs
docker-compose logs backend
docker-compose logs frontend

# Debug containers
docker-compose exec backend bash
docker-compose exec frontend sh
```

## Environment Variables

### Backend:
- `PORT`: Server port (default: 5000)
- `HF_REPO_ID`: Hugging Face model repository
- `PYTHONUNBUFFERED`: Python output buffering

### Frontend:
- No environment variables needed for production build
- API URLs are configured in `src/config.js`

## Performance Optimization

### Backend:
- Single Gunicorn worker (ML models are memory intensive)
- 120s timeout for model loading
- Optimized Docker layers for faster builds

### Frontend:
- Multi-stage build reduces image size
- Nginx gzip compression
- Static asset caching
- Minified production build

## Security Considerations

- No sensitive data in Docker images
- Environment variables for configuration
- Security headers in Nginx
- Regular base image updates recommended

## Monitoring

Health check endpoints:
- Backend: `http://localhost:5000/health`
- Frontend: `http://localhost:80` (Nginx status)

Both services include Docker health checks for automatic restart on failure.
