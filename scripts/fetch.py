#!/usr/bin/env python3
"""
RSS feed fetching script with deduplication.
Fetches latest entry from RSS feed and saves HTML content and metadata.
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, Any, Optional

import feedparser
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def load_last_guid() -> Optional[str]:
    """Load the last processed GUID from file."""
    try:
        with open("latest.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None


def save_last_guid(guid: str) -> None:
    """Save the current GUID to file."""
    with open("latest.txt", "w") as f:
        f.write(guid)


def fetch_feed(feed_url: str) -> Dict[str, Any]:
    """Fetch RSS feed and return parsed data."""
    try:
        feed = feedparser.parse(feed_url)
        
        if feed.bozo:
            print(f"Warning: Feed parsing issues: {feed.bozo_exception}")
        
        if not feed.entries:
            print("No entries found in feed")
            sys.exit(1)
            
        return feed
    except Exception as e:
        print(f"Error fetching feed: {e}")
        sys.exit(1)


def get_latest_entry(feed: Dict[str, Any]) -> Dict[str, Any]:
    """Get the latest entry from the feed."""
    latest_entry = feed.entries[0]
    
    # Extract relevant information
    entry_data = {
        "title": latest_entry.get("title", ""),
        "link": latest_entry.get("link", ""),
        "guid": latest_entry.get("id", latest_entry.get("guid", "")),
        "published": latest_entry.get("published", ""),
        "summary": latest_entry.get("summary", ""),
        "content": latest_entry.get("content", []),
        "author": latest_entry.get("author", ""),
        "tags": [tag.get("term", "") for tag in latest_entry.get("tags", [])],
    }
    
    return entry_data


def extract_html_content(entry: Dict[str, Any]) -> str:
    """Extract HTML content from entry."""
    # Try to get full content first
    if entry.get("content"):
        for content in entry["content"]:
            if content.get("type") == "text/html":
                return content.get("value", "")
    
    # Fallback to summary
    return entry.get("summary", "")


def main() -> None:
    """Main function to fetch and process RSS feed."""
    feed_url = os.environ.get("FEED_URL")
    if not feed_url:
        print("Error: FEED_URL environment variable is required")
        sys.exit(1)
    
    # Fetch the RSS feed
    feed = fetch_feed(feed_url)
    latest_entry = get_latest_entry(feed)
    
    # Generate date prefix from RSS published date
    try:
        # Parse RSS published date (e.g., "Thu, 17 Jul 2025 05:44:39 GMT")
        published_date = datetime.strptime(latest_entry["published"], "%a, %d %b %Y %H:%M:%S %Z")
        date_prefix = published_date.strftime("%Y-%m-%d")
    except (ValueError, KeyError):
        # Fallback to system date if parsing fails
        print("Warning: Could not parse RSS published date, using system date")
        date_prefix = datetime.now().strftime("%Y-%m-%d")
    
    current_guid = latest_entry["guid"]
    last_guid = load_last_guid()
    
    # Check if this is a new entry
    if current_guid == last_guid:
        print("No new entries found. Skipping...")
        print("::set-output name=has_new_content::false")
        sys.exit(0)
    
    # Extract HTML content
    html_content = extract_html_content(latest_entry)
    
    if not html_content:
        print("No HTML content found in entry")
        sys.exit(1)
    
    # Save HTML content with date prefix
    html_filename = f"output/{date_prefix}_issue.html"
    os.makedirs("output", exist_ok=True)
    with open(html_filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    # Save metadata
    metadata = {
        "title": latest_entry["title"],
        "link": latest_entry["link"],
        "guid": current_guid,
        "published": latest_entry["published"],
        "author": latest_entry["author"],
        "tags": latest_entry["tags"],
        "processed_at": datetime.now().isoformat(),
    }
    
    meta_filename = f"output/{date_prefix}_meta.json"
    with open(meta_filename, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    # Save the GUID for deduplication
    save_last_guid(current_guid)
    
    print(f"Successfully processed: {latest_entry['title']}")
    print(f"GUID: {current_guid}")
    print(f"Published: {latest_entry['published']}")
    print(f"Output files: {html_filename}, {meta_filename}")
    print("::set-output name=has_new_content::true")


if __name__ == "__main__":
    main()