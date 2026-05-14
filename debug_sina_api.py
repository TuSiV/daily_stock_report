#!/usr/bin/env python3
import requests

def debug_sina_api():
    print("=== 调试新浪财经API ===\n")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://finance.sina.com.cn/'
    }
    
    # 测试多个新浪API地址
    urls = [
        'https://hq.sinajs.cn/list=gb_dji,gb_ixic,gb_spx',
        'https://hq.sinajs.cn/list=sh000001,sz399001',
        'https://gupiao.sina.com.cn/api/openapi.php/FinanceServer.MarketIndexService.getUSIndex'
    ]
    
    for url in urls:
        print(f"\n测试URL: {url}")
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            print(f"状态码: {resp.status_code}")
            print(f"响应内容: {resp.text[:500]}")
        except Exception as e:
            print(f"错误: {e}")

if __name__ == '__main__':
    debug_sina_api()
