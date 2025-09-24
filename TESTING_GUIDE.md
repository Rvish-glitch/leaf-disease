# 🧪 Testing Your Docker Deployment

This guide provides comprehensive testing methods for your Dockerized leaf disease detection application.

## Prerequisites Check

### 1. Docker Installation Test
```bash
# Check Docker version
docker --version

# Check Docker Compose version  
docker-compose --version

# Test Docker daemon
docker run hello-world
```

### 2. Project Structure Check
```bash
# Verify all Docker files exist
ls -la backend/Dockerfile
ls -la frontend/Dockerfile
ls -la docker-compose.yml
ls -la deploy.sh
```

## Testing Methods

### Method 1: Quick Health Check Test

```bash
# Build and start services
sudo docker-compose up --build -d

# Wait 30 seconds for services to start
sleep 30

# Test backend health
curl -f http://localhost:5000/health

# Test frontend access
curl -f http://localhost:80

# Check service status
sudo docker-compose ps
```

### Method 2: Interactive Testing

```bash
# Start services with logs visible
sudo docker-compose up --build

# In another terminal, run tests:
# Test backend API
curl -X GET http://localhost:5000/health | jq '.'

# Test file upload
curl -X POST -F "file=@backend/tomato_-_septoria_leaf_spot.jpg" \
  http://localhost:5000/predict | jq '.'
```

### Method 3: Using the Deploy Script

```bash
# Make script executable (if not already)
chmod +x deploy.sh

# Interactive menu
./deploy.sh

# Or direct commands
./deploy.sh dev    # Development deployment
./deploy.sh logs   # View logs
./deploy.sh stop   # Stop services
```

### Method 4: Manual Container Testing

```bash
# Test backend only
cd backend
sudo docker build -t leaf-backend .
sudo docker run -p 5000:5000 -e HF_REPO_ID=rishabh914/leaf-disease-detection leaf-backend

# Test frontend only
cd frontend  
sudo docker build -t leaf-frontend .
sudo docker run -p 3000:80 leaf-frontend
```

## Test Endpoints

### Backend API Tests

```bash
# Health check
curl http://localhost:5000/health

# Root endpoint
curl http://localhost:5000/

# Predictions endpoint
curl http://localhost:5000/predictions

# File upload test (using sample image)
curl -X POST \
  -F "file=@backend/tomato_-_septoria_leaf_spot.jpg" \
  http://localhost:5000/predict
```

### Frontend Tests

```bash
# Homepage access
curl -I http://localhost:80

# Check if static files load
curl -I http://localhost:80/static/css/main.css
curl -I http://localhost:80/static/js/main.js
```

## Expected Responses

### ✅ Healthy Backend Response
```json
{
  "status": "healthy",
  "message": "Leaf Disease Detection API is running",
  "model_source": "Hugging Face",
  "hf_repo": "rishabh914/leaf-disease-detection",
  "version": "2.0"
}
```

### ✅ Successful Prediction Response
```json
{
  "success": true,
  "prediction": {
    "class": "Tomato___Septoria_leaf_spot",
    "confidence": 0.95,
    "probabilities": {...}
  },
  "model_source": "Hugging Face",
  "hf_repo": "rishabh914/leaf-disease-detection"
}
```

### ✅ Healthy Container Status
```bash
$ sudo docker-compose ps
NAME                  IMAGE               COMMAND                  SERVICE     CREATED         STATUS                   PORTS
leaf-disease-backend  leaf-backend        "gunicorn --bind 0.0…"   backend     2 minutes ago   Up 2 minutes (healthy)   0.0.0.0:5000->5000/tcp
leaf-disease-frontend leaf-frontend       "/docker-entrypoint.…"   frontend    2 minutes ago   Up 2 minutes (healthy)   0.0.0.0:80->80/tcp
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Permission Denied (Docker)
```bash
# Solution: Add user to docker group and restart session
sudo usermod -aG docker $USER
# Then logout and login again, or run:
newgrp docker
```

#### 2. Port Already in Use
```bash
# Check what's using the port
sudo netstat -tulpn | grep :5000
sudo netstat -tulpn | grep :80

