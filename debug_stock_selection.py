#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')
from modules.time_service import TimeService
from modules.data_fetcher import DataFetcher
from modules.ai_analyzer import AIAnalyzer
from modules.stock_analyzer import StockAnalyzer

def debug_stock_selection():
    print("=== 调试股票选择逻辑 ===\n")
    
    # 获取数据
    ts = TimeService()
    time_info = ts.get_time_info()
    print(f"时间: {time_info['date']}")
    
    fetcher = DataFetcher()
    data = fetcher.fetch_all_data(time_info)
    
    # 检查龙虎榜数据
    lhb = data.get('lhb', {}).get('top_buy', [])
    print(f"\n--- 龙虎榜数据 ({len(lhb)}条) ---")
    for i, stock in enumerate(lhb[:10]):
        print(f"{i+1}. {stock['name']}({stock['code']}): 净买{stock['net_buy']:.2f}万, 涨幅{stock['pct']}%")
    
    # 测试AI选股
    ai = AIAnalyzer()
    print(f"\n--- AI选股测试 ---")
    print(f"AI启用: {ai.enabled}")
    
    if ai.enabled and lhb:
        sectors = data.get('sectors', [])
        result = ai.ai_select_stocks(data, lhb, sectors)
        print(f"AI选择的股票代码: {result['selected_codes']}")
        print(f"市场逻辑: {result.get('market_logic', '')}")
        
        # 匹配股票名称
        code_to_name = {s.get('code', ''): s.get('name', '') for s in lhb}
        for code in result['selected_codes'][:5]:
            if code in code_to_name:
                print(f"  {code}: {code_to_name[code]}")
    else:
        print("AI未启用或龙虎榜为空")
    
    # 测试股票分析器
    print("\n--- 股票分析器选择结果 ---")
    analyzer = StockAnalyzer()
    enhanced_data = data.copy()
    if ai.enabled and lhb:
        enhanced_data['ai_selected_codes'] = result.get('selected_codes', [])
        enhanced_data['ai_stock_reasons'] = result.get('ai_reasons', [])
    
    analysis = analyzer.analyze_stocks(enhanced_data)
    selected = analysis.get('selected_stocks', [])
    
    print(f"最终选择的股票 ({len(selected)}只):")
    for stock in selected:
        print(f"  {stock['name']}({stock['code']}): {stock['industry']}")

if __name__ == '__main__':
    debug_stock_selection()
