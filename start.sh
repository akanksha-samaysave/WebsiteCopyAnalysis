#!/bin/bash

# Landing Page Intelligence - Startup Script

echo "🚀 Starting Landing Page Intelligence Application..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose is not installed. Please install docker-compose first."
    exit 1
fi

# Pull latest images
echo "📦 Pulling latest images..."
docker-compose pull

# Build images
echo "🔨 Building images..."
docker-compose build

# Start services
echo "▶️  Starting services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 5

# Check if backend is healthy
echo "🏥 Checking backend health..."
max_attempts=30
attempt=0

while [ $attempt -lt $max_attempts ]; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo "✅ Backend is healthy"
        break
    fi
    echo "Waiting for backend... ($((attempt + 1))/$max_attempts)"
    sleep 1
    attempt=$((attempt + 1))
done

if [ $attempt -eq $max_attempts ]; then
    echo "⚠️  Backend health check timed out. Check logs with: docker-compose logs backend"
fi

# Print useful information
echo ""
echo "✨ Landing Page Intelligence is running!"
echo ""
echo "📱 Frontend: http://localhost:3000"
echo "🔌 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "📖 View logs:"
echo "   Backend:  docker-compose logs -f backend"
echo "   Frontend: docker-compose logs -f frontend"
echo ""
echo "🛑 To stop: docker-compose down"
echo ""
