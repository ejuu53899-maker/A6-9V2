@echo off
setlocal enabledelayedexpansion

:: ============================================================
:: MQL5 Google Drive Setup & Streaming Mode
:: ============================================================

set "GDRIVE_GIT_URL=https://drive.google.com/drive/folders/14qZgVQOnh7lNQreV1Nq7wlAiqBoc7OFc"
set "GDRIVE_CURSIR_URL=https://drive.google.com/drive/folders/1vG7mPy5KETtatMqVUnkqgXDoXmtpzCO1"

echo ============================================================
echo    MQL5 Google Drive Setup
echo ============================================================
echo.
echo This script helps you set up Google Drive Streaming Mode
echo using rclone.
echo.

:: Check for rclone
where rclone >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] rclone not found in PATH.
    echo Please install rclone from https://rclone.org/downloads/
    echo.
    echo Alternatively, you can access the folders directly:
    echo GIT: %GDRIVE_GIT_URL%
    echo CURSIR: %GDRIVE_CURSIR_URL%
    echo.
    pause
    goto :eof
)

echo [INFO] rclone found.
echo.
echo Options:
echo   1) Configure Google Drive remote (rclone config)
echo   2) Start Streaming Mode (Mount Google Drive to G:)
echo   3) Sync MQL5 to Google Drive
echo   4) Open Google Drive folders in browser
echo   0) Exit
echo.

set /p choice="Enter your choice [0-4]: "

if "%choice%"=="1" (
    echo [INFO] Starting rclone config...
    echo Please follow the prompts to create a remote named 'google-drive'.
    echo Use 'drive' as the storage type.
    rclone config
    goto :end
)

if "%choice%"=="2" (
    echo [INFO] Starting Streaming Mode...
    echo Attempting to mount 'google-drive:' to G:
    echo [NOTE] This requires WinFsp (https://winfsp.dev/) to be installed.
    start /b rclone mount google-drive: G: --vfs-cache-mode full --vfs-cache-max-age 24h --dir-cache-time 5m
    echo [SUCCESS] Mount command issued in background.
    echo If successful, your Google Drive will appear as drive G:
    goto :end
)

if "%choice%"=="3" (
    echo [INFO] Syncing mt5/MQL5 to Google Drive...
    rclone sync mt5/MQL5 google-drive:MQL5 --progress
    goto :end
)

if "%choice%"=="4" (
    echo [INFO] Opening Google Drive folders...
    start %GDRIVE_GIT_URL%
    start %GDRIVE_CURSIR_URL%
    goto :end
)

if "%choice%"=="0" goto :eof

:end
echo.
echo Press any key to exit...
pause >nul
