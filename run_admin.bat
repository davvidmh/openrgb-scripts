@echo off
net session >nul 2>&1
if %errorlevel% neq 0 (
    powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process cmd.exe -ArgumentList '/c \"\"%~f0\"\"' -Verb RunAs"
    exit /b
)

title OpenRGB Launcher
cls
echo Closing conflicting Asus bloatware...
taskkill /F /IM asus_framework.exe >nul 2>&1
taskkill /F /IM ArmourySocketServer.exe >nul 2>&1
taskkill /F /IM ArmourySwAgent.exe >nul 2>&1
taskkill /F /IM NoiseCancelingEngine.exe >nul 2>&1
taskkill /F /IM AcPowerNotification.exe >nul 2>&1
taskkill /F /IM OpenRGB.exe >nul 2>&1

schtasks /change /tn "\ASUS\ArmourySocketServer" /disable >nul 2>&1
schtasks /change /tn "\ASUS\NoiseCancelingEngine" /disable >nul 2>&1
schtasks /change /tn "\ASUS\AcPowerNotification" /disable >nul 2>&1

sc start PawnIO >nul 2>&1

echo Starting OpenRGB with SDK server...
set "EXE="
if exist "%USERPROFILE%\OpenRGB\OpenRGB Windows 64-bit\OpenRGB.exe" set "EXE=%USERPROFILE%\OpenRGB\OpenRGB Windows 64-bit\OpenRGB.exe"
if exist "%ProgramFiles%\OpenRGB\OpenRGB.exe" set "EXE=%ProgramFiles%\OpenRGB\OpenRGB.exe"

if "%EXE%"=="" (
    start "" OpenRGB.exe --server
) else (
    start "" "%EXE%" --server
)

timeout /t 6 /nobreak >nul
python "%~dp0sync_white.py"
pause
