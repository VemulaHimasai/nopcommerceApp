@echo off

REM Change directory to the location of this run.bat file.
REM In Jenkins, this will be the Jenkins workspace.
cd /d "%~dp0"

echo ========================================
echo Running SANITY OR REGRESSION Test Cases
echo ========================================

REM Run tests using the Python virtual environment in Jenkins workspace
.venv\Scripts\python.exe -m pytest -v -s -m "sanity or regression" --html=./Reports/report_firefox.html testCases/ --browser firefox

set TEST_RESULT=%ERRORLEVEL%

echo.
echo ========================================
echo SANITY OR REGRESSION Test Execution Completed
echo ========================================

exit /b %TEST_RESULT%
