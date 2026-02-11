from __future__ import annotations

from datetime import datetime
from pathlib import Path
import re
import random

POSTS_DIR = Path("_posts")

def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"-+", "-", text)
    return (text[:80].strip("-") or "post")

def connectors_body() -> str:
    items = [
        ("und", "Ich lerne Deutsch und ich mache Hausaufgaben."),
        ("aber", "Ich möchte kommen, aber ich habe keine Zeit."),
        ("oder", "Willst du Tee oder Kaffee?"),
        ("weil", "Ich bleibe zu Hause, weil ich müde bin."),
        ("deshalb", "Ich war krank, deshalb bin ich nicht gekommen."),
        ("trotzdem", "Es regnet, trotzdem gehe ich spazieren."),
        ("dann", "Ich frühstücke, dann gehe ich zur Arbeit."),
        ("zuerst … dann", "Zuerst lerne ich Vokabeln, dann übe ich Schreiben."),
        ("nicht nur … sondern auch", "Ich lerne nicht nur Wörter, sondern auch Grammatik."),
        ("wenn", "Wenn ich Zeit habe, übe ich jeden Tag."),
        ("dass", "Ich denke, dass Deutsch interessant ist."),
        ("zum Beispiel", "Ich mag Obst, zum Beispiel Äpfel und Bananen."),
    ]

    lines = [
        "Hier sind **12 nützliche Konnektoren (A2)** mit Beispielen, die du sofort in Briefen und Texten verwenden kannst:",
        ""
    ]
    for i, (w, ex) in enumerate(items, 1):
        lines.append(f"**{i}) {w}**")
        lines.append(f"- {ex}")
        lines.append("")

    lines += [
        "---",
        "## Mini-Übung (A2)",
        "Verbinde die Sätze mit einem passenden Konnektor:",
        "1) Ich lerne jeden Tag. Ich mache Fortschritte.",
        "2) Ich möchte Deutsch sprechen. Ich bin noch unsicher.",
        "3) Es ist spät. Ich schreibe noch eine Aufgabe.",
        "",
        "**Tipp:** Nutze *weil / deshalb / trotzdem / aber*.",
        "",
        "Want structured practice? Try **Falowen**: https://falowen.app",
    ]
    return "\n".join(lines).strip()

def build_post(title: str, excerpt: str, category: str, tags: list[str], image_url: str, body: str) -> str:
    today = datetime.utcnow().strftime("%Y-%m-%d")
    tag_string = ", ".join(tags)

    fm = [
        "---",
        "layout: post",
        f'title: "{title}"',
        f"date: {today}",
        f"tags: [{tag_string}]",
        f"categories: [{category}]",
        f'excerpt: "{excerpt}"',
        f"image: {image_url}",
        "---",
        "",
    ]
    return "\n".join(fm) + body + "\n"

def main() -> int:
    POSTS_DIR.mkdir(parents=True, exist_ok=True)

    # Simple weekly rotation pool (expand anytime)
    topics = [
        {
            "title": "A2: 12 Konnektoren mit Beispielen (für Briefe)",
            "excerpt": "12 Verbindungswörter, die deine A2-Texte sofort besser machen.",
            "category": "A2",
            "tags": ["falowen", "german", "a2", "writing"],
            "image": "https://images.unsplash.com/photo-1529070538774-1843cb3265df",
            "body": connectors_body(),
        }
    ]

    topic = random.choice(topics)

    today = datetime.utcnow().strftime("%Y-%m-%d")
    slug = slugify(topic["title"])
    filename = f"{today}-{slug}.md"
    path = POSTS_DIR / filename

    # Avoid duplicate file creation if rerun same day
    if path.exists():
        print(f"Post already exists: {path}")
        return 0

    md = build_post(
        title=topic["title"],
        excerpt=topic["excerpt"],
        category=topic["category"],
        tags=topic["tags"],
        image_url=topic["image"],
        body=topic["body"],
    )

    path.write_text(md, encoding="utf-8")
    print(f"Created: {path}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
