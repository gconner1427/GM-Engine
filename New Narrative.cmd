@echo off
title GM Engine: New Narrative
set /p NAME=Name of the narrative:
set /p PARENT=Folder to create it in (blank for %USERPROFILE%\GM Narratives):
if "%PARENT%"=="" (
    python "%~dp0engine\gm.py" new-narrative "%NAME%"
) else (
    python "%~dp0engine\gm.py" new-narrative "%NAME%" --at "%PARENT%"
)
pause
