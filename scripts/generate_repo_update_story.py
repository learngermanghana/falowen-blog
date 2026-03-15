from __future__ import annotations

import argparse
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib import error, request

from scripts.generate_post import build_post, slugify

POSTS_DIR = Path("_posts")
TARGET_REPO = "learngermanghana/falowenexamtrainer"
COMMITS_API = f"https://api.github.com/repos/{TARGET_REPO}/commits"
UNSPLASH_IMAGE_URL = "https://source.unsplash.com/1600x900/?education,technology,software"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a blog story from the latest updates in falowenexamtrainer."
    )
    parser.add_argument("--date", help="Publishing date in YYYY-MM-DD format (default: current UTC date).")
    parser.add_argument("--limit", type=int, default=5, help="How many recent commits to include.")
    parser.add_argument("--max-files-per-commit", type=int, default=3, help="How many changed files to show per commit.")
    parser.add_argument("--dry-run", action="store_true", help="Print details without creating a file.")
    return parser.parse_args()


def resolve_publish_date(raw_date: str | None) -> str:
    if raw_date is None:
        return datetime.utcnow().strftime("%Y-%m-%d")
    datetime.strptime(raw_date, "%Y-%m-%d")
    return raw_date


def github_headers() -> dict[str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "falowen-blog-bot",
    }
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def request_json(url: str) -> Any:
    req = request.Request(url, headers=github_headers())
    try:
        with request.urlopen(req, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))
    except error.URLError as exc:
        raise RuntimeError(f"Unable to fetch GitHub data from {url}: {exc}") from exc


def fetch_recent_commits(limit: int) -> list[dict[str, Any]]:
    commits = request_json(f"{COMMITS_API}?per_page={limit}")
    if not isinstance(commits, list):
        raise RuntimeError("Unexpected GitHub API response for commits.")
    return commits


def fetch_commit_details(sha: str) -> dict[str, Any]:
    details = request_json(f"{COMMITS_API}/{sha}")
    if not isinstance(details, dict):
        raise RuntimeError(f"Unexpected GitHub API response for commit {sha}.")
    return details


def normalize_commit(commit_item: dict[str, Any], max_files: int) -> dict[str, Any]:
    message = commit_item.get("commit", {}).get("message", "").strip()
    first_line = message.splitlines()[0] if message else "Update"
    commit_date = commit_item.get("commit", {}).get("author", {}).get("date", "")
    author = commit_item.get("commit", {}).get("author", {}).get("name", "Unknown")
    sha = commit_item.get("sha", "")
    url = commit_item.get("html_url", "")

    details = fetch_commit_details(sha)
    files = details.get("files", []) if isinstance(details.get("files", []), list) else []
    changed_files = []
    for file_item in files[:max_files]:
        filename = file_item.get("filename", "unknown")
        status = file_item.get("status", "modified")
        additions = int(file_item.get("additions", 0))
        deletions = int(file_item.get("deletions", 0))
        changed_files.append(
            {
                "filename": filename,
                "status": status,
                "additions": additions,
                "deletions": deletions,
            }
        )

    return {
        "message": first_line,
        "date": commit_date,
        "author": author,
        "sha": sha,
        "short_sha": sha[:7],
        "url": url,
        "changed_files": changed_files,
    }


def clean_commit_message(message: str) -> str:
    lowered = message.lower()
    prefixes = ["feat:", "fix:", "chore:", "refactor:", "docs:", "test:"]
    for prefix in prefixes:
        if lowered.startswith(prefix):
            return message[len(prefix):].strip().capitalize()
    return message


def build_story_body(commits: list[dict[str, Any]]) -> str:
    lines = [
        "## Latest product updates in simple words",
        "",
        "Here is a quick summary of what changed recently in Falowen Exam Trainer.",
        "",
        f"Source: https://github.com/{TARGET_REPO}",
        "",
        "---",
        "",
        "## What is new",
        "",
    ]

    for item in commits:
        date_fragment = item["date"][:10] if item["date"] else "unknown date"
        short_message = clean_commit_message(item["message"])
        lines.append(f"- **{short_message}**")
        lines.append(f"  By {item['author']} on {date_fragment} ([view update]({item['url']}))")
        if item["changed_files"]:
            lines.append("  Main areas updated:")
            for changed in item["changed_files"]:
                lines.append(f"  - `{changed['filename']}`")

    lines.extend(
        [
            "",
            "---",
            "",
            "## Why this helps learners",
            "",
            "These updates improve how learners study, practice, and track progress. "
            "You can quickly see what is getting better each week.",
        ]
    )
    return "\n".join(lines) + "\n"


def story_already_exists(path: Path, permalink_slug: str, latest_sha: str) -> bool:
    if path.exists():
        print(f"Story already exists for today: {path}")
        return True

    for post_file in POSTS_DIR.glob("*.md"):
        content = post_file.read_text(encoding="utf-8")
        if f"permalink: /{permalink_slug}/" in content:
            print(f"Story already exists for latest commit ({latest_sha}): {post_file}")
            return True

    return False


def main() -> int:
    args = parse_args()
    publish_date = resolve_publish_date(args.date)
    POSTS_DIR.mkdir(parents=True, exist_ok=True)

    recent = fetch_recent_commits(args.limit)
    if not recent:
        print("No recent commits returned; skipping.")
        return 0

    commits = [normalize_commit(item, args.max_files_per_commit) for item in recent]
    latest_sha = commits[0]["short_sha"]
    title = f"Falowen Exam Trainer Update: {latest_sha}"
    permalink_slug = f"falowen-exam-trainer-update-{latest_sha}"
    filename = f"{publish_date}-{slugify(title)}.md"
    path = POSTS_DIR / filename

    if story_already_exists(path, permalink_slug, latest_sha):
        return 0

    markdown = build_post(
        title=title,
        excerpt="Simple weekly summary of the latest Falowen Exam Trainer updates.",
        category="Product Updates",
        tags=["falowen", "examtrainer", "github", "updates", "automation"],
        image_url=UNSPLASH_IMAGE_URL,
        image_alt="Unsplash photo symbolizing software updates and learning technology",
        permalink_slug=permalink_slug,
        seo_title=title,
        seo_description="Read a simple weekly summary of the latest Falowen Exam Trainer improvements.",
        body=build_story_body(commits),
        publish_date=publish_date,
    )

    if args.dry_run:
        print(f"[dry-run] Would create: {path}")
        print(f"[dry-run] Title: {title}")
        return 0

    path.write_text(markdown, encoding="utf-8")
    print(f"Created: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
