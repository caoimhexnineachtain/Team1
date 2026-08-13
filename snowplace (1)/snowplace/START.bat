@echo off
echo ============================================
echo  SNOW PLACE LIKE HOME - Website
echo ============================================
echo.
echo Starting server...
cd /d "%~dp0backend"
if not exist node_modules (
    echo Installing dependencies first...
    npm install
)
echo.
echo Server starting at http://localhost:3000
echo Press Ctrl+C to stop.
echo.
node server.js
pause
