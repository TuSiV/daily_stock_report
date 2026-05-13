#!/usr/bin/env python3
import requests
from datetime import datetime, timedelta
import re

class TimeService:
    WEEKDAYS = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    WEEKDAYS_CN = ['Week1','Week2','Week3','Week4','Week5','Week6','Week7']

    def __init__(self):
        self.ntsc_url = 'http://www.ntsc.ac.cn'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

    def get_time_info(self):
        now = self._get_ntsc_time()
        yesterday = now - timedelta(days=1)
        is_trading = self._is_a_stock_trading_day(now)
        last_trading = self._get_last_trading_day(now) if not is_trading else now
        return {
            'date': now.strftime('%Y-%m-%d'),
            'date_cn': f'{now.year}year{now.month}month{now.day}day',
            'weekday': self.WEEKDAYS[now.weekday()],
            'weekday_cn': self.WEEKDAYS_CN[now.weekday()],
            'year': now.year,
            'month': now.month,
            'day': now.day,
            'is_trading_day': is_trading,
            'last_trading_date': last_trading.strftime('%Y-%m-%d'),
            'yesterday': yesterday.strftime('%Y-%m-%d'),
            'search_date': f'{now.year}year{now.month}month{now.day}day',
            'timestamp': now.strftime('%Y-%m-%d %H:%M:%S')
        }

    def _get_ntsc_time(self):
        # Try multiple time sources (eastmoney first as it's most reliable)
        sources = [
            self._get_time_from_eastmoney,
            self._get_time_from_baidu,
            self._get_time_from_ntsc,
        ]
        
        for source_func in sources:
            try:
                result = source_func()
                if result and result.year >= 2024:
                    return result
            except Exception:
                continue
        
        # Fallback to system time
        return datetime.now()
    
    def _get_time_from_ntsc(self):
        resp = requests.get(self.ntsc_url, headers=self.headers, timeout=10)
        resp.encoding = 'utf-8'
        match = re.search(r'(20\d{2})[年/-](\d{1,2})[月/-](\d{1,2})', resp.text)
        if match:
            return datetime(int(match.group(1)), int(match.group(2)), int(match.group(3)))
        return None
    
    def _get_time_from_eastmoney(self):
        # Use eastmoney API to get current trading date
        url = 'https://push2his.eastmoney.com/api/qt/stock/kline/get?secid=1.000001&fields1=f1&fields2=f51&klt=101&fqt=1&beg=20260101&end=20500101&lmt=5'
        resp = requests.get(url, headers=self.headers, timeout=10)
        data = resp.json()
        if data.get('data') and data['data'].get('klines'):
            # Get the last (most recent) kline
            date_str = data['data']['klines'][-1].split(',')[0]
            return datetime.strptime(date_str, '%Y-%m-%d')
        return None
    
    def _get_time_from_baidu(self):
        resp = requests.get('https://www.baidu.com', headers=self.headers, timeout=10)
        # Try to find date in response headers or content
        import email.utils
        date_str = resp.headers.get('Date', '')
        if date_str:
            try:
                dt = email.utils.parsedate_to_datetime(date_str)
                return dt.replace(hour=0, minute=0, second=0, microsecond=0)
            except:
                pass
        return None

    def _is_a_stock_trading_day(self, dt):
        if dt.weekday() >= 5:
            return False
        from config.settings import A_STOCK_HOLIDAYS_2026
        date_str = dt.strftime('%Y-%m-%d')
        return date_str not in A_STOCK_HOLIDAYS_2026

    def _get_last_trading_day(self, dt):
        d = dt - timedelta(days=1)
        while not self._is_a_stock_trading_day(d):
            d -= timedelta(days=1)
        return d
