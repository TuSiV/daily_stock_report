#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')

from modules.data_fetcher import DataFetcher

def test_news():
    fetcher = DataFetcher()

    # 模拟time_info
    time_info = {
        'date': '2026-05-13',
        'weekday': 'Wednesday',
        'yesterday': '2026-05-12',
        'tz_offset': 8
    }

    print("Fetching news...")
    news = fetcher._fetch_news(time_info)

    print("\n=== News Statistics ===")
    print(f"all_news count: {len(news.get('all_news', []))}")
    print(f"geopolitics count: {len(news.get('geopolitics', []))}")
    print(f"policy count: {len(news.get('policy', []))}")
    print(f"other count: {len(news.get('other', []))}")

    print("\n=== Sample all_news (first 10) ===")
    for i, item in enumerate(news.get('all_news', [])[:10]):
        print(f"{i+1}. [{item.get('source', '')}] {item.get('title', '')[:80]}")

    print("\n=== Geopolitics News ===")
    for item in news.get('geopolitics', [])[:5]:
        print(f"- {item.get('title', '')}")

    return news

if __name__ == '__main__':
    test_news()
