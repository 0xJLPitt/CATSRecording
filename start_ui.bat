@echo off
cd /d C:\Users\User\CATSRecording
call mamba activate dev
cd main
python run_ui.py
pause
