#!/usr/bin/env python3

import json
import requests
from dataclasses import dataclass
from typing import List
from config.settings import USER_AGENT, REQUEST_TIMEOUT


@dataclass
class Kline:
    date: str
    open: float
    close: float
    high: float
    low: float
    volume: float
    index: int = 0


@dataclass
class Fractal:
    index: int
    kline: Kline
    type: str


@dataclass
class Bi:
    start: Fractal
    end: Fractal
    direction: str
    high: float
    low: float


@dataclass
class ZhongShu:
    start_bi: int
    end_bi: int
    high: float
    low: float
    gg: float
    dd: float


@dataclass
class BuyPoint:
    type: int
    price: float
    date: str
    description: str


class ChanAnalyzer:
    def __init__(self):
        self.headers = {"User-Agent": USER_AGENT}
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def get_klines(self, code, period="daily", count=100):
        # 根据股票代码判断市场
        if code.startswith("6"):
            secid = f"1.{code}"
            qq_code = f"sh{code}"
        elif code.startswith("0") or code.startswith("3"):
            secid = f"0.{code}"
            qq_code = f"sz{code}"
        elif code.startswith("8") or code.startswith("4"):
            secid = f"0.{code}"
            qq_code = f"sz{code}"
        else:
            secid = f"0.{code}"
            qq_code = f"sz{code}"

        klt_map = {"daily": 101, "60min": 60, "15min": 15, "30min": 30, "weekly": 102}
        klt = klt_map.get(period, 101)

        # 1. 优先尝试腾讯财经API（日线稳定）
        if period == "daily":
            klines = self._get_klines_tencent(qq_code, period, count)
            if klines:
                return klines

        # 2. 如果腾讯失败或非日线，尝试新浪财经
        klines = self._get_klines_sina(code, period, count)
        if klines:
            return klines

        # 3. 如果新浪失败，尝试东方财富API
        klines = self._get_klines_eastmoney(secid, klt, count)
        if klines:
            return klines

        # 4. 如果东方财富也失败，尝试腾讯分钟线
        if period != "daily":
            klines = self._get_klines_tencent(qq_code, period, count)
            if klines:
                return klines

        print(f"All K-line sources failed for {code}")
        return []
    
    def _get_klines_eastmoney(self, secid, klt, count):
        """从东方财富获取K线数据"""
        url = "https://push2his.eastmoney.com/api/qt/stock/kline/get"
        params = {
            "secid": secid,
            "fields1": "f1,f2,f3,f4,f5,f6",
            "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
            "klt": klt,
            "fqt": 1,
            "beg": 0,
            "end": 20500101,
            "lmt": count
        }
        
        try:
            resp = self.session.get(url, params=params, timeout=REQUEST_TIMEOUT)
            data = resp.json()
            klines = []
            if data.get("data") and data["data"].get("klines"):
                for i, k in enumerate(data["data"]["klines"]):
                    parts = k.split(",")
                    klines.append(Kline(
                        date=parts[0],
                        open=float(parts[1]),
                        close=float(parts[2]),
                        high=float(parts[3]),
                        low=float(parts[4]),
                        volume=float(parts[5]),
                        index=i
                    ))
            return klines
        except Exception as e:
            return []
    
    def _get_klines_sina(self, code, period, count):
        """从新浪财经获取K线数据（备用）"""
        try:
            # 新浪财经K线API
            period_map = {"daily": "240", "60min": "60", "15min": "15", "30min": "30", "weekly": "1200"}
            period_sina = period_map.get(period, "240")
            
            url = f"https://quotes.sina.cn/cn/api/jsonp_v2.php/var%20_k=/CN_MarketDataService.getKLineData"
            params = {
                "symbol": f"sh{code}" if code.startswith("6") else f"sz{code}",
                "scale": period_sina,
                "ma": "no",
                "datalen": count
            }
            
            resp = self.session.get(url, params=params, timeout=REQUEST_TIMEOUT)
            if resp and resp.status_code == 200:
                # 解析JSONP响应
                text = resp.text
                json_str = text[text.index("(") + 1:text.rindex(")")]
                data = json.loads(json_str)
                
                klines = []
                for i, item in enumerate(data):
                    klines.append(Kline(
                        date=item.get("day", ""),
                        open=float(item.get("open", 0)),
                        close=float(item.get("close", 0)),
                        high=float(item.get("high", 0)),
                        low=float(item.get("low", 0)),
                        volume=float(item.get("volume", 0)),
                        index=i
                    ))
                return klines
        except Exception as e:
            print(f"Sina K-line error: {e}")
        return []
    
    def _get_klines_tencent(self, code, period, count):
        """从腾讯财经获取K线数据（备用）"""
        try:
            # 腾讯财经K线API
            period_map = {"daily": "day", "60min": "60min", "15min": "15min", "30min": "30min", "weekly": "week"}
            period_qq = period_map.get(period, "day")
            
            market = "sh" if code.startswith("6") else "sz"
            url = f"https://web.ifzq.gtimg.cn/appstock/app/fqkline/get"
            params = {
                "param": f"{market}{code},{period_qq},,{count},qfq",
                "_var": f"kline_{period_qq}"
            }
            
            resp = self.session.get(url, params=params, timeout=REQUEST_TIMEOUT)
            if resp and resp.status_code == 200:
                text = resp.text
                # 解析响应
                json_str = text[text.index("=") + 1:]
                data = json.loads(json_str)
                
                klines = []
                if data.get("data") and data["data"].get(f"{market}{code}"):
                    stock_data = data["data"][f"{market}{code}"]
                    kline_key = f"qfq{period_qq}" if f"qfq{period_qq}" in stock_data else period_qq
                    
                    if kline_key in stock_data:
                        for i, item in enumerate(stock_data[kline_key]):
                            if len(item) >= 6:
                                klines.append(Kline(
                                    date=item[0],
                                    open=float(item[1]),
                                    close=float(item[2]),
                                    high=float(item[3]),
                                    low=float(item[4]),
                                    volume=float(item[5]) if len(item) > 5 else 0,
                                    index=i
                                ))
                return klines
        except Exception as e:
            print(f"Tencent K-line error: {e}")
        return []
    
    def find_fractals(self, klines):
        fractals = []
        for i in range(1, len(klines) - 1):
            prev = klines[i - 1]
            curr = klines[i]
            next_k = klines[i + 1]
            
            if prev.high < curr.high and curr.high > next_k.high:
                if prev.low < curr.low and curr.low > next_k.low:
                    fractals.append(Fractal(index=i, kline=curr, type="top"))
            elif prev.low > curr.low and curr.low < next_k.low:
                if prev.high > curr.high and curr.high < next_k.high:
                    fractals.append(Fractal(index=i, kline=curr, type="bottom"))
        
        return fractals
    
    def find_bi(self, klines, fractals):
        if len(fractals) < 2:
            return []
        
        bis = []
        i = 0
        
        while i < len(fractals) - 1:
            start = fractals[i]
            end = fractals[i + 1]
            
            if start.type == end.type:
                i += 1
                continue
            
            if abs(end.index - start.index) < 4:
                i += 1
                continue
            
            if start.type == "bottom" and end.type == "top":
                direction = "up"
            elif start.type == "top" and end.type == "bottom":
                direction = "down"
            else:
                i += 1
                continue
            
            high = max(k.high for k in klines[start.index:end.index + 1])
            low = min(k.low for k in klines[start.index:end.index + 1])
            
            bis.append(Bi(start=start, end=end, direction=direction, high=high, low=low))
            i += 1
        
        return bis
    
    def find_zhongshu(self, bis):
        if len(bis) < 3:
            return []
        
        zhongshus = []
        i = 0
        
        while i < len(bis) - 2:
            bi1 = bis[i]
            bi2 = bis[i + 1]
            bi3 = bis[i + 2]
            
            zg = min(bi1.high, bi2.high, bi3.high)
            zd = max(bi1.low, bi2.low, bi3.low)
            
            if zg > zd:
                gg = max(bi1.high, bi2.high, bi3.high)
                dd = min(bi1.low, bi2.low, bi3.low)
                zhongshus.append(ZhongShu(start_bi=i, end_bi=i + 2, high=zg, low=zd, gg=gg, dd=dd))
                i += 3
            else:
                i += 1
        
        return zhongshus
    
    def analyze_trend(self, bis, zhongshus):
        if not bis:
            return "unknown"
        
        if zhongshus:
            last_bi = bis[-1]
            if last_bi.direction == "up":
                bottoms = [b for b in bis[-5:] if b.direction == "up"]
                if len(bottoms) >= 2 and bottoms[-1].low > bottoms[-2].low:
                    return "uptrend"
            if last_bi.direction == "down":
                tops = [b for b in bis[-5:] if b.direction == "down"]
                if len(tops) >= 2 and tops[-1].high < tops[-2].high:
                    return "downtrend"
            return "consolidation"
        
        return "uptrend" if bis[-1].direction == "up" else "downtrend"
    
    def find_buy_points(self, klines, bis, zhongshus):
        buy_points = []
        if not bis or not zhongshus:
            return buy_points
        
        last_zs = zhongshus[-1]
        last_bi = bis[-1]
        
        # Type 1: downtrend ends below center
        if last_bi.direction == "down" and last_bi.low < last_zs.low:
            if last_bi.end.type == "bottom":
                buy_points.append(BuyPoint(type=1, price=last_bi.end.kline.close, date=last_bi.end.kline.date, description="一买：下跌趋势在中枢下方结束"))
        
        # Type 2: pullback stays above center
        if len(bis) >= 3:
            prev_bi = bis[-3]
            if prev_bi.direction == "down" and prev_bi.low < last_zs.low:
                if last_bi.direction == "down" and last_bi.low > last_zs.low:
                    buy_points.append(BuyPoint(type=2, price=last_bi.end.kline.close, date=last_bi.end.kline.date, description="二买：回调不破中枢"))
        
        # Type 3: break above center
        if last_bi.direction == "up" and last_bi.high > last_zs.high:
            buy_points.append(BuyPoint(type=3, price=last_bi.end.kline.close, date=last_bi.end.kline.date, description="三买：突破中枢上沿"))
        
        return buy_points
    
    def analyze(self, code):
        result = {
            "daily": {"trend": "unknown", "buy_point": "none", "key_level": ""},
            "60min": {"trend": "unknown", "buy_point": "none", "key_level": ""},
            "15min": {"trend": "unknown", "buy_point": "none", "key_level": ""}
        }
        
        for period in ["daily", "60min", "15min"]:
            klines = self.get_klines(code, period, 100)
            if not klines:
                continue
            
            fractals = self.find_fractals(klines)
            bis = self.find_bi(klines, fractals)
            zhongshus = self.find_zhongshu(bis)
            trend = self.analyze_trend(bis, zhongshus)
            buy_points = self.find_buy_points(klines, bis, zhongshus)
            
            key_levels = []
            if zhongshus:
                zs = zhongshus[-1]
                key_levels.append(f"中枢:{zs.low:.2f}-{zs.high:.2f}")
            if bis:
                last_bi = bis[-1]
                if last_bi.direction == "up":
                    key_levels.append(f"支撑:{last_bi.low:.2f}")
                else:
                    key_levels.append(f"压力:{last_bi.high:.2f}")
            
            buy_point = "无"
            if buy_points:
                bp = buy_points[-1]
                buy_types = {1: "一买", 2: "二买", 3: "三买"}
                buy_point = f"{buy_types.get(bp.type, '未知')}({bp.date})"
            
            trend_cn = {
                "uptrend": "上涨趋势",
                "downtrend": "下跌趋势",
                "consolidation": "盘整",
                "unknown": "未知"
            }.get(trend, trend)
            
            result[period] = {
                "trend": trend_cn,
                "buy_point": buy_point,
                "key_level": ", ".join(key_levels) if key_levels else "暂无",
                "buy_points": buy_points,
                "zhongshus": zhongshus,
                "bis": bis
            }
        
        return result
