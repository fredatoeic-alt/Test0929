/**
 * 台灣上市公司高成長股票分析 - 資料計算與分析工具
 */

export const PERIOD_COLORS = {
  '2021FY': '#3E77BD',
  '2022FY': '#3B9C82',
  '2023FY': '#D98A2B',
  'ALL': '#3B629B'
};

/**
 * 清理與驗證單筆資料
 */
export function sanitizeRecord(raw) {
  if (!raw) return null;
  const period = String(raw.FinancialPeriod || '').trim();
  const industry = String(raw.Industry || '').trim();
  const highGrowth = String(raw.HighGrowth || '').trim().toUpperCase();
  const stockReturn = parseFloat(raw.StockReturn);

  if (!period || !industry) return null;

  return {
    ...raw,
    FinancialPeriod: period,
    Industry: industry,
    HighGrowth: highGrowth === 'Y' ? 'Y' : 'N',
    StockReturn: isNaN(stockReturn) ? null : stockReturn,
    ROE: isNaN(parseFloat(raw.ROE)) ? null : parseFloat(raw.ROE),
    ROA: isNaN(parseFloat(raw.ROA)) ? null : parseFloat(raw.ROA),
    EPS: isNaN(parseFloat(raw.EPS)) ? null : parseFloat(raw.EPS),
  };
}

/**
 * 計算 KPI 指標
 */
export function calculateKPIs(data) {
  const totalCount = data.length;
  if (totalCount === 0) {
    return {
      totalCount: 0,
      highGrowthCount: 0,
      highGrowthRate: 0,
      avgStockReturn: 0
    };
  }

  const highGrowthCount = data.filter(d => d.HighGrowth === 'Y').length;
  const highGrowthRate = (highGrowthCount / totalCount) * 100;

  const validReturns = data.filter(d => d.StockReturn !== null && !isNaN(d.StockReturn));
  const sumReturn = validReturns.reduce((acc, curr) => acc + curr.StockReturn, 0);
  const avgStockReturn = validReturns.length > 0 ? (sumReturn / validReturns.length) : 0;

  return {
    totalCount,
    highGrowthCount,
    highGrowthRate,
    avgStockReturn
  };
}

/**
 * 計算各財務年度高成長比例 (2021FY, 2022FY, 2023FY)
 */
export function calculatePeriodStats(allData, selectedPeriod = '2021FY') {
  const targetPeriods = ['2021FY', '2022FY', '2023FY'];
  
  return targetPeriods.map(period => {
    const periodRecords = allData.filter(d => d.FinancialPeriod === period);
    const count = periodRecords.length;
    const highGrowthCount = periodRecords.filter(d => d.HighGrowth === 'Y').length;
    const rate = count > 0 ? (highGrowthCount / count) * 100 : 0;

    return {
      period,
      count,
      highGrowthCount,
      rate: Number(rate.toFixed(2)),
      fillColor: PERIOD_COLORS[period] || '#3E77BD',
      isSelected: selectedPeriod === 'ALL' || selectedPeriod === period,
      isExplicitlyFocused: selectedPeriod === period
    };
  });
}

/**
 * 各產業高成長股票比例 Top 10 (觀測筆數 >= 30)
 */
export function calculateIndustryRanking(data, minCount = 30, topN = 10) {
  const industryMap = new Map();

  data.forEach(item => {
    const ind = item.Industry;
    if (!industryMap.has(ind)) {
      industryMap.set(ind, {
        industry: ind,
        count: 0,
        highGrowthCount: 0,
        returnSum: 0,
        validReturnCount: 0
      });
    }
    const stat = industryMap.get(ind);
    stat.count += 1;
    if (item.HighGrowth === 'Y') {
      stat.highGrowthCount += 1;
    }
    if (item.StockReturn !== null && !isNaN(item.StockReturn)) {
      stat.returnSum += item.StockReturn;
      stat.validReturnCount += 1;
    }
  });

  const eligible = Array.from(industryMap.values())
    .filter(item => item.count >= minCount)
    .map(item => {
      const rate = (item.highGrowthCount / item.count) * 100;
      const avgReturn = item.validReturnCount > 0 ? (item.returnSum / item.validReturnCount) : 0;
      return {
        industry: item.industry,
        count: item.count,
        highGrowthCount: item.highGrowthCount,
        rate: Number(rate.toFixed(2)),
        avgReturn: Number(avgReturn.toFixed(2))
      };
    });

  eligible.sort((a, b) => b.rate - a.rate || b.count - a.count);

  return eligible.slice(0, topN);
}

/**
 * 依截圖格式與規則動態生成 Finding
 */
export function generateFindings(currentFilteredData, allData, selectedPeriod) {
  const currentKPI = calculateKPIs(currentFilteredData);
  const fmtRate = currentKPI.highGrowthRate.toFixed(2);
  const hg = currentKPI.highGrowthCount.toLocaleString();
  const total = currentKPI.totalCount.toLocaleString();

  const prevPeriodMap = {
    '2022FY': '2021FY',
    '2023FY': '2022FY'
  };

  let mainStatement = `高成長股票占比${fmtRate}%（${hg}／${total}筆）。`;

  if (selectedPeriod === 'ALL') {
    mainStatement += `涵蓋2021FY至2023FY整體觀測結果，不同產業的高成長比例存在顯著差異，建議結合產業排名進一步觀察。`;
    return {
      periodText: '全部年度',
      mainStatement
    };
  }

  const prevPeriod = prevPeriodMap[selectedPeriod];
  if (prevPeriod) {
    const prevData = allData.filter(d => d.FinancialPeriod === prevPeriod);
    const prevKPI = calculateKPIs(prevData);
    const diffRate = (currentKPI.highGrowthRate - prevKPI.highGrowthRate).toFixed(2);
    const sign = diffRate >= 0 ? '+' : '';
    mainStatement += `相較前一年度（${prevPeriod}）高成長比例變動 ${sign}${diffRate} 個百分點，不同產業的高成長比例存在差異，建議結合產業排名進一步觀察。`;
  } else {
    mainStatement += `不同產業的高成長比例存在差異，建議結合產業排名進一步觀察。`;
  }

  return {
    periodText: selectedPeriod,
    mainStatement
  };
}
