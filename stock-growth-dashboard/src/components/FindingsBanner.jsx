import React from 'react';

export default function FindingsBanner({ findings }) {
  if (!findings) return null;

  return (
    <section className="pbi-finding-section" aria-label="高成長分析Finding">
      <div className="pbi-finding-box">
        <div className="pbi-finding-tag">高成長分析Finding</div>
        <div className="pbi-finding-headline">
          <span className="pbi-finding-prefix">{findings.periodText}｜研究發現：</span>
          <span className="pbi-finding-text">{findings.mainStatement}</span>
        </div>
      </div>
    </section>
  );
}
