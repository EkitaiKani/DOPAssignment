@echo off
setlocal

NET SESSION >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo This script requires administrative privileges. Please wait...
    powershell -Command "Start-Process cmd -ArgumentList '/c %~s0' -Verb RunAs"
    EXIT /B
)

:: PostgreSQL version and installer URL
set POSTGRES_VERSION=17
set POSTGRES_DOWNLOAD_URL=https://get.enterprisedb.com/postgresql/postgresql-17.2-3-windows-x64.exe

:: Database configuration
set PG_INSTALL_DIR=C:\Program Files\PostgreSQL\%POSTGRES_VERSION%
set PG_DATA_DIR=C:\PostgreSQL\data
set PG_USER=postgres
set PG_PASSWORD=bafjoiaibudfkasf
set PG_DATABASE=DOPAssignment
set PG_HOST=localhost
set PG_PORT=5432

:: File paths
set INSTALLER_FILE=%TEMP%\postgresql_installer.exe
set SQL_FILE=%~dp0database-setup.sql

:: Step 1: Download PostgreSQL installer using curl (if available)
echo Downloading PostgreSQL %POSTGRES_VERSION%...
curl -L -o "%INSTALLER_FILE%" "%POSTGRES_DOWNLOAD_URL%"
if %ERRORLEVEL% neq 0 (
    echo Failed to download PostgreSQL installer.
    pause
    exit /b
)

:: Step 2: Run the installer silently
echo Installing PostgreSQL...
"%INSTALLER_FILE%" --mode unattended --unattendedmodeui minimalWithDialogs --superpassword %PG_PASSWORD% --prefix "%PG_INSTALL_DIR%" --datadir "%PG_DATA_DIR%"
if %ERRORLEVEL% neq 0 (
    echo PostgreSQL installation failed.
    pause
    exit /b
)

:: Step 3: Verify installation path
if not exist "%PG_INSTALL_DIR%\bin\psql.exe" (
    echo PostgreSQL binary not found in "%PG_INSTALL_DIR%\bin".
    pause
    exit /b
)

:: Step 4: Create the database
echo Creating the database...
set PGPASSWORD=%PG_PASSWORD%
"%PG_INSTALL_DIR%\bin\psql.exe" -U postgres -h %PG_HOST% -p %PG_PORT% -d postgres -c "CREATE DATABASE \"%PG_DATABASE%\";"
if %ERRORLEVEL% neq 0 (
    echo Failed to create the database.
    pause
    exit /b
)

:: Step 5: Run SQL commands from the file
echo Running SQL commands from the file: %SQL_FILE%
set PGPASSWORD=%PG_PASSWORD%
"%PG_INSTALL_DIR%\bin\psql.exe" -U %PG_USER% -h %PG_HOST% -p %PG_PORT% -d "%PG_DATABASE%" -a -f "%SQL_FILE%"
if %ERRORLEVEL% neq 0 (
    echo SQL execution failed.
    pause
    exit /b
)

:: Step 6: Verify PostgreSQL service
echo Verifying PostgreSQL service...
sc query "postgresql-x64-%POSTGRES_VERSION%" | findstr /i "RUNNING" >nul
if %ERRORLEVEL% neq 0 (
    echo PostgreSQL service is not running.
    pause
    exit /b
)

:: Cleanup
del /f /q "%INSTALLER_FILE%"
echo PostgreSQL setup completed successfully!
