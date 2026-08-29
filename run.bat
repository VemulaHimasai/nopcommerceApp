@echo off

cd /d C:\Users\hp\PycharmProjects\Python_Selenium_Hybrid

echo ========================================
echo Running SANITY OR REGRESSION  Test Cases
echo ========================================

@REM .venv\Scripts\python.exe -m pytest -v -s -m "sanity or regression" --html=./Reports/report_chrome.html testCases/ --browser chrome

.venv\Scripts\python.exe -m pytest -v -s -m "sanity or regression" --html=./Reports/report_firefox.html testCases/ --browser firefox

@REM .venv\Scripts\python.exe -m pytest -v -s -m "regression" --html=./Reports/report-chrome.html testCases/ --browser chrome
@REM .venv\Scripts\python.exe -m pytest -v -s -m "regression" --html=./Reports/report-firefox.html testCases/ --browser firefox

echo.
echo ========================================
echo SANITY OR REGRESSION Test Execution Completed
echo ========================================

pause