# Flask Hello World 一頁式網站

[![CI/CD Pipeline](https://github.com/fredatoeic-alt/Test0929/actions/workflows/deploy.yml/badge.svg)](https://github.com/fredatoeic-alt/Test0929/actions/workflows/deploy.yml)

這是一個基於 **Python Flask** 網站微框架所打造的現代化「Hello World」一頁式網站（Single-Page Website）。

---

## 專案結構

```text
Test0929/
├── app.py              # Flask 後端主程式（包含首頁路由與互動 API）
├── test_app.py         # Pytest 單元測試腳本
├── templates/
│   └── index.html      # 一頁式網站前端 HTML 模板（支援 Jinja2 動態渲染）
├── static/
│   └── style.css       # 現代化深色漸層響應式 CSS 樣式
├── .github/workflows/
│   └── deploy.yml      # GitHub Actions CI/CD Pipeline
├── render.yaml         # Render Blueprint 部署配置
├── requirements.txt    # Python 相依套件清單 (Flask, Gunicorn)
├── run.bat             # Windows 專用一鍵啟動腳本 (支援 venv)
└── README.md           # 專案說明文件
```

---

## 功能特點

1. **一頁式導覽設計（Single-Page Layout）**：
   - 頂部固定模糊導覽列（Sticky Glassmorphism Header）。
   - 主視覺 Banner（Hero Section）搭配醒目的「Hello, World!」標題與行動呼籲。
   - 網站特色展示區（Features Grid）。
   - 伺服器狀態展示面板（即時顯示 Python 版本、Flask 版本與啟動時間）。

2. **前端與後端即時 API 互動**：
   - 內建非同步 Fetch API，使用者可在前端輸入姓名，發送非同步 POST 請求至 Flask 後端 `/api/hello`，由後端返回客製化 JSON 回應並動態更新在頁面上。

---

## 如何啟動執行

### 方法一：一鍵啟動（推薦）
在 Windows 檔案總管中，直接雙擊專案目錄下的 **`run.bat`** 即可自動透過 Python 啟動伺服器。

### 方法二：透過命令列啟動
開啟 PowerShell 或 CMD 終端機，執行以下指令：

```powershell
# 若使用 Anaconda Python：
& "C:\Users\freej\anaconda3\python.exe" app.py

# 或若 Python 已加入環境變數 PATH：
python app.py
```

### 開啟網站
伺服器啟動成功後，請開啟瀏覽器瀏覽：
👉 **http://127.0.0.1:5000**

---

## 🚀 CI/CD 與 Render 自動部署設定

本專案配置了完整的 GitHub Actions CI/CD 流水線：

1. **CI（持續整合）**：
   - 每次推送到 `main` 分支或發起 Pull Request 時，自動於 Ubuntu 環境安裝依賴並透過 `pytest test_app.py` 執行自動化測試。
2. **CD（持續部署至 Render）**：
   - 當測試全部通過後，自動透過 Render Deploy Hook 觸發線上即時部署。

### ⚙️ 設定步驟

1. **在 Render 上建立 Web Service**：
   - 登入 [Render](https://render.com/)，點擊 **New +** -> **Web Service**（或 **Blueprint** 並選擇此倉庫）。
   - Runtime: `Python`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
2. **取得 Deploy Hook URL**：
   - 進入 Render 建立的 Web Service 頁面 -> **Settings**。
   - 找到 **Deploy Hook** 區塊，複製 Webhook URL（格式類似 `https://api.render.com/deploy/srv-xxxxxx?key=yyyyyy`）。
3. **在 GitHub 倉庫設定 Secret**：
   - 前往 GitHub 倉庫 -> **Settings** -> **Secrets and variables** -> **Actions**。
   - 點擊 **New repository secret**：
     - **Name**：`RENDER_DEPLOY_HOOK_URL`
     - **Secret**：貼上剛才從 Render 複製的 Deploy Hook URL。
4. **完成**：
   - 未來只要執行 `git push origin main`，GitHub Actions 就會自動跑測試並在通過後觸發 Render 部署上線！

