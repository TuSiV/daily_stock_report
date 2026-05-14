#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')
from modules.time_service import TimeService
from modules.data_fetcher import DataFetcher

def test_a_stock_fetch():
    print("=== 测试A股数据获取 ===\n")
    
    ts = TimeService()
    time_info = ts.get_time_info()
    print(f"Time info:")
    print(f"  date: {time_info['date']}")
    print(f"  last_trading_date: {time_info['last_trading_date']}")
    print()
    
    fetcher = DataFetcher()
    print("Fetching A-stock data...")
    a_stock = fetcher._fetch_a_stock(time_info)
    
    print()
    print(f"Result:")
    print(f"  上证指数: {a_stock['sh']}")
    print(f"  深证成指: {a_stock['sz']}")
    print(f"  创业板指: {a_stock['cy']}")
    print(f"  两市合计成交: {a_stock['total_vol']}亿")

if __name__ == '__main__':
    test_a_stock_fetch()
