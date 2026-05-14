#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')
from datetime import datetime
from modules.time_service import TimeService

def debug_time():
    print("=== 调试时间服务 ===\n")

    ts = TimeService()

    # 测试各个时间源
    print("1. 系统当前时间:")
    print(f"   {datetime.now()}")

    print("\n2. 东方财富API返回的时间:")
    try:
        eastmoney_time = ts._get_time_from_eastmoney()
        print(f"   {eastmoney_time}")
    except Exception as e:
        print(f"   失败: {e}")

    print("\n3. 百度时间:")
    try:
        baidu_time = ts._get_time_from_baidu()
        print(f"   {baidu_time}")
    except Exception as e:
        print(f"   失败: {e}")

    print("\n4. NTSC时间:")
    try:
        ntsc_time = ts._get_time_from_ntsc()
        print(f"   {ntsc_time}")
    except Exception as e:
        print(f"   失败: {e}")

    print("\n5. get_time_info() 完整返回:")
    try:
        time_info = ts.get_time_info()
        import pprint
        pprint.pprint(time_info)
    except Exception as e:
        print(f"   失败: {e}")

if __name__ == '__main__':
    debug_time()
