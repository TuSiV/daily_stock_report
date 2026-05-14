
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.data_fetcher import DataFetcher
from modules.time_service import TimeService

print("=" * 80)
print("详细调试新闻数据获取")
print("=" * 80)

ts = TimeService()
time_info = ts.get_time_info()

df = DataFetcher()
news = df._fetch_news(time_info)

print(f"\n获取到所有新闻总数: {len(news['all_news'])}")
print(f"\n分类为地缘政治的新闻: {len(news['geopolitics'])}")
print(f"分类为政府政策的新闻: {len(news['policy'])}")

print("\n" + "=" * 80)
print("所有获取到的新闻列表 (前30条):")
print("=" * 80)
for i, item in enumerate(news['all_news'][:30], 1):
    title = item.get('title', '')
    source = item.get('source', '')
    print(f"[{i:2d}] [{source:10s}] {title}")

print("\n" + "=" * 80)
print("分类为地缘政治的新闻:")
print("=" * 80)
if len(news['geopolitics']) == 0:
    print("(无)")
else:
    for i, item in enumerate(news['geopolitics'], 1):
        print(f"[{i}] {item.get('title', '')}")

print("\n" + "=" * 80)
print("分类为政府政策的新闻:")
print("=" * 80)
if len(news['policy']) == 0:
    print("(无)")
else:
    for i, item in enumerate(news['policy'], 1):
        print(f"[{i}] {item.get('title', '')}")

print("\n" + "=" * 80)
print("调试完成")
print("=" * 80)

