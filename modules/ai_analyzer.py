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
    
    def ai_select_stocks(self, market_data: Dict, lhb_stocks: List[Dict], sectors: List[Dict]) -> Dict:
        """AI综合分析市场数据，智能选择股票"""
        # 1. 收集所有维度的数据
        us_stock = market_data.get('us_stock', {})
        commodity = market_data.get('commodity', {})
        a_stock = market_data.get('a_stock', {})
        
        # 准备AI需要的所有数据
        data_text = []
        
        # 美股市场
        djia = us_stock.get('djia', {})
        nasdaq = us_stock.get('nasdaq', {})
        sp500 = us_stock.get('sp500', {})
        data_text.append(f"【美股市场】道指:{djia.get('point',0)}({djia.get('pct',0)}),纳指:{nasdaq.get('point',0)}({nasdaq.get('pct',0)}),标普500:{sp500.get('point',0)}({sp500.get('pct',0)})")
        
        # 大宗商品
        gold = commodity.get('gold', {})
        wti = commodity.get('wti', {})
        brent = commodity.get('brent', {})
        data_text.append(f"【大宗商品】黄金:{gold.get('price',0)}({gold.get('pct',0)}),WTI原油:{wti.get('price',0)}({wti.get('pct',0)}),布油:{brent.get('price',0)}({brent.get('pct',0)})")
        
        # A股市场
        sh = a_stock.get('sh', {})
        sz = a_stock.get('sz', {})
        cy = a_stock.get('cy', {})
        total_vol = a_stock.get('total_vol', 0)
        data_text.append(f"【A股市场】上证:{sh.get('point',0)}({sh.get('pct',0)}),深证:{sz.get('point',0)}({sz.get('pct',0)}),创业板:{cy.get('point',0)}({cy.get('pct',0)}),成交额:{total_vol}亿")
        
        # 板块涨幅
        data_text.append("\n【板块涨幅TOP5】")
        for i, sec in enumerate(sectors[:5]):
            data_text.append(f"{i+1}. {sec.get('name','')}: {sec.get('pct',0)}%")
        
        # 龙虎榜候选股票
        data_text.append("\n【龙虎榜候选股票】")
        for i, stock in enumerate(lhb_stocks[:15]):
            name = stock.get('name', '')
            code = stock.get('code', '')
            pct = stock.get('pct', 0)
            net_buy = stock.get('net_buy', 0)
            close = stock.get('close', 0)
            data_text.append(f"{i+1}. {name}({code}) | 涨跌幅:{pct}% | 净买入:{net_buy}万 | 收盘价:{close}元")
        
        # AI综合分析和选股
        prompt = f"""作为顶级股票分析师，请基于以下多维度数据，智能选择最值得关注的3-5只股票：

{chr(10).join(data_text)}

选股分析维度：
1. 全球宏观局势（美股、大宗商品对A股影响）
2. 市场情绪与资金流向
3. 强势板块与产业链传导
4. 个股基本面与技术面共振
5. 资金认可度（龙虎榜净买入）

请按以下JSON格式返回（不要包含Markdown标记）：
{{
    "selected_stocks": [
        {{
            "code": "股票代码",
            "name": "股票名称",
            "reason": "选股理由（150字以内）"
        }},
        ...
    ],
    "market_logic": "今日市场整体分析（100字以内）"
}}

**重要要求：**
- **必须**从提供的【龙虎榜候选股票】列表中选择股票
- **股票代码必须与龙虎榜中的代码完全一致**，不要虚构代码
- 优先选择涨幅榜靠前板块中的股票
- 结合龙虎榜净买入金额和涨跌幅综合判断
- 理由要具体、有针对性
"""
        
        result = self._call_ai(prompt, max_tokens=1000)
        
        if result:
            try:
                import json
                import re
                json_match = re.search(r'\{[\s\S]*\}', result)
                if json_match:
                    parsed = json.loads(json_match.group())
                    return {
                        'selected_codes': [s.get('code', '') for s in parsed.get('selected_stocks', [])],
                        'ai_reasons': parsed.get('selected_stocks', []),
                        'market_logic': parsed.get('market_logic', '')
                    }
            except Exception as e:
                print(f'AI选股解析错误: {e}')
        
        # AI失败时的回退方案
        return {
            'selected_codes': [s.get('code', '') for s in lhb_stocks[:5]],
            'ai_reasons': [],
            'market_logic': '全球宏观环境与国内政策'
        }
    
    def ai_select_stocks_chanlun(self, market_data: Dict, chanlun_analysis: List[Dict], sectors: List[Dict], news_analysis: Dict) -> Dict:
        """基于缠论理论智能选股，结合市场数据和新闻信息"""
        if not self.enabled or not chanlun_analysis:
            return {
                'selected_codes': [],
                'ai_reasons': [],
                'market_logic': '缠论分析暂无'
            }
        
        # 1. 收集市场数据
        us_stock = market_data.get('us_stock', {})
        commodity = market_data.get('commodity', {})
        a_stock = market_data.get('a_stock', {})
        
        # 2. 准备缠论分析数据
        data_text = []
        
        # 市场概况
        djia = us_stock.get('djia', {})
        nasdaq = us_stock.get('nasdaq', {})
        sp500 = us_stock.get('sp500', {})
        data_text.append(f"【美股市场】道指:{djia.get('point',0)}({djia.get('pct',0)}%),纳指:{nasdaq.get('point',0)}({nasdaq.get('pct',0)}%),标普500:{sp500.get('point',0)}({sp500.get('pct',0)}%)")
        
        sh = a_stock.get('sh', {})
        sz = a_stock.get('sz', {})
        cy = a_stock.get('cy', {})
        total_vol = a_stock.get('total_vol', 0)
        data_text.append(f"【A股市场】上证:{sh.get('point',0)}({sh.get('pct',0)}%),深证:{sz.get('point',0)}({sz.get('pct',0)}%),创业板:{cy.get('point',0)}({cy.get('pct',0)}%),成交额:{total_vol}亿")
        
        # 板块数据
        data_text.append("\n【强势板块TOP5】")
        for i, sec in enumerate(sectors[:5]):
            data_text.append(f"{i+1}. {sec.get('name','')}: {sec.get('pct',0)}%")
        
        # 新闻分析
        data_text.append("\n【地缘政治分析】")
        geo_news = news_analysis.get('geopolitics', {})
        data_text.append(geo_news.get('analysis', '暂无')[:100])
        
        data_text.append("\n【宏观经济分析】")
        macro_news = news_analysis.get('macro_economy', {})
        data_text.append(macro_news.get('analysis', '暂无')[:100])
        
        data_text.append("\n【政策分析】")
        policy_news = news_analysis.get('government_policy', {})
        data_text.append(policy_news.get('analysis', '暂无')[:100])
        
        # 3. 准备缠论分析数据
        data_text.append("\n【缠论技术分析候选股票】")
        for i, stock in enumerate(chanlun_analysis[:15]):
            name = stock.get('name', '')
            code = stock.get('code', '')
            close = stock.get('close', 0)
            pct = stock.get('pct', 0)
            daily = stock.get('daily', {})
            min60 = stock.get('60min', {})
            min15 = stock.get('15min', {})
            
            data_text.append(f"\n{i+1}. {name}({code}) | 收盘价:{close} | 涨跌幅:{pct}%")
            data_text.append(f"   日线趋势:{daily.get('trend','未知')} | 买点:{daily.get('buy_point','无')} | 关键位:{daily.get('key_level','暂无')}")
            data_text.append(f"   60分钟趋势:{min60.get('trend','未知')} | 买点:{min60.get('buy_point','无')}")
            data_text.append(f"   15分钟趋势:{min15.get('trend','未知')} | 买点:{min15.get('buy_point','无')}")
        
        # 4. AI选股提示词
        prompt = f"""作为缠论技术分析专家，请基于以下多维数据，运用缠论理论选择最值得关注的3-5只股票：

{chr(10).join(data_text)}

缠论选股核心原则：
1. **趋势判断**：优先选择日线、60分钟、15分钟多周期共振向上的股票
2. **买卖点识别**：
   - 一买：下跌趋势结束后的首次买点（风险收益比最佳）
   - 二买：回调不破前低，形成二买（安全性较高）
   - 三买：突破中枢后的回踩确认（趋势确认）
3. **中枢分析**：关注中枢突破、中枢震荡的股票
4. **多周期共振**：日线、60分钟、15分钟趋势一致时信号最强
5. **市场环境**：结合全球宏观、板块热点、资金流向综合判断

请按以下JSON格式返回（不要包含Markdown标记）：
{{
    "selected_stocks": [
        {{
            "code": "股票代码",
            "name": "股票名称",
            "reason": "选股理由（基于缠论理论，150字以内）",
            "chanlun_level": "买点级别（一买/二买/三买/多周期共振）"
        }},
        ...
    ],
    "market_logic": "今日市场整体缠论分析（100字以内）"
}}

**重要要求：**
- 必须从提供的【缠论技术分析候选股票】列表中选择
- 优先选择有明确缠论买点的股票（一买、二买、三买）
- 结合市场环境和板块热点进行综合判断
- 理由要具体引用缠论概念（中枢、笔、线段、买卖点等）
"""
        
        result = self._call_ai(prompt, max_tokens=1200)
        
        if result:
            try:
                import json
                import re
                json_match = re.search(r'\{[\s\S]*\}', result)
                if json_match:
                    parsed = json.loads(json_match.group())
                    return {
                        'selected_codes': [s.get('code', '') for s in parsed.get('selected_stocks', [])],
                        'ai_reasons': parsed.get('selected_stocks', []),
                        'market_logic': parsed.get('market_logic', '')
                    }
            except Exception as e:
                print(f'缠论AI选股解析错误: {e}')
        
        # 回退方案：选择有缠论买点的股票
        buy_point_stocks = [s for s in chanlun_analysis if '买' in str(s.get('daily', {}).get('buy_point', ''))]
        if not buy_point_stocks:
            buy_point_stocks = chanlun_analysis[:5]
        
        return {
            'selected_codes': [s.get('code', '') for s in buy_point_stocks[:5]],
            'ai_reasons': [{'code': s.get('code', ''), 'name': s.get('name', ''), 'reason': f"缠论{s.get('daily', {}).get('buy_point', '无买点')}", 'chanlun_level': s.get('daily', {}).get('buy_point', '无')} for s in buy_point_stocks[:5]],
            'market_logic': '基于缠论技术分析，选择有明确买点的股票'
        }
    
    def select_and_analyze_all_news(self, all_news: List[Dict]) -> Dict:
        """AI直接从所有新闻中筛选地缘政治、宏观经济、政府政策新闻并生成分析"""
        if not all_news or len(all_news) == 0:
            return {
                'geopolitics': {
                    'selected_news': [{'title': '今日无重大地缘政治事件', 'source': ''}],
                    'analysis': '暂无新闻数据'
                },
                'macro_economy': {
                    'selected_news': [{'title': '今日无重大宏观经济事件', 'source': ''}],
                    'analysis': '暂无新闻数据'
                },
                'government_policy': {
                    'selected_news': [{'title': '今日无重大政府政策变化', 'source': ''}],
                    'analysis': '暂无新闻数据'
                }
            }
        
        # 准备新闻列表给AI
        news_list_text = []
        for i, item in enumerate(all_news[:30]):  # 处理最多30条新闻给AI筛选
            title = item.get('title', '')[:200]  # 限制标题长度
            digest = item.get('digest', '')[:200]  # 限制摘要长度
            source = item.get('source', '')
            news_list_text.append(f"[{i+1}] 来源:{source}\n标题:{title}\n摘要:{digest[:100]}")
        
        prompt = f"""作为专业的财经分析师，请从以下新闻列表中，同时完成三类新闻的筛选：

1. 地缘政治新闻：筛选出与地缘政治最相关的新闻（可能包括：冲突、制裁、外交、军事、战争、重大国际事件、中美关系、贸易争端等）
2. 宏观经济新闻：筛选出与宏观经济最相关的新闻（可能包括：GDP、CPI、PPI、PMI、就业数据、央行政策、利率、汇率、通胀、财政政策、经济数据发布、重要经济会议等）
3. 政府政策新闻：筛选出与政府政策变化最相关的新闻（可能包括：国务院政策、证监会政策、监管新规、产业政策、税收政策、金融政策、房地产政策、新能源政策、科技政策等）

每类新闻请：
- 去除重复报道（同一事件保留最完整的一条）
- 选择最重要的3-5条
- 同时生成该类新闻对市场的影响分析（100字以内）

请严格按以下JSON格式返回（不要包含Markdown标记）：
{{
    "geopolitics": {{
        "selected_news": [{{"title": "新闻标题", "source": "来源"}}, ...],
        "analysis": "影响分析"
    }},
    "macro_economy": {{
        "selected_news": [{{"title": "新闻标题", "source": "来源"}}, ...],
        "analysis": "影响分析"
    }},
    "government_policy": {{
        "selected_news": [{{"title": "新闻标题", "source": "来源"}}, ...],
        "analysis": "影响分析"
    }}
}}

新闻列表：
{chr(10).join(news_list_text)}"""
        
        result = self._call_ai(prompt, max_tokens=1200)
        
        # 默认返回值
        default_result = {
            'geopolitics': {
                'selected_news': [{'title': '今日无重大地缘政治事件', 'source': ''}],
                'analysis': '分析暂无'
            },
            'macro_economy': {
                'selected_news': [{'title': '今日无重大宏观经济事件', 'source': ''}],
                'analysis': '分析暂无'
            },
            'government_policy': {
                'selected_news': [{'title': '今日无重大政府政策变化', 'source': ''}],
                'analysis': '分析暂无'
            }
        }
        
        if result:
            try:
                import json
                import re
                
                # 清理响应中的特殊字符
                cleaned_result = result.replace('\u00a0', ' ').replace('\u200b', '')
                
                # 尝试找到JSON片段
                json_match = re.search(r'\{[\s\S]*\}', cleaned_result)
                if json_match:
                    json_str = json_match.group()
                    
                    # 尝试解析
                    parsed = json.loads(json_str)
                    
                    # 确保每个类别都有数据
                    for category in ['geopolitics', 'macro_economy', 'government_policy']:
                        if category not in parsed:
                            parsed[category] = default_result[category]
                        else:
                            # 如果该类别没有选中新闻，使用默认值
                            if 'selected_news' not in parsed[category] or len(parsed[category]['selected_news']) == 0:
                                parsed[category] = default_result[category]
                    
                    print(f'AI新闻筛选成功: 地缘{len(parsed["geopolitics"]["selected_news"])}条, 宏观{len(parsed["macro_economy"]["selected_news"])}条, 政策{len(parsed["government_policy"]["selected_news"])}条')
                    return parsed
                else:
                    print('AI新闻筛选: 未找到JSON片段')
            except json.JSONDecodeError as e:
                print(f'AI新闻筛选JSON解析错误: {e}')
                print(f'AI响应前500字符: {result[:500]}')
            except Exception as e:
                print(f'AI新闻筛选解析错误: {e}')
        
        return default_result

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

    def analyze_us_stock(self, us_stock_data: Dict) -> str:
        """Generate US stock market summary"""
        djia_point = us_stock_data.get('djia', {}).get('point', 0)
        djia_pct = us_stock_data.get('djia', {}).get('pct', 0)
        nasdaq_point = us_stock_data.get('nasdaq', {}).get('point', 0)
        nasdaq_pct = us_stock_data.get('nasdaq', {}).get('pct', 0)
        sp500_point = us_stock_data.get('sp500', {}).get('point', 0)
        sp500_pct = us_stock_data.get('sp500', {}).get('pct', 0)
        
        prompt = f"""作为股票分析师，请根据以下美股数据生成总结：

道琼斯工业指数：{djia_point}点，涨跌幅{djia_pct:+.2f}%
纳斯达克综合指数：{nasdaq_point}点，涨跌幅{nasdaq_pct:+.2f}%
标普500指数：{sp500_point}点，涨跌幅{sp500_pct:+.2f}%

请用中文简洁总结（50字以内），包括：
1. 今日市场整体表现
2. 市场情绪判断"""
        
        result = self._call_ai(prompt, max_tokens=100)
        return result if result else '美股市场数据'
    
    def analyze_us_stock_notes(self, us_stock_data: Dict) -> Dict:
        """Generate notes for each US stock index"""
        djia_point = us_stock_data.get('djia', {}).get('point', 0)
        djia_pct = us_stock_data.get('djia', {}).get('pct', 0)
        nasdaq_point = us_stock_data.get('nasdaq', {}).get('point', 0)
        nasdaq_pct = us_stock_data.get('nasdaq', {}).get('pct', 0)
        sp500_point = us_stock_data.get('sp500', {}).get('point', 0)
        sp500_pct = us_stock_data.get('sp500', {}).get('pct', 0)
        
        notes = {}
        
        prompt_dj = f"""作为股票分析师，请为道琼斯工业指数生成简短备注：

当前：{djia_point}点，{djia_pct:+.2f}%

请用中文生成一句话备注（20字以内），说明该指数的主要特征或关键信息。"""
        result = self._call_ai(prompt_dj, max_tokens=50)
        notes['djia'] = result if result else '道琼斯工业平均指数'
        
        prompt_nasdaq = f"""作为股票分析师，请为纳斯达克综合指数生成简短备注：

当前：{nasdaq_point}点，{nasdaq_pct:+.2f}%

请用中文生成一句话备注（20字以内），说明该指数的主要特征或关键信息。"""
        result = self._call_ai(prompt_nasdaq, max_tokens=50)
        notes['nasdaq'] = result if result else '纳斯达克综合指数'
        
        prompt_sp = f"""作为股票分析师，请为标普500指数生成简短备注：

当前：{sp500_point}点，{sp500_pct:+.2f}%

请用中文生成一句话备注（20字以内），说明该指数的主要特征或关键信息。"""
        result = self._call_ai(prompt_sp, max_tokens=50)
        notes['sp500'] = result if result else '标普500指数'
        
        return notes
    
    def analyze_commodity(self, commodity_data: Dict) -> str:
        """Generate commodity market summary"""
        gold_price = commodity_data.get('gold', {}).get('price', 0)
        gold_pct = commodity_data.get('gold', {}).get('pct', 0)
        wti_price = commodity_data.get('wti', {}).get('price', 0)
        wti_pct = commodity_data.get('wti', {}).get('pct', 0)
        brent_price = commodity_data.get('brent', {}).get('price', 0)
        brent_pct = commodity_data.get('brent', {}).get('pct', 0)
        
        prompt = f"""作为商品分析师，请根据以下数据生成总结：

现货黄金：{gold_price}美元/盎司，涨跌幅{gold_pct:+.2f}%
WTI原油：{wti_price}美元/桶，涨跌幅{wti_pct:+.2f}%
布伦特原油：{brent_price}美元/桶，涨跌幅{brent_pct:+.2f}%

请用中文简洁总结（50字以内），包括：
1. 今日大宗商品整体表现
2. 重点关注要点"""
        
        result = self._call_ai(prompt, max_tokens=100)
        return result if result else '大宗商品价格分析'
    
    def analyze_a_stock_market(self, a_stock_data: Dict) -> str:
        """Generate A-share market summary"""
        sh_point = a_stock_data.get('sh', {}).get('point', 0)
        sh_pct = a_stock_data.get('sh', {}).get('pct', 0)
        sz_point = a_stock_data.get('sz', {}).get('point', 0)
        sz_pct = a_stock_data.get('sz', {}).get('pct', 0)
        cy_point = a_stock_data.get('cy', {}).get('point', 0)
        cy_pct = a_stock_data.get('cy', {}).get('pct', 0)
        total_vol = a_stock_data.get('total_vol', 0)
        
        prompt = f"""作为A股分析师，请根据以下数据生成总结：

上证指数：{sh_point}点，涨跌幅{sh_pct:+.2f}%
深证成指：{sz_point}点，涨跌幅{sz_pct:+.2f}%
创业板指：{cy_point}点，涨跌幅{cy_pct:+.2f}%
两市成交额：{total_vol:.2f}亿元

请用中文简洁总结（50字以内），包括：
1. 今日A股整体表现
2. 市场情绪判断"""
        
        result = self._call_ai(prompt, max_tokens=100)
        return result if result else 'A股市场整体表现'
    
    def generate_key_drivers(self, market_data: Dict) -> str:
        """Generate key drivers summary"""
        sectors = market_data.get('sectors', [])
        sectors_text = ''
        for i, sector in enumerate(sectors[:3]):
            sectors_text += f"{sector.get('name', '')}：{sector.get('pct', 0):+.2f}%\n"
        
        prompt = f"""作为股票分析师，请根据以下板块数据提炼今日市场的关键驱动因素：

{sectors_text}
请用中文简洁总结（60字以内），包括：
1. 主要上涨/下跌的板块
2. 可能的驱动因素"""
        
        result = self._call_ai(prompt, max_tokens=120)
        return result if result else '板块轮动带动市场'
    
    def generate_market_logic(self, market_data: Dict) -> str:
        """Generate market logic summary"""
        us_pct = market_data.get('us_stock', {}).get('djia', {}).get('pct', 0)
        a_pct = market_data.get('a_stock', {}).get('sh', {}).get('pct', 0)
        
        prompt = f"""作为股票分析师，请分析今日市场的主要逻辑：

美股道琼斯：{us_pct:+.2f}%
A股上证：{a_pct:+.2f}%

请用中文简洁总结（40字以内），说明：
1. 全球市场与国内市场的关系
2. 主要政策导向"""
        
        result = self._call_ai(prompt, max_tokens=80)
        return result if result else '全球宏观环境与国内政策'
    
    def enhance_report(self, report_data: Dict) -> Dict:
        """Enhance report with AI analysis"""
        if not self.enabled:
            return report_data
        
        enhanced = report_data.copy()
        
        # Analyze US stock
        print('AI: Analyzing US stock market...')
        us_summary = self.analyze_us_stock(report_data.get('us_stock', {}))
        enhanced['us_stock']['summary'] = us_summary
        
        # Generate US stock notes
        print('AI: Generating US stock notes...')
        us_notes = self.analyze_us_stock_notes(report_data.get('us_stock', {}))
        if us_notes.get('djia'):
            enhanced['us_stock']['djia']['note'] = us_notes['djia']
        if us_notes.get('nasdaq'):
            enhanced['us_stock']['nasdaq']['note'] = us_notes['nasdaq']
        if us_notes.get('sp500'):
            enhanced['us_stock']['sp500']['note'] = us_notes['sp500']
        
        # Analyze commodity
        print('AI: Analyzing commodity market...')
        commodity_summary = self.analyze_commodity(report_data.get('commodity', {}))
        enhanced['commodity']['summary'] = commodity_summary
        
        # Analyze A stock market
        print('AI: Analyzing A-share market...')
        a_stock_summary = self.analyze_a_stock_market(report_data.get('a_stock', {}))
        enhanced['market_summary']['market_note'] = a_stock_summary
        
        # Generate key drivers and logic
        print('AI: Generating key drivers...')
        enhanced['key_drivers'] = self.generate_key_drivers(report_data)
        enhanced['market_logic'] = self.generate_market_logic(report_data)
        
        # AI智能统一筛选所有新闻（地缘政治、宏观经济、政府政策）
        news = report_data.get('news', {})
        all_news = news.get('all_news', [])
        if all_news:
            print('AI: Selecting and analyzing all news categories...')
            all_news_result = self.select_and_analyze_all_news(all_news)
            
            # 处理地缘政治新闻
            geo_result = all_news_result.get('geopolitics', {})
            selected = geo_result.get('selected_news', [])
            enhanced['geopolitics_selected'] = selected
            enhanced['geopolitics_analysis'] = geo_result.get('analysis', '分析暂无')
            
            # 处理宏观经济新闻
            macro_result = all_news_result.get('macro_economy', {})
            selected = macro_result.get('selected_news', [])
            enhanced['macro_economy_selected'] = selected
            enhanced['macro_economy_analysis'] = macro_result.get('analysis', '分析暂无')
            
            # 处理政府政策新闻
            policy_result = all_news_result.get('government_policy', {})
            selected = policy_result.get('selected_news', [])
            enhanced['government_policy_selected'] = selected
            enhanced['government_policy_analysis'] = policy_result.get('analysis', '分析暂无')
        else:
            # 默认值
            enhanced['geopolitics_selected'] = [{'title': '今日无重大地缘政治事件', 'source': ''}]
            enhanced['geopolitics_analysis'] = '分析暂无'
            enhanced['macro_economy_selected'] = [{'title': '今日无重大宏观经济事件', 'source': ''}]
            enhanced['macro_economy_analysis'] = '分析暂无'
            enhanced['government_policy_selected'] = [{'title': '今日无重大政府政策变化', 'source': ''}]
            enhanced['government_policy_analysis'] = '分析暂无'
        
        # AI智能选股：综合分析多维度数据
        lhb_data = report_data.get('lhb', {})
        lhb = lhb_data.get('top_buy', [])
        sectors = report_data.get('sectors', [])
        if lhb and sectors:
            print('AI: AI Intelligent stock selection...')
            ai_result = self.ai_select_stocks(report_data, lhb, sectors)
            enhanced['ai_selected_codes'] = ai_result.get('selected_codes', [])
            enhanced['ai_stock_reasons'] = ai_result.get('ai_reasons', [])
            # 更新市场逻辑（如果AI有更好的分析）
            if ai_result.get('market_logic'):
                enhanced['market_logic'] = ai_result['market_logic']
        
        # Enhance sector drivers
        sectors = report_data.get('sectors', [])
        for i, sector in enumerate(sectors[:10]):  # 分析全部10个板块
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
