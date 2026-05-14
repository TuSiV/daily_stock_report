#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')
from modules.time_service import TimeService
from modules.data_fetcher import DataFetcher

def check_all_data():
    print("=== 全面检查所有数据是否使用最新数据 ===\n")

    ts = TimeService()
    time_info = ts.get_time_info()

    print("1. 时间信息：")
    print(f"   报告日期 (date): {time_info['date']}")
    print(f"   上一交易日 (last_trading_date): {time_info['last_trading_date']}")
    print(f"   昨天 (yesterday): {time_info['yesterday']}")
    print(f"   是否交易日 (is_trading_day): {time_info['is_trading_day']}")

    print("\n2. 获取所有市场数据...")
    fetcher = DataFetcher()
    data = fetcher.fetch_all_data(time_info)

    print("\n3. 检查每个数据：")

    # 检查美股
    print("\n   美股 (us_stock):")
    us = data.get('us_stock', {})
    print(f"   - 道指: {us.get('djia', {})}")
    print(f"   - 纳指: {us.get('nasdaq', {})}")
    print(f"   - 标普: {us.get('sp500', {})}")

    # 检查大宗商品
    print("\n   大宗商品 (commodity):")
    cm = data.get('commodity', {})
    print(f"   - 黄金: {cm.get('gold', {})}")
    print(f"   - WTI原油: {cm.get('wti', {})}")
    print(f"   - 布油: {cm.get('brent', {})}")

    # 检查A股
    print("\n   A股 (a_stock):")
    a = data.get('a_stock', {})
    print(f"   - 上证指数: {a.get('sh', {})}")
    print(f"   - 深证成指: {a.get('sz', {})}")
    print(f"   - 创业板指: {a.get('cy', {})}")

    # 检查板块
    print("\n   板块 (sectors):")
    sec = data.get('sectors', [])
    for i, s in enumerate(sec[:5]):
        print(f"   - {i+1}. {s.get('name', '')}: {s.get('pct', 0)}%")

    # 检查龙虎榜
    print("\n   龙虎榜 (lhb):")
    lhb = data.get('lhb', {}).get('top_buy', [])
    for i, s in enumerate(lhb[:5]):
        print(f"   - {i+1}. {s.get('name', '')}: 净买 {s.get('net_buy', 0)}万, 涨幅 {s.get('pct', 0)}%, 交易日期 {s.get('trade_date', '')}")

    # 检查北向资金
    print("\n   北向资金 (northbound):")
    nb = data.get('northbound', {})
    print(f"   - 净买入: {nb.get('total_net', 0)}")

    # 检查新闻
    print("\n   新闻 (news):")
    news = data.get('news', {})
    all_news = news.get('all_news', [])
    print(f"   - 全部新闻数量: {len(all_news)}")
    for i, n in enumerate(all_news[:5]):
        print(f"   - [{n.get('source', '')}] {n.get('title', '')[:60]}")

    print("\n=== 检查完成 ===")

if __name__ == '__main__':
    check_all_data()
