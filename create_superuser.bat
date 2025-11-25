@echo off
REM Create Superuser Script for PyCalorie (Windows)

echo ========================================
echo   PyCalorie - Create Admin Account
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
call env\Scripts\activate.bat

REM Create superuser
echo Creating superuser account...
echo You will be prompted for:
echo   - Username
echo   - Email (optional)
echo   - Password (will be hidden)
echo.

python manage.py createsuperuser

echo.
echo ========================================
echo Superuser created successfully!
echo.
echo You can now login to the admin panel at:
echo http://127.0.0.1:8000/admin
echo ========================================
echo.

pause
