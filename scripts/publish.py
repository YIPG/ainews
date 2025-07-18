#!/usr/bin/env python3
"""
Newsletter publishing script for GitHub Pages.
Converts translated markdown to HTML and updates the archive.
"""

import json
import re
import os
import sys
from datetime import datetime
from pathlib import Path
import markdown
from markdown.extensions import codehilite, tables, toc

def extract_title_and_summary(markdown_content):
    """Extract title and create a summary from markdown content."""
    lines = markdown_content.strip().split('\n')
    
    # Find the first header (title)
    title = "AI技術ニュースレター"
    for line in lines:
        if line.startswith('＃ ') or line.startswith('# '):
            title = line.replace('＃ ', '').replace('# ', '').strip()
            break
    
    # Create summary from first few meaningful paragraphs
    summary_lines = []
    char_count = 0
    max_chars = 150
    
    for line in lines:
        line = line.strip()
        # Skip headers, images, bullet points, and empty lines, but allow paragraphs with links
        if (line.startswith('#') or line.startswith('＃') or 
            line.startswith('![') or 
            line.startswith('- ') or line.startswith('* ') or line.startswith('> ') or
            not line):
            continue
        
        # Clean up markdown formatting for display
        clean_line = line
        # Remove markdown links: [text](url) -> text
        clean_line = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', clean_line)
        # Remove bold markdown: **text** -> text
        clean_line = re.sub(r'\*\*([^*]+)\*\*', r'\1', clean_line)
        
        # Check if adding this line would exceed the limit
        if char_count + len(clean_line) > max_chars:
            # If we have some content already, break
            if summary_lines:
                break
            # If this is the first line and it's too long, truncate it
            clean_line = clean_line[:max_chars - char_count - 3] + '...'
            summary_lines.append(clean_line)
            break
            
        summary_lines.append(clean_line)
        char_count += len(clean_line)
        
        if char_count > 100:  # Minimum summary length
            break
    
    summary = ' '.join(summary_lines)
    if len(summary) > max_chars:
        summary = summary[:max_chars] + '...'
    elif summary and not summary.endswith('...'):
        summary = summary + '...'
    
    return title, summary

