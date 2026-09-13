@echo off

echo ========================================
echo Running SANITY OR REGRESSION Test Cases
echo ========================================

echo Current Directory:
cd

echo.
echo Python version:
.venv\Scripts\python.exe --version

echo.
echo Running pytest...

.venv\Scripts\python.exe -m pytest -v -s -m "sanity or regression" --html=./Reports/report_chrome.html testCases/ --browser chrome

@REM .venv\Scripts\python.exe -m pytest -v -s -m "sanity or regression" --html=./Reports/report_firefox.html testCases/ --browser firefox

echo.
echo ========================================
echo SANITY OR REGRESSION Test Execution Completed
echo ========================================

exit /b %ERRORLEVEL%