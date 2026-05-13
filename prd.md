# 每日选股分析任务 — 定时任务执行指令

---

## 第零步：获取权威时间（必须首先执行）

从www.ntsc.ac.cn获取中国科学院国家授时中心的实时北京时间：

### 非交易日标注

如果当日非交易日（区分美股非交易日和A股非交易日）时：
- 报告标题下方注明"今日为非交易日，报告基于YYYY年M月D日（周X）收盘数据"
- 美股和A股数据均使用最近一个交易日的收盘数据

---

## 第一步：搜索隔夜全球市场动态

**搜索关键词必须强制包含当前完整年月日**，格式为 `"YYYY年M月D日"`，例如：
- ✅ `"2030年5月1日 美股收盘 道琼斯 纳斯达克"`
- ❌ `"5月1日 美股收盘"` （缺少年份，可能搜到往年数据）
- ❌ `"美股收盘"` （完全没有日期）

**数据年份校验（必须执行）：**
- 搜索结果中每条数据必须验证年份是否与授时中心返回的年份一致
- 发现年份不匹配的数据（如2026年搜索却返回2024/2025年数据）**立即丢弃**
- 若某次搜索返回的数据年份全部不匹配，必须重新搜索并加更精确的日期关键词

需获取：
1. **美股三大指数**（道琼斯、纳斯达克、标普500）收盘点位和涨跌幅
2. **地缘政治**重大事件（冲突、外交、制裁等）
3. **大宗商品**价格（原油、黄金等）
4. **政府政策**（中国央行货币政策、财政政策、行业监管政策等）
5. **其他影响A股的重大事件**（美联储政策、贸易摩擦等）

---

## 第二步：搜索A股市场数据

**搜索关键词必须强制包含当前完整年月日**，格式为 `"YYYY年M月D日"`，例如：
- ✅ `"2030年5月1日 A股 收盘 板块涨幅 龙虎榜"`
- ❌ `"A股收盘 板块涨幅"` （缺少日期）

**数据年份校验（必须执行）：**
- 同第一步，严格验证每条数据的年份
- 特别注意：搜索"A股收盘"时经常返回往年同月同日数据，必须核对年份

需获取：
1. **三大指数**（上证、深成、创业板）收盘点位、涨跌幅、成交额
2. **板块涨幅排名** TOP10（含涨幅和驱动因素）
3. **板块跌幅**（资金流出的方向）
4. **龙虎榜数据**：
   - 龙虎榜净买入额排名前10个股（含金额、涨跌幅、换手率）
   - 机构席位净买入排名前5
   - 北向资金（深沪股通）净买入排名前5
5. **北向资金**整体净流入/流出金额
6. **主力资金**整体流向
7. **关键政策事件**（央行政策、行业政策等）

---

## 第三步：综合分析筛选5只股票

### 选股标准（必须全部满足）

1. **板块逻辑**：当日强势板块中的个股，有明确的题材/政策/事件驱动
2. **资金验证**：龙虎榜净买入 > 5000万，且机构或北向资金有参与
3. **多来源覆盖**：5只股票应覆盖不同行业，不集中在单一板块
4. **缠论买点**：需分析日线、60分钟、15分钟三个级别，优先选择二买/三买
5. **量价配合**：成交量放大、换手充分、封板/收盘强势

### 价格交叉验证

每只股票的收盘价必须从至少2个不同来源验证一致（如东方财富、同花顺、新浪财经、证券之星等）。

### 每只股票必须包含

- 所属行业/概念
- 价格验证表格（来源、收盘价、涨跌幅）
- 资金面数据（龙虎榜净买入、机构净买入、北向净买入）
- **缠论多级别分析表格**（级别、走势类型、买点类型、关键位置）
- 量价配合分析
- **操作建议表格**（买入区间、止损位、第一目标、第二目标）

---

## 第四步：生成报告

### 报告模板

严格按照下面的格式生成Markdown报告。

# 📊 每日选股分析报告

**日期：{date}（{weekday}）**

---

## 一、隔夜全球市场动态

### 🇺🇸 美股市场（{yesterday}收盘）

