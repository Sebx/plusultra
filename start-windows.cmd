@echo off
setlocal
cd /d "%~dp0"
title plusultra
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0local-server.ps1" %*
if errorlevel 1 (
  echo.
  echo The local server could not start.
  pause
)
