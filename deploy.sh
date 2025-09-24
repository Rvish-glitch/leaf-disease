#!/bin/bash

# Leaf Disease Detection - Docker Deployment Script

set -e

echo "🐳 Leaf Disease Detection Docker Deployment"
echo "=========================================="

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        echo "❌ Error: Docker is not running. Please start Docker first."
        exit 1
    fi
    echo "✅ Docker is running"
}

# Function to check if docker-compose is available
check_docker_compose() {
    if ! command -v docker-compose &> /dev/null; then
        echo "❌ Error: docker-compose not found. Please install docker-compose."
        exit 1
    fi
    echo "✅ docker-compose is available"
}

# Function to deploy development environment
deploy_dev() {
    echo "🚀 Deploying development environment..."
    docker-compose down --remove-orphans
    docker-compose up --build -d
    echo "✅ Development environment deployed!"
    echo "📱 Frontend: http://localhost"
    echo "🔧 Backend API: http://localhost:5000"
}

# Function to deploy production environment
deploy_prod() {
    echo "🚀 Deploying production environment..."
    docker-compose -f docker-compose.prod.yml down --remove-orphans
    docker-compose -f docker-compose.prod.yml up --build -d
    echo "✅ Production environment deployed!"
    echo "📱 Frontend: http://localhost"
    echo "🔧 Backend API: http://localhost:5000"
}

# Function to stop services
stop_services() {
    echo "🛑 Stopping services..."
    docker-compose down --remove-orphans
    docker-compose -f docker-compose.prod.yml down --remove-orphans 2>/dev/null || true
    echo "✅ Services stopped"
}

# Function to view logs
view_logs() {
    echo "📋 Viewing logs..."
    docker-compose logs -f
}

# Function to clean up Docker resources
cleanup() {
    echo "🧹 Cleaning up Docker resources..."
    docker system prune -f
    docker volume prune -f
    echo "✅ Cleanup completed"
}

# Main menu
show_menu() {
    echo ""
    echo "Select deployment option:"
    echo "1) Deploy Development Environment"
    echo "2) Deploy Production Environment"
    echo "3) Stop All Services"
    echo "4) View Logs"
    echo "5) Cleanup Docker Resources"
    echo "6) Exit"
    echo ""
}

# Main script
main() {
    check_docker
    check_docker_compose

    if [ $# -eq 0 ]; then
        while true; do
            show_menu
            read -p "Enter your choice [1-6]: " choice
            case $choice in
                1) deploy_dev ;;
                2) deploy_prod ;;
                3) stop_services ;;
                4) view_logs ;;
                5) cleanup ;;
                6) echo "👋 Goodbye!"; exit 0 ;;
                *) echo "❌ Invalid option. Please try again." ;;
            esac
        done
    else
        case $1 in
            "dev") deploy_dev ;;
            "prod") deploy_prod ;;
            "stop") stop_services ;;
            "logs") view_logs ;;
            "cleanup") cleanup ;;
            *)
                echo "Usage: $0 [dev|prod|stop|logs|cleanup]"
                echo "  dev     - Deploy development environment"
                echo "  prod    - Deploy production environment"
                echo "  stop    - Stop all services"
                echo "  logs    - View service logs"
                echo "  cleanup - Clean Docker resources"
                exit 1
                ;;
        esac
    fi
}

# Run main function
main "$@"