def markdown_to_html(markdown_content, title, date):
    """Convert markdown content to HTML with custom styling."""
    
    # Preprocess markdown to convert full-width # to regular #
    processed_content = markdown_content.replace('＃', '#')
    
    # Configure markdown extensions
    md = markdown.Markdown(extensions=[
        'codehilite',
        'tables',
        'toc',
        'fenced_code'
    ])
    
    # Convert markdown to HTML
    content_html = md.convert(processed_content)
    
    # Create full HTML page with improved accessibility and bearblog-inspired design
    html_template = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | AIニュース</title>
    <meta name="description" content="{title} - AIニュース {date}。最新のAI技術動向を日本語でお届け。">
    <meta name="keywords" content="AI,人工知能,ニュースレター,{date},機械学習,深層学習,日本語">
    <meta name="author" content="AIニュース">
    <link rel="canonical" href="https://yipg.github.io/ainews/docs/newsletters/{date}.html">
    
    <!-- Open Graph meta tags -->
    <meta property="og:title" content="{title} | AIニュース">
    <meta property="og:description" content="{title} - AIニュース {date}。最新のAI技術動向を日本語でお届け。">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://yipg.github.io/ainews/docs/newsletters/{date}.html">
    <meta property="og:site_name" content="AIニュース">
    <meta property="og:locale" content="ja_JP">
    <meta property="article:published_time" content="{date}T09:00:00+00:00">
    <meta property="article:author" content="AIニュース">
    <meta property="article:section" content="AI技術ニュース">
    
    <!-- Twitter Card meta tags -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title} | AIニュース">
    <meta name="twitter:description" content="{title} - AIニュース {date}。最新のAI技術動向を日本語でお届け。">
    
    <!-- Favicon -->
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>✏️</text></svg>">
    <link rel="alternate icon" href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAA7EAAAOxAGVKw4bAAAA">
    
    <!-- RSS Feed -->
    <link rel="alternate" type="application/rss+xml" title="AIニュース RSS Feed" href="../feed.xml">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: Verdana, Geneva, sans-serif;
            font-size: 1em;
            line-height: 1.7;
            letter-spacing: 0.02em;
            max-width: 720px;
            margin: 0 auto;
            padding: 20px;
            background-color: #fff;
            color: #111;
            word-wrap: break-word;
        }}
        
        nav {{
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 1px solid #ddd;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: nowrap;
        }}
        
        .site-title {{
            font-size: 1.1em;
            font-weight: bold;
            color: #111;
            text-decoration: none;
            flex-shrink: 0;
        }}
        
        .site-title:hover {{
            text-decoration: underline;
        }}
        
        .nav-links {{
            font-size: 0.85em;
            white-space: nowrap;
        }}
        
        .nav-links a {{
            color: #111;
            text-decoration: none;
            margin-left: 12px;
        }}
        
        .nav-links a:hover {{
            text-decoration: underline;
        }}
        
        
        h1, h2, h3, h4, h5, h6 {{
            margin: 35px 0 20px 0;
            line-height: 1.3;
            color: #111;
            letter-spacing: 0.01em;
        }}
        
        h1 {{ font-size: 1.5em; }}
        h2 {{ font-size: 1.3em; }}
        h3 {{ font-size: 1.1em; }}
        
        p {{
            margin: 20px 0;
        }}
        
        a {{
            color: #0969da;
            text-decoration: none;
        }}
        
        a:hover {{
            text-decoration: underline;
        }}
        
        ul, ol {{
            margin: 20px 0;
            padding-left: 30px;
        }}
        
        li {{
            margin: 8px 0;
        }}
        
        blockquote {{
            border-left: 3px solid #ccc;
            margin: 25px 0;
            padding: 0 25px;
            color: #555;
            font-style: italic;
        }}
        
        code {{
            background-color: #f6f8fa;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Courier New', Courier, monospace;
            font-size: 0.9em;
        }}
        
        pre {{
            background-color: #f6f8fa;
            border-radius: 6px;
            padding: 20px;
            overflow-x: auto;
            margin: 25px 0;
        }}
        
        pre code {{
            background: none;
            padding: 0;
        }}
        
        img {{
            max-width: 100%;
            height: auto;
            margin: 25px 0;
            border-radius: 3px;
        }}
        
        hr {{
            border: none;
            border-top: 1px solid #ddd;
            margin: 35px 0;
        }}
        
        footer {{
            margin-top: 40px;
            padding-top: 15px;
            border-top: 1px solid #ddd;
            text-align: center;
            color: #555;
            font-size: 0.85em;
        }}
        
        footer a {{
            color: #555;
            text-decoration: none;
            margin: 0 8px;
        }}
        
        footer a:hover {{
            text-decoration: underline;
        }}
        
        @media (max-width: 600px) {{
            body {{
                padding: 15px;
                font-size: 0.95em;
            }}
            
            nav {{
                flex-direction: column;
                align-items: flex-start;
                gap: 10px;
            }}
            
            .nav-links {{
                font-size: 0.8em;
            }}
            
            .nav-links a {{
                margin-left: 0;
                margin-right: 12px;
            }}
            
            .article-title {{
                font-size: 1.4em;
            }}
        }}
        
        @media (max-width: 480px) {{
            body {{
                font-size: 0.9em;
                padding: 12px;
            }}
            
            .site-title {{
                font-size: 1em;
            }}
            
            .nav-links {{
                font-size: 0.75em;
            }}
            
            .article-title {{
                font-size: 1.3em;
            }}
        }}
        
        @media (prefers-color-scheme: dark) {{
            body {{
                background-color: #111;
                color: #eee;
            }}
            
            nav {{
                border-bottom-color: #444;
            }}
            
            .site-title, .nav-links a, .article-title, h1, h2, h3, h4, h5, h6 {{
                color: #eee;
            }}
            
            .article-date {{
                color: #ccc;
            }}
            
            blockquote {{
                border-left-color: #555;
                color: #ccc;
            }}
            
            code {{
                background-color: #2d3748;
                color: #e2e8f0;
            }}
            
            pre {{
                background-color: #2d3748;
            }}
            
            hr, footer {{
                border-color: #444;
            }}
            
            footer, footer a {{
                color: #ccc;
            }}
        }}
    </style>
