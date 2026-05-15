#!/usr/bin/env python3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import markdown


class EmailSender:
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.qq.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.sender_email = os.getenv('SENDER_EMAIL', '')
        self.sender_password = os.getenv('SENDER_PASSWORD', '')
        self.receiver_emails = os.getenv('RECEIVER_EMAILS', '').split(',')

    def send_email(self, report_path, pdf_path, time_info):
        if not self.sender_email or not self.sender_password:
            print('email config missing, skip')
            return

        msg = MIMEMultipart('alternative')
        msg['From'] = self.sender_email
        msg['To'] = ','.join(self.receiver_emails)
        msg['Subject'] = '每日选股分析报告 - ' + time_info['date']

        # Read MD content and convert to HTML
        md_content = ''
        if report_path and os.path.exists(report_path):
            with open(report_path, 'r', encoding='utf-8') as f:
                md_content = f.read()

        if md_content:
            # Convert MD to HTML for email body
            html_body = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])
            
            # Add CSS styling
            html_content = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
body { font-family: "Microsoft YaHei", "SimHei", sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; color: #333; line-height: 1.6; }
h1 { color: #1a1a2e; border-bottom: 3px solid #e94560; padding-bottom: 10px; }
h2 { color: #16213e; border-bottom: 2px solid #0f3460; padding-bottom: 8px; margin-top: 25px; }
h3 { color: #0f3460; margin-top: 18px; }
table { border-collapse: collapse; width: 100%; margin: 10px 0; font-size: 13px; }
th { background-color: #1a1a2e; color: white; padding: 8px 6px; text-align: left; }
td { padding: 6px; border: 1px solid #ddd; }
tr:nth-child(even) { background-color: #f8f9fa; }
strong { color: #e94560; }
hr { border: none; border-top: 2px solid #eee; margin: 20px 0; }
blockquote { border-left: 4px solid #e94560; padding-left: 16px; color: #666; }
</style>
</head>
<body>
""" + html_body + """
</body>
</html>"""
            
            # Attach HTML as main content
            msg.attach(MIMEText(html_content, 'html', 'utf-8'))
        else:
            # Fallback to plain text
            body = '报告生成失败，请检查系统日志。'
            msg.attach(MIMEText(body, 'plain', 'utf-8'))

        # Attach PDF only (not MD)
        if pdf_path and os.path.exists(pdf_path):
            with open(pdf_path, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename= report.pdf')
            msg.attach(part)

        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.sendmail(self.sender_email, self.receiver_emails, msg.as_string())
            server.quit()
            print('email sent')
        except Exception as e:
            print('email failed:', e)
