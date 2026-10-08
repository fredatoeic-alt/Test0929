# Flask + SQLite + Bootstrap 5 訂單管理系統 (OrderPro)

本專案為基於 **Flask 3**、**SQLite 3** 與 **Bootstrap 5 (Dark Glassmorphism)** 打造的企業級訂單管理系統。

---

## 📋 資料表架構 (Database Schema)

1. **`customer` (客戶資料表)**
   - `客戶編號` (Primary Key, TEXT)
   - `名稱` (TEXT)
   - `電話` (TEXT)
   - `地址` (TEXT)

2. **`product` (商品資料表)**
   - `商品編號` (Primary Key, TEXT)
   - `名稱` (TEXT)
   - `單價` (REAL, CHECK >= 0)
   - `庫存` (INTEGER, CHECK >= 0)
   - `分類` (TEXT)

3. **`orders` (訂單主檔)**
   - `訂單編號` (Primary Key, TEXT)
   - `客戶編號` (Foreign Key -> customer)
   - `訂單日期` (TEXT)
   - `狀態` (TEXT, 可為 '處理中' / '已出貨' / '已完成' / '已取消')
   - `業務人員` (TEXT)

4. **`order_item` (訂單明細 - 複合主鍵)**
   - `訂單編號` (Foreign Key -> orders)
   - `商品編號` (Foreign Key -> product)
   - `數量` (INTEGER, CHECK > 0)
   - `單價` (REAL, 保存下單當時單價，商品改價不影響歷史訂單)
   - **複合主鍵**：`(訂單編號, 商品編號)`

---

## ✨ 核心功能特色

- **管理員驗證系統**：保護系統存取權限。
- **客戶與商品 CRUD 維護**：完整建立、查詢、更新、刪除客戶與商品資料。
- **靈活新增訂單**：客戶選單採用下拉式選擇，商品支援一次勾選多項並即時動態計算小計與總額。
- **下單歷史單價隔離**：`order_item` 保存下單當時的價格，後續修改商品單價不影響已成立的歷史訂單。
- **訂單狀態即時更新**：可於訂單列表中直接切換狀態（處理中 / 已出貨 / 已完成 / 已取消），即時發送非同步 AJAX 請求完成更新。
- **專屬訂單頁面與 QRCode 出貨單**：每張訂單享有獨立 `/order/<訂單編號>` 頁面，自動繪製出貨單及附帶可掃描跳轉的 QRCode，支援一鍵專用列印樣式。
- **5 筆繁體中文測試資料**：系統初始化時已自動匯入包含台灣半導體、陽明海運、鴻海、統一超商與長榮航空等 5 筆繁體中文完整測試數據。

---

## 🔑 管理員帳號密碼

- **帳號 (Username)**：`admin`
- **密碼 (Password)**：`admin123`

---

## 🚀 啟動方式

### 1. 初始化資料庫與測試資料 (視需要執行)
若需重新產生包含 5 筆測試資料的全新資料庫，請在終端機執行：
```powershell
python create_db.py
```

### 2. 啟動 Flask 網站服務
直接雙擊 `run.bat` 或在終端機執行：
```powershell
python app.py
```

### 3. 開啟瀏覽器存取
👉 **http://127.0.0.1:5000**
使用管理員帳密 `admin` / `admin123` 登入即可開始維護。

### 4. 執行測試單元腳本
```powershell
python -m pytest test_app.py -v
```
