#!/usr/bin/env python3
"""
HTML to Markdown conversion script.
Converts HTML content to Markdown format while preserving headings and links.
"""

import sys
from typing import Optional

import html2text


def convert_html_to_markdown(html_content: str) -> str:
    """Convert HTML content to Markdown format."""
    h = html2text.HTML2Text()
    
    # Configure html2text settings
    h.ignore_images = False
    h.ignore_links = False
    h.ignore_emphasis = False
    h.body_width = 0  # No line wrapping
    h.unicode_snob = True
    h.escape_snob = True
    
    # Convert HTML to Markdown
    markdown_content = h.handle(html_content)
    
    # Clean up the output
    markdown_content = markdown_content.strip()
    
    return markdown_content


def read_html_file(file_path: str) -> str:
    """Read HTML content from file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)


def main() -> None:
    """Main function to convert HTML to Markdown."""
    if len(sys.argv) != 2:
        print("Usage: python convert.py <html_file>")
        print("Example: python convert.py issue.html")
        sys.exit(1)
    
    html_file = sys.argv[1]
    
    # Read HTML content
    html_content = read_html_file(html_file)
    
    if not html_content.strip():
        print("Error: HTML file is empty")
        sys.exit(1)
    
    # Convert to Markdown
    markdown_content = convert_html_to_markdown(html_content)
    
    if not markdown_content.strip():
        print("Error: Conversion resulted in empty content")
        sys.exit(1)
    
    # Output to stdout
    print(markdown_content)


if __name__ == "__main__":
    main()