#!/usr/bin/env python3
"""Create one dated, illustrated Falowen article per marketing calendar slot."""
from __future__ import annotations

import argparse
from datetime import date, datetime, timezone
import json
import os
from pathlib import Path
import re
from urllib import request

POSTS_DIR = Path("_posts")
API_URL = "https://api.openai.com/v1/chat/completions"
MODEL = "gpt-4.1-mini"

# Explicit dates prevent repeat posts and cap the trial at four weeks.
# Images are existing, repository-owned assets, verified before publishing.
# Product links are the public endpoints; never infer price, dates or eligibility.
CALENDAR = {
    "2026-11-03": {
        "title": "German A1: Mit, Bei and Zu Explained with Examples",
        "category": "German Grammar",
        "keyword": "German dative prepositions mit bei zu",
        "brief": "Teach mit, bei and zu (each followed by dative), clear use cases and six accurate examples with English translations. Include a short practice quiz.",
        "target": "https://www.falowen.app",
        "cta": "Practise dative prepositions in structured lessons on Falowen.",
        "image": "/assets/img/blog-library/27-dative.svg"
    },
    "2026-11-06": {
        "title": "How to Prepare for Goethe-Style German Exams Online",
        "category": "Exam Preparation",
        "keyword": "German exam practice online",
        "brief": "Give specific preparation tips for Lesen, Hören, Schreiben and Sprechen. Explain the difference between independent Goethe-style practice and an official Goethe exam; AI-assisted feedback is not an official score.",
        "target": "https://exams.falowen.app",
        "cta": "Explore Goethe-style practice on Falowen Exams.",
        "image": "/assets/img/blog-library/23-exam-preparation.svg"
    },
    "2026-11-10": {
        "title": "10 Useful German Phrases for Everyday Conversations",
        "category": "Speaking Practice",
        "keyword": "German phrases for daily conversations",
        "brief": "Teach ten useful A1 and A2 expressions with accurate German, English meanings and situations. Clarify when to use formal Sie and informal du.",
        "target": "https://www.falowen.app",
        "cta": "Develop everyday German skills with Falowen.",
        "image": "/assets/img/blog-library/05-essential-vocabulary.svg"
    },
    "2026-11-13": {
        "title": "Learn German with Music: Listening and Vocabulary Exercises",
        "category": "German Music",
        "keyword": "learn German with music",
        "brief": "Teach a simple 15-minute routine: listen, note new phrases, practise pronunciation, retell in original German sentences. Introduce Falowen Music without inventing songs, artists or commercial terms.",
        "target": "https://music.falowen.app",
        "cta": "Explore German-learning songs and listening practice on Falowen Music.",
        "image": "/assets/img/blog-library/33-music.svg"
    },
    "2026-11-17": {
        "title": "German A2: Perfekt vs Praeteritum Made Simple",
        "category": "German Grammar",
        "keyword": "Perfekt vs Präteritum German A2",
        "brief": "Compare Perfekt and Präteritum in speech and writing, with natural examples including war and hatte. Include six accurate German examples and a quick test.",
        "target": "https://www.falowen.app",
        "cta": "Practise A2 German grammar with Falowen.",
        "image": "/assets/img/blog-library/41-adjective-endings.svg"
    },
    "2026-11-20": {
        "title": "How to Study German Effectively with a Workbook",
        "category": "German Books",
        "keyword": "German language workbooks",
        "brief": "Provide a practical workbook routine covering explanation, exercises, error correction, and revision. Mention the Falowen book catalogue and only say digital and printed formats where available. Do not invent titles, stock or prices.",
        "target": "https://www.falowen.app/books",
        "cta": "Browse the current German book catalogue on Falowen.",
        "image": "/assets/img/blog-library/48-german-books.svg"
    },
    "2026-11-24": {
        "title": "Goethe-Style Speaking Practice: Five Mistakes to Avoid",
        "category": "Speaking Practice",
        "keyword": "German Sprechen practice",
        "brief": "Explain five common A1/A2 speaking-practice mistakes and their solutions, with short realistic original German dialogues. Do not imply official examination affiliation or guaranteed pass results.",
        "target": "https://exams.falowen.app",
        "cta": "Explore speaking and other exam-style exercises at Falowen Exams.",
        "image": "/assets/img/blog-library/28-speaking.svg"
    },
    "2026-11-27": {
        "title": "How to Choose Your Next German Class in Ghana or Online",
        "category": "German Classes",
        "keyword": "upcoming German classes in Ghana",
        "brief": "Explain how to choose A1, A2 or B1 and compare guided live classes with self-study. Do not invent registration deadlines, places, fees or start dates; direct readers to the live schedule.",
        "target": "https://www.falowen.app/classes",
        "cta": "Check current class options and start dates on the Falowen Classes page.",
        "image": "/assets/img/blog-library/36-classes.svg"
    },
}

