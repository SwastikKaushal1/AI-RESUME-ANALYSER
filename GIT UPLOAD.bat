@echo off
cd /d %~dp0

REM Set Git Username and Email (If not already set)
git config --global user.name "SwastikKaushal"
git config --global user.email "swastikkaushal2022008@gmail.com"

echo Adding all files...
git add .

echo Committing changes...
set /p commit_msg="Enter commit message: "
git commit -m "%commit_msg%"

echo Pushing to GitHub...
git push origin main

echo All done! Press any key to exit...
pause >nul
