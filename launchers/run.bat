@echo off
REM ╔═════════════════╦════════════════════════════════════════════╗
REM ║ Author          ║ CH3CKMATE-2002 (Andreas Hanna)             ║
REM ╠═════════════════╬════════════════════════════════════════════╣
REM ║ Contributors    ║ Monika                                     ║
REM ╚═════════════════╩════════════════════════════════════════════╝

REM ══════════════════════════════════════╗
REM ║ Script Metadata                     ║
REM ══════════════════════════════════════╝
SET SCRIPT_NAME=%~n0
SET SCRIPT_AUTHOR=CH3CKMATE-2002 (Andreas Hanna)
SET SCRIPT_CONTRIBUTORS=Monika
SET SCRIPT_VERSION=1.0
SET SCRIPT_COPYRIGHT=Copyright@2024 by %SCRIPT_AUTHOR%

REM Change to script directory
CD /D "%~dp0"
CD ".."

REM Check if Python is installed
WHERE python >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    ECHO "Python is not installed. Please install Python 3 to run this app."
    EXIT /B 1
)

REM Run the Python script
python main.py %*

