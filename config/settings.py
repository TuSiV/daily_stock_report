import os
from dotenv import load_dotenv

# Load .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

#!/usr/bin/env python3
import os

# Project paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
REPORTS_DIR = os.path.join(OUTPUT_DIR, 'reports')
LOGS_DIR = os.path.join(OUTPUT_DIR, 'logs')

# NTSC time server
NTSC_URL = 'http://www.ntsc.ac.cn'

# User-Agent for requests
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

# Request timeout
REQUEST_TIMEOUT = 15

# Request interval (seconds) to avoid anti-crawling
REQUEST_INTERVAL = 2

# Stock selection criteria
MIN_LHB_NET_BUY = 50000000  # 5000wan
NUM_STOCKS_TO_SELECT = 5

# Email config (from env vars)
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.qq.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
SENDER_EMAIL = os.getenv('SENDER_EMAIL', '')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD', '')
RECEIVER_EMAILS = os.getenv('RECEIVER_EMAILS', '').split(',')

# Report settings
REPORT_WIDTH = 800
REPORT_DPI = 300

# Trading calendar
A_STOCK_HOLIDAYS_2026 = [
    '2026-01-01', '2026-01-02',  # New Year
    '2026-01-26', '2026-01-27', '2026-01-28', '2026-01-29', '2026-01-30',  # Spring Festival
    '2026-04-06',  # Qingming
    '2026-05-01', '2026-05-02', '2026-05-03',  # Labor Day
    '2026-06-19',  # Dragon Boat
    '2026-09-25',  # Mid-Autumn
    '2026-10-01', '2026-10-02', '2026-10-03', '2026-10-04', '2026-10-05',  # National Day
]
