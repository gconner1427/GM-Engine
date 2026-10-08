@echo off
title GM Engine: New Narrative
set /p NAME=Name of the narrative:
set /p PARENT=Folder to create it in (blank for %USERPROFILE%\GM Narratives):
set /p YOU=Narration: third person like a novel, or second person ("you") like a GM at the table? Type 2 for second (blank for third):
set PERSON=third
if "%YOU%"=="2" set PERSON=second
if "%PARENT%"=="" (
    python "%~dp0engine\gm.py" new-narrative "%NAME%" --person %PERSON%
) else (
    python "%~dp0engine\gm.py" new-narrative "%NAME%" --at "%PARENT%" --person %PERSON%
)
pause
