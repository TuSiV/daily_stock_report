#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')
from modules.time_service import TimeService
from modules.data_fetcher import DataFetcher

def test():
    print("=== 测试数据获取 ===")
    
    ts = TimeService()
    time_info = ts.get_time_info()
    
    fetcher = DataFetcher()
    
    print("\n1. 测试大宗商品获取...")
    commodity = fetcher._fetch_commodity(time_info)
    print(f"大宗商品: {commodity}")
    
    print("\n2. 测试板块数据获取...")
    sectors = fetcher._fetch_sectors(time_info)
    print(f"板块数量: {len(sectors)}")
    for i, s in enumerate(sectors[:5]):
        print(f"  {i+1}. {s}")
    
    print("\n3. 测试龙虎榜获取...")
    lhb = fetcher._fetch_lhb(time_info)
    print(f"龙虎榜 top_buy: {len(lhb.get('top_buy', []))}")
    
    print("\n4. 测试北向资金获取...")
    northbound = fetcher._fetch_northbound(time_info)
    print(f"北向资金: {northbound}")

if __name__ == '__main__':
    test()
