"""
create_db.py — 建立 orders.db 資料庫結構與測試資料
"""
import sqlite3
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'orders.db')

if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
conn.execute('PRAGMA foreign_keys = ON')
cur = conn.cursor()

# ── 1. customer 客戶 ─────────────────────────────────────────
cur.execute('''
CREATE TABLE customer (
    客戶編號  TEXT PRIMARY KEY,
    名稱      TEXT NOT NULL,
    電話      TEXT,
    地址      TEXT
)
''')

# ── 2. product 商品 ──────────────────────────────────────────
cur.execute('''
CREATE TABLE product (
    商品編號  TEXT PRIMARY KEY,
    名稱      TEXT NOT NULL,
    單價      REAL NOT NULL CHECK(單價 >= 0),
    庫存      INTEGER NOT NULL DEFAULT 0,
    分類      TEXT
)
''')

# ── 3. orders 訂單 ───────────────────────────────────────────
cur.execute('''
CREATE TABLE orders (
    訂單編號  TEXT PRIMARY KEY,
    客戶編號  TEXT NOT NULL,
    訂單日期  TEXT NOT NULL,
    狀態      TEXT NOT NULL DEFAULT '處理中',
    業務人員  TEXT,
    FOREIGN KEY (客戶編號) REFERENCES customer(客戶編號)
)
''')

# ── 4. order_item 訂單明細 (複合主鍵) ──────────────────────────
cur.execute('''
CREATE TABLE order_item (
    訂單編號  TEXT NOT NULL,
    商品編號  TEXT NOT NULL,
    數量      INTEGER NOT NULL CHECK(數量 > 0),
    單價      REAL NOT NULL CHECK(單價 >= 0),
    PRIMARY KEY (訂單編號, 商品編號),
    FOREIGN KEY (訂單編號) REFERENCES orders(訂單編號),
    FOREIGN KEY (商品編號) REFERENCES product(商品編號)
)
''')

# ── 測試資料 ─────────────────────────────────────────────────
customers = [
    ('C001', '台灣半導體股份有限公司', '02-27001234', '台北市信義區松仁路100號'),
    ('C002', '陽明海運股份有限公司',   '07-33125678', '高雄市前鎮區成功二路88號'),
    ('C003', '鴻海精密工業股份有限公司', '02-22688000', '新北市土城區自由街2號'),
    ('C004', '統一超商股份有限公司',   '06-2536789',  '台南市東區中華東路三段5號'),
    ('C005', '長榮航空股份有限公司',   '03-3515151',  '桃園市大園區航站南路15號'),
]
cur.executemany('INSERT INTO customer VALUES (?,?,?,?)', customers)

products = [
    ('P001', '無線藍牙耳機',       1290.0,  150, '3C電子'),
    ('P002', '機械式鍵盤',         2490.0,   80, '3C電子'),
    ('P003', '辦公室升降桌',       8900.0,   30, '辦公家具'),
    ('P004', 'A4影印紙(五包裝)',    450.0,  500, '文具耗材'),
    ('P005', '人體工學椅',        12500.0,   25, '辦公家具'),
]
cur.executemany('INSERT INTO product VALUES (?,?,?,?,?)', products)

orders = [
    ('O001', 'C001', '2024-06-01', '已出貨', '林志明'),
    ('O002', 'C002', '2024-06-05', '已完成', '王美玲'),
    ('O003', 'C003', '2024-06-10', '處理中', '張大偉'),
    ('O004', 'C001', '2024-06-15', '已取消', '林志明'),
    ('O005', 'C004', '2024-06-20', '已出貨', '陳怡君'),
]
cur.executemany('INSERT INTO orders VALUES (?,?,?,?,?)', orders)

# order_item 保存「下單當時的單價」
order_items = [
    ('O001', 'P001',  5,  1290.0),   # 原價
    ('O001', 'P002',  3,  2490.0),   # 原價
    ('O001', 'P004', 10,   420.0),   # 下單折扣價
    ('O002', 'P003',  2,  8900.0),
    ('O002', 'P005',  1, 12500.0),
    ('O003', 'P001', 20,  1190.0),   # 大量採購折扣
    ('O004', 'P002',  1,  2490.0),
    ('O004', 'P004',  5,   450.0),
    ('O005', 'P003',  1,  8500.0),   # 特惠價
    ('O005', 'P005',  3, 12500.0),
]
cur.executemany('INSERT INTO order_item VALUES (?,?,?,?)', order_items)

conn.commit()
conn.close()

print(f'[OK] 資料庫已成功建立並初始化：{DB_PATH}')
print('     customer: 5 筆 | product: 5 筆 | orders: 5 筆 | order_item: 10 筆')
