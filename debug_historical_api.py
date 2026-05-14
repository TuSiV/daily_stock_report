#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')
import requests
import time
from datetime import datetime

def debug_historical_api():
    print("=== 调试东方财富历史行情API ===\n")
    
    # 测试历史K线API
    indices = [
        ('sh', '1.000001', '上证指数'),
        ('sz', '0.399001', '深证成指'),
        ('cy', '0.399006', '创业板指')
    ]
    
    for key, secid, name in indices:
        # 获取最近的K线数据
        url = f'https://push2his.eastmoney.com/api/qt/stock/kline/get?secid={secid}&fields1=f1,f2,f3,f4,f5,f6&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61&klt=101&fqt=1&beg=0&end=20500101'
        print(f"{name} (secid={secid}):")
        print(f"URL: {url}")
        
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                if data.get('data'):
                    klines = data['data'].get('klines', [])
                    if klines:
                        # 取最近的一条
                        latest = klines[-1].split(',')
                        date = latest[0]
                        close = float(latest[2])
                        pct = float(latest[8])
                        vol = float(latest[6]) / 100000000  # 成交额
                        print(f"  最新日期: {date}")
                        print(f"  收盘点位: {close}")
                        print(f"  涨跌幅: {pct}%")
                        print(f"  成交额: {vol:.2f}亿")
                    else:
                        print("  无K线数据")
                else:
                    print("  data为空")
        except Exception as e:
            print(f"  错误: {e}")
        print()

if __name__ == '__main__':
    debug_historical_api()
