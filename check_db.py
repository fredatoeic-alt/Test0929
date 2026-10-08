"""
check_db.py — 讀取 orders.db 並印出所有資料表內容供驗證
"""

import sqlite3
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "orders.db")

if not os.path.exists(DB_PATH):
    print("[ERROR] 找不到 orders.db，請先執行 create_db.py")
    exit(1)

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row  # 讓結果可用欄位名稱存取
cur = conn.cursor()

TABLES = ["customer", "product", "orders", "order_item"]

for table in TABLES:
    print("=" * 70)
    print(f"[TABLE] {table}")
    print("=" * 70)

    cur.execute(f"SELECT * FROM {table};")
    rows = cur.fetchall()

    if not rows:
        print("  (無資料)")
        print()
        continue

    # 取得欄位名稱
    columns = rows[0].keys()
    # 計算每欄的最大寬度（含標題）
    widths = {}
    for col in columns:
        widths[col] = max(
            len(col),
            max(len(str(row[col])) for row in rows)
        )

    # 印出標題列
    header = " | ".join(col.ljust(widths[col]) for col in columns)
    print(f"  {header}")
    print(f"  {'-+-'.join('-' * widths[col] for col in columns)}")

    # 印出資料列
    for row in rows:
        line = " | ".join(str(row[col]).ljust(widths[col]) for col in columns)
        print(f"  {line}")

    print(f"  → 共 {len(rows)} 筆\n")

# ── 額外：印出訂單明細的彙總查詢 ──
print("=" * 70)
print("[SUMMARY] 訂單金額彙總（訂單編號 / 客戶名稱 / 品項數 / 訂單總額）")
print("=" * 70)

cur.execute("""
    SELECT o.訂單編號,
           c.名稱       AS 客戶名稱,
           COUNT(*)     AS 品項數,
           SUM(oi.數量 * oi.單價) AS 訂單總額
    FROM orders o
    JOIN customer c    ON o.客戶編號 = c.客戶編號
    JOIN order_item oi ON o.訂單編號 = oi.訂單編號
    GROUP BY o.訂單編號
    ORDER BY o.訂單編號;
""")

rows = cur.fetchall()
columns = rows[0].keys()
widths = {}
for col in columns:
    widths[col] = max(len(col), max(len(str(row[col])) for row in rows))

header = " | ".join(col.ljust(widths[col]) for col in columns)
print(f"  {header}")
print(f"  {'-+-'.join('-' * widths[col] for col in columns)}")
for row in rows:
    line = " | ".join(str(row[col]).ljust(widths[col]) for col in columns)
    print(f"  {line}")

print()
conn.close()
print("[OK] 驗證完成")
