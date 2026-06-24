@echo off
REM Landing Page Intelligence - Startup Script for Windows

echo 🚀 Starting Landing Page Intelligence Application...

REM Check if Docker is installed
where docker >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Docker is not installed. Please install Docker first.
    exit /b 1
)

REM Check if docker-compose is installed
where docker-compose >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ docker-compose is not installed. Please install docker-compose first.
    exit /b 1
)

REM Build images
echo 🔨 Building images...
docker-compose build

REM Start services
echo ▶️  Starting services...
docker-compose up -d

REM Wait for services
echo ⏳ Waiting for services to start...
timeout /t 5 /nobreak

REM Print useful information
echo.
echo ✨ Landing Page Intelligence is running!
echo.
echo 📱 Frontend: http://localhost:3000
echo 🔌 Backend API: http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs
echo.
echo 📖 View logs:
echo    Backend:  docker-compose logs -f backend
echo    Frontend: docker-compose logs -f frontend
echo.
echo 🛑 To stop: docker-compose down
echo.
