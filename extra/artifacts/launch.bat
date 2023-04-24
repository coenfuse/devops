@echo OFF

setlocal

:: change to the directory containing the batch script
cd /d %~dp0

:: start the application with the configuration file
app\lamina.exe --config config\lamina.toml

pause
endlocal