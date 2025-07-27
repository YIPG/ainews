#!/usr/bin/env python3
"""
Post translated newsletter summary to Twitter/X.
Extracts a short summary and posts with link to full article.
"""

import os
import sys
import re
from typing import Optional
import tweepy
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def is_quiet_day(content: str) -> bool:
    """
    Check if this is a "quiet day" newsletter with minimal content.
    """
    lines = content.strip().split('\n')
    
    # Check for quiet day indicators
    for line in lines[:10]:  # Check first 10 lines
        if '静かな一日' in line or 'quiet day' in line.lower():
            return True
    
    return False


def extract_tweet_summary(content: str, max_length: int = 100) -> str:
    """
    Extract a very short summary suitable for tweeting.
    Looks for the first major news item or key point.
    """
    lines = content.strip().split('\n')
    
    # Look for first bullet point or major news item
    found_content = False
    for i, line in enumerate(lines):
        line = line.strip()
        
        # Skip headers and metadata
        if line.startswith('#') or line.startswith('>') or not line:
            continue
            
        # Look for bullet points with actual news
        if line.startswith('- ') and '**' in line:
            # Extract the bold title
            match = re.search(r'\*\*([^*]+)\*\*', line)
            if match:
                title = match.group(1)
                # Clean up and return
                return title.strip()
        
        # Look for first substantial paragraph after headers
        if not found_content and len(line) > 30 and not line.startswith('['):
            found_content = True
            # Extract first sentence
            sentence_match = re.match(r'^([^。！？]+[。！？])', line)
            if sentence_match:
                summary = sentence_match.group(1)
            else:
                summary = line
            
            # Truncate if needed
            if len(summary) > max_length:
                if '、' in summary[:max_length-3]:
                    cut_point = summary[:max_length-3].rfind('、')
                    summary = summary[:cut_point] + '...'
                else:
                    summary = summary[:max_length-3] + '...'
            
            return summary
    
    # Fallback
    return "AIニュースレターの最新号を公開しました"


def post_tweet(message: str) -> bool:
    """Post a tweet using Twitter API v2."""
    try:
        # Get credentials from environment
        api_key = os.environ.get('TWITTER_API_KEY')
        api_secret = os.environ.get('TWITTER_API_SECRET')
        access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
        access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
        
        if not all([api_key, api_secret, access_token, access_token_secret]):
            print("Error: Twitter API credentials not found in environment")
            return False
        
        # Create client
        client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret
        )
        
        # Post tweet
        response = client.create_tweet(text=message)
        print(f"Tweet posted successfully: {response.data['id']}")
        return True
        
    except tweepy.TweepyException as e:
        print(f"Error posting tweet: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False


def main():
    """Main function to process translated file and post tweet."""
    if len(sys.argv) != 3:
        print("Usage: python tweet.py <translated_markdown_file> <date_prefix>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    date_prefix = sys.argv[2]
    
    try:
        # Read translated content
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if it's a quiet day
        if is_quiet_day(content):
            print("Quiet day detected - skipping tweet")
            sys.exit(0)
        
        # Extract summary
        summary = extract_tweet_summary(content)
        
        # Build tweet with URL
        url = f"https://yipg.github.io/ainews/newsletters/{date_prefix}.html"
        
        # Calculate available space for summary (140 - URL length - 1 space)
        # Twitter automatically shortens URLs to ~23 chars
        available_length = 140 - 24 - 1
        
        # Truncate summary if needed
        if len(summary) > available_length:
            summary = summary[:available_length-3] + '...'
        
        # Compose tweet
        tweet = f"{summary} {url}"
        
        print(f"Tweet ({len(tweet)} chars): {tweet}")
        
        # Post tweet
        if post_tweet(tweet):
            sys.exit(0)
        else:
            sys.exit(1)
            
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()