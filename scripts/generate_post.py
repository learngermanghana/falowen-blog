from __future__ import annotations

from datetime import datetime, date
from pathlib import Path
import re

POSTS_DIR = Path("_posts")

def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"-+", "-", text)
    return (text[:80].strip("-") or "post")

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
    return "\n".join(fm) + body.strip() + "\n"

# ---------- Topic Generators ----------

def a1_vocab_body() -> str:
    words = [
        ("der Alltag", "Ich beschreibe meinen Alltag."),
        ("frühstücken", "Ich frühstücke um 7 Uhr."),
        ("arbeiten", "Ich arbeite von Montag bis Freitag."),
        ("einkaufen", "Ich kaufe im Supermarkt ein."),
        ("kochen", "Am Abend koche ich Nudeln."),
        ("spazieren gehen", "Ich gehe gern spazieren."),
        ("lernen", "Ich lerne jeden Tag Deutsch."),
        ("schlafen", "Ich schlafe um 22 Uhr."),
    ]
    lines = [
        "Heute lernst du **A1-Wortschatz** zum Thema **Alltag**:",
        "",
        "## Wörter + Beispiele",
    ]
    for w, ex in words:
        lines.append(f"- **{w}**: {ex}")
    lines += [
        "",
        "---",
        "## Mini-Übung",
        "Schreibe 5 Sätze über deinen Alltag. Nutze mindestens 4 Wörter von oben.",
        "",
        "Want structured practice? Try **Falowen**: https://falowen.app",
    ]
    return "\n".join(lines)

def a2_connectors_body() -> str:
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
        "",
        "## Konnektoren + Beispiele",
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

def b1_opinion_body() -> str:
    phrases = [
        ("Meiner Meinung nach, ...", "Meiner Meinung nach ist Online-Lernen sehr praktisch."),
        ("Ich bin der Ansicht, dass ...", "Ich bin der Ansicht, dass Sport gesund ist."),
        ("Einerseits ..., andererseits ...", "Einerseits spart man Zeit, andererseits fehlt der Kontakt."),
        ("Außerdem ...", "Außerdem ist es oft günstiger."),
        ("Jedoch ...", "Jedoch braucht man Disziplin."),
        ("Zum Schluss ...", "Zum Schluss möchte ich sagen, dass Übung wichtig ist."),
    ]
    lines = [
        "Heute: **B1 Redemittel**, um deine Meinung klar auszudrücken.",
        "",
        "## Redemittel + Beispiele",
    ]
    for p, ex in phrases:
        lines.append(f"- **{p}** → {ex}")
    lines += [
        "",
        "---",
        "## Schreibaufgabe (B1)",
        "Thema: **Sollte man jeden Tag Deutsch lernen?** Schreibe 8–10 Sätze und nutze mindestens 4 Redemittel.",
        "",
        "Want structured practice? Try **Falowen**: https://falowen.app",
    ]
    return "\n".join(lines)

def b2_discussion_body() -> str:
    lines = [
        "Heute: **B2 Diskussionsthema** mit Leitfragen und Argumentationshilfen.",
        "",
        "## Thema: Künstliche Intelligenz im Alltag",
        "- Welche Vorteile hat KI für Lernen und Arbeit?",
        "- Welche Risiken gibt es (Datenschutz, Abhängigkeit, Fake News)?",
        "- Sollte KI in der Schule stärker eingesetzt werden?",
        "",
        "## Nützliche B2-Strukturen",
        "- **Es lässt sich feststellen, dass ...**",
        "- **Nicht zu unterschätzen ist, dass ...**",
        "- **Demgegenüber steht jedoch, dass ...**",
        "- **Zusammenfassend kann man sagen, dass ...**",
        "",
        "---",
        "## Aufgabe",
        "Schreibe 180–220 Wörter und baue mindestens 4 Strukturen ein.",
        "",
        "Want structured practice? Try **Falowen**: https://falowen.app",
    ]
    return "\n".join(lines)

# ---------- Rotation Logic ----------

def week_index_utc() -> int:
    # ISO week number (1..53) – stable weekly rotation
    return date.today().isocalendar().week

def get_topic_for_week() -> dict:
    topics = [
        {
            "title": "A1: Alltag – 8 wichtige Wörter mit Beispielen",
            "excerpt": "Lerne A1-Wortschatz zum Alltag und schreibe eigene Sätze.",
            "category": "A1",
            "tags": ["falowen", "german", "a1", "vocabulary"],
            "image": "https://images.unsplash.com/photo-1529070538774-1843cb3265df",
            "body": a1_vocab_body(),
        },
        {
            "title": "A2: 12 Konnektoren mit Beispielen (für Briefe)",
            "excerpt": "12 Verbindungswörter, die deine A2-Texte sofort besser machen.",
            "category": "A2",
            "tags": ["falowen", "german", "a2", "writing"],
            "image": "https://images.unsplash.com/photo-1529070538774-1843cb3265df",
            "body": a2_connectors_body(),
        },
        {
            "title": "B1: Meinung äußern – 6 Redemittel mit Beispielen",
            "excerpt": "B1-Sätze, um Pro/Contra klar zu formulieren.",
            "category": "B1",
            "tags": ["falowen", "german", "b1", "writing"],
            "image": "https://images.unsplash.com/photo-1529070538774-1843cb3265df",
            "body": b1_opinion_body(),
        },
        {
            "title": "B2: Diskussion – KI im Alltag (Aufgabe + Strukturen)",
            "excerpt": "B2-Thema mit Leitfragen und Strukturen für starke Argumente.",
            "category": "B2",
            "tags": ["falowen", "german", "b2", "discussion"],
            "image": "https://images.unsplash.com/photo-1529070538774-1843cb3265df",
            "body": b2_discussion_body(),
        },
    ]
    idx = (week_index_utc() - 1) % len(topics)
    return topics[idx]

def main() -> int:
    POSTS_DIR.mkdir(parents=True, exist_ok=True)

    topic = get_topic_for_week()

    today = datetime.utcnow().strftime("%Y-%m-%d")
    slug = slugify(topic["title"])
    filename = f"{today}-{slug}.md"
    path = POSTS_DIR / filename

    # If rerun same day, do nothing
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
