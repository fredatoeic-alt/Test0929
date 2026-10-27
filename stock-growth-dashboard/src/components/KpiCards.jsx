import React from 'react';

export default function KpiCards({ kpi }) {
  const { totalCount, highGrowthCount, highGrowthRate, avgStockReturn } = kpi;

  const cards = [
    {
      id: 'kpi-obs-count',
      label: '觀測筆數',
      value: totalCount.toLocaleString(),
    },
    {
      id: 'kpi-high-growth-count',
      label: '高成長筆數',
      value: highGrowthCount.toLocaleString(),
    },
    {
      id: 'kpi-high-growth-rate',
      label: '高成長比例',
      value: `${highGrowthRate.toFixed(2)}%`,
    },
    {
      id: 'kpi-avg-return',
      label: '平均隔年報酬率',
      value: `${avgStockReturn.toFixed(2)}%`,
    }
  ];

  return (
    <section className="pbi-kpi-container" aria-label="核心 KPI 指標卡片">
      {cards.map((card) => (
        <div key={card.id} id={card.id} className="pbi-kpi-card">
          <div className="pbi-kpi-label">{card.label}</div>
          <div className="pbi-kpi-value">{card.value}</div>
        </div>
      ))}
    </section>
  );
}
