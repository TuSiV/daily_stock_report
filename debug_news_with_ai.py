
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.data_fetcher import DataFetcher
from modules.time_service import TimeService
from modules.ai_analyzer import AIAnalyzer

def main():
    print("="*100)
    print("调试新闻获取和AI分析")
    print("="*100)
    
    ts = TimeService()
    time_info = ts.get_time_info()
    
    df = DataFetcher()
    ai = AIAnalyzer()
    
    print("\n【步骤1】获取新闻数据...")
    news = df._fetch_news(time_info)
    
    print(f"\n【新闻统计】")
    print(f"all_news 数量: {len(news.get('all_news', []))}")
    print(f"geopolitics 数量: {len(news.get('geopolitics', []))}")
    print(f"policy 数量: {len(news.get('policy', []))}")
    print(f"other 数量: {len(news.get('other', []))}")
    
    print(f"\n【all_news 详细列表】")
    all_news = news.get('all_news', [])
    for i, item in enumerate(all_news):
        title = item.get('title', '')
        source = item.get('source', '')
        print(f"{i+1:2d}. [{source:10s}] {title}")
    
    print(f"\n【检查关键词匹配】")
    keywords = ['特朗普', '北京', '中美', '会谈', '贸易', '冲突', '军事', '外交', '制裁']
    matched_news = []
    for item in all_news:
        title = item.get('title', '')
        found = [kw for kw in keywords if kw in title]
        if found:
            matched_news.append(item)
            print(f"✓ 发现新闻: [{item.get('source')}] {title} (关键词: {', '.join(found)})")
    
    if not matched_news:
        print("✗ 没有找到匹配的新闻")
    
    print(f"\n【步骤2】AI筛选和分析...")
    if ai.enabled:
        result = ai.select_and_analyze_all_news(all_news)
        
        print(f"\n【AI返回结果】")
        print(f"geopolitics 新闻数: {len(result.get('geopolitics', {}).get('selected_news', []))}")
        print(f"macro_economy 新闻数: {len(result.get('macro_economy', {}).get('selected_news', []))}")
        print(f"government_policy 新闻数: {len(result.get('government_policy', {}).get('selected_news', []))}")
        
        print(f"\n【地缘政治新闻】")
        geo_news = result.get('geopolitics', {}).get('selected_news', [])
        if geo_news:
            for i, item in enumerate(geo_news):
                print(f"{i+1:2d}. [{item.get('source')}] {item.get('title')}")
        else:
            print("(无)")
        print(f"影响分析: {result.get('geopolitics', {}).get('analysis')}")
        
        print(f"\n【宏观经济新闻】")
        macro_news = result.get('macro_economy', {}).get('selected_news', [])
        if macro_news:
            for i, item in enumerate(macro_news):
                print(f"{i+1:2d}. [{item.get('source')}] {item.get('title')}")
        else:
            print("(无)")
        print(f"影响分析: {result.get('macro_economy', {}).get('analysis')}")
        
        print(f"\n【政府政策新闻】")
        policy_news = result.get('government_policy', {}).get('selected_news', [])
        if policy_news:
            for i, item in enumerate(policy_news):
                print(f"{i+1:2d}. [{item.get('source')}] {item.get('title')}")
        else:
            print("(无)")
        print(f"影响分析: {result.get('government_policy', {}).get('analysis')}")
    else:
        print(f"AI未启用")
    
    print(f"\n【调试完成】")

if __name__ == "__main__":
    main()
