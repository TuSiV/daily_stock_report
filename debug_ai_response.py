#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')
from modules.time_service import TimeService
from modules.data_fetcher import DataFetcher
from modules.ai_analyzer import AIAnalyzer

def debug_ai_response():
    print("=== 调试AI新闻筛选响应 ===\n")
    
    # 获取新闻数据
    ts = TimeService()
    time_info = ts.get_time_info()
    
    fetcher = DataFetcher()
    news_data = fetcher._fetch_news(time_info)
    
    print(f"all_news数量: {len(news_data['all_news'])}")
    
    # 测试AI分析
    ai = AIAnalyzer()
    
    if ai.enabled and news_data['all_news']:
        # 直接调用_call_ai获取原始响应
        news_list_text = []
        for i, item in enumerate(news_data['all_news'][:30]):
            title = item.get('title', '')[:200]
            digest = item.get('digest', '')[:200]
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

请严格按以下JSON格式返回（不要包含Markdown标记，不要包含任何额外解释）：
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
        
        print("\n=== AI原始响应 ===")
        raw_result = ai._call_ai(prompt, max_tokens=1200)
        print(f"响应内容:\n{raw_result}")
        print(f"\n响应长度: {len(raw_result)}")
        
        # 尝试解析
        print("\n=== 尝试解析JSON ===")
        try:
            import json
            import re
            json_match = re.search(r'\{[\s\S]*\}', raw_result)
            if json_match:
                print(f"找到JSON片段: {json_match.group()[:500]}...")
                parsed = json.loads(json_match.group())
                print("JSON解析成功！")
            else:
                print("未找到JSON片段")
        except Exception as e:
            print(f"JSON解析失败: {e}")

if __name__ == '__main__':
    debug_ai_response()
