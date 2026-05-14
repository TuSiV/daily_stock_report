#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')
from modules.time_service import TimeService
from modules.data_fetcher import DataFetcher
from modules.ai_analyzer import AIAnalyzer

def debug_news_flow():
    print("=== 调试新闻获取和AI分析流程 ===\n")
    
    # 1. 获取时间信息
    ts = TimeService()
    time_info = ts.get_time_info()
    print(f"时间信息: {time_info['date']}")
    
    # 2. 获取新闻数据
    fetcher = DataFetcher()
    news_data = fetcher._fetch_news(time_info)
    
    print(f"\n--- 新闻获取结果 ---")
    print(f"all_news 数量: {len(news_data['all_news'])}")
    print(f"geopolitics 数量: {len(news_data['geopolitics'])}")
    print(f"policy 数量: {len(news_data['policy'])}")
    print(f"other 数量: {len(news_data['other'])}")
    
    print("\n--- all_news 内容 ---")
    for i, news in enumerate(news_data['all_news'][:10]):
        print(f"{i+1}. [{news['source']}] {news['title'][:60]}")
    
    # 3. 测试AI分析
    print("\n--- AI分析测试 ---")
    ai = AIAnalyzer()
    print(f"AI是否启用: {ai.enabled}")
    
    if ai.enabled and news_data['all_news']:
        print("\n开始AI筛选分析...")
        result = ai.select_and_analyze_all_news(news_data['all_news'])
        
        print("\n--- AI分析结果 ---")
        for category in ['geopolitics', 'macro_economy', 'government_policy']:
            cat_data = result.get(category, {})
            news_list = cat_data.get('selected_news', [])
            analysis = cat_data.get('analysis', '')
            
            print(f"\n{category}:")
            print(f"  选中新闻: {len(news_list)}条")
            for news in news_list:
                print(f"    - {news.get('title', '')}")
            print(f"  分析: {analysis}")
    else:
        if not ai.enabled:
            print("AI未启用，请检查DASHSCOPE_API_KEY环境变量")
        if not news_data['all_news']:
            print("all_news为空，无法进行AI分析")

if __name__ == '__main__':
    debug_news_flow()
