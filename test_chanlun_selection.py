#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')
from modules.time_service import TimeService
from modules.data_fetcher import DataFetcher
from modules.ai_analyzer import AIAnalyzer
from modules.chanlun import ChanAnalyzer

def test_chanlun_selection():
    print("=== 测试基于缠论的AI选股流程 ===\n")
    
    # 获取时间信息
    ts = TimeService()
    time_info = ts.get_time_info()
    print(f"时间: {time_info['date']}")
    
    # 获取市场数据
    fetcher = DataFetcher()
    market_data = fetcher.fetch_all_data(time_info)
    
    # 获取热门股票
    print("\n--- 获取热门股票 ---")
    hot_stocks = fetcher.fetch_hot_stocks(limit=20)  # 测试用20只
    print(f"获取到 {len(hot_stocks)} 只热门股票")
    
    # 进行缠论分析
    print("\n--- 缠论技术分析 ---")
    chan_analyzer = ChanAnalyzer()
    chanlun_analysis = []
    
    for stock in hot_stocks[:10]:  # 测试用前10只
        code = stock.get('code', '')
        name = stock.get('name', '')
        if code:
            try:
                chan_result = chan_analyzer.analyze(code)
                stock['daily'] = chan_result.get('daily', {})
                stock['60min'] = chan_result.get('60min', {})
                stock['15min'] = chan_result.get('15min', {})
                chanlun_analysis.append(stock)
                
                daily = stock['daily']
                print(f"{name}({code}): 趋势={daily.get('trend','未知')}, 买点={daily.get('buy_point','无')}")
            except Exception as e:
                print(f'{name}({code}) 缠论分析失败: {e}')
    
    print(f"\n完成缠论分析: {len(chanlun_analysis)} 只")
    
    # AI新闻筛选
    print("\n--- AI新闻筛选 ---")
    ai = AIAnalyzer()
    news_analysis = ai.select_and_analyze_all_news(market_data.get('news', {}).get('all_news', []))
    
    # 基于缠论的AI选股
    print("\n--- 基于缠论的AI选股 ---")
    sectors = market_data.get('sectors', [])
    ai_selection = ai.ai_select_stocks_chanlun(
        market_data, 
        chanlun_analysis, 
        sectors,
        news_analysis
    )
    
    print(f"AI选择的股票: {ai_selection['selected_codes']}")
    print(f"市场逻辑: {ai_selection.get('market_logic', '')}")
    
    print("\n--- 选股理由 ---")
    for reason in ai_selection.get('ai_reasons', []):
        print(f"{reason.get('name', '')}({reason.get('code', '')}):")
        print(f"  理由: {reason.get('reason', '')}")
        print(f"  级别: {reason.get('chanlun_level', '')}")

if __name__ == '__main__':
    test_chanlun_selection()
