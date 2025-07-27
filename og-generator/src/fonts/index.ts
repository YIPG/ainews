// フォント設定
// 本来はローカルフォントファイルをimportしますが、
// 今はオンラインフォントをfetchして使用します

export async function loadNotoSansJP() {
  try {
    // システムフォントやローカルフォントが使えない場合のフォールバック
    // 実際のプロダクションでは、フォントファイルをプロジェクトに含めるべき
    console.log('Note: Using fallback font loading method');
    return null; // フォールバックフォントを使用
  } catch (error) {
    console.warn('Failed to load Noto Sans JP, using fallback');
    return null;
  }
}

export async function loadInterFont() {
  try {
    // Interフォントをフォールバックとして使用
    const response = await fetch('https://fonts.gstatic.com/s/inter/v12/UcCO3FwrK3iLTeHuS_fvQtMwCp50KnMw2boKoduKmMEVuLyfAZ9hiA.woff2');
    
    if (!response.ok) {
      throw new Error(`Failed to fetch Inter font: ${response.status}`);
    }
    
    const fontData = await response.arrayBuffer();
    return Buffer.from(fontData);
  } catch (error) {
    console.warn('Failed to load Inter font');
    return null;
  }
}