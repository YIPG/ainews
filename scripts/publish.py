#!/usr/bin/env python3
"""
Buttondown API publishing script.
Publishes rendered email content to Buttondown.
"""

import argparse
import os
import sys
from typing import Dict, Any, Optional

import requests


def read_email_content(file_path: str) -> str:
    """Read email content from file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: Email file '{file_path}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading email file: {e}")
        sys.exit(1)


def publish_to_buttondown(content: str, api_key: str, draft: bool = False) -> Dict[str, Any]:
    """Publish email to Buttondown API."""
    api_url = "https://api.buttondown.email/v1/emails"
    
    headers = {
        "Authorization": f"Token {api_key}",
        "Content-Type": "application/json",
    }
    
    # Extract title from first line of content
    lines = content.strip().split("\n")
    title = lines[0].strip() if lines else "AI Newsletter"
    
    # Prepare API payload
    payload = {
        "subject": title,
        "body": content,
        "status": "draft" if draft else "published",
        "email_type": "public",
    }
    
    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.json()
        
    except requests.exceptions.HTTPError as e:
        if response.status_code == 401:
            print("Error: Invalid API key")
        elif response.status_code == 400:
            print(f"Error: Bad request - {response.text}")
        else:
            print(f"Error: HTTP {response.status_code} - {response.text}")
        sys.exit(1)
        
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
        sys.exit(1)


def send_slack_notification(webhook_url: str, message: str) -> None:
    """Send notification to Slack."""
    try:
        payload = {"text": message}
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
    except Exception as e:
        print(f"Warning: Failed to send Slack notification: {e}")


def main() -> None:
    """Main function to publish email."""
    parser = argparse.ArgumentParser(description="Publish email to Buttondown")
    parser.add_argument("email_file", help="Path to email HTML file")
    parser.add_argument("--draft", action="store_true", help="Publish as draft")
    
    args = parser.parse_args()
    
    # Get API key from environment
    api_key = os.environ.get("BD_API_KEY")
    if not api_key:
        print("Error: BD_API_KEY environment variable is required")
        sys.exit(1)
    
    # Read email content
    content = read_email_content(args.email_file)
    
    if not content.strip():
        print("Error: Email file is empty")
        sys.exit(1)
    
    # Publish to Buttondown
    print(f"Publishing to Buttondown ({'draft' if args.draft else 'live'})...")
    result = publish_to_buttondown(content, api_key, draft=args.draft)
    
    print(f"Successfully published!")
    print(f"Email ID: {result.get('id', 'N/A')}")
    print(f"Status: {result.get('status', 'N/A')}")
    print(f"URL: {result.get('url', 'N/A')}")
    
    # Send Slack notification on success (if webhook is configured)
    slack_webhook = os.environ.get("SLACK_WEBHOOK")
    if slack_webhook and not args.draft:
        subject = result.get("subject", "AI Newsletter")
        send_slack_notification(
            slack_webhook,
            f"✅ Japanese AI Newsletter published successfully: {subject}"
        )


if __name__ == "__main__":
    main()