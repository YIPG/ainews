#!/usr/bin/env python3
"""
Translation script using Azure OpenAI.
Translates English markdown content to Japanese with quality checks.
"""

import os
import sys
import time

from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def load_translation_prompt() -> str:
    """Load the translation system prompt."""
    try:
        with open("prompts/translator.txt", "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        # Fallback prompt if file doesn't exist
        return """あなたはバイリンガル編集者です。入力はMarkdownの英語ニュースレターです。以下のルールで日本語に翻訳してください。
- 見出しは全角。
- 固有名詞・社名は原文のまま。
- 箇条書きはMarkdownのまま保持。
- 口語ではなく、ビジネス向けの丁寧体。"""


def create_azure_client() -> AzureOpenAI:
    """Create Azure OpenAI client."""
    endpoint = os.environ.get("AOAI_ENDPOINT")
    api_key = os.environ.get("AOAI_KEY")
    
    if not endpoint or not api_key:
        print("Error: AOAI_ENDPOINT and AOAI_KEY environment variables are required")
        sys.exit(1)
    
    return AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=api_key,
        api_version="2025-04-01-preview"
    )


def translate_with_retry(client: AzureOpenAI, content: str, system_prompt: str, max_retries: int = 3) -> str:
    """Translate content with exponential backoff retry."""
    deployment_name = os.environ.get("AOAI_DEPLOYMENT", "gpt4-1-translation")
    
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=deployment_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": content}
                ],
                temperature=0.2,
                max_tokens=16384,
                top_p=1.0,
                frequency_penalty=0,
                presence_penalty=0
            )
            
            translated_content = response.choices[0].message.content
            if not translated_content:
                raise Exception("Empty response from translation API")
            
            return translated_content.strip()
            
        except Exception as e:
            if "429" in str(e) and attempt < max_retries - 1:
                wait_time = 2 ** attempt
                print(f"Rate limit hit, waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
                continue
            else:
                print(f"Translation failed after {attempt + 1} attempts: {e}")
                sys.exit(1)
    
    print("Translation failed after all retries")
    sys.exit(1)


def quality_check(client: AzureOpenAI, original: str, translated: str) -> float:
    """Perform quality check on translation."""
    deployment_name = os.environ.get("AOAI_DEPLOYMENT", "gpt4-1-translation")
    
    quality_prompt = """あなたは翻訳品質評価の専門家です。以下の英語原文と日本語翻訳を比較して、翻訳品質を0.0から1.0のスコアで評価してください。

評価基準：
- 文章の欠落や追加がないか
- 意味が正確に伝わっているか
- 幻覚（hallucination）がないか
- 自然な日本語表現になっているか

0.95以上で高品質とします。数値のみで回答してください。

原文：
{original}

翻訳：
{translated}

スコア："""
    
    try:
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "user", "content": quality_prompt.format(original=original, translated=translated)}
            ],
            temperature=0.1,
            max_tokens=100
        )
        
        score_text = response.choices[0].message.content.strip()
        try:
            score = float(score_text)
            return score
        except ValueError:
            print(f"Invalid score format: {score_text}")
            return 0.0
            
    except Exception as e:
        print(f"Quality check failed: {e}")
        return 0.0


def read_markdown_file(file_path: str) -> str:
    """Read markdown content from file."""
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
    """Main function to translate markdown content."""
    if len(sys.argv) != 2:
        print("Usage: python translate.py <markdown_file>")
        print("Example: python translate.py 2024-01-15_issue.md")
        sys.exit(1)
    
    markdown_file = sys.argv[1]
    
    # Read markdown content
    content = read_markdown_file(markdown_file)
    
    if not content.strip():
        print("Error: Markdown file is empty")
        sys.exit(1)
    
    # Load translation prompt
    system_prompt = load_translation_prompt()
    
    # Create Azure OpenAI client
    client = create_azure_client()
    
    # Translate content
    print("Translating content...", file=sys.stderr)
    translated_content = translate_with_retry(client, content, system_prompt)
    
    # Output translated content
    print(translated_content)


if __name__ == "__main__":
    main()