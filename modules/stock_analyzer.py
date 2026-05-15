#!/usr/bin/env python3
from config.settings import NUM_STOCKS_TO_SELECT


class StockAnalyzer:
    def __init__(self):
        pass

    def analyze_stocks(self, data):
        """分析股票，使用AI选择的股票"""
        candidates = self._select_candidates(data)
        analyzed = []
        sectors = data.get('sectors', [])
        sector_names = [s.get('name', '') for s in sectors[:3]]

        for i, stock in enumerate(candidates[:NUM_STOCKS_TO_SELECT]):
            analysis = self._analyze_single(stock, data, i, sector_names)
            analyzed.append(analysis)

        return {
            'selected_stocks': analyzed,
            'market_summary': data.get('market_summary', {}),
            'us_stock': data.get('us_stock', {}),
            'commodity': data.get('commodity', {}),
            'a_stock': data.get('a_stock', {}),
            'sectors': data.get('sectors', []),
            'lhb': data.get('lhb', {}),
            'northbound': data.get('northbound', {}),
            'news': data.get('news', {}),
            'ai_market_logic': data.get('ai_market_logic', '')
        }

    def _select_candidates(self, data):
        """选择候选股票 - 优先使用AI选择的股票"""
        candidates = []
        
        # 获取AI选择的股票代码
        ai_selected_codes = data.get('ai_selected_codes', [])
        
        # 获取缠论分析结果
        chanlun_analysis = data.get('chanlun_analysis', [])
        
        # 获取热门股票列表（用于补充）
        hot_stocks = data.get('hot_stocks', [])
        
        # 构建缠论分析股票映射
        code_to_stock = {s.get('code', ''): s for s in chanlun_analysis}
        
        # 构建热门股票映射
        hot_code_to_stock = {s.get('code', ''): s for s in hot_stocks}
        
        # 记录已选的股票代码
        selected_codes = set()
        
        if ai_selected_codes and len(ai_selected_codes) > 0:
            # 使用AI选择的股票，从缠论分析结果中匹配
            for code in ai_selected_codes:
                if code in code_to_stock and code not in selected_codes:
                    candidates.append(code_to_stock[code])
                    selected_codes.add(code)
                    if len(candidates) >= NUM_STOCKS_TO_SELECT:
                        break
                elif code in hot_code_to_stock and code not in selected_codes:
                    # 如果缠论分析中没有，从热门股票中获取
                    candidates.append(hot_code_to_stock[code])
                    selected_codes.add(code)
                    if len(candidates) >= NUM_STOCKS_TO_SELECT:
                        break
            
            # 统计有效选择数量
            effective_count = len(candidates)
            print(f'AI选择股票: {ai_selected_codes}, 有效匹配: {effective_count}只')
        
        # 如果候选股票不足，从缠论分析结果中补充
        if len(candidates) < NUM_STOCKS_TO_SELECT:
            # 优先选择有缠论买点的股票
            buy_point_stocks = [s for s in chanlun_analysis if '买' in str(s.get('daily', {}).get('buy_point', ''))]
            buy_point_stocks = sorted(buy_point_stocks, key=lambda x: x.get('amount', 0), reverse=True)
            
            for item in buy_point_stocks:
                code = item.get('code', '')
                if code not in selected_codes and len(candidates) < NUM_STOCKS_TO_SELECT:
                    candidates.append(item)
                    selected_codes.add(code)
        
        # 如果仍然不足，从热门股票中补充（确保有5只）
        if len(candidates) < NUM_STOCKS_TO_SELECT:
            # 按成交额排序的热门股票
            sorted_hot = sorted(hot_stocks, key=lambda x: x.get('amount', 0), reverse=True)

            for item in sorted_hot:
                code = item.get('code', '')
                if code not in selected_codes and len(candidates) < NUM_STOCKS_TO_SELECT:
                    candidates.append(item)
                    selected_codes.add(code)

        # 如果仍然不足，从龙虎榜数据中补充
        if len(candidates) < NUM_STOCKS_TO_SELECT:
            lhb_stocks = data.get('lhb', {}).get('top_buy', [])
            sorted_lhb = sorted(lhb_stocks, key=lambda x: x.get('net_buy', 0), reverse=True)

            for item in sorted_lhb:
                code = item.get('code', '')
                if code not in selected_codes and len(candidates) < NUM_STOCKS_TO_SELECT:
                    # 转换LHB数据格式为候选格式
                    candidate = {
                        'code': code,
                        'name': item.get('name', ''),
                        'close': item.get('close', 0),
                        'pct': item.get('pct', 0),
                        'vol': 0,
                        'amount': 0,
                        'turnover': 0,
                        'industry': '',
                        'daily': {},
                        '60min': {},
                        '15min': {}
                    }
                    candidates.append(candidate)
                    selected_codes.add(code)
        
        print(f'最终候选股票数量: {len(candidates)}只')
        return candidates

    def _analyze_single(self, stock, data, index, sector_names):
        """分析单只股票"""
        name = stock.get('name', 'Unknown')
        code = stock.get('code', '000000')
        close = stock.get('close', 0)
        pct = stock.get('pct', 0)
        amount = stock.get('amount', 0)
        
        # 行业分类：优先使用股票自身的行业字段
        industry = stock.get('industry', '')
        if not industry or industry == '':
            # 如果没有行业字段，使用默认值
            industry = '热门板块'

        # 获取缠论分析结果
        daily = stock.get('daily', {})
        min60 = stock.get('60min', {})
        min15 = stock.get('15min', {})

        # 计算交易级别 - 默认止损5%
        stop_loss = round(close * 0.95, 2)
        target1 = round(close * 1.10, 2)
        target2 = round(close * 1.20, 2)
        buy_low = round(close * 0.98, 2)
        buy_high = round(close * 1.02, 2)

        # 使用缠论关键位 - 限制最大止损幅度为8%
        max_stop_loss = round(close * 0.92, 2)  # 最大止损8%
        if daily.get('key_level'):
            key_level = daily['key_level']
            # 尝试提取支撑位
            if '支撑' in str(key_level):
                try:
                    import re
                    support_match = re.search(r'支撑[:：]?(\d+\.?\d*)', str(key_level))
                    if support_match:
                        chan_stop = float(support_match.group(1))
                        # 只有当缠论支撑位在合理范围内时才使用（不超过8%）
                        if chan_stop >= max_stop_loss:
                            stop_loss = chan_stop
                        else:
                            stop_loss = max_stop_loss
                except:
                    pass

        # 确保止损位不超过最大止损幅度
        if stop_loss < max_stop_loss:
            stop_loss = max_stop_loss

        risk = close - stop_loss
        reward = target1 - close
        rr = round(reward / risk, 1) if risk > 0 else 0
        
        # 盈亏比验证：如果小于1:1，标记风险较高
        rr_note = ''
        if rr < 1.0:
            rr_note = '（风险较高）'

        # 成交量描述
        if daily.get('trend') == '上涨趋势':
            volume_desc = '放量上涨，买盘强劲'
        elif daily.get('trend') == '盘整':
            volume_desc = '成交量正常，等待方向'
        else:
            volume_desc = '成交量萎缩，观望为主'

        # 成交额处理：amount是成交量（股），需要转换为亿元
        amount_yi = amount / 100000000  # 转换为亿

        # 获取AI选股理由
        ai_reasons = data.get('ai_stock_reasons', [])
        ai_reason = ''
        for reason in ai_reasons:
            if reason.get('code') == code:
                ai_reason = reason.get('reason', '')
                break
        
        # 如果没有AI选股理由，生成一个基于股票特征的理由
        if not ai_reason:
            trend = daily.get('trend', '未知')
            buy_point = daily.get('buy_point', '无')
            if '买' in str(buy_point):
                ai_reason = f'{industry}板块，{trend}，出现{buy_point}信号，技术面表现较好。'
            elif trend == '上涨趋势':
                ai_reason = f'{industry}板块，{trend}，多头排列，关注回调买入机会。'
            else:
                ai_reason = f'{industry}板块，资金关注度高，关注后续走势变化。'

        return {
            'name': name,
            'code': code,
            'industry': industry,
            'close': str(close),
            'pct': str(pct),
            'capital': f'成交额: {amount_yi:.2f}亿，{volume_desc}',
            'd_trend': daily.get('trend', '未知'),
            'd_buy': daily.get('buy_point', '无'),
            'd_key': daily.get('key_level', '暂无'),
            '60_trend': min60.get('trend', '未知'),
            '60_buy': min60.get('buy_point', '无'),
            '60_key': min60.get('key_level', '暂无'),
            '15_trend': min15.get('trend', '未知'),
            '15_buy': min15.get('buy_point', '无'),
            '15_key': min15.get('key_level', '暂无'),
            'volume': volume_desc,
            'buy_range': f'{buy_low}-{buy_high}',
            'buy_note': '等待回调买入，切勿追高',
            'stop': str(stop_loss),
            'stop_note': '跌破支撑位止损，严格纪律',
            'target1': str(target1),
            'target1_note': '第一阻力位，部分止盈',
            'target2': str(target2),
            'target2_note': '第二阻力位，考虑清仓',
            'rr': f'{rr}:1{rr_note}',
            'ai_reason': ai_reason
        }
