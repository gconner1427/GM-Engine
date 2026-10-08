@echo off
rem Opens the play window. pythonw keeps a console from sitting behind it.
where pythonw >nul 2>nul
if errorlevel 1 (
    python "%~dp0engine\gm.py" play %*
) else (
    start "" pythonw "%~dp0engine\gm.py" play %*
)
