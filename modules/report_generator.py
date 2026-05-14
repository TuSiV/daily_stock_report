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
        r = r.replace('{last_trading_date}', str(time_info.get('last_trading_date', '')))

        # US stock
        us = data.get('us_stock', {})
        for key, prefix in [('djia','dj'),('nasdaq','nasdaq'),('sp500','sp500')]:
            item = us.get(key, {})
            r = r.replace('{' + prefix + '_point}', self._fmt_num(item.get('point', '-')))
            r = r.replace('{' + prefix + '_pct}', self._fmt_pct(item.get('pct', '-')))
            r = r.replace('{' + prefix + '_note}', str(item.get('note', '')))
        r = r.replace('{us_summary}', str(us.get('summary', '美股数据获取中')))

        # 地缘政治 - 使用AI筛选后的新闻
        geo_selected = data.get('geopolitics_selected', [])
        geo_analysis = data.get('geopolitics_analysis', '')
        
        if geo_selected:
            geo_text_list = []
            for i, item in enumerate(geo_selected[:5]):
                title = item.get('title', '')
                source = item.get('source', '')
                geo_text_list.append(f'{i+1}. {title}')
            geo_text = '\n'.join(geo_text_list)
        else:
            geo_text = '今日无重大地缘政治事件'
        
        r = r.replace('{geopolitics_items}', geo_text)
        r = r.replace('{geopolitics_summary}', geo_analysis if geo_analysis else '暂无详细分析')
        
        # 宏观经济 - 使用AI筛选后的新闻
        macro_selected = data.get('macro_economy_selected', [])
        macro_analysis = data.get('macro_economy_analysis', '')
        
        if macro_selected:
            macro_text_list = []
            for i, item in enumerate(macro_selected[:5]):
                title = item.get('title', '')
                source = item.get('source', '')
                macro_text_list.append(f'{i+1}. {title}')
            macro_text = '\n'.join(macro_text_list)
        else:
            macro_text = '今日无重大宏观经济事件'
        
        r = r.replace('{macro_economy_items}', macro_text)
        r = r.replace('{macro_economy_summary}', macro_analysis if macro_analysis else '暂无详细分析')
        
        # 政府政策 - 使用AI筛选后的新闻
        policy_selected = data.get('government_policy_selected', [])
        policy_analysis = data.get('government_policy_analysis', '')
        
        if policy_selected:
            policy_text_list = []
            for i, item in enumerate(policy_selected[:5]):
                title = item.get('title', '')
                source = item.get('source', '')
                policy_text_list.append(f'{i+1}. {title}')
            policy_text = '\n'.join(policy_text_list)
        else:
            policy_text = '今日无重大政府政策变化'
        
        r = r.replace('{government_policy_items}', policy_text)
        r = r.replace('{government_policy_summary}', policy_analysis if policy_analysis else '暂无详细分析')

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
        r = r.replace('{key_drivers}', str(data.get('key_drivers', '板块轮动带动市场')))
        r = r.replace('{logic_1}', str(data.get('market_logic', '全球宏观环境与国内政策')))

        # Stocks - 加入 AI 选股理由
        stocks = data.get('selected_stocks', [])
        ai_reasons = data.get('ai_stock_reasons', [])
        
        # 创建 code -> reason 的映射
        reason_map = {}
        for reason_item in ai_reasons:
            code = reason_item.get('code', '')
            reason = reason_item.get('reason', '')
            if code and reason:
                reason_map[code] = reason
        
        for i in range(5):
            idx = str(i+1)
            if i < len(stocks):
                s = stocks[i].copy()
                # 查找 AI 生成的选股理由
                code = s.get('code', '')
                if code in reason_map:
                    s['reason'] = reason_map[code]
                elif s.get('ai_reason'):
                    # 如果reason_map中没有，使用stock_analyzer生成的理由
                    s['reason'] = s['ai_reason']
                # 替换模板变量
                for k, v in s.items():
                    r = r.replace('{stock_' + idx + '_' + k + '}', str(v))
            else:
                keys = ['name', 'code', 'industry', 'close', 'pct', 'capital', 'reason',
                       'd_trend', 'd_buy', 'd_key', '60_trend', '60_buy', '60_key',
                       '15_trend', '15_buy', '15_key', 'volume', 'buy_range', 'buy_note',
                       'stop', 'stop_note', 'target1', 'target1_note', 'target2', 'target2_note', 'rr']
                for k in keys:
                    r = r.replace('{stock_' + idx + '_' + k + '}', '')

        # 清理未替换的占位符（如 {stock_4_reason} 等
        import re
        r = re.sub(r'\{stock_\d+_reason\}', '精选优质标的，资金关注度高', r)

        # Risk and sources - use AI risk warning if available
        risk_warning = data.get('risk_warning', '')
        if risk_warning:
            r = r.replace('{risk_items}', risk_warning)
        else:
            r = r.replace('{risk_items}', '市场有风险，投资需谨慎')
        r = r.replace('{data_sources}', '东方财富、新浪财经、国家授时中心')

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
                val = val.replace('%', '')
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
            # val 单位是万元
            if v >= 10000:
                # 转换为亿元
                return f'{v/10000:.2f}亿'
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
