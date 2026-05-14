
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.data_fetcher import DataFetcher
from modules.time_service import TimeService

def main():
    print("="*80)
    print("新闻数据调试 - 检查实际获取到的新闻")
    print("="*80)
    
    ts = TimeService()
    time_info = ts.get_time_info()
    
    df = DataFetcher()
    
    print(f"\n正在调用 _fetch_news 获取新闻...")
    news = df._fetch_news(time_info)
    
    print(f"\n结果：")
    print(f"- all_news 数量: {len(news.get('all_news', []))}")
    print(f"- geopolitics 数量: {len(news.get('geopolitics', []))}")
    print(f"- policy 数量: {len(news.get('policy', []))}")
    
    print(f"\n" + "="*80)
    print("所有新闻列表：")
    print("="*80)
    
    all_news = news.get('all_news', [])
    for i, item in enumerate(all_news):
        title = item.get('title', '')
        source = item.get('source', '')
        print(f"{i+1:2d}. [{source:10s}] {title}")
    
    print(f"\n" + "="*80)
    print("被分类为地缘政治的新闻：")
    print("="*80)
    
    geo_news = news.get('geopolitics', [])
    if geo_news:
        for i, item in enumerate(geo_news):
            title = item.get('title', '')
            source = item.get('source', '')
            print(f"{i+1:2d}. [{source:10s}] {title}")
    else:
        print("(无)")
    
    print(f"\n" + "="*80)
    print("检查新闻标题中是否包含特朗普、北京等关键词：")
    print("="*80)
    
    keywords = ['特朗普', '北京', '中美', '会谈', '贸易', '冲突', '军事', '外交']
    for i, item in enumerate(all_news):
        title = item.get('title', '')
        found = [kw for kw in keywords if kw in title]
        if found:
            source = item.get('source', '')
            print(f"{i+1:2d}. [{source:10s}] {title} (关键词: {', '.join(found)})")

if __name__ == "__main__":
    main()

