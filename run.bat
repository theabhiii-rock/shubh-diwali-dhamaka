@echo off
title Shubh Diwali Mega Skill Contest 2026 - Production Server
color 0E
echo ==============================================================================
echo     SHUBH DIWALI MEGA SKILL CONTEST 2026 - CULTURAL TRIVIA & PRIZE PLATFORM
echo     Grand Prize Pool: 32 Lakhs for 100 Winners (30x50k, 50x30k, 20x10k)
echo     Fulfillment: Licensed Store Digital Vouchers and Doorstep Delivery
echo ==============================================================================
echo.
echo [1] Verifying environment and initializing SQLite database...
python -c "import server; server.init_db()"
echo.
echo [2] Starting Local Server on http://localhost:8080 ...
echo [3] Launching web browser...
start http://localhost:8080
echo.
echo ==============================================================================
echo   Server is LIVE and Serving Production UI (Port 8080)
echo   Game of Skill Architecture: Active (Article 19(1)(g) Compliant)
echo   Press Ctrl+C to stop the server anytime.
echo ==============================================================================
python server.py 8080
pause
