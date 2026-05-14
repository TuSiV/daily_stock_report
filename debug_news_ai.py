#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')

from modules.data_fetcher import DataFetcher
from modules.ai_analyzer import AIAnalyzer
import os

def test_news_ai():
    fetcher = DataFetcher()
    analyzer = AIAnalyzer()

    time_info = {'date': '2026-05-13', 'weekday': 'Wednesday', 'yesterday': '2026-05-12', 'tz_offset': 8}

    print("Step 1: Fetching news...")
    news = fetcher._fetch_news(time_info)
    all_news = news.get('all_news', [])

    print(f"\nTotal news: {len(all_news)}")

    if not all_news:
        print("No news fetched!")
        return

    print("\nStep 2: AI selecting and analyzing news...")
    result = analyzer.select_and_analyze_all_news(all_news)

    print("\n=== AI Result ===")
    print(f"Geopolitics: {len(result.get('geopolitics', {}).get('selected_news', []))} items")
    print(f"Macro Economy: {len(result.get('macro_economy', {}).get('selected_news', []))} items")
    print(f"Government Policy: {len(result.get('government_policy', {}).get('selected_news', []))} items")

    geo_news = result.get('geopolitics', {}).get('selected_news', [])
    if geo_news:
        print("\n=== Geopolitics News ===")
        for i, item in enumerate(geo_news):
            print(f"{i+1}. {item.get('title', '')[:60]}")
        print(f"\nAnalysis: {result.get('geopolitics', {}).get('analysis', '')}")

    macro_news = result.get('macro_economy', {}).get('selected_news', [])
    if macro_news:
        print("\n=== Macro Economy News ===")
        for i, item in enumerate(macro_news):
            print(f"{i+1}. {item.get('title', '')[:60]}")

    policy_news = result.get('government_policy', {}).get('selected_news', [])
    if policy_news:
        print("\n=== Government Policy News ===")
        for i, item in enumerate(policy_news):
            print(f"{i+1}. {item.get('title', '')[:60]}")

if __name__ == '__main__':
    test_news_ai()