# Kill processes or change ports in docker-compose.yml
```

#### 3. Container Build Failures
```bash
# Clear Docker cache and rebuild
sudo docker system prune -a
sudo docker-compose build --no-cache
```

#### 4. Model Download Issues
```bash
# Check logs for Hugging Face connection
sudo docker-compose logs backend

# Common issue: No internet or wrong repo ID
```

#### 5. Frontend Not Loading
```bash
# Check nginx container
sudo docker-compose exec frontend nginx -t
sudo docker-compose logs frontend
```

## Performance Testing

### Load Testing Backend
```bash
# Install Apache Bench
sudo dnf install httpd-tools

# Test API performance
ab -n 10 -c 2 http://localhost:5000/health

# Test with file upload (create test script)
for i in {1..5}; do
  curl -X POST -F "file=@backend/tomato_-_septoria_leaf_spot.jpg" \
    http://localhost:5000/predict &
done
wait
```

### Memory and CPU Monitoring
```bash
# Monitor container resources
sudo docker stats

# Check detailed container info
sudo docker-compose exec backend ps aux
sudo docker-compose exec backend df -h
```

## Production Readiness Tests

### Security Tests
```bash
# Check for exposed secrets
sudo docker-compose exec backend env | grep -E "(SECRET|KEY|PASSWORD)"

# Verify no development ports exposed
sudo docker-compose ps
```

### Health Check Tests
```bash
# Test health check endpoints
curl -f http://localhost:5000/health || echo "Backend health check failed"
curl -f http://localhost:80 || echo "Frontend health check failed"

# Check Docker health status
sudo docker inspect $(sudo docker-compose ps -q backend) | grep -A 5 '"Health"'
```

### Backup and Recovery Tests
```bash
# Test volume persistence
sudo docker-compose down
sudo docker-compose up -d
# Verify uploads and predictions persist
```

## Automated Testing Script

Save this as `test-deployment.sh`:

```bash
#!/bin/bash
set -e

echo "🧪 Starting automated deployment tests..."

# Build and start services
echo "📦 Building and starting services..."
sudo docker-compose up --build -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 45

# Test backend health
echo "🔍 Testing backend health..."
if curl -f http://localhost:5000/health; then
    echo "✅ Backend health check passed"
else
    echo "❌ Backend health check failed"
    exit 1
fi

# Test frontend access
echo "🔍 Testing frontend access..."
if curl -f http://localhost:80 > /dev/null; then
    echo "✅ Frontend access test passed"
else
    echo "❌ Frontend access test failed"
    exit 1
fi

# Test prediction API
echo "🔍 Testing prediction API..."
if [ -f "backend/tomato_-_septoria_leaf_spot.jpg" ]; then
    if curl -X POST -F "file=@backend/tomato_-_septoria_leaf_spot.jpg" \
       http://localhost:5000/predict > /dev/null; then
        echo "✅ Prediction API test passed"
    else
        echo "❌ Prediction API test failed"
    fi
else
    echo "⚠️  Sample image not found, skipping prediction test"
fi

# Check container status
echo "🔍 Checking container status..."
sudo docker-compose ps

echo "🎉 All tests completed!"
echo "🌐 Access your app at:"
echo "   Frontend: http://localhost"
echo "   Backend API: http://localhost:5000"
```

## Manual UI Testing

1. **Open browser to http://localhost**
2. **Upload a test image** (use `backend/tomato_-_septoria_leaf_spot.jpg`)
3. **Click "Detect Disease"**
4. **Verify prediction results appear**
5. **Check browser console** for any errors (F12)

## Cleanup After Testing

```bash
# Stop services
sudo docker-compose down

# Remove containers and volumes
sudo docker-compose down -v

# Clean up images (optional)
sudo docker system prune -a
```

Remember to test both development and production configurations!
