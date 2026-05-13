@echo off
echo Setting up Daily Stock Report scheduled task...
echo.

REM Create the scheduled task to run daily at 8:00 AM
schtasks /create /tn "DailyStockReport" /tr "python D:\Project\daily_stock_report_open\main.py" /sc daily /st 08:00 /f

if %errorlevel% equ 0 (
    echo.
    echo Task "DailyStockReport" created successfully!
    echo The report will run daily at 8:00 AM
    echo.
    echo To run now, use: python D:\Project\daily_stock_report_open\main.py
    echo To delete task, use: schtasks /delete /tn "DailyStockReport" /f
) else (
    echo.
    echo Failed to create task. Please run as Administrator.
)

pause
