#!/usr/bin/env python3
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://finance.sina.com.cn/'
}

url = 'https://hq.sinajs.cn/list=hf_GC,hf_CL,hf_OIL'
resp = requests.get(url, headers=headers)

print("Raw data:")
for line in resp.text.split('\n'):
    if line.strip():
        print(f"\n{line}")
        if '=' in line:
            fields = line.split('"')[1].split(',')
            print("\nField analysis:")
            for i, f in enumerate(fields):
                print(f"  Field {i}: {f}")
