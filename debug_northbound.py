#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')
from modules.data_fetcher import DataFetcher
import requests

def debug_northbound():
    print("=== 调试北向资金API ===\n")
    
    fetcher = DataFetcher()
    
    url1 = 'https://push2.eastmoney.com/api/qt/kamt.rtmin/get?fields1=f1,f2,f3,f4&fields2=f51,f52,f53,f54,f55,f56'
    print(f"调用API 1: {url1}")
    resp1 = requests.get(url1, timeout=10)
    print(f"状态码: {resp1.status_code}")
    print(f"响应内容 (前200字符): {str(resp1.text[:200])}\n")
    
    data1 = resp1.json()
    print("API 1 响应完整数据:")
    print(data1)
    print()
    
    url2 = 'https://push2.eastmoney.com/api/qt/kamtbs.wpt?fields=f1,f2,f3,f4'
    print(f"调用API 2: {url2}")
    resp2 = requests.get(url2, timeout=10)
    print(f"状态码: {resp2.status_code}")
    print(f"响应内容 (前200字符): {str(resp2.text[:200])}\n")
    
    data2 = resp2.json()
    print("API 2 响应完整数据:")
    print(data2)

if __name__ == '__main__':
    debug_northbound()
