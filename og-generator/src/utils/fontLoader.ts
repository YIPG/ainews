import fs from 'fs/promises';
import path from 'path';

/**
 * カスタムフォントローダー
 * ブログ記事 https://blog.okaryo.studio/20250115-load-local-fonts-in-astro/ を参考
 */

// フォントファイルをBufferとして読み込む関数
export async function loadFontFile(fontPath: string): Promise<Buffer | null> {
  try {
    const absolutePath = path.resolve(fontPath);
    
    // ファイルの存在確認
    try {
      await fs.access(absolutePath);
    } catch {
      console.warn(`Font file not found: ${absolutePath}`);
      return null;
    }
    
    // ファイルタイプチェック（TTF/OTF のみ許可）
    const buffer = await fs.readFile(absolutePath);
    const signature = buffer.subarray(0, 4);
    
    // TTF: \x00\x01\x00\x00 または OTF: OTTO
    const isTTF = signature[0] === 0x00 && signature[1] === 0x01 && 
                  signature[2] === 0x00 && signature[3] === 0x00;
    const isOTF = signature.toString('ascii') === 'OTTO';
    
    if (!isTTF && !isOTF) {
      console.warn(`Invalid font file format: ${absolutePath}`);
      console.warn(`Signature: ${signature.toString('hex')}`);
      return null;
    }
    
    console.log(`✅ Loaded font: ${path.basename(fontPath)} (${isTTF ? 'TTF' : 'OTF'})`);
    return buffer;
  } catch (error) {
    console.error(`Error loading font file ${fontPath}:`, error);
    return null;
  }
}

// 複数のフォントソースを試行する関数
export async function loadNotoSansJP(): Promise<Buffer | null> {
  const fontPaths = [
    // プロジェクト内のフォント（優先） - src ディレクトリから読み込み
    path.resolve(__dirname, '../../src/fonts/NotoSansJP-Bold.ttf'),
    path.resolve(__dirname, '../../src/fonts/NotoSansJP-Regular.ttf'),
    
    // システムフォント (macOS)
    '/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc',
    '/Library/Fonts/NotoSansJP-Bold.ttf',
    
    // システムフォント (Linux)
    '/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc',
    '/usr/share/fonts/opentype/noto/NotoSansJP-Bold.otf',
  ];
  
  for (const fontPath of fontPaths) {
    console.log(`Trying font: ${fontPath}`);
    const buffer = await loadFontFile(fontPath);
    if (buffer) {
      return buffer;
    }
  }
  
  console.warn('Could not load any Noto Sans JP font');
  return null;
}

// Web フォントをダウンロードする関数（フォールバック）
export async function loadWebFont(): Promise<Buffer | null> {
  try {
    console.log('Attempting to download web font...');
    
    // 動作確認済みのフォントURL（Inter font）
    const response = await fetch('https://fonts.gstatic.com/s/inter/v13/UcC73FwrK3iLTeHuS_fvQtMwCp50KnMa1ZL7W0Q5n-wU.woff2');
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    
    // WOFF2 は Satori では使えないので、これは失敗するはず
    // 実際のプロダクションでは TTF ファイルを使用
    const arrayBuffer = await response.arrayBuffer();
    console.log('Downloaded web font, but WOFF2 format may not work with Satori');
    return Buffer.from(arrayBuffer);
  } catch (error) {
    console.warn('Failed to download web font:', error);
    return null;
  }
}