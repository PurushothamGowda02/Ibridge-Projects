@echo off
echo Checking if MongoDB container exists...
docker ps -a --filter "name=lms_db" --format "{{.Names}}"

echo.
echo Stopping and removing old container if exists...
docker stop lms_db 2>nul
docker rm lms_db 2>nul

echo.
echo Starting fresh MongoDB container...
docker run -d --name lms_db -p 27017:27017 mongo:latest

echo.
echo Waiting for MongoDB to be ready...
timeout /t 5 /nobreak >nul

echo.
echo MongoDB container status:
docker ps --filter "name=lms_db"

echo.
echo MongoDB is ready! You can now use the registration page.
pause