| 指数 | 收盘点位 | 涨跌幅 | 备注 |
|------|---------|--------|------|
| 道琼斯工业指数 | {dj_point} | {dj_pct}% | {dj_note} |
| 纳斯达克综合指数 | {nasdaq_point} | {nasdaq_pct}% | {nasdaq_note} |
| 标普500指数 | {sp500_point} | {sp500_pct}% | {sp500_note} |

**要点：** {us_summary}

### 🌍 地缘政治

{geopolitics_items}

### 🛢️ 大宗商品

| 品种 | 最新价格 | 涨跌幅 |
|------|---------|--------|
| 现货黄金 | {gold_price} | {gold_pct} |
| WTI原油 | {wti_price} | {wti_pct} |
| 布伦特原油 | {brent_price} | {brent_pct} |

**要点：** {commodity_summary}

---

## 二、A股市场复盘（{date}）

### 📈 三大指数表现

| 指数 | 收盘点位 | 涨跌幅 | 成交额 |
|------|---------|--------|--------|
| 上证指数 | {sh_point} | {sh_pct}% | {sh_vol}亿 |
| 深证成指 | {sz_point} | {sz_pct}% | {sz_vol}亿 |
| 创业板指 | {cy_point} | {cy_pct}% | {cy_vol}亿 |

**两市合计成交：{total_vol}亿元。** {market_note}

### 🔥 板块涨幅排名（TOP10）

| 排名 | 板块 | 涨跌幅 | 驱动因素 |
|------|------|--------|----------|
| 1 | {sector_1} | {sector_1_pct}% | {sector_1_reason} |
| 2 | {sector_2} | {sector_2_pct}% | {sector_2_reason} |
| 3 | {sector_3} | {sector_3_pct}% | {sector_3_reason} |
| 4 | {sector_4} | {sector_4_pct}% | {sector_4_reason} |
| 5 | {sector_5} | {sector_5_pct}% | {sector_5_reason} |
| 6 | {sector_6} | {sector_6_pct}% | {sector_6_reason} |
| 7 | {sector_7} | {sector_7_pct}% | {sector_7_reason} |
| 8 | {sector_8} | {sector_8_pct}% | {sector_8_reason} |
| 9 | {sector_9} | {sector_9_pct}% | {sector_9_reason} |
| 10 | {sector_10} | {sector_10_pct}% | {sector_10_reason} |

**跌幅居前：** {decline_sectors}

### 💰 资金流向

**主力资金：** {main_flow_summary}

**龙虎榜资金净买入TOP5：**

| 股票 | 龙虎榜净买入 | 涨跌幅 |
|------|-------------|--------|
| {lhb_1_name} | {lhb_1_amount} | {lhb_1_pct}% |
| {lhb_2_name} | {lhb_2_amount} | {lhb_2_pct}% |
| {lhb_3_name} | {lhb_3_amount} | {lhb_3_pct}% |
| {lhb_4_name} | {lhb_4_amount} | {lhb_4_pct}% |
| {lhb_5_name} | {lhb_5_amount} | {lhb_5_pct}% |

**机构龙虎榜净买入TOP3：**

| 股票 | 机构净买入 | 涨跌幅 |
|------|-----------|--------|
| {inst_1_name} | {inst_1_amount} | {inst_1_pct}% |
| {inst_2_name} | {inst_2_amount} | {inst_2_pct}% |
| {inst_3_name} | {inst_3_amount} | {inst_3_pct}% |

**北向资金龙虎榜净买入TOP3：**

| 股票 | 北向净买入 | 涨跌幅 |
|------|-----------|--------|
| {north_1_name} | {north_1_amount} | {north_1_pct}% |
| {north_2_name} | {north_2_amount} | {north_2_pct}% |
| {north_3_name} | {north_3_amount} | {north_3_pct}% |

### 📌 关键驱动因素

{key_drivers}

---

## 三、缠论选股分析

### 选股逻辑

