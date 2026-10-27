import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
  LabelList
} from 'recharts';

export default function PeriodGrowthChart({ periodStats, selectedPeriod }) {
  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="pbi-tooltip">
          <div className="pbi-tooltip-header">{data.period}</div>
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
        </div>
      );
    }
    return null;
  };

  const renderTopLabel = (props) => {
    const { x, y, width, value } = props;
    if (value === undefined || value === null) return null;
    return (
      <text
        x={x + width / 2}
        y={y - 8}
        fill="#333333"
        textAnchor="middle"
        dominantBaseline="bottom"
        fontSize="12.5"
        fontWeight="500"
      >
        {`${Number(value).toFixed(2)}%`}
      </text>
    );
  };

  return (
    <div className="pbi-chart-card" id="period-growth-chart-card">
      <div className="pbi-chart-title-area">
        <h2 className="pbi-chart-main-title">各財務年度對應之高成長股票比例</h2>
        <div className="pbi-chart-subtitle">高成長比例 依據 FinancialPeriod</div>
      </div>

      <div className="pbi-chart-plot" style={{ height: 320, width: '100%' }}>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={periodStats}
            margin={{ top: 25, right: 20, left: -10, bottom: 10 }}
            barSize={46}
          >
            <CartesianGrid strokeDasharray="0 0" vertical={false} stroke="#ECEFF1" />
            <XAxis
              dataKey="period"
              tickLine={false}
              axisLine={{ stroke: '#B0BEC5' }}
              tick={{ fill: '#546E7A', fontSize: 12 }}
            />
            <YAxis
              tickLine={false}
              axisLine={{ stroke: '#B0BEC5' }}
              tick={{ fill: '#78909C', fontSize: 11 }}
              unit="%"
              domain={[0, 50]}
              ticks={[0, 10, 20, 30, 40, 50]}
            />
            <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(0,0,0,0.03)' }} />
            <Bar dataKey="rate">
              <LabelList dataKey="rate" content={renderTopLabel} />
              {periodStats.map((entry) => {
                const isSelected = selectedPeriod === 'ALL' || selectedPeriod === entry.period;
                const opacity = isSelected ? 1.0 : 0.35;
                return (
                  <Cell
                    key={`pbi-cell-${entry.period}`}
                    fill={entry.fillColor}
                    fillOpacity={opacity}
                  />
                );
              })}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="pbi-chart-note">
        註：2021FY財務資料對應2022年預測基準，並以2023年股價漲幅判定是否為高成長股票；其餘年度依此類推。
      </div>
    </div>
  );
}
