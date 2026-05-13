#!/usr/bin/env python3
"""AI Analysis Module using Qwen (通义千问)"""

import os
import json
from typing import List, Dict, Optional

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class AIAnalyzer:
    def __init__(self):
        self.api_key = os.getenv('DASHSCOPE_API_KEY', '')
        self.model = os.getenv('QWEN_MODEL', 'qwen3.6-35b-a3b')
        
        if OPENAI_AVAILABLE and self.api_key:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
            )
            self.enabled = True
        else:
            self.enabled = False
            print('AI disabled: DASHSCOPE_API_KEY not set or openai not installed')

    def _call_ai(self, prompt: str, max_tokens: int = 500) -> str:
        """Call Qwen API using OpenAI compatible mode"""
        if not self.enabled:
            return ''
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一位专业的股票分析师，擅长分析A股市场、缠论技术分析和投资建议。请用中文简洁回答。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f'AI call error: {e}')
            return ''

    def analyze_news(self, news_items: List[Dict]) -> str:
        """Analyze news impact on market"""
        if not news_items:
            return '今日无重大新闻事件'
        
        news_text = '\n'.join([f"- {item.get('title', '')}" for item in news_items[:5]])
        
        prompt = f"""作为一位专业的股票分析师，请分析以下新闻对A股市场的影响：

{news_text}

请用中文简洁分析（100字以内）：
1. 利好/利空哪些板块
2. 对市场情绪的影响
3. 投资者应关注的要点"""
        
        result = self._call_ai(prompt)
        return result if result else '新闻分析暂无'

    def analyze_sector_driver(self, sector_name: str, pct_change: float) -> str:
        """Analyze sector driving factors"""
        prompt = f"""作为股票分析师，请分析板块"{sector_name}"今日涨跌幅{pct_change:+.2f}%的可能驱动因素。

请用中文简洁回答（50字以内），可能的原因包括：
- 政策利好
- 行业景气
- 资金追捧
- 业绩超预期
- 技术突破
- 其他"""
        
        result = self._call_ai(prompt, max_tokens=100)
        return result if result else '驱动因素分析暂无'

    def generate_stock_reason(self, stock_info: Dict) -> str:
        """Generate stock selection reason"""
        name = stock_info.get('name', '')
        code = stock_info.get('code', '')
        sector = stock_info.get('industry', '')
        pct = stock_info.get('pct', 0)
        net_buy = stock_info.get('net_buy', 0)
        chan_trend = stock_info.get('d_trend', '')
        chan_buy = stock_info.get('d_buy', '')
        
        # Convert to proper types
        try:
            pct_val = float(pct)
        except:
            pct_val = 0
        try:
            net_buy_val = float(net_buy)
        except:
            net_buy_val = 0
        
        prompt = f"""作为股票分析师，请为以下股票生成选股理由：

股票：{name}({code})
所属板块：{sector}
涨跌幅：{pct_val:+.2f}%
龙虎榜净买入：{net_buy_val:.2f}万
缠论走势：{chan_trend}
缠论买点：{chan_buy}

请用中文简洁说明选股理由（100字以内），包括：
1. 为什么选择这只股票
2. 核心逻辑
3. 预期走势"""
        
        result = self._call_ai(prompt)
        return result if result else f'{sector}板块龙头，资金关注度高'

    def generate_trading_advice(self, stock_info: Dict) -> str:
        """Generate trading advice"""
        name = stock_info.get('name', '')
        close = stock_info.get('close', 0)
        stop_loss = stock_info.get('stop', 0)
        target1 = stock_info.get('target1', 0)
        buy_range = stock_info.get('buy_range', '')
        
        prompt = f"""作为股票分析师，请为以下股票生成操作建议：

股票：{name}
当前价：{close}元
买入区间：{buy_range}
止损位：{stop_loss}元
第一目标：{target1}元

请用中文简洁的操作建议（80字以内），包括：
1. 买入时机
2. 持仓策略
3. 止盈止损建议"""
        
        result = self._call_ai(prompt)
        return result if result else f'建议在{buy_range}区间买入，止损{stop_loss}元'

    def generate_risk_warning(self, market_data: Dict) -> str:
        """Generate risk warning"""
        us_stock = market_data.get('us_stock', {})
        a_stock = market_data.get('a_stock', {})
        
        sh_pct = a_stock.get('sh', {}).get('pct', 0)
        dj_pct = us_stock.get('djia', {}).get('pct', 0)
        
        try:
            sh_val = float(sh_pct)
        except:
            sh_val = 0
        try:
            dj_val = float(dj_pct)
        except:
            dj_val = 0
        
        prompt = f"""作为股票分析师，请根据以下市场数据生成风险提示：

美股道琼斯涨跌幅：{dj_val:+.2f}%
A股上证涨跌幅：{sh_val:+.2f}%

请用中文简洁的风险提示（100字以内），包括：
1. 市场主要风险
2. 投资者注意事项
3. 风险控制建议"""
        
        result = self._call_ai(prompt)
        return result if result else '市场有风险，投资需谨慎。建议控制仓位，设置止损。'

    def enhance_report(self, report_data: Dict) -> Dict:
        """Enhance report with AI analysis"""
        if not self.enabled:
            return report_data
        
        enhanced = report_data.copy()
        
        # Enhance news analysis
        news = report_data.get('news', {})
        if news.get('geopolitics'):
            print('AI: Analyzing news...')
            enhanced['geopolitics_analysis'] = self.analyze_news(news['geopolitics'])
        
        # Enhance sector drivers
        sectors = report_data.get('sectors', [])
        for i, sector in enumerate(sectors[:3]):
            print(f'AI: Analyzing sector {sector.get("name", "")}...')
            driver = self.analyze_sector_driver(sector.get('name', ''), sector.get('pct', 0))
            enhanced['sectors'][i]['reason'] = driver
        
        # Enhance stock analysis
        stocks = report_data.get('selected_stocks', [])
        for i, stock in enumerate(stocks):
            print(f'AI: Analyzing stock {stock.get("name", "")}...')
            enhanced['selected_stocks'][i]['reason'] = self.generate_stock_reason(stock)
            enhanced['selected_stocks'][i]['advice'] = self.generate_trading_advice(stock)
        
        # Generate risk warning
        print('AI: Generating risk warning...')
        enhanced['risk_warning'] = self.generate_risk_warning(report_data)
        
        return enhanced
