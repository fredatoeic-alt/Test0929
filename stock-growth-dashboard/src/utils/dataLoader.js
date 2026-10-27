import Papa from 'papaparse';
import { sanitizeRecord } from './analytics';

export const DEFAULT_CSV_PATH = '/data/stock_data.csv';

/**
 * 自動解碼二進位 Buffer（支援 UTF-8 與 Big5 / CP950）
 */
function decodeBuffer(buffer) {
  try {
    const utf8Decoder = new TextDecoder('utf-8', { fatal: true });
    return utf8Decoder.decode(buffer);
  } catch {
    // 若 UTF-8 解碼失敗，使用繁體中文 Big5 解碼
    const big5Decoder = new TextDecoder('big5');
    return big5Decoder.decode(buffer);
  }
}

/**
 * 從 URL 下載並解析 CSV
 */
export async function loadCsvFromUrl(url = DEFAULT_CSV_PATH) {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`無法讀取資料檔 (${response.status} ${response.statusText})`);
    }
    const buffer = await response.arrayBuffer();
    const csvText = decodeBuffer(buffer);
    return parseCsvString(csvText);
  } catch (error) {
    console.error('CSV 載入失敗:', error);
    throw error;
  }
}

/**
 * 解析 CSV 字串為結構化資料
 */
export function parseCsvString(csvString) {
  return new Promise((resolve, reject) => {
    Papa.parse(csvString, {
      header: true,
      skipEmptyLines: 'greedy',
      dynamicTyping: true,
      complete: (results) => {
        if (results.errors && results.errors.length > 0) {
          console.warn('CSV 解析警告:', results.errors);
        }
        const cleaned = results.data
          .map(sanitizeRecord)
          .filter(Boolean);

        if (cleaned.length === 0) {
          reject(
            new Error(
              'CSV 檔中未找到任何有效股票資料，請檢查欄位格式 (FinancialPeriod, Industry, HighGrowth, StockReturn)'
            )
          );
        } else {
          resolve(cleaned);
        }
      },
      error: (err) => {
        reject(err);
      }
    });
  });
}

/**
 * 解析使用者上傳的 File 物件（支援 UTF-8 與 Big5 編碼）
 */
export function parseUploadedFile(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const buffer = e.target.result;
        const text = decodeBuffer(buffer);
        resolve(parseCsvString(text));
      } catch (err) {
        reject(err);
      }
    };
    reader.onerror = () => reject(new Error('讀取檔案失敗'));
    reader.readAsArrayBuffer(file);
  });
}
