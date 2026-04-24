#!/usr/bin/env python3
"""
The Busbar — News Fetcher

Fetches content from the source pool (sources.json) for the last 7 days.
Outputs raw article data as JSON for the AI agent to curate.

Strategy:
1. RSS feeds as primary source (fast, structured)
2. Web scraping as fallback for sources without RSS
3. curl fallback on connection issues
4. Filters to last 7 days (weekly cadence)
"""

import json
import re
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from typing import Optional
from dataclasses import dataclass, field, asdict
from pathlib import Path

import feedparser
import requests
from bs4 import BeautifulSoup
from dateutil import parser as dateutil_parser


SOURCES_FILE = Path(__file__).parent / "sources.json"


@dataclass
class Article:
    title: str
    url: str
    source: str
    category: str
    tier: str
    published: Optional[datetime] = None
    summary: str = ""


def load_sources() -> list[dict]:
    with open(SOURCES_FILE) as f:
        data = json.load(f)
    sources = []
    for tier, items in data.items():
        for item in items:
            item["tier"] = tier
            sources.append(item)
    return sources


def fetch_url(url: str, timeout: int = 30) -> Optional[str]:
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        resp = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
        if resp.status_code == 200 and len(resp.text) > 100:
            return resp.text
        print(f"  [requests] Status {resp.status_code} for {url}", file=sys.stderr)
    except Exception as e:
        print(f"  [requests] Error for {url}: {e}", file=sys.stderr)

    try:
        print(f"  [curl] Fallback for {url}...", file=sys.stderr)
        result = subprocess.run(
            ["curl", "-sL", "-H", "User-Agent: Mozilla/5.0", "--max-time", str(timeout), url],
            capture_output=True, text=True, timeout=timeout + 5
        )
        if result.returncode == 0 and len(result.stdout) > 100:
            return result.stdout
    except Exception as e:
        print(f"  [curl] Error for {url}: {e}", file=sys.stderr)

    return None


