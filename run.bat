@echo off
chcp 65001 >nul
echo ========================================================
echo  啟動 Flask 訂單管理系統 (OrderPro)
echo ========================================================
echo.

if exist "venv\Scripts\python.exe" (
    echo [資訊] 使用 venv 虛擬環境執行...
    "venv\Scripts\python.exe" app.py
) else if exist "C:\Users\freej\anaconda3\python.exe" (
    echo [資訊] 使用 Anaconda Python 執行...
    "C:\Users\freej\anaconda3\python.exe" app.py
) else (
    echo [資訊] 使用系統預設 Python 執行...
    python app.py
)

pause
