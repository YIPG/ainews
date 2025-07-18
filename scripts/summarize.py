#!/usr/bin/env python3
"""
Extract summary from translated newsletter for Discord posting.
Limits output to ~1500 characters for Discord embed description.
"""

import sys
import re
from typing import Optional, Tuple


def extract_title_and_date(content: str) -> Tuple[Optional[str], Optional[str]]:
    """Extract title and date from newsletter content."""
    lines = content.strip().split('\n')
    
    title = None
    date = None
    
    for line in lines[:10]:  # Check first 10 lines
        # Look for main title (usually # or ##)
        if line.startswith('#') and not title:
            title = line.lstrip('#').strip()
        
        # Look for date pattern
        date_match = re.search(r'\d{4}年\d{1,2}月\d{1,2}日', line)
        if date_match and not date:
            date = date_match.group()
    
    return title, date


def extract_summary(content: str, max_length: int = 1500) -> str:
    """
    Extract summary from newsletter content.
    Takes first few paragraphs up to max_length characters.
    """
    # Remove title and metadata from the beginning
    lines = content.strip().split('\n')
    
    # Skip headers and empty lines at the start
    content_start = 0
    for i, line in enumerate(lines):
        if line.strip() and not line.startswith('#'):
            content_start = i
            break
    
    # Collect paragraphs
    paragraphs = []
    current_paragraph = []
    
    for line in lines[content_start:]:
        if line.strip() == '':
            if current_paragraph:
                paragraphs.append(' '.join(current_paragraph))
                current_paragraph = []
        else:
            # Skip headers and links
            if not line.startswith('#') and not line.startswith('['):
                current_paragraph.append(line.strip())
    
    # Add last paragraph if exists
    if current_paragraph:
        paragraphs.append(' '.join(current_paragraph))
    
    # Build summary up to max_length
    summary = ""
    for para in paragraphs:
        if len(summary) + len(para) + 2 <= max_length:  # +2 for newlines
            if summary:
                summary += "\n\n"
            summary += para
        else:
            # Add partial paragraph if there's room
            remaining = max_length - len(summary) - 5  # -5 for "..."
            if remaining > 50:  # Only add if meaningful content
                words = para.split()
                partial = ""
                for word in words:
                    if len(partial) + len(word) + 1 <= remaining:
                        if partial:
                            partial += " "
                        partial += word
                    else:
                        break
                if partial:
                    summary += "\n\n" + partial + "..."
            break
    
    return summary.strip()


def main():
    """Main function to process input file."""
    if len(sys.argv) != 2:
        print("Usage: python summarize.py <translated_markdown_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        title, date = extract_title_and_date(content)
        summary = extract_summary(content)
        
        # Output as JSON-like format for easy parsing in bash
        print(f"TITLE:{title or 'Japanese AI Newsletter'}")
        print(f"DATE:{date or 'Latest'}")
        print("SUMMARY_START")
        print(summary)
        print("SUMMARY_END")
        
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()