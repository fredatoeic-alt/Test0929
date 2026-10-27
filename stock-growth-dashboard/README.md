# 台灣上市公司高成長股票分析 - 互動式 Web Dashboard

本專案為交大「AI與商業數據分析」課程學習成果專案。原先於 Power BI Desktop 建立高成長股票分析儀表板，現使用 **React + Vite + Recharts** 開發為高互動性、現代專業、支援 RWD 的 Web Dashboard，後續可透過 GitHub 進行版本控制，並部署至 Render Static Site 提供公開線上展示。

---

## 一、畫面與資訊架構

- **頁面標題**：「Dashboard 1｜上市公司高成長分析」
- **五大核心區域**：
  1. **財務年度選擇器**：支援「全部年度 (2021FY～2023FY)」、「2021FY」、「2022FY」、「2023FY」切換，聯動全頁數據。
  2. **四張核心 KPI 卡片**：
     - **觀測筆數**：有效研究觀測資料筆數
     - **高成長筆數**：`HighGrowth == 'Y'` 的筆數
     - **高成長比例**：`高成長筆數 / 觀測筆數 × 100`（保留小數兩位）
     - **平均隔年報酬率**：`StockReturn` 平均值（保留小數兩位，紅漲綠跌金融色彩）
  3. **各財務年度對應之高成長股票比例直條圖**：
     - 固定年度識別色：`2021FY` 藍色 (#477FC4)、`2022FY` 綠色 (#42A58C)、`2023FY` 橘色 (#E39A37)
     - 顯示數值標籤（如 42.15%）
     - 選擇單一年度時，保留三年度對比，但聚焦突出選定年度、淡化其他年度。
  4. **各產業高成長股票比例 Top 10**：
     - 水平橫條圖，自動依高成長比例降冪排序
     - 嚴格篩選**觀測筆數 > 30 筆**之產業
     - 橫條圖顏色依所選年度動態變更
     - 滑鼠移入（Tooltip）顯示產業名稱、觀測筆數、高成長筆數、高成長比例與平均報酬率
  5. **Finding 研究發現與關鍵洞察**：
     - 頁面底部深藍色圓角區塊（白色文字）
     - 嚴格依資料與規則動態運算產生（非固定寫死、非即時 AI 猜測，保證 100% 精準）
     - 單一年度自動計算與前一財務年度的高成長比例變化（百分點）

---

## 二、專案結構

```
stock-growth-dashboard/
├── index.html                   # HTML 入口（繁體中文語系、完整 Meta 標籤）
├── package.json                 # 專案依賴與腳本
├── vite.config.js               # Vite 設定
├── public/
│   └── data/
│       └── stock_data.csv       # 【正式資料替換位置】預設讀取的 CSV 檔案
└── src/
    ├── main.jsx                 # React 入口
    ├── App.jsx                  # 儀表板主頁面與狀態聯動中心
    ├── index.css                # 專業 BI 風格 CSS 樣式系統（包含 RWD 手機/電腦支援）
    ├── components/
    │   ├── Header.jsx           # 頂部標題、年度下拉選單、資料狀態列
    │   ├── KpiCards.jsx         # 四張核心 KPI 指標卡片
    │   ├── PeriodGrowthChart.jsx# 各財務年度直條圖（年度固定色、聚焦高亮）
    │   ├── IndustryTop10Chart.jsx# 各產業 Top 10 水平橫條圖（門檻 > 30 筆）
    │   ├── FindingsBanner.jsx   # 底部深藍圓角 Finding 洞察區塊
    │   └── DataUploadModal.jsx  # 資料替換與即時上傳驗證彈窗
    └── utils/
        ├── analytics.js         # 所有 KPI、產業排名、圖表及 Finding 運算邏輯
        └── dataLoader.js        # CSV 讀取、PapaParse 解析與資料型態清理
```

---

## 三、安裝與本機啟動

在專案目錄下執行以下指令：

```bash
# 1. 進入專案目錄
cd stock-growth-dashboard

# 2. 安裝套件
npm install

# 3. 啟動本機開發伺服器
npm run dev
```

啟動後於瀏覽器開啟終端機提示的本機網址（例如 `http://localhost:5173`）即可操作互動儀表板。

---

## 四、正式資料替換方式

當您取得正式的上市公司研究資料 CSV 檔案時，有兩種替換方式：

### 方式 A：直接替換本機檔案（推薦，部署後即載入）
將正式 CSV 檔案重新命名為 `stock_data.csv`，覆蓋放置於：
```
stock-growth-dashboard/public/data/stock_data.csv
```
重新整理網頁即可載入正式研究資料。

### 方式 B：在網頁上即時上傳測試
點擊網頁右上角「**更換資料**」按鈕，將您的 CSV 檔案拖曳或選擇上傳，系統將立即解析並更新所有圖表與 Finding。

### CSV 欄位格式規範
CSV 檔案須包含以下欄位（標題英文大小寫須一致）：
- `FinancialPeriod`：財務資料年度（例如：`2021FY`、`2022FY`、`2023FY`）
- `Industry`：產業別（例如：`半導體業`、`電子零組件業` 等）
- `HighGrowth`：高成長標記（`Y` 代表高成長，`N` 代表非高成長）
- `StockReturn`：隔年股票報酬率（**以百分點儲存**，例如 `20` 代表 20%）
- 其他可選欄位：`StockID`, `StockName`, `ROE`, `ROA`, `EPS` 等

---

## 五、後續 Render 部署設定指引

當本機測試確認無誤，後續透過 GitHub 部署至 Render Static Site 時，設定如下：

- **Build Command**: `npm run build`
- **Publish Directory**: `dist`
- **Node Version**: 18 以上（目前環境為 Node 24）
