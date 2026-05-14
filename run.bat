@echo off
cd /d %~dp0
set PATH=C:\Python314;C:\Python314\Scripts;%PATH%
python main.py %*
pause
