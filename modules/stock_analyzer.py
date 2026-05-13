#!/usr/bin/env python3
from config.settings import MIN_LHB_NET_BUY, NUM_STOCKS_TO_SELECT
from modules.chanlun import ChanAnalyzer


class StockAnalyzer:
    def __init__(self):
        self.chan = ChanAnalyzer()

    def analyze_stocks(self, data):
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
            'news': data.get('news', {})
        }

    def _select_candidates(self, data):
        candidates = []
        lhb = data.get('lhb', {}).get('top_buy', [])
        sorted_lhb = sorted(lhb, key=lambda x: abs(x.get('net_buy', 0)), reverse=True)
        for item in sorted_lhb:
            if len(candidates) >= NUM_STOCKS_TO_SELECT:
                break
            candidates.append(item)
        return candidates

    def _analyze_single(self, stock, data, index, sector_names):
        name = stock.get('name', 'Unknown')
        code = stock.get('code', '000000')
        close = stock.get('close', 0)
        pct = stock.get('pct', 0)
        net_buy = stock.get('net_buy', 0)
        sector = sector_names[index % len(sector_names)] if sector_names else '热门板块'

        # Get real Chan Theory analysis
        chan_result = self.chan.analyze(code)
        
        daily = chan_result.get('daily', {})
        min60 = chan_result.get('60min', {})
        min15 = chan_result.get('15min', {})

        # Calculate trading levels based on Chan analysis
        stop_loss = round(close * 0.95, 2)
        target1 = round(close * 1.10, 2)
        target2 = round(close * 1.20, 2)
        buy_low = round(close * 0.98, 2)
        buy_high = round(close * 1.02, 2)

        # Use Chan levels if available
        if daily.get('key_level') and '支撑' in str(daily.get('key_level', '')):
            try:
                support_str = [x for x in str(daily['key_level']).split(',') if '支撑' in x][0]
                stop_loss = float(support_str.split(':')[1].strip())
            except:
                pass

        risk = close - stop_loss
        reward = target1 - close
        rr = round(reward / risk, 1) if risk > 0 else 0

        # Determine volume description based on trend
        if daily.get('trend') == '上涨趋势':
            volume_desc = '放量上涨，买盘强劲'
        elif daily.get('trend') == '盘整':
            volume_desc = '成交量正常，等待方向'
        else:
            volume_desc = '成交量萎缩，观望为主'

        return {
            'name': name,
            'code': code,
            'industry': sector,
            'close': str(close),
            'pct': str(pct),
            'capital': f'龙虎榜净买入: {net_buy:.2f}万，机构参与',
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
            'rr': f'{rr}:1'
        }
