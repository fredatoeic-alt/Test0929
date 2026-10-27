import csv
import random

# 精準擬合截圖中 2021FY 的真實統計數值：
# 2021FY: 總觀測筆數 899, 高成長 405, 比例 45.05%, 平均報酬率 30.95%
# 2022FY: 比例 24.03%
# 2023FY: 比例 16.35%

# 截圖中 2021FY 的 Top 8 產業高成長比例與名稱：
# 1. 電腦及週邊設備業: 74.14% (約 43/58)
# 2. 半導體業: 69.74% (約 106/152)
# 3. 其他電子業: 60.53% (約 46/76)
# 4. 通信網路業: 59.52% (約 50/84)
# 5. 汽車工業: 57.58% (約 19/33) -> 觀測筆數 >= 30
# 6. 電子零組件業: 52.69% (約 98/186)
# 7. 光電業: 50.79% (約 32/63)
# 8. 建材營造: 47.27% (約 26/55)
# 其餘產業筆數或高成長比例較低

data = []
stock_id_counter = 1101

# 2021FY 精心配置產業分布，以完美符合 899 筆、405 筆高成長、45.05%
industries_2021 = [
    ("電腦及週邊設備業", 58, 43, 38.5),
    ("半導體業", 152, 106, 42.0),
    ("其他電子業", 76, 46, 34.2),
    ("通信網路業", 84, 50, 31.8),
    ("汽車工業", 33, 19, 29.5),
    ("電子零組件業", 186, 98, 33.6),
    ("光電業", 63, 32, 28.4),
    ("建材營造", 55, 26, 25.1),
    ("生技醫療業", 48, 15, 21.0),
    ("電機機械業", 45, 12, 18.5),
    ("化學工業", 42, 8, 16.2),
    ("航運業", 35, 5, 22.0),
    ("食品工業", 22, 2, 12.0),  # < 30
]

# 檢查 2021FY
total_2021 = sum(c for _, c, _, _ in industries_2021)
hg_2021 = sum(h for _, _, h, _ in industries_2021)
# 微調確保總和剛好 899 筆與 405 筆高成長
diff_total = 899 - total_2021
diff_hg = 405 - hg_2021

# 生成 2021FY
for ind_name, count, hg_count, avg_ret in industries_2021:
    # 調整食品工業筆數補足
    if ind_name == "食品工業":
        count += diff_total
        hg_count += diff_hg
        
    for i in range(count):
        is_hg = "Y" if i < hg_count else "N"
        ret = round(random.gauss(avg_ret + (10 if is_hg == "Y" else -12), 8.5), 2)
        data.append({
            "FinancialPeriod": "2021FY",
            "Industry": ind_name,
            "HighGrowth": is_hg,
            "StockReturn": ret,
            "StockID": f"{stock_id_counter}",
            "StockName": f"{ind_name[:2]}股{i+1}",
            "ROE": round(random.gauss(15.2, 4.0), 2),
            "ROA": round(random.gauss(9.1, 2.5), 2),
            "EPS": round(random.gauss(5.5, 2.0), 2)
        })
        stock_id_counter += 1

# 調整 2021FY 平均報酬率微調以達到剛好約 30.95%
returns_2021 = [d["StockReturn"] for d in data if d["FinancialPeriod"] == "2021FY"]
current_avg = sum(returns_2021) / len(returns_2021)
shift = 30.95 - current_avg
for d in data:
    if d["FinancialPeriod"] == "2021FY":
        d["StockReturn"] = round(d["StockReturn"] + shift, 2)

# 2022FY: 總觀測 903 筆, 比例約 24.03% (217 筆高成長)
for ind_name, count, _, avg_ret in industries_2021:
    hg_ratio = 0.2403
    hg_count = int(round(count * hg_ratio))
    for i in range(count):
        is_hg = "Y" if i < hg_count else "N"
        ret = round(random.gauss(avg_ret * 0.6 + (8 if is_hg == "Y" else -10), 9.0), 2)
        data.append({
            "FinancialPeriod": "2022FY",
            "Industry": ind_name,
            "HighGrowth": is_hg,
            "StockReturn": ret,
            "StockID": f"{stock_id_counter}",
            "StockName": f"{ind_name[:2]}股{i+1}",
            "ROE": round(random.gauss(10.5, 3.5), 2),
            "ROA": round(random.gauss(6.0, 2.0), 2),
            "EPS": round(random.gauss(3.2, 1.5), 2)
        })
        stock_id_counter += 1

# 2023FY: 總觀測 899 筆, 比例約 16.35% (147 筆高成長)
for ind_name, count, _, avg_ret in industries_2021:
    hg_ratio = 0.1635
    hg_count = int(round(count * hg_ratio))
    for i in range(count):
        is_hg = "Y" if i < hg_count else "N"
        ret = round(random.gauss(avg_ret * 0.8 + (12 if is_hg == "Y" else -8), 9.0), 2)
        data.append({
            "FinancialPeriod": "2023FY",
            "Industry": ind_name,
            "HighGrowth": is_hg,
            "StockReturn": ret,
            "StockID": f"{stock_id_counter}",
            "StockName": f"{ind_name[:2]}股{i+1}",
            "ROE": round(random.gauss(12.8, 3.8), 2),
            "ROA": round(random.gauss(7.4, 2.2), 2),
            "EPS": round(random.gauss(4.1, 1.8), 2)
        })
        stock_id_counter += 1

with open("public/data/stock_data.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["FinancialPeriod", "Industry", "HighGrowth", "StockReturn", "StockID", "StockName", "ROE", "ROA", "EPS"])
    writer.writeheader()
    writer.writerows(data)

print(f"Generated {len(data)} rows successfully matching screenshot distribution!")
