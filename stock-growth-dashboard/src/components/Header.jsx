import React from 'react';
import { UploadCloud, ChevronDown, RefreshCw } from 'lucide-react';

export default function Header({
  selectedPeriod,
  onPeriodChange,
  dataSourceName,
  isDemo,
  onOpenUploadModal,
  onResetData
}) {
  return (
    <header className="pbi-header">
      <div className="pbi-header-top">
        <h1 className="pbi-main-title">Dashboard 1｜上市公司高成長分析</h1>
        <div className="pbi-header-tools">
          <button
            type="button"
            className="pbi-tool-btn"
            onClick={onOpenUploadModal}
            title="更換或上傳自訂 CSV"
          >
            <UploadCloud size={14} />
            <span>更換資料</span>
          </button>
          {!isDemo && (
            <button
              type="button"
              className="pbi-tool-btn reset"
              onClick={onResetData}
              title="重設為預設資料"
            >
              <RefreshCw size={12} />
              <span>重設</span>
            </button>
          )}
        </div>
      </div>

      {/* 1. 財務年度選擇器（對齊 Power BI 下拉選單樣式） */}
      <div className="pbi-filter-group">
        <label htmlFor="period-select" className="pbi-filter-label">
          財務年度
        </label>
        <div className="pbi-select-box">
          <select
            id="period-select"
            value={selectedPeriod}
            onChange={(e) => onPeriodChange(e.target.value)}
            className="pbi-dropdown-select"
          >
            <option value="2021FY">2021FY</option>
            <option value="2022FY">2022FY</option>
            <option value="2023FY">2023FY</option>
            <option value="ALL">全部年度 (2021FY～2023FY)</option>
          </select>
          <ChevronDown size={16} className="pbi-select-arrow" />
        </div>
      </div>
    </header>
  );
}