综合以下维度进行筛选：
1. **世界局势影响**：{logic_1}
2. **板块涨幅排名**：聚焦当日资金集中流入的强势板块
3. **龙虎榜资金净买入**：机构与游资共同青睐的标的
4. **北向资金动向**：外资持续加仓方向
5. **缠论技术买点**：日线/60分钟/15分钟多级别共振，二买/三买优先

---

### 🥇 股票一：{stock_1_name}（{stock_1_code}）

**行业：** {stock_1_industry}

**价格验证：**

| 来源 | 收盘价（元） | 涨跌幅 |
|------|-------------|--------|
| {stock_1_src_1} | {stock_1_price} | {stock_1_pct}% |
| {stock_1_src_2} | {stock_1_price} | {stock_1_pct}% |

✅ 多源交叉验证一致：**{stock_1_price}元**

**资金面：**
{stock_1_capital}

**缠论分析：**

| 级别 | 走势类型 | 买点类型 | 关键位置 |
|------|---------|---------|---------|
| 日线 | {stock_1_d_trend} | {stock_1_d_buy} | {stock_1_d_key} |
| 60分钟 | {stock_1_60_trend} | {stock_1_60_buy} | {stock_1_60_key} |
| 15分钟 | {stock_1_15_trend} | {stock_1_15_buy} | {stock_1_15_key} |

**量价配合：** {stock_1_volume}

**操作建议：**

| 项目 | 价位 | 说明 |
|------|------|------|
| 买入区间 | {stock_1_buy_range} | {stock_1_buy_note} |
| 止损位 | {stock_1_stop} | {stock_1_stop_note} |
| 第一目标 | {stock_1_target1} | {stock_1_target1_note} |
| 第二目标 | {stock_1_target2} | {stock_1_target2_note} |

---

### 🥈 股票二：{stock_2_name}（{stock_2_code}）

**行业：** {stock_2_industry}

**价格验证：**

| 来源 | 收盘价（元） | 涨跌幅 |
|------|-------------|--------|
| {stock_2_src_1} | {stock_2_price} | {stock_2_pct}% |
| {stock_2_src_2} | {stock_2_price} | {stock_2_pct}% |

✅ 多源交叉验证一致：**{stock_2_price}元**

**资金面：**
{stock_2_capital}

**缠论分析：**

| 级别 | 走势类型 | 买点类型 | 关键位置 |
|------|---------|---------|---------|
| 日线 | {stock_2_d_trend} | {stock_2_d_buy} | {stock_2_d_key} |
| 60分钟 | {stock_2_60_trend} | {stock_2_60_buy} | {stock_2_60_key} |
| 15分钟 | {stock_2_15_trend} | {stock_2_15_buy} | {stock_2_15_key} |

**量价配合：** {stock_2_volume}

**操作建议：**

| 项目 | 价位 | 说明 |
|------|------|------|
| 买入区间 | {stock_2_buy_range} | {stock_2_buy_note} |
| 止损位 | {stock_2_stop} | {stock_2_stop_note} |
| 第一目标 | {stock_2_target1} | {stock_2_target1_note} |
| 第二目标 | {stock_2_target2} | {stock_2_target2_note} |

---

### 🥉 股票三：{stock_3_name}（{stock_3_code}）

**行业：** {stock_3_industry}

**价格验证：**

| 来源 | 收盘价（元） | 涨跌幅 |
|------|-------------|--------|
| {stock_3_src_1} | {stock_3_price} | {stock_3_pct}% |
| {stock_3_src_2} | {stock_3_price} | {stock_3_pct}% |

✅ 多源交叉验证一致：**{stock_3_price}元**

**资金面：**
{stock_3_capital}

**缠论分析：**

| 级别 | 走势类型 | 买点类型 | 关键位置 |
|------|---------|---------|---------|
| 日线 | {stock_3_d_trend} | {stock_3_d_buy} | {stock_3_d_key} |
| 60分钟 | {stock_3_60_trend} | {stock_3_60_buy} | {stock_3_60_key} |
| 15分钟 | {stock_3_15_trend} | {stock_3_15_buy} | {stock_3_15_key} |

**量价配合：** {stock_3_volume}

**操作建议：**