def parse_date(date_str: str) -> Optional[datetime]:
    if not date_str:
        return None
    try:
        dt = dateutil_parser.parse(date_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except (ValueError, TypeError):
        return None


def is_within_window(dt: Optional[datetime], cutoff: datetime) -> bool:
    if dt is None:
        return False
    try:
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt >= cutoff
    except Exception:
        return False


def parse_rss_feed(content: str, source: dict, cutoff: datetime) -> list[Article]:
    articles = []
    feed = feedparser.parse(content)

    for entry in feed.entries:
        date_str = entry.get("published") or entry.get("updated") or entry.get("created")
        pub_date = parse_date(date_str)

        if not is_within_window(pub_date, cutoff):
            continue

        title = entry.get("title", "").strip()
        link = entry.get("link", "").strip()

        summary = ""
        if entry.get("summary"):
            soup = BeautifulSoup(entry.summary, "html.parser")
            summary = soup.get_text(separator=" ", strip=True)[:500]

        if title and link:
            articles.append(Article(
                title=title,
                url=link,
                source=source["name"],
                category=source.get("category", ""),
                tier=source.get("tier", ""),
                published=pub_date,
                summary=summary,
            ))

    return articles


def parse_generic_web(content: str, source: dict, cutoff: datetime) -> list[Article]:
    articles = []
    soup = BeautifulSoup(content, "lxml")
    seen_urls = set()

    for item in soup.select("article a[href], .post a[href], h2 a[href], h3 a[href]"):
        title = item.get_text(strip=True)
        if not title or len(title) < 10:
            continue

        href = item.get("href", "")
        if not href:
            continue

        base = source["url"].split("/")[0] + "//" + source["url"].split("/")[2]
        url = href if href.startswith("http") else base + href

        if url in seen_urls:
            continue
        seen_urls.add(url)

        articles.append(Article(
            title=title,
            url=url,
            source=source["name"],
            category=source.get("category", ""),
            tier=source.get("tier", ""),
            published=None,
            summary="",
        ))

    return articles


def deduplicate(articles: list[Article]) -> list[Article]:
    seen_urls = set()
    seen_titles = set()
    unique = []

    for a in articles:
        normalized_url = a.url.rstrip("/").lower()
        normalized_title = a.title.lower().strip()

        if normalized_url in seen_urls:
            continue
        if normalized_title in seen_titles:
            continue

        seen_urls.add(normalized_url)
        seen_titles.add(normalized_title)
        unique.append(a)

    return unique


def fetch_all_news(max_age_days: int = 7, tiers: list[str] = None) -> list[Article]:
    if tiers is None:
        tiers = ["tier_a", "tier_b"]

    cutoff = datetime.now(timezone.utc) - timedelta(days=max_age_days)
    all_articles: list[Article] = []
    stats = {"success": 0, "failed": 0}

    print(f"\n{'='*60}", file=sys.stderr)
    print(f"The Busbar Fetcher — articles since {cutoff.strftime('%Y-%m-%d')}", file=sys.stderr)
    print(f"{'='*60}\n", file=sys.stderr)

    sources = [s for s in load_sources() if s.get("tier") in tiers]

    for source in sources:
        if source.get("type") not in ("rss", "web"):
            continue
        # Skip non-feed sources (youtube, recall portals — handled manually by agent)
        if source.get("category") in ("youtube", "recall", "standards", "trade_show"):
            continue

        print(f"[{source['name']}] Fetching...", file=sys.stderr)
        content = fetch_url(source["url"])

        if not content:
            print(f"  FAILED\n", file=sys.stderr)
            stats["failed"] += 1
            continue

        try:
            if source["type"] == "rss":
                articles = parse_rss_feed(content, source, cutoff)
            else:
                articles = parse_generic_web(content, source, cutoff)

            all_articles.extend(articles)
            stats["success"] += 1
            print(f"  OK — {len(articles)} articles in last {max_age_days} days\n", file=sys.stderr)

        except Exception as e:
            print(f"  PARSE ERROR: {e}\n", file=sys.stderr)
            stats["failed"] += 1

    all_articles = deduplicate(all_articles)
    all_articles.sort(
        key=lambda a: a.published or datetime.min.replace(tzinfo=timezone.utc),
        reverse=True
    )

    print(f"\n{'='*60}", file=sys.stderr)
    print(f"Result: {len(all_articles)} unique articles", file=sys.stderr)
    print(f"Sources: {stats['success']} OK, {stats['failed']} failed", file=sys.stderr)
    print(f"{'='*60}\n", file=sys.stderr)

    return all_articles


def format_output(articles: list[Article], output_format: str = "text") -> str:
    if output_format == "json":
        data = []
        for a in articles:
            d = asdict(a)
            d["published"] = a.published.isoformat() if a.published else None
            data.append(d)
        return json.dumps(data, indent=2, ensure_ascii=False)

    lines = []
    lines.append(f"# The Busbar — Raw Feed — Last 7 Days")
    lines.append(f"# Run: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append(f"# Count: {len(articles)} articles")
    lines.append("")

    current_tier = None
    for a in articles:
        if a.tier != current_tier:
            current_tier = a.tier
            lines.append(f"\n## {current_tier.upper()}\n")

        date_str = a.published.strftime("%Y-%m-%d") if a.published else "date unknown"
        lines.append(f"### [{a.source}] {a.title}")
        lines.append(f"    Date:     {date_str}")
        lines.append(f"    Category: {a.category}")
        lines.append(f"    URL:      {a.url}")
        if a.summary:
            lines.append(f"    {a.summary[:200]}...")
        lines.append("")

    return "\n".join(lines)


def main():
    import argparse

    ap = argparse.ArgumentParser(description="The Busbar — Fetch DC electrical news for the last N days")
    ap.add_argument("--days", type=int, default=10, help="Max age in days (default: 10 — covers weekend lag and slow-publishing sources)")
    ap.add_argument("--tiers", type=str, default="tier_a,tier_b", help="Comma-separated tiers to scan")
    ap.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    ap.add_argument("--output", type=str, default=None, help="Output file (default: stdout)")
    args = ap.parse_args()

    tiers = [t.strip() for t in args.tiers.split(",")]
    articles = fetch_all_news(max_age_days=args.days, tiers=tiers)
    result = format_output(articles, output_format=args.format)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"Output written to {args.output}", file=sys.stderr)
    else:
        print(result)


if __name__ == "__main__":
    main()
