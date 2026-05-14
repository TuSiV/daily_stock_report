#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')
from datetime import datetime
from modules.time_service import TimeService

def check_trading_day():
    print("=== 检查交易日 ===\n")
    
    ts = TimeService()
    time_info = ts.get_time_info()
    
    print(f"今天日期: {time_info['date']}")
    print(f"星期: {time_info['weekday_cn']}")
    print(f"是否是交易日: {time_info['is_trading_day']}")
    print(f"上一交易日: {time_info['last_trading_date']}")
    
    # 手动计算今天是星期几
    today = datetime.strptime(time_info['date'], '%Y-%m-%d')
    weekday = today.weekday()  # 0=周一, 6=周日
    print(f"\n今天是周{weekday+1} (0=周一, 6=周日)")
    
    if weekday >= 5:
        print("今天是周末，不是交易日")
    else:
        print("今天是工作日")

if __name__ == '__main__':
    check_trading_day()
