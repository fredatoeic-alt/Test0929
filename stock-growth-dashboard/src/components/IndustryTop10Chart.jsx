import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  LabelList
} from 'recharts';
import { PERIOD_COLORS } from '../utils/analytics';

export default function IndustryTop10Chart({ industryData, selectedPeriod }) {
  const barColor = PERIOD_COLORS[selectedPeriod] || PERIOD_COLORS['ALL'];
  const displayPeriod = selectedPeriod === 'ALL' ? '全部年度' : selectedPeriod;

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="pbi-tooltip">
          <div className="pbi-tooltip-header">{data.industry}</div>
          <div className="pbi-tooltip-item">
            <span>高成長比例：</span>
            <strong>{data.rate.toFixed(2)}%</strong>
          </div>
          <div className="pbi-tooltip-item">
            <span>高成長筆數：</span>
            <span>{data.highGrowthCount.toLocaleString()} 筆</span>
          </div>
          <div className="pbi-tooltip-item">
            <span>觀測總筆數：</span>
            <span>{data.count.toLocaleString()} 筆</span>
          </div>
          <div className="pbi-tooltip-item">
            <span>平均報酬率：</span>
            <span>{data.avgReturn.toFixed(2)}%</span>
          </div>
        </div>
      );
    }
    return null;
  };

  const renderRightLabel = (props) => {
    const { x, y, width, height, value } = props;
    if (value === undefined || value === null) return null;
    return (
      <text
        x={x + width + 6}
        y={y + height / 2}
        fill="#333333"
        textAnchor="start"
        dominantBaseline="central"
        fontSize="11.5"
        fontWeight="400"
      >
        {`${Number(value).toFixed(2)}%`}
      </text>
    );
  };

  return (
    <div className="pbi-chart-card" id="industry-top10-chart-card">
      <div className="pbi-chart-title-area">
        <h2 className="pbi-chart-main-title">
          {displayPeriod}｜各產業高成長股票比例 Top 10（觀測筆數≥30）
        </h2>
        <div className="pbi-chart-subtitle">高成長比例 依據 Industry 與 FinancialPeriod</div>
      </div>

      {industryData.length === 0 ? (
        <div className="pbi-chart-empty">
          <p>在此篩選條件下，無觀測筆數 ≥ 30 筆之產業數據。</p>
        </div>
      ) : (
        <div className="pbi-chart-plot" style={{ height: 320, width: '100%' }}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              layout="vertical"
              data={industryData}
              margin={{ top: 10, right: 65, left: 10, bottom: 5 }}
              barSize={16}
            >
              <CartesianGrid strokeDasharray="0 0" horizontal={false} stroke="#ECEFF1" />
              <XAxis
                type="number"
                unit="%"
                tickLine={false}
                axisLine={{ stroke: '#B0BEC5' }}
                tick={{ fill: '#78909C', fontSize: 11 }}
                domain={[0, 80]}
                ticks={[0, 20, 40, 60, 80]}
              />
              <YAxis
                type="category"
                dataKey="industry"
                tickLine={false}
                axisLine={{ stroke: '#B0BEC5' }}
                tick={{ fill: '#455A64', fontSize: 11.5 }}
                width={125}
              />
              <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(0,0,0,0.03)' }} />
              <Bar dataKey="rate" fill={barColor}>
                <LabelList dataKey="rate" content={renderRightLabel} />
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}

      <div className="pbi-chart-legend">
        <span className="pbi-legend-dot" style={{ backgroundColor: barColor }} />
        <span className="pbi-legend-text">{displayPeriod}</span>
      </div>
    </div>
  );
}
