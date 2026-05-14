#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')
from modules.data_fetcher import DataFetcher

def test_us_stock():
    print("=== 测试美股数据获取 ===\n")
    
    fetcher = DataFetcher()
    print("Fetching US stock data...")
    
    # 调用fetch_all_data获取所有数据
    from modules.time_service import TimeService
    ts = TimeService()
    time_info = ts.get_time_info()
    
    us_stock = fetcher._fetch_us_stock(time_info)
    
    print("\n结果：")
    print(f"道琼斯: {us_stock['djia']}")
    print(f"纳斯达克: {us_stock['nasdaq']}")
    print(f"标普500: {us_stock['sp500']}")

if __name__ == '__main__':
    test_us_stock()
