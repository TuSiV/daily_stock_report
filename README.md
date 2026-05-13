# Daily Stock Analysis Report

Automated daily stock analysis report system.

## Setup

1. Install Python 3.8+
2. Install dependencies: pip install -r requirements.txt
3. Set environment variables for email:
   - SMTP_SERVER (default: smtp.qq.com)
   - SMTP_PORT (default: 587)
   - SENDER_EMAIL
   - SENDER_PASSWORD
   - RECEIVER_EMAILS (comma-separated)

## Usage

Run manually: python main.py

Schedule via Windows Task Scheduler:
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger: Daily at 8:00 AM
4. Set action: Start program run.bat
5. Set start in: Project directory

## Project Structure

- main.py - Entry point
- config/ - Configuration and template
- modules/ - Core modules
- utils/ - Utility functions
- output/ - Generated reports and logs
