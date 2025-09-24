#!/bin/bash
set -e

echo "🧪 Starting automated deployment tests..."
echo "========================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    local status=$1
    local message=$2
    case $status in
        "success") echo -e "${GREEN}✅ $message${NC}" ;;
        "error") echo -e "${RED}❌ $message${NC}" ;;
        "warning") echo -e "${YELLOW}⚠️  $message${NC}" ;;
        "info") echo -e "${BLUE}ℹ️  $message${NC}" ;;
    esac
}

# Function to check if port is available
check_port() {
    local port=$1
    if netstat -tuln | grep -q ":$port "; then
        return 1
    fi
    return 0
}

# Check prerequisites
echo "🔍 Checking prerequisites..."

# Check Docker
if ! command -v docker &> /dev/null; then
    print_status "error" "Docker is not installed"
    exit 1
fi
print_status "success" "Docker is available"

# Check Docker Compose
if ! command -v docker-compose &> /dev/null; then
    print_status "error" "Docker Compose is not installed"
    exit 1
fi
print_status "success" "Docker Compose is available"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_status "error" "Docker daemon is not running. Starting Docker..."
    sudo systemctl start docker
    sleep 5
    if ! docker info > /dev/null 2>&1; then
        print_status "error" "Failed to start Docker daemon"
        exit 1
    fi
fi
print_status "success" "Docker daemon is running"

# Check for required files
required_files=("docker-compose.yml" "backend/Dockerfile" "frontend/Dockerfile")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        print_status "error" "Required file missing: $file"
        exit 1
    fi
done
print_status "success" "All required Docker files found"

# Check if ports are available
if ! check_port 5000; then
    print_status "warning" "Port 5000 is in use, stopping existing services..."
    sudo docker-compose down 2>/dev/null || true
    sleep 2
fi

if ! check_port 80; then
    print_status "warning" "Port 80 is in use, this might cause conflicts"
fi

# Build and start services
echo ""
print_status "info" "Building and starting services..."
if sudo docker-compose up --build -d; then
    print_status "success" "Services started successfully"
else
    print_status "error" "Failed to start services"
    sudo docker-compose logs
    exit 1
fi

# Wait for services to be ready
print_status "info" "Waiting for services to initialize..."
sleep 30

# Function to wait for service
wait_for_service() {
    local url=$1
    local name=$2
    local max_attempts=20
    local attempt=0
    
    while [ $attempt -lt $max_attempts ]; do
        if curl -f -s "$url" > /dev/null 2>&1; then
            return 0
        fi
        attempt=$((attempt + 1))
        sleep 3
        echo -n "."
    done
    return 1
}

# Test backend health
echo ""
print_status "info" "Testing backend health..."
if wait_for_service "http://localhost:5000/health" "backend"; then
    print_status "success" "Backend health check passed"
    
    # Get detailed health info
    echo "Backend response:"
    curl -s http://localhost:5000/health | jq '.' 2>/dev/null || curl -s http://localhost:5000/health
else
    print_status "error" "Backend health check failed"
    echo "Backend logs:"
    sudo docker-compose logs backend | tail -20
fi

# Test frontend access
echo ""
print_status "info" "Testing frontend access..."
if wait_for_service "http://localhost:80" "frontend"; then
    print_status "success" "Frontend access test passed"
else
    print_status "error" "Frontend access test failed"
    echo "Frontend logs:"
    sudo docker-compose logs frontend | tail -10
fi

# Test prediction API if sample image exists
echo ""
print_status "info" "Testing prediction API..."
if [ -f "backend/tomato_-_septoria_leaf_spot.jpg" ]; then
    if curl -X POST -F "file=@backend/tomato_-_septoria_leaf_spot.jpg" \
       -s http://localhost:5000/predict | grep -q "success"; then
        print_status "success" "Prediction API test passed"
    else
        print_status "error" "Prediction API test failed"
        echo "Trying to get error details..."
        curl -X POST -F "file=@backend/tomato_-_septoria_leaf_spot.jpg" \
             http://localhost:5000/predict 2>/dev/null | jq '.' 2>/dev/null || echo "API returned invalid JSON"
    fi
else
    print_status "warning" "Sample image not found, skipping prediction test"
fi

# Check container status
echo ""
print_status "info" "Checking container status..."
sudo docker-compose ps

# Check container health
echo ""
print_status "info" "Checking container health status..."
backend_health=$(sudo docker inspect $(sudo docker-compose ps -q backend) 2>/dev/null | jq -r '.[0].State.Health.Status // "no-health-check"')
frontend_health=$(sudo docker inspect $(sudo docker-compose ps -q frontend) 2>/dev/null | jq -r '.[0].State.Health.Status // "no-health-check"')

echo "Backend health: $backend_health"
echo "Frontend health: $frontend_health"

# Check resource usage
echo ""
print_status "info" "Container resource usage:"
sudo docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"

# Final summary
echo ""
echo "🎉 Testing Summary:"
echo "==================="
print_status "success" "Docker deployment is working!"
echo ""
echo "🌐 Access your application:"
echo "   Frontend: http://localhost"
echo "   Backend API: http://localhost:5000"
echo "   Health Check: http://localhost:5000/health"
echo ""
echo "📋 Useful commands:"
echo "   View logs: sudo docker-compose logs"
echo "   Stop services: sudo docker-compose down"
echo "   Restart: sudo docker-compose restart"
echo ""

# Optional: Open browser
if command -v xdg-open &> /dev/null; then
    read -p "Do you want to open the application in your browser? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        xdg-open http://localhost &
    fi
fi

print_status "success" "Test completed successfully! Your Docker deployment is ready."
