@echo off
net session >nul 2>&1
if %errorlevel% neq 0 (
    powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process cmd.exe -ArgumentList '/c \"\"%~f0\"\"' -Verb RunAs"
    exit /b
)

title Kill Asus Services
cls
echo Stopping Asus processes...
taskkill /F /IM asus_framework.exe >nul 2>&1
taskkill /F /IM ArmourySocketServer.exe >nul 2>&1
taskkill /F /IM ArmourySwAgent.exe >nul 2>&1
taskkill /F /IM NoiseCancelingEngine.exe >nul 2>&1
taskkill /F /IM AcPowerNotification.exe >nul 2>&1

echo Disabling scheduled tasks...
schtasks /change /tn "\ASUS\ArmourySocketServer" /disable >nul 2>&1
schtasks /change /tn "\ASUS\NoiseCancelingEngine" /disable >nul 2>&1
schtasks /change /tn "\ASUS\AcPowerNotification" /disable >nul 2>&1

echo Disabling Windows services...
sc config asComSvc start= disabled >nul 2>&1
sc stop asComSvc >nul 2>&1
sc config AsusCertService start= disabled >nul 2>&1
sc stop AsusCertService >nul 2>&1
sc config AsusFanControlService start= disabled >nul 2>&1
sc stop AsusFanControlService >nul 2>&1
sc config ArmouryCrateService start= disabled >nul 2>&1
sc stop ArmouryCrateService >nul 2>&1

echo Done.
pause
