#!/usr/bin/env python3
import os
from config.settings import REPORTS_DIR

class ReportGenerator:
    def __init__(self):
        self.template_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'template.md')
        self.output_dir = REPORTS_DIR
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_report(self, analysis_results, time_info):
        template = self._load_template()
        report = self._fill_template(template, analysis_results, time_info)
        return self._save_report(report, time_info)

    def _load_template(self):
        try:
            with open(self.template_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return '# Report Template not found'

    def _fill_template(self, template, data, time_info):
        r = template

        # Time info
        r = r.replace('{date}', str(time_info.get('date', '')))
        r = r.replace('{weekday}', str(time_info.get('weekday', '')))
        r = r.replace('{yesterday}', str(time_info.get('yesterday', '')))

        # US stock
        us = data.get('us_stock', {})
        for key, prefix in [('djia','dj'),('nasdaq','nasdaq'),('sp500','sp500')]:
            item = us.get(key, {})
            r = r.replace('{' + prefix + '_point}', self._fmt_num(item.get('point', '-')))
            r = r.replace('{' + prefix + '_pct}', self._fmt_pct(item.get('pct', '-')))
            r = r.replace('{' + prefix + '_note}', str(item.get('note', '')))
        r = r.replace('{us_summary}', str(us.get('summary', '美股三大指数涨跌不一')))

        # Geopolitics - use AI analysis if available
        geo_analysis = data.get('geopolitics_analysis', '')
        if geo_analysis:
            r = r.replace('{geopolitics_items}', geo_analysis)
        else:
            news = data.get('news', {})
            geo_items = news.get('geopolitics', [])
            if geo_items:
                geo_text = chr(10).join(['- ' + item.get('title', '') for item in geo_items[:5]])
            else:
                geo_text = '- 今日无重大地缘政治事件'
            r = r.replace('{geopolitics_items}', geo_text)

        # Commodity
        cm = data.get('commodity', {})
        for key in ['gold', 'wti', 'brent']:
            item = cm.get(key, {})
            r = r.replace('{' + key + '_price}', self._fmt_num(item.get('price', '-')))
            r = r.replace('{' + key + '_pct}', self._fmt_pct(item.get('pct', '-')))
        r = r.replace('{commodity_summary}', str(cm.get('summary', '大宗商品价格波动不大')))

        # A-stock
        ast = data.get('a_stock', {})
        for key, prefix in [('sh','sh'),('sz','sz'),('cy','cy')]:
            item = ast.get(key, {})
            r = r.replace('{' + prefix + '_point}', self._fmt_num(item.get('point', '-')))
            r = r.replace('{' + prefix + '_pct}', self._fmt_pct(item.get('pct', '-')))
            r = r.replace('{' + prefix + '_vol}', self._fmt_vol(item.get('vol', 0)))
        ms = data.get('market_summary', {})
        r = r.replace('{total_vol}', self._fmt_vol(ms.get('total_vol', 0)))
        r = r.replace('{market_note}', str(ms.get('market_note', '')))

        # Sectors
        sectors = data.get('sectors', [])
        for i in range(10):
            idx = str(i+1)
            if i < len(sectors):
                s = sectors[i]
                r = r.replace('{sector_' + idx + '}', str(s.get('name', '-')))
                r = r.replace('{sector_' + idx + '_pct}', self._fmt_pct(s.get('pct', '-')))
                r = r.replace('{sector_' + idx + '_reason}', str(s.get('reason', '-')))
            else:
                r = r.replace('{sector_' + idx + '}', '-')
                r = r.replace('{sector_' + idx + '_pct}', '-')
                r = r.replace('{sector_' + idx + '_reason}', '-')
        r = r.replace('{decline_sectors}', '详见板块排名')

        # Capital flow
        r = r.replace('{main_flow_summary}', '详见龙虎榜数据')

        # LHB
        lhb = data.get('lhb', {}).get('top_buy', [])
        for i in range(5):
            idx = str(i+1)
            if i < len(lhb):
                item = lhb[i]
                r = r.replace('{lhb_' + idx + '_name}', str(item.get('name', '-')))
                r = r.replace('{lhb_' + idx + '_amount}', self._fmt_amount(item.get('net_buy', 0)))
                r = r.replace('{lhb_' + idx + '_pct}', self._fmt_pct(item.get('pct', '-')))
            else:
                r = r.replace('{lhb_' + idx + '_name}', '-')
                r = r.replace('{lhb_' + idx + '_amount}', '-')
                r = r.replace('{lhb_' + idx + '_pct}', '-')

        # Institutional (use first 3 from lhb)
        for i in range(3):
            idx = str(i+1)
            if i < len(lhb):
                item = lhb[i]
                r = r.replace('{inst_' + idx + '_name}', str(item.get('name', '-')))
                r = r.replace('{inst_' + idx + '_amount}', self._fmt_amount(item.get('net_buy', 0)))
                r = r.replace('{inst_' + idx + '_pct}', self._fmt_pct(item.get('pct', '-')))
                r = r.replace('{north_' + idx + '_name}', str(item.get('name', '-')))
                r = r.replace('{north_' + idx + '_amount}', self._fmt_amount(item.get('net_buy', 0)))
                r = r.replace('{north_' + idx + '_pct}', self._fmt_pct(item.get('pct', '-')))
            else:
                for prefix in ['inst', 'north']:
                    r = r.replace('{' + prefix + '_' + idx + '_name}', '-')
                    r = r.replace('{' + prefix + '_' + idx + '_amount}', '-')
                    r = r.replace('{' + prefix + '_' + idx + '_pct}', '-')

        # Key drivers
        r = r.replace('{key_drivers}', '板块轮动带动市场情绪，关注政策面和资金面变化')
        r = r.replace('{logic_1}', '全球宏观环境与国内政策导向')

        # Stocks
        stocks = data.get('selected_stocks', [])
        for i in range(5):
            idx = str(i+1)
            if i < len(stocks):
                s = stocks[i]
                for k, v in s.items():
                    r = r.replace('{stock_' + idx + '_' + k + '}', str(v))
            else:
                defaults = {
                    'name': '-', 'code': '-', 'industry': '-', 'close': '-', 'pct': '-',
                    'capital': '-', 'reason': '-', 'd_trend': '-', 'd_buy': '-', 'd_key': '-',
                    '60_trend': '-', '60_buy': '-', '60_key': '-',
                    '15_trend': '-', '15_buy': '-', '15_key': '-',
                    'volume': '-', 'buy_range': '-', 'buy_note': '-',
                    'stop': '-', 'stop_note': '-', 'target1': '-', 'target1_note': '-',
                    'target2': '-', 'target2_note': '-', 'rr': '-'
                }
                for k, v in defaults.items():
                    r = r.replace('{stock_' + idx + '_' + k + '}', v)

        # Risk and sources - use AI risk warning if available
        risk_warning = data.get('risk_warning', '')
        if risk_warning:
            r = r.replace('{risk_items}', risk_warning)
        else:
            r = r.replace('{risk_items}', '- 市场风险：宏观经济不确定性\n- 个股风险：板块轮动风险\n- 操作风险：追涨杀跌风险')
        r = r.replace('{data_sources}', '东方财富、新浪财经、国家授时中心、通义千问AI')

        return r

    def _fmt_num(self, val):
        try:
            if isinstance(val, str):
                val = val.replace(',', '')
            return str(round(float(val), 2))
        except:
            return str(val)

    def _fmt_pct(self, val):
        try:
            if isinstance(val, str):
                val = val.replace('%', '').replace('+', '')
            v = float(val)
            return f'{v:+.2f}'
        except:
            return str(val)

    def _fmt_vol(self, val):
        try:
            v = float(val)
            return f'{v:.2f}'
        except:
            return str(val)

    def _fmt_amount(self, val):
        try:
            v = float(val)
            if v >= 10000:
                return f'{v:.2f}亿'
            return f'{v:.2f}万'
        except:
            return str(val)

    def _save_report(self, content, time_info):
        filename = 'daily_report_' + str(time_info.get('date', 'unknown')) + '.md'
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print('Report saved to', filepath)
        return filepath
