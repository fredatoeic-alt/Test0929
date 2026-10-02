@echo off
chcp 65001 >nul
echo ========================================================
echo  啟動 Python Flask Hello World 一頁式網站
echo ========================================================
echo.

if exist "C:\Users\freej\anaconda3\python.exe" (
    echo [資訊] 使用 Anaconda Python 執行...
    "C:\Users\freej\anaconda3\python.exe" app.py
) else (
    echo [資訊] 使用系統預設 Python 執行...
    python app.py
)

pause
