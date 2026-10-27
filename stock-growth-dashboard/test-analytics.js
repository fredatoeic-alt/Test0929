import {
  calculateKPIs,
  calculatePeriodStats,
  calculateIndustryRanking,
  generateFindings
} from './src/utils/analytics.js';

const mockData = [
  { FinancialPeriod: '2021FY', Industry: '半導體業', HighGrowth: 'Y', StockReturn: 30.5 },
  { FinancialPeriod: '2021FY', Industry: '半導體業', HighGrowth: 'N', StockReturn: 10.0 },
  { FinancialPeriod: '2022FY', Industry: '半導體業', HighGrowth: 'N', StockReturn: -5.0 },
  { FinancialPeriod: '2022FY', Industry: '電子零組件業', HighGrowth: 'Y', StockReturn: 15.0 },
  { FinancialPeriod: '2023FY', Industry: '生技醫療業', HighGrowth: 'Y', StockReturn: 25.0 }
];

console.log('--- 測試 1: 全部 KPI 計算 ---');
const kpisAll = calculateKPIs(mockData);
if (kpisAll.totalCount === 5 && kpisAll.highGrowthCount === 3 && kpisAll.highGrowthRate === 60) {
  console.log('✓ KPI 計算正確！');
} else {
  console.error('✗ KPI 計算有誤！');
  process.exit(1);
}

console.log('--- 測試 2: 各財務年度高成長比例計算 ---');
const periodStats = calculatePeriodStats(mockData, '2022FY');
if (periodStats.length === 3 && periodStats.find(p => p.period === '2022FY').isExplicitlyFocused) {
  console.log('✓ 年度統計與聚焦狀態正確！');
} else {
  console.error('✗ 年度統計有誤！');
  process.exit(1);
}

console.log('--- 測試 3: Finding 生成測試 ---');
const finding2022 = generateFindings(mockData.filter(d => d.FinancialPeriod === '2022FY'), mockData, '2022FY');
console.log('Finding 2022FY Statement:', finding2022.mainStatement);
if (finding2022.mainStatement.includes('高成長股票占比50.00%')) {
  console.log('✓ Finding 生成正確！');
} else {
  console.error('✗ Finding 生成有誤！');
  process.exit(1);
}

console.log('所有單元邏輯測試全部通過！');
