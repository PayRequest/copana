#!/usr/bin/env python3
"""
News Briefing — Relevant news from RSS feeds.

Fetches and scores news by relevance to your interests.
Configurable via FEEDS dict or NEWS_FEEDS env var.

Can run standalone or be called from morning_briefing.py.
"""

import os
import sys
import requests
import feedparser
from pathlib import Path
from datetime import datetime

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / '.env')

sys.path.insert(0, str(Path(__file__).parent))
from copana_utils import send_notification, log

# Default feeds — customize these for your interests
FEEDS = {
    "Tech": [
        "https://hnrss.org/best?count=5",
    ],
    "AI": [
        "https://techcrunch.com/category/artificial-intelligence/feed/",
    ],
}

# Override with env var: comma-separated URLs
custom_feeds = os.getenv('NEWS_FEEDS', '')
if custom_feeds:
    FEEDS = {"News": [url.strip() for url in custom_feeds.split(',') if url.strip()]}

# Keywords to boost (stories matching these rank higher)
BOOST_KEYWORDS = [
    "ai", "claude", "anthropic", "openai", "startup", "saas", "indie",
]

# Keywords to skip
SKIP_KEYWORDS = [
    "sports", "celebrity", "entertainment", "kardashian",
]

MAX_ITEMS = 8


def fetch_feed(url, timeout=10):
    """Fetch and parse an RSS feed."""
    try:
        response = requests.get(url, timeout=timeout, headers={
            "User-Agent": "Copana/1.0 (personal news aggregator)"
        })
        feed = feedparser.parse(response.content)
        return feed.entries[:5]
    except Exception as e:
        print(f"  Error fetching {url}: {e}")
        return []


def score_item(item):
    """Score a news item by relevance."""
    text = f"{item.get('title', '')} {item.get('summary', '')}".lower()

    for kw in SKIP_KEYWORDS:
        if kw in text:
            return -1

    score = 0
    for kw in BOOST_KEYWORDS:
        if kw in text:
            score += 2

    # Recency boost
    published = item.get("published_parsed") or item.get("updated_parsed")
    if published:
        try:
            pub_date = datetime(*published[:6])
            hours_ago = (datetime.now() - pub_date).total_seconds() / 3600
            if hours_ago < 12:
                score += 2
            elif hours_ago < 24:
                score += 1
        except (TypeError, ValueError):
            pass

    return score


def get_news(max_items=MAX_ITEMS):
    """Fetch and rank news from all feeds."""
    all_items = []

    for category, urls in FEEDS.items():
        for url in urls:
            entries = fetch_feed(url)
            for entry in entries:
                score = score_item(entry)
                if score < 0:
                    continue

                title = entry.get("title", "").strip()
                if len(title) > 80:
                    title = title[:77] + "..."

                all_items.append({
                    "category": category,
                    "title": title,
                    "link": entry.get("link", ""),
                    "score": score,
                })

    # Sort by score, deduplicate
    seen = set()
    result = []
    for item in sorted(all_items, key=lambda x: x["score"], reverse=True):
        key = item["title"].lower()[:50]
        if key not in seen:
            seen.add(key)
            result.append(item)
            if len(result) >= max_items:
                break

    return result


def format_news(items, include_links=False):
    """Format news items for display."""
    if not items:
        return "NEWS: Nothing relevant today\n"

    msg = "NEWS:\n"
    current_cat = None
    for item in items:
        if item["category"] != current_cat:
            current_cat = item["category"]
            msg += f"\n{current_cat}\n"
        msg += f"  - {item['title']}\n"
        if include_links and item.get("link"):
            msg += f"    {item['link']}\n"

    return msg


def get_news_for_briefing():
    """Called by morning_briefing.py — returns formatted section."""
    items = get_news(max_items=5)
    return format_news(items)


def main():
    """Run standalone — fetch and display/send news."""
    print("Fetching news...")
    items = get_news()
    message = format_news(items, include_links=True)
    print(message)

    if "--send" in sys.argv:
        if send_notification(message):
            print("\nSent!")
        else:
            print("\nFailed to send (check .env)")
    else:
        print("\n(Use --send to send notification)")


if __name__ == "__main__":
    main()
