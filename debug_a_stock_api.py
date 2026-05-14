#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')
import requests
from modules.data_fetcher import DataFetcher

def debug_a_stock_api():
    print("=== 调试A股API数据 ===")
    
    # 测试API1: push2.eastmoney.com 实时API
    indices = [('sh','1.000001','上证指数'),('sz','0.399001','深证成指'),('cy','0.399006','创业板指')]
    
    for key, code, name in indices:
        url = f'https://push2.eastmoney.com/api/qt/stock/get?secid={code}&fields=f43,f44,f45,f46,f47,f170,f48'
        print(f"\n{name} ({code}):")
        print(f"URL: {url}")
        
        resp = requests.get(url, timeout=10)
        print(f"Status: {resp.status_code}")
        
        if resp.status_code == 200:
            data = resp.json()
            print(f"Response: {data}")
            
            d = data.get('data')
            if d:
                print(f"  收盘点位(f43): {d.get('f43', 0)} / 100 = {d.get('f43', 0)/100}")
                print(f"  涨跌幅(f170): {d.get('f170', 0)} / 100 = {d.get('f170', 0)/100}%")
                print(f"  成交额(f48): {d.get('f48', 0)} / 100000000 = {d.get('f48', 0)/100000000}亿")

if __name__ == '__main__':
    debug_a_stock_api()
