@echo off
REM PyCalorie Windows Setup Script
REM This script automates the installation and setup process for Windows

echo ========================================
echo   PyCalorie Project Setup for Windows
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python 3.10+ from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [OK] Python is installed
python --version
echo.

REM Check if Git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Git is not installed. You may need it for version control.
    echo Download from: https://git-scm.com/downloads
    echo.
)

REM Check if virtual environment exists
if exist "env\" (
    echo [INFO] Virtual environment already exists
    echo.
) else (
    echo [STEP 1/7] Creating virtual environment...
    python -m venv env
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
    echo.
)

REM Activate virtual environment
echo [STEP 2/7] Activating virtual environment...
call env\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)
echo [OK] Virtual environment activated
echo.

REM Upgrade pip
echo [STEP 3/7] Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install dependencies
echo [STEP 4/7] Installing dependencies from requirements.txt...
echo This may take a few minutes...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] Dependencies installed
echo.

REM Check if .env file exists
if exist ".env" (
    echo [INFO] .env file already exists
    echo.
) else (
    echo [STEP 5/7] Creating .env file from template...
    if exist "env.sample" (
        copy env.sample .env >nul
        echo [OK] .env file created
        echo.
        echo [IMPORTANT] Please edit .env file and add:
        echo   1. SECRET_KEY - Generate a strong random key
        echo   2. GOOGLE_API_KEY - Get from https://ai.google.dev/
        echo.
        echo Opening .env file in notepad...
        timeout /t 2 >nul
        notepad .env
    ) else (
        echo [WARNING] env.sample not found. Creating basic .env file...
        (
            echo # True for development, False for production
            echo DEBUG=True
            echo.
            echo # Generate a strong secret key
            echo SECRET_KEY=change-this-to-a-strong-random-key
            echo.
            echo # Google GENAI API Key for calorie prediction
            echo # Get your key from: https://ai.google.dev/
            echo GOOGLE_API_KEY=your-google-api-key-here
            echo.
            echo # Database Configuration (Optional - defaults to SQLite)
            echo # DB_ENGINE=postgresql
            echo # DB_HOST=localhost
            echo # DB_NAME=pycalorie_db
            echo # DB_USERNAME=pycalorie_user
            echo # DB_PASS=secure_password
            echo # DB_PORT=5432
        ) > .env
        echo [OK] Basic .env file created
        echo.
        echo Opening .env file in notepad...
        notepad .env
    )
)

REM Check if database exists
if exist "db.sqlite3" (
    echo [INFO] Database already exists
    echo.
) else (
    echo [STEP 6/7] Setting up database...
    echo Running migrations...
    python manage.py makemigrations
    python manage.py migrate
    if errorlevel 1 (
        echo [ERROR] Database migration failed
        pause
        exit /b 1
    )
    echo [OK] Database created and migrated
    echo.
)

REM Collect static files
echo [STEP 7/7] Collecting static files...
python manage.py collectstatic --noinput
if errorlevel 1 (
    echo [WARNING] Static files collection had issues, but continuing...
)
echo [OK] Static files collected
echo.

echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo Next steps:
echo   1. Make sure you've configured your .env file with:
echo      - SECRET_KEY (required)
echo      - GOOGLE_API_KEY (required for AI features)
echo.
echo   2. Create a superuser account (admin):
echo      python manage.py createsuperuser
echo.
echo   3. Run the development server:
echo      python manage.py runserver
echo.
echo   4. Open your browser to:
echo      http://127.0.0.1:8000
echo.
echo   5. Admin panel:
echo      http://127.0.0.1:8000/admin
echo.
echo ========================================
echo.

REM Ask if user wants to create superuser now
set /p create_super="Do you want to create a superuser (admin) account now? (Y/N): "
if /i "%create_super%"=="Y" (
    echo.
    echo Creating superuser account...
    python manage.py createsuperuser
    echo.
)

REM Ask if user wants to start the server now
set /p start_server="Do you want to start the development server now? (Y/N): "
if /i "%start_server%"=="Y" (
    echo.
    echo ========================================
    echo   Starting Django Development Server
    echo ========================================
    echo.
    echo Server will be available at: http://127.0.0.1:8000
    echo Press CTRL+C to stop the server
    echo.
    python manage.py runserver
) else (
    echo.
    echo To start the server later, run:
    echo   env\Scripts\activate
    echo   python manage.py runserver
    echo.
)

pause
