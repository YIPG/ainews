#!/usr/bin/env python3
"""
Email composition script using Jinja2.
Renders translated content using email template.
"""

import json
import sys
from datetime import datetime
from typing import Dict, Any

from jinja2 import Environment, FileSystemLoader, Template


def load_metadata(meta_file: str) -> Dict[str, Any]:
    """Load metadata from JSON file."""
    try:
        with open(meta_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Metadata file '{meta_file}' not found")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error parsing metadata JSON: {e}")
        sys.exit(1)


def read_content_file(content_file: str) -> str:
    """Read translated content from file."""
    try:
        with open(content_file, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: Content file '{content_file}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading content file: {e}")
        sys.exit(1)


def load_template() -> Template:
    """Load Jinja2 template."""
    try:
        env = Environment(loader=FileSystemLoader("templates"))
        return env.get_template("issue.j2")
    except Exception as e:
        print(f"Error loading template: {e}")
        # Fallback to basic template
        return Template("""{{ title }}

{{ content }}

---

元記事: {{ original_link }}
発行日: {{ published_date }}
""")


def format_date(date_str: str) -> str:
    """Format date string for Japanese display."""
    try:
        # Parse common date formats
        for fmt in ["%a, %d %b %Y %H:%M:%S %z", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%SZ"]:
            try:
                dt = datetime.strptime(date_str, fmt)
                return dt.strftime("%Y年%m月%d日")
            except ValueError:
                continue
        
        # If parsing fails, return original string
        return date_str
    except Exception:
        return date_str


def render_email(metadata: Dict[str, Any], content: str) -> str:
    """Render email using template."""
    template = load_template()
    
    # Prepare template variables
    template_vars = {
        "title": metadata.get("title", ""),
        "content": content,
        "original_link": metadata.get("link", ""),
        "published_date": format_date(metadata.get("published", "")),
        "author": metadata.get("author", ""),
        "tags": metadata.get("tags", []),
        "guid": metadata.get("guid", ""),
        "processed_at": metadata.get("processed_at", ""),
        "current_date": datetime.now().strftime("%Y年%m月%d日"),
    }
    
    try:
        rendered = template.render(**template_vars)
        return rendered
    except Exception as e:
        print(f"Error rendering template: {e}")
        sys.exit(1)


def main() -> None:
    """Main function to render email."""
    if len(sys.argv) != 3:
        print("Usage: python render.py <meta_file> <content_file>")
        print("Example: python render.py meta.json issue_ja.md")
        sys.exit(1)
    
    meta_file = sys.argv[1]
    content_file = sys.argv[2]
    
    # Load metadata and content
    metadata = load_metadata(meta_file)
    content = read_content_file(content_file)
    
    if not content.strip():
        print("Error: Content file is empty")
        sys.exit(1)
    
    # Render email
    rendered_email = render_email(metadata, content)
    
    # Output rendered email
    print(rendered_email)


if __name__ == "__main__":
    main()