| 项目 | 价位 | 说明 |
|------|------|------|
| 买入区间 | {stock_3_buy_range} | {stock_3_buy_note} |
| 止损位 | {stock_3_stop} | {stock_3_stop_note} |
| 第一目标 | {stock_3_target1} | {stock_3_target1_note} |
| 第二目标 | {stock_3_target2} | {stock_3_target2_note} |

---

### 🏅 股票四：{stock_4_name}（{stock_4_code}）

**行业：** {stock_4_industry}

**价格验证：**

| 来源 | 收盘价（元） | 涨跌幅 |
|------|-------------|--------|
| {stock_4_src_1} | {stock_4_price} | {stock_4_pct}% |
| {stock_4_src_2} | {stock_4_price} | {stock_4_pct}% |

✅ 多源交叉验证一致：**{stock_4_price}元**

**资金面：**
{stock_4_capital}

**缠论分析：**

| 级别 | 走势类型 | 买点类型 | 关键位置 |
|------|---------|---------|---------|
| 日线 | {stock_4_d_trend} | {stock_4_d_buy} | {stock_4_d_key} |
| 60分钟 | {stock_4_60_trend} | {stock_4_60_buy} | {stock_4_60_key} |
| 15分钟 | {stock_4_15_trend} | {stock_4_15_buy} | {stock_4_15_key} |

**量价配合：** {stock_4_volume}

**操作建议：**

| 项目 | 价位 | 说明 |
|------|------|------|
| 买入区间 | {stock_4_buy_range} | {stock_4_buy_note} |
| 止损位 | {stock_4_stop} | {stock_4_stop_note} |
| 第一目标 | {stock_4_target1} | {stock_4_target1_note} |
| 第二目标 | {stock_4_target2} | {stock_4_target2_note} |

---

### 🏅 股票五：{stock_5_name}（{stock_5_code}）

**行业：** {stock_5_industry}

**价格验证：**

| 来源 | 收盘价（元） | 涨跌幅 |
|------|-------------|--------|
| {stock_5_src_1} | {stock_5_price} | {stock_5_pct}% |
| {stock_5_src_2} | {stock_5_price} | {stock_5_pct}% |

✅ 多源交叉验证一致：**{stock_5_price}元**

**资金面：**
{stock_5_capital}

**缠论分析：**

| 级别 | 走势类型 | 买点类型 | 关键位置 |
|------|---------|---------|---------|
| 日线 | {stock_5_d_trend} | {stock_5_d_buy} | {stock_5_d_key} |
| 60分钟 | {stock_5_60_trend} | {stock_5_60_buy} | {stock_5_60_key} |
| 15分钟 | {stock_5_15_trend} | {stock_5_15_buy} | {stock_5_15_key} |

**量价配合：** {stock_5_volume}

**操作建议：**

| 项目 | 价位 | 说明 |
|------|------|------|
| 买入区间 | {stock_5_buy_range} | {stock_5_buy_note} |
| 止损位 | {stock_5_stop} | {stock_5_stop_note} |
| 第一目标 | {stock_5_target1} | {stock_5_target1_note} |
| 第二目标 | {stock_5_target2} | {stock_5_target2_note} |

---

## 四、操作建议汇总

| 股票 | 代码 | 收盘价 | 买入区间 | 止损位 | 第一目标 | 第二目标 | 盈亏比 |
|------|------|--------|---------|--------|---------|---------|--------|
| {stock_1_name} | {stock_1_code} | {stock_1_price} | {stock_1_buy_range} | {stock_1_stop} | {stock_1_target1} | {stock_1_target2} | {stock_1_rr} |
| {stock_2_name} | {stock_2_code} | {stock_2_price} | {stock_2_buy_range} | {stock_2_stop} | {stock_2_target1} | {stock_2_target2} | {stock_2_rr} |
| {stock_3_name} | {stock_3_code} | {stock_3_price} | {stock_3_buy_range} | {stock_3_stop} | {stock_3_target1} | {stock_3_target2} | {stock_3_rr} |
| {stock_4_name} | {stock_4_code} | {stock_4_price} | {stock_4_buy_range} | {stock_4_stop} | {stock_4_target1} | {stock_4_target2} | {stock_4_rr} |
| {stock_5_name} | {stock_5_code} | {stock_5_price} | {stock_5_buy_range} | {stock_5_stop} | {stock_5_target1} | {stock_5_target2} | {stock_5_rr} |

