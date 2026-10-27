import React, { useState, useEffect, useMemo } from 'react';
import Header from './components/Header';
import KpiCards from './components/KpiCards';
import PeriodGrowthChart from './components/PeriodGrowthChart';
import IndustryTop10Chart from './components/IndustryTop10Chart';
import FindingsBanner from './components/FindingsBanner';
import DataUploadModal from './components/DataUploadModal';
import { loadCsvFromUrl, DEFAULT_CSV_PATH } from './utils/dataLoader';
import {
  calculateKPIs,
  calculatePeriodStats,
  calculateIndustryRanking,
  generateFindings
} from './utils/analytics';
import { Loader2, AlertCircle } from 'lucide-react';

export default function App() {
  const [allData, setAllData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedPeriod, setSelectedPeriod] = useState('2021FY');
  const [dataSourceName, setDataSourceName] = useState('正式研究資料 (stock_data.csv)');
  const [isDemo, setIsDemo] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);

  // 初次載入正式 CSV
  const loadDefaultData = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await loadCsvFromUrl(DEFAULT_CSV_PATH);
      setAllData(data);
      setDataSourceName('正式研究資料 (stock_data.csv)');
      setIsDemo(false);
    } catch (err) {
      console.error(err);
      setError(err.message || '無法載入預設資料');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDefaultData();
  }, []);

  // 處理使用者上傳自訂資料
  const handleCustomDataLoaded = (customData, fileName) => {
    setAllData(customData);
    setDataSourceName(fileName || '自訂上傳資料');
    setIsDemo(false);
    setSelectedPeriod('ALL'); // 重設為全部年度以綜觀全局
  };

  // 當前篩選條件下的資料集
  const currentFilteredData = useMemo(() => {
    if (!allData || allData.length === 0) return [];
    if (selectedPeriod === 'ALL') return allData;
    return allData.filter((d) => d.FinancialPeriod === selectedPeriod);
  }, [allData, selectedPeriod]);

  // 2. 四大 KPI 指標計算
  const kpis = useMemo(() => {
    return calculateKPIs(currentFilteredData);
  }, [currentFilteredData]);

  // 3. 各財務年度對應之高成長股票比例直條圖數據
  const periodStats = useMemo(() => {
    return calculatePeriodStats(allData, selectedPeriod);
  }, [allData, selectedPeriod]);

  // 4. 各產業高成長股票比例 Top 10 (觀測筆數 > 30)
  const industryTop10 = useMemo(() => {
    return calculateIndustryRanking(currentFilteredData, 30, 10);
  }, [currentFilteredData]);

  // 5. Finding 研究發現自動生成
  const findings = useMemo(() => {
    if (!allData || allData.length === 0) return null;
    return generateFindings(currentFilteredData, allData, selectedPeriod);
  }, [currentFilteredData, allData, selectedPeriod]);

  return (
    <div className="dashboard-wrapper">
      {/* 頂部導覽與控制區 */}
      <Header
        selectedPeriod={selectedPeriod}
        onPeriodChange={setSelectedPeriod}
        dataSourceName={dataSourceName}
        isDemo={isDemo}
        onOpenUploadModal={() => setIsModalOpen(true)}
        onResetData={loadDefaultData}
      />

      <main className="dashboard-main">
        {loading ? (
          <div className="loading-container">
            <Loader2 className="spinner" size={44} />
            <p className="loading-text">正在讀取並分析股票數據，請稍候...</p>
          </div>
        ) : error ? (
          <div className="error-container">
            <AlertCircle size={48} className="error-icon" />
            <h3 className="error-title">資料載入失敗</h3>
            <p className="error-desc">{error}</p>
            <button type="button" className="btn btn-primary" onClick={loadDefaultData}>
              重新嘗試載入
            </button>
          </div>
        ) : (
          <>
            {/* 2. 四張 KPI 卡片 */}
            <KpiCards kpi={kpis} selectedPeriod={selectedPeriod} />

            {/* 3 & 4. 兩大核心圖表網格 */}
            <section className="charts-grid" aria-label="分析圖表區">
              {/* 3. 各財務年度直條圖 */}
              <PeriodGrowthChart
                periodStats={periodStats}
                selectedPeriod={selectedPeriod}
              />

              {/* 4. 各產業 Top 10 水平橫條圖 */}
              <IndustryTop10Chart
                industryData={industryTop10}
                selectedPeriod={selectedPeriod}
              />
            </section>

            {/* 5. Finding 研究發現區塊 */}
            <FindingsBanner findings={findings} />
          </>
        )}
      </main>

      <footer className="dashboard-footer">
        <p>
          交大課程學習成果專案 © 台灣上市公司高成長股票分析互動式 Dashboard
          {isDemo && <span className="footer-badge">目前使用示範數據展示</span>}
        </p>
      </footer>

      {/* 資料替換/上傳模態視窗 */}
      <DataUploadModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onDataLoaded={handleCustomDataLoaded}
        onResetDefault={loadDefaultData}
      />
    </div>
  );
}
