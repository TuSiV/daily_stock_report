# 每日选股分析报告

**日期：{date}（{weekday}）**

---

## 一、隔夜全球市场动态

### 美股市场（{yesterday}收盘）

| 指数 | 收盘点位 | 涨跌幅 | 备注 |
|------|---------|--------|------|
| 道琼斯工业指数 | {dj_point} | {dj_pct}% | {dj_note} |
| 纳斯达克综合指数 | {nasdaq_point} | {nasdaq_pct}% | {nasdaq_note} |
| 标普500指数 | {sp500_point} | {sp500_pct}% | {sp500_note} |

**要点：** {us_summary}

### 地缘政治

{geopolitics_items}

### 大宗商品

| 品种 | 最新价格 | 涨跌幅 |
|------|---------|--------|
| 现货黄金 | {gold_price} | {gold_pct} |
| WTI原油 | {wti_price} | {wti_pct} |
| 布伦特原油 | {brent_price} | {brent_pct} |

**要点：** {commodity_summary}

---

## 二、A股市场复盘（{date}）

### 三大指数表现

| 指数 | 收盘点位 | 涨跌幅 | 成交额 |
|------|---------|--------|--------|
| 上证指数 | {sh_point} | {sh_pct}% | {sh_vol}亿 |
| 深证成指 | {sz_point} | {sz_pct}% | {sz_vol}亿 |
| 创业板指 | {cy_point} | {cy_pct}% | {cy_vol}亿 |

**两市合计成交：{total_vol}亿元。** {market_note}

### 板块涨幅排名（TOP10）

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

### 资金流向

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

### 关键驱动因素

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

### 股票一：{stock_1_name}（{stock_1_code}）

**行业：** {stock_1_industry}

**价格验证：**

| 来源 | 收盘价（元） | 涨跌幅 |
|------|-------------|--------|
| 东方财富 | {stock_1_close} | {stock_1_pct}% |
| 新浪财经 | {stock_1_close} | {stock_1_pct}% |

**资金面：**
{stock_1_capital}

**AI选股理由：**
{stock_1_reason}

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

### 股票二：{stock_2_name}（{stock_2_code}）

**行业：** {stock_2_industry}

**价格验证：**

| 来源 | 收盘价（元） | 涨跌幅 |
|------|-------------|--------|
| 东方财富 | {stock_2_close} | {stock_2_pct}% |
| 新浪财经 | {stock_2_close} | {stock_2_pct}% |

**资金面：**
{stock_2_capital}

**AI选股理由：**
{stock_2_reason}

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

### 股票三：{stock_3_name}（{stock_3_code}）

**行业：** {stock_3_industry}

**价格验证：**

| 来源 | 收盘价（元） | 涨跌幅 |
|------|-------------|--------|
| 东方财富 | {stock_3_close} | {stock_3_pct}% |
| 新浪财经 | {stock_3_close} | {stock_3_pct}% |

**资金面：**
{stock_3_capital}

**AI选股理由：**
{stock_3_reason}

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

### 股票四：{stock_4_name}（{stock_4_code}）

**行业：** {stock_4_industry}

**价格验证：**

| 来源 | 收盘价（元） | 涨跌幅 |
|------|-------------|--------|
| 东方财富 | {stock_4_close} | {stock_4_pct}% |
| 新浪财经 | {stock_4_close} | {stock_4_pct}% |

**资金面：**
{stock_4_capital}

**AI选股理由：**
{stock_4_reason}

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

### 股票五：{stock_5_name}（{stock_5_code}）

**行业：** {stock_5_industry}

**价格验证：**

| 来源 | 收盘价（元） | 涨跌幅 |
|------|-------------|--------|
| 东方财富 | {stock_5_close} | {stock_5_pct}% |
| 新浪财经 | {stock_5_close} | {stock_5_pct}% |

**资金面：**
{stock_5_capital}

**AI选股理由：**
{stock_5_reason}

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
| {stock_1_name} | {stock_1_code} | {stock_1_close} | {stock_1_buy_range} | {stock_1_stop} | {stock_1_target1} | {stock_1_target2} | {stock_1_rr} |
| {stock_2_name} | {stock_2_code} | {stock_2_close} | {stock_2_buy_range} | {stock_2_stop} | {stock_2_target1} | {stock_2_target2} | {stock_2_rr} |
| {stock_3_name} | {stock_3_code} | {stock_3_close} | {stock_3_buy_range} | {stock_3_stop} | {stock_3_target1} | {stock_3_target2} | {stock_3_rr} |
| {stock_4_name} | {stock_4_code} | {stock_4_close} | {stock_4_buy_range} | {stock_4_stop} | {stock_4_target1} | {stock_4_target2} | {stock_4_rr} |
| {stock_5_name} | {stock_5_code} | {stock_5_close} | {stock_5_buy_range} | {stock_5_stop} | {stock_5_target1} | {stock_5_target2} | {stock_5_rr} |

---

## 五、风险提示

{risk_items}

---

> **免责声明：** 本报告仅供参考，不构成投资建议。股市有风险，投资需谨慎。缠论分析基于技术理论，实际走势可能与预期存在偏差。请根据自身风险承受能力独立决策。

---

*报告生成时间：{date} | 数据来源：{data_sources}*