---

## 五、风险提示

{risk_items}

---

> ⚠️ **免责声明：** 本报告仅供参考，不构成投资建议。股市有风险，投资需谨慎。缠论分析基于技术理论，实际走势可能与预期存在偏差。请根据自身风险承受能力独立决策。

---

*报告生成时间：{date} | 数据来源：{data_sources}*

---

## 第五步：转换为PNG和PDF

使用下面的python生成png和pdf

#!/usr/bin/env python3
"""Markdown to PNG/PDF converter: MD -> HTML -> PDF -> PNG (300 DPI)"""
import sys
import os
import markdown


def md_to_png(md_path, png_path, width=800):
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    html_body = markdown.markdown(md_content, extensions=['tables', 'fenced_code', 'toc'])

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
@page {{
    size: {width}px auto;
    margin: 0;
}}
body {{
    font-family: "Noto Sans CJK SC", "WenQuanYi Micro Hei", "Microsoft YaHei", -apple-system, sans-serif;
    max-width: {width}px;
    margin: 0 auto;
    padding: 30px 20px;
    background: #ffffff;
    color: #333333;
    font-size: 14px;
    line-height: 1.6;
}}
h1 {{ color: #1a1a2e; border-bottom: 3px solid #e94560; padding-bottom: 10px; font-size: 24px; }}
h2 {{ color: #16213e; border-bottom: 2px solid #0f3460; padding-bottom: 8px; margin-top: 30px; font-size: 20px; }}
h3 {{ color: #0f3460; margin-top: 20px; font-size: 17px; }}
table {{ border-collapse: collapse; width: 100%; margin: 12px 0; font-size: 13px; }}
th {{ background-color: #1a1a2e; color: white; padding: 8px 6px; text-align: left; font-weight: bold; }}
td {{ padding: 6px; border: 1px solid #ddd; }}
tr:nth-child(even) {{ background-color: #f8f9fa; }}
strong {{ color: #e94560; }}
blockquote {{ border-left: 4px solid #e94560; padding-left: 16px; color: #666; margin: 12px 0; }}
hr {{ border: none; border-top: 2px solid #eee; margin: 20px 0; }}
</style>
</head>
<body>
{html_body}
</body>
</html>"""

    # Step 1: HTML -> PDF via WeasyPrint
    pdf_path = png_path.replace('.png', '.pdf')
    from weasyprint import HTML
    HTML(string=html).write_pdf(pdf_path)
    print(f"PDF saved to {pdf_path}")

    # Step 2: PDF -> PNG at 300 DPI
    from pdf2image import convert_from_path
    from PIL import Image

    images = convert_from_path(pdf_path, dpi=300)

    if len(images) == 1:
        images[0].save(png_path, 'PNG')
    else:
        # 多页时垂直拼接
        total_height = sum(img.height for img in images)
        max_width = max(img.width for img in images)
        combined = Image.new('RGB', (max_width, total_height), 'white')
        y_offset = 0
        for img in images:
            combined.paste(img, (0, y_offset))
            y_offset += img.height
        combined.save(png_path, 'PNG')

    print(f"PNG saved to {png_path}")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python md_to_png.py <input.md> <output.png>")
        sys.exit(1)
    md_to_png(sys.argv[1], sys.argv[2], width=800)


---

## 注意事项

1. **日期是第一优先级**：所有数据必须与授时中心日期一致，发现年份不匹配的数据立即丢弃
2. **搜索关键词必须包含完整年月日**：格式为 `"YYYY年M月D日"`，绝不使用无年份或无日期的关键词
3. **非交易日标注**：非交易日执行时，使用最近交易日数据并在报告中注明
4. **搜索效率**：合并搜索、避免重复
5. **报告质量**：操作建议必须包含具体价位，不可含糊
6. **免责声明**：报告末尾必须包含免责声明