def slugify(title: str) -> str:
    text = title.lower().replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", text)).strip("-")

def render_front_matter(publish_date: str, spec: dict[str, str], slug: str) -> str:
    title = spec["title"]
    excerpt = f"{title}. Clear examples and practical guidance for German learners."
    return (
        "---\n"
        "layout: post\n"
        f"title: {json.dumps(title, ensure_ascii=False)}\n"
        f"date: {publish_date}\n"
        f"categories: {json.dumps([spec['category']])}\n"
        f"tags: {json.dumps(['falowen', 'german', 'ecosystem-campaign'])}\n"
        f"excerpt: {json.dumps(excerpt, ensure_ascii=False)}\n"
        f"description: {json.dumps(excerpt, ensure_ascii=False)}\n"
        f"image: {spec['image']}\n"
        f"image_alt: {json.dumps('Falowen German learning: ' + title, ensure_ascii=False)}\n"
        f"permalink: /{slug}/\n"
        "---\n\n"
    )

def generate_article(spec: dict[str, str]) -> str:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key or api_key == "***":
        raise RuntimeError("OPENAI_API_KEY is not configured; stopping without creating an article.")
    prompt = (
        "Write an original, accurate 450–650 word educational blog article in markdown. "
        "Provide clear H2 headings, topic-specific accurate German examples with English meanings, "
        "a three-question practice activity and concrete study advice. Do not include a top-level "
        "Markdown H1, front matter, a final CTA, URLs or code fences; these are handled by the publisher. "
        "Write for learners in Ghana and beyond. Never fabricate prices, stock, students' testimonials, "
        "class start dates, product capabilities or partnership with Goethe-Institut. "
        "Keep educational value at least 80% of the article.\n\n"
        f"Title: {spec['title']}\nPrimary keyword: {spec['keyword']}\n"
        f"Editorial brief: {spec['brief']}"
    )
    body = json.dumps({
        "model": os.getenv("OPENAI_MODEL", MODEL).strip() or MODEL,
        "messages": [
            {"role": "system", "content": "You are a careful teacher of German as a foreign language writing for Falowen Blog."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.5,
    }).encode("utf-8")
    req = request.Request(
        API_URL,
        data=body,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    with request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    article = data["choices"][0]["message"]["content"].strip()
    if len(article) < 1400 or "## " not in article:
        raise RuntimeError("AI article did not meet the minimum quality checks; no post will be published.")
    return article

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", help="YYYY-MM-DD (default: today's UTC/Ghana date)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    today = date.fromisoformat(args.date) if args.date else datetime.now(timezone.utc).date()
    spec = CALENDAR.get(today.isoformat())
    if spec is None:
        print(f"No ecosystem post scheduled for {today.isoformat()}.")
        return 0

    image = Path(spec["image"].lstrip("/"))
    if not image.is_file():
        raise FileNotFoundError(f"Image missing: {image}")
    slug = slugify(spec["title"])
    output = POSTS_DIR / f"{today.isoformat()}-{slug}.md"
    if output.is_file():
        print(f"Already generated, skipping: {output}")
        return 0
    if args.dry_run:
        print(f"[dry-run] {today}: {spec['title']} -> {output}; image={image}; target={spec['target']}")
        return 0

    article = generate_article(spec)
    article += f"\n\n## Explore more with Falowen\n\n{spec['cta']}\n\n[Open Falowen]({spec['target']})\n"
    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    output.write_text(render_front_matter(today.isoformat(), spec, slug) + article, encoding="utf-8")
    print(f"Created illustrated article: {output}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
