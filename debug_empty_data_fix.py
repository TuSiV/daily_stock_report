
#!/usr/bin/env python3
import requests
import json
from config.settings import USER_AGENT

session = requests.Session()
session.headers.update({'User-Agent': USER_AGENT})

print('='*60)
print('测试 1: 标普500指数 - 东方财富API')
print('='*60)
try:
    url = 'https://push2.eastmoney.com/api/qt/stock/get?secid=100.SPX&amp;fields=f43,f44,f45,f46,f47,f170,f48'
    resp = session.get(url, timeout=10)
    print(f'Status: {resp.status_code}')
    data = resp.json()
    print(f'Response: {json.dumps(data, ensure_ascii=False, indent=2)[:5