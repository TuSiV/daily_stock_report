#!/usr/bin/env python3
import re

class DataProcessor:
    def __init__(self):
        pass

    def process_data(self, raw_data):
        processed = {}
        processed['us_stock'] = self._process_us_stock(raw_data.get('us_stock', {}))
        processed['commodity'] = self._process_commodity(raw_data.get('commodity', {}))
        processed['a_stock'] = self._process_a_stock(raw_data.get('a_stock', {}))
        processed['sectors'] = self._process_sectors(raw_data.get('sectors', []))
        processed['lhb'] = self._process_lhb(raw_data.get('lhb', {}))
        processed['northbound'] = self._process_northbound(raw_data.get('northbound', {}))
        processed['news'] = raw_data.get('news', {})
        processed['market_summary'] = self._generate_market_summary(processed)
        return processed

    def _safe_float(self, val, default=0.0):
        try:
            if isinstance(val, str):
                val = val.replace(',', '').replace('%', '').strip()
            return float(val)
        except (ValueError, TypeError):
            return default

    def _process_us_stock(self, data):
        result = {}
        for key in ['djia', 'nasdaq', 'sp500']:
            item = data.get(key, {})
            result[key] = {
                'point': self._safe_float(item.get('point', 0)),
                'pct': self._safe_float(item.get('pct', 0)),
                'note': ''
            }
        result['summary'] = data.get('summary', '')
        return result

    def _process_commodity(self, data):
        result = {}
        for key in ['gold', 'wti', 'brent']:
            item = data.get(key, {})
            result[key] = {
                'price': self._safe_float(item.get('price', 0)),
                'pct': self._safe_float(item.get('pct', 0))
            }
        result['summary'] = data.get('summary', '')
        return result

    def _process_a_stock(self, data):
        result = {}
        for key in ['sh', 'sz', 'cy']:
            item = data.get(key, {})
            result[key] = {
                'point': self._safe_float(item.get('point', 0)),
                'pct': self._safe_float(item.get('pct', 0)),
                'vol': self._safe_float(item.get('vol', 0))
            }
        result['total_vol'] = self._safe_float(data.get('total_vol', 0))
        return result

    def _process_sectors(self, data):
        result = []
        for item in data:
            result.append({
                'rank': item.get('rank', 0),
                'name': item.get('name', ''),
                'pct': self._safe_float(item.get('pct', 0)),
                'reason': item.get('reason', '')
            })
        return result

    def _process_lhb(self, data):
        result = {'top_buy':[], 'inst_buy':[], 'north_buy':[]}
        for item in data.get('top_buy', []):
            result['top_buy'].append({
                'name': item.get('name', ''),
                'code': item.get('code', ''),
                'net_buy': self._safe_float(item.get('net_buy', 0)) / 10000,
                'pct': self._safe_float(item.get('pct', 0)),
                'close': self._safe_float(item.get('close', 0))
            })
        return result

    def _process_northbound(self, data):
        return {
            'total_net': self._safe_float(data.get('total_net', 0)) / 100000000,
            'top_buy': data.get('top_buy', [])
        }

    def _generate_market_summary(self, data):
        sh = data.get('a_stock', {}).get('sh', {})
        total_vol = data.get('a_stock', {}).get('total_vol', 0)
        note = ''
        if sh.get('pct', 0) > 0:
            note = '市场上涨'
        elif sh.get('pct', 0) < 0:
            note = '市场下跌'
        else:
            note = '市场持平'
        return {
            'total_vol': round(total_vol, 2),
            'market_note': note
        }
