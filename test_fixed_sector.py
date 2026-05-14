#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')
from modules.data_fetcher import DataFetcher
from modules.time_service import TimeService

ts = TimeService()
fetcher = DataFetcher()
time_info = ts.get_time_info()
sectors = fetcher._fetch_sectors(time_info)
print('板块数据:')
for i, s in enumerate(sectors[:5]):
    print(f'{i+1}. {s["name"]}: {s["pct"]}%')