</head>
<body>
    <nav>
        <a href="../index.html" class="site-title">✏️ AIニュース</a>
        <div class="nav-links">
            <a href="../index.html">ホーム</a>
            <a href="./archive.html">アーカイブ</a>
            <a href="../feed.xml">RSS</a>
        </div>
    </nav>

    <main>
        {content_html}
    </main>

    <footer>
        <p>
            <a href="https://github.com/YIPG/ainews">GitHub</a>
            <a href="https://news.smol.ai/">news.smol.ai</a>
        </p>
    </footer>
</body>
</html>"""
    
    return html_template

def update_archive_index(date, title, summary, filename):
    """Update the archive index JSON file."""
    index_path = Path("docs/newsletters/index.json")
    
    # Load existing data
    if index_path.exists():
        with open(index_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {"newsletters": [], "lastUpdated": None, "totalCount": 0}
    
    # Check if this newsletter already exists
    existing = None
    for i, newsletter in enumerate(data["newsletters"]):
        if newsletter["date"] == date:
            existing = i
            break
    
    newsletter_entry = {
        "date": date,
        "title": title,
        "summary": summary,
        "filename": filename
    }
    
    if existing is not None:
        # Update existing entry
        data["newsletters"][existing] = newsletter_entry
    else:
        # Add new entry
        data["newsletters"].append(newsletter_entry)
    
    # Update metadata
    data["lastUpdated"] = datetime.now().isoformat()
    data["totalCount"] = len(data["newsletters"])
    
    # Save updated data
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def generate_rss_feed():
    """Generate RSS feed for the newsletters."""
    index_path = Path("docs/newsletters/index.json")
    
    if not index_path.exists():
        return
    
    with open(index_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Sort newsletters by date (newest first)
    newsletters = sorted(data["newsletters"], key=lambda x: x["date"], reverse=True)
    
    # Take only the latest 20 for RSS
    newsletters = newsletters[:20]
    
    rss_items = []
    for newsletter in newsletters:
        rss_items.append(f"""    <item>
      <title>{newsletter['title']}</title>
      <link>https://yipg.github.io/ainews/docs/newsletters/{newsletter['filename']}</link>
      <description><![CDATA[{newsletter['summary']}]]></description>
      <pubDate>{datetime.strptime(newsletter['date'], '%Y-%m-%d').strftime('%a, %d %b %Y 09:00:00 +0000')}</pubDate>
      <guid>https://yipg.github.io/ainews/docs/newsletters/{newsletter['filename']}</guid>
    </item>""")
    
    rss_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>AI技術ニュースレター</title>
    <link>https://yipg.github.io/ainews/</link>
    <description>AI技術に関する最新ニュースの日本語翻訳ニュースレター</description>
    <language>ja</language>
    <lastBuildDate>{datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')}</lastBuildDate>
    <generator>AI Newsletter Archive System</generator>
{chr(10).join(rss_items)}
  </channel>
</rss>"""
    
    with open("docs/feed.xml", 'w', encoding='utf-8') as f:
        f.write(rss_content)

def main():
    """Main publishing function."""
    if len(sys.argv) != 2:
        print("Usage: python publish.py <translated_markdown_file>")
        sys.exit(1)
    
    markdown_file = sys.argv[1]
    
    if not os.path.exists(markdown_file):
        print(f"Error: File {markdown_file} does not exist")
        sys.exit(1)
    
    # Extract date from filename (assuming YYYY-MM-DD format)
    filename_base = Path(markdown_file).stem
    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', filename_base)
    if not date_match:
        print(f"Error: Could not extract date from filename {markdown_file}")
        sys.exit(1)
    
    date = date_match.group(1)
    output_filename = f"{date}.html"
    output_path = f"docs/newsletters/{output_filename}"
    
    # Read markdown content
    with open(markdown_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Extract title and summary
    title, summary = extract_title_and_summary(markdown_content)
    
    # Convert to HTML
    html_content = markdown_to_html(markdown_content, title, date)
    
    # Ensure output directory exists
    os.makedirs("docs/newsletters", exist_ok=True)
    
    # Write HTML file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # Update archive index
    update_archive_index(date, title, summary, output_filename)
    
    # Generate RSS feed
    generate_rss_feed()
    
    print(f"Published newsletter: {output_path}")
    print(f"Title: {title}")
    print(f"Summary: {summary[:100]}...")

if __name__ == "__main__":
    main()