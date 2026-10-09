@echo off
net session >nul 2>&1
if %errorlevel% neq 0 (
    powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process cmd.exe -ArgumentList '/c \"\"%~f0\"\"' -Verb RunAs"
    exit /b
)

title Register OpenRGB Autostart Task
cls
echo Setting PawnIO service to auto-start...
sc config PawnIO start= auto >nul 2>&1
net start PawnIO >nul 2>&1

echo Creating Task Scheduler task (Runs elevated on logon with no UAC prompt)...
schtasks /create /tn "OpenRGB_AutoWhite" /tr "\"%~dp0run_admin.bat\"" /sc ONLOGON /rl HIGHEST /f

echo Done. The task will run automatically whenever you log into Windows.
pause
