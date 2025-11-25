@echo off
REM Quick Start Script for PyCalorie (Windows)
REM Activates virtual environment and starts the development server

echo ========================================
echo   PyCalorie - Quick Start
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "env\" (
    echo [ERROR] Virtual environment not found!
    echo Please run setup.bat first to install the project.
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call env\Scripts\activate.bat

REM Check if .env exists
if not exist ".env" (
    echo [WARNING] .env file not found!
    echo Please create .env file with your configuration.
    echo.
    pause
    exit /b 1
)

REM Check if database exists
if not exist "db.sqlite3" (
    echo [INFO] Database not found. Running migrations...
    python manage.py migrate
    echo.
)

REM Start development server
echo ========================================
echo   Starting Django Development Server
echo ========================================
echo.
echo Server URL: http://127.0.0.1:8000
echo Admin Panel: http://127.0.0.1:8000/admin
echo.
echo Press CTRL+C to stop the server
echo.

python manage.py runserver
