#!/usr/bin/env python3
import requests
from config.settings import USER_AGENT

url = 'https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=20&po=1&np=1&fltt=2&invt=2&fid=f3&fs=m:90+t:2&fields=f12,f14,f3'
headers = {'User-Agent': USER_AGENT}

resp = requests.get(url, headers=headers)
print(f"状态码: {resp.status_code}")
print(f"完整响应: {resp.text}")

data = resp.json()
if data.get('data') and data['data'].get('diff'):
    for i, item in enumerate(data['data']['diff'][:3]):
        print(f"\n{i+1}. 原始 f3: {item.get('f3', 0)}")
        print(f"   板块: {item.get('f14', '')}")
