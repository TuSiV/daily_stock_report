
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.data_fetcher import DataFetcher
from modules.time_service import TimeService

print("开始调试新闻获取...")

ts = TimeService()
time_info = ts.get_time_info()

df = DataFetcher()
news = df._fetch_news(time_info)

print(f"\n获取到 {len(news['all_news'])} 条新闻")
print(f"分类到地缘政治: {len(news['geopolitics'])} 条")

print("\n=== 全部新闻 ===")
for i, item in enumerate(news['all_news'][:20], 1):
    print(f"[{i}] {item['source']}: {item['title']}")

print("\n=== 分类为地缘政治的新闻 ===")
for i, item in enumerate(news['geopolitics'][:10], 1):
    print(f"[{i}] {item['source']}: {item['title']}")

