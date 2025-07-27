import { ImageResponse } from '@vercel/og';
import { NewsletterTemplate } from './templates/newsletter.js';
import sharp from 'sharp';
import yargs from 'yargs';
import { hideBin } from 'yargs/helpers';
import fs from 'fs/promises';
import path from 'path';
import { loadNotoSansJP } from './utils/fontLoader.js';

interface Arguments {
  title: string;
  date: string;
  output: string;
}

async function generateOGImage(args: Arguments) {
  try {
    console.log('Generating OG image...');
    console.log(`Title: ${args.title}`);
    console.log(`Date: ${args.date}`);
    console.log(`Output: ${args.output}`);

    // Noto Sans JP フォントを読み込み
    console.log('Loading Noto Sans JP font...');
    const notoSansJP = await loadNotoSansJP();
    
    const fonts = [];
    
    if (notoSansJP) {
      fonts.push({
        name: 'Noto Sans JP',
        data: notoSansJP,
        weight: 700 as const,
        style: 'normal' as const,
      });
      console.log('✅ Using Noto Sans JP font');
    } else {
      console.log('⚠️  Using default font (Noto Sans JP not available)');
    }

    // Generate the image using Satori
    const imageResponse = new ImageResponse(
      NewsletterTemplate({
        title: args.title,
        date: args.date,
      }),
      {
        width: 1200,
        height: 630,
        fonts,
      }
    );

    // Convert to buffer
    const arrayBuffer = await imageResponse.arrayBuffer();
    const buffer = Buffer.from(arrayBuffer);

    // Ensure output directory exists
    const outputDir = path.dirname(args.output);
    await fs.mkdir(outputDir, { recursive: true });

    // Save as PNG using sharp for better quality
    await sharp(buffer)
      .png({ quality: 95, compressionLevel: 9 })
      .toFile(args.output);

    console.log(`✅ OG image generated successfully: ${args.output}`);
  } catch (error) {
    console.error('Error generating OG image:', error);
    process.exit(1);
  }
}

// Parse command line arguments
const argv = yargs(hideBin(process.argv))
  .options({
    title: {
      type: 'string',
      demandOption: true,
      describe: 'Newsletter title',
    },
    date: {
      type: 'string',
      demandOption: true,
      describe: 'Newsletter date',
    },
    output: {
      type: 'string',
      demandOption: true,
      describe: 'Output file path',
    },
  })
  .help()
  .parseSync() as Arguments;

// Generate the image
generateOGImage(argv);