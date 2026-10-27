import React, { useState } from 'react';
import { X, UploadCloud, FileText, CheckCircle2, AlertTriangle } from 'lucide-react';
import { parseUploadedFile } from '../utils/dataLoader';

export default function DataUploadModal({ isOpen, onClose, onDataLoaded, onResetDefault }) {
  const [dragActive, setDragActive] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);

  if (!isOpen) return null;

  const handleFiles = async (files) => {
    if (!files || files.length === 0) return;
    const file = files[0];
    if (!file.name.endsWith('.csv') && !file.name.endsWith('.txt')) {
      setErrorMsg('請上傳 .csv 格式之檔案');
      return;
    }

    try {
      setIsProcessing(true);
      setErrorMsg('');
      const data = await parseUploadedFile(file);
      onDataLoaded(data, file.name);
      onClose();
    } catch (err) {
      setErrorMsg(err.message || '檔案解析失敗，請確認內容格式');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFiles(e.dataTransfer.files);
    }
  };

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div className="modal-title-group">
            <UploadCloud size={20} className="modal-icon" />
            <h3 className="modal-title">資料檔管理與替換</h3>
          </div>
          <button type="button" className="modal-close-btn" onClick={onClose}>
            <X size={18} />
          </button>
        </div>

        <div className="modal-body">
          {/* 正式資料檔替換說明 */}
          <div className="info-box">
            <h4 className="info-box-title">
              <FileText size={16} />
              本機正式檔案替換路徑：
            </h4>
            <code className="path-code">stock-growth-dashboard/public/data/stock_data.csv</code>
            <p className="info-desc">
              後續若要永久更新研究資料，直接將您的正式研究 CSV 檔儲存並命名為 <code>stock_data.csv</code> 覆蓋此路徑即可。
            </p>
          </div>

          {/* 欄位規範 */}
          <div className="specs-box">
            <h4>必備欄位規範：</h4>
            <div className="field-tags">
              <span className="field-tag required">FinancialPeriod (如 2021FY)</span>
              <span className="field-tag required">Industry (產業別)</span>
              <span className="field-tag required">HighGrowth (Y / N)</span>
              <span className="field-tag required">StockReturn (隔年報酬率, 20代表20%)</span>
              <span className="field-tag optional">StockID / StockName (選填)</span>
            </div>
          </div>

          {/* 即時檔案上傳測試區塊 */}
          <div
            className={`dropzone ${dragActive ? 'active' : ''}`}
            onDragEnter={() => setDragActive(true)}
            onDragLeave={() => setDragActive(false)}
            onDragOver={(e) => { e.preventDefault(); setDragActive(true); }}
            onDrop={handleDrop}
          >
            <input
              type="file"
              id="csv-file-input"
              accept=".csv"
              style={{ display: 'none' }}
              onChange={(e) => handleFiles(e.target.files)}
            />
            <label htmlFor="csv-file-input" className="dropzone-label">
              <UploadCloud size={36} className="dropzone-icon" />
              <p className="dropzone-text">
                點擊此處選擇 CSV 檔案，或將檔案拖曳至此進行即時預覽
              </p>
              <span className="dropzone-hint">支援繁體中文 UTF-8 編碼 CSV</span>
            </label>
          </div>

          {isProcessing && <div className="processing-indicator">資料解析中，請稍候...</div>}

          {errorMsg && (
            <div className="error-alert">
              <AlertTriangle size={16} />
              <span>{errorMsg}</span>
            </div>
          )}
        </div>

        <div className="modal-footer">
          <button
            type="button"
            className="btn btn-secondary"
            onClick={() => {
              onResetDefault();
              onClose();
            }}
          >
            恢復預設示範資料
          </button>
          <button type="button" className="btn btn-primary" onClick={onClose}>
            關閉
          </button>
        </div>
      </div>
    </div>
  );
}
