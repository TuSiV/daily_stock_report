#!/usr/bin/env python3
import requests
from config.settings import USER_AGENT

url = 'https://hq.sinajs.cn/list=gb_dji,gb_ixic,gb_spx'
headers = {
    'User-Agent': USER_AGENT,
    'Referer': 'https://finance.sina.com.cn/'
}

resp = requests.get(url, headers=headers)
print(f"响应: {resp.text}")
