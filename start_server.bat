@echo off
title SARA Web Server
cd /d "%~dp0"
echo Starting SARA Web Server...
echo Access at: http://localhost:5000
echo.
python run.py
pause
