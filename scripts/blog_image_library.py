"""Locally committed editorial images for Falowen Blog.

New automated posts always choose a topic-relevant local cover. The whole
catalogue is committed under assets/img/blog-library (no runtime image API).
"""
from __future__ import annotations

from pathlib import Path

IMAGE_SLUGS = (
    "01-ghana-german",
    "02-alphabet",
    "03-greetings",
    "04-introductions",
    "05-essential-vocabulary",
    "06-falowen-learning",
    "07-numbers",
    "08-days-of-week",
    "09-time",
    "10-simple-sentences",
    "11-academy",
    "12-articles",
    "13-common-verbs",
    "14-family",
    "15-classroom",
    "16-questions",
    "17-shopping",
    "18-online-study",
    "19-pronunciation",
    "20-daily-routine",
    "21-mistakes",
    "22-study-abroad",
    "23-exam-preparation",
    "24-travel",
    "25-letter-writing",
    "26-accusative",
    "27-dative",
    "28-speaking",
    "29-reading",
    "30-listening",
    "31-word-order",
    "32-hobbies",
    "33-music",
    "34-study-buddy",
    "35-connectors",
    "36-classes",
    "37-routine",
    "38-comparisons",
    "39-relative-clauses",
    "40-prepositions",
    "41-adjective-endings",
    "42-modal-verbs",
    "43-konjunktiv",
    "44-past-tense",
    "45-b1-writing",
    "46-a2-listening",
    "47-courses",
    "48-german-books",
    "49-learning-community",
    "50-grammar-practice",
)
IMAGE_BASE = "/assets/img/blog-library"

# Each theme has several suitable choices; recurring calendar articles rotate
# through the variants rather than showing the same default art every month.
TOPIC_IMAGES = (
    ("alphabet", (2, 5, 15)),
    ("greetings", (3, 28, 49)),
    ("introduce yourself", (4, 28, 3)),
    ("vocabulary", (5, 15, 17, 24)),
    ("german words", (5, 15, 17, 13)),
    ("numbers", (7, 10, 5)),
    ("days of the week", (8, 20, 37)),
    ("tell the time", (9, 20, 37)),
    ("simple sentences", (10, 31, 35)),
    ("academy", (11, 36, 47)),
    ("der, die, das", (12, 26, 27)),
    ("verbs", (13, 42, 44)),
    ("family", (14, 49, 28)),
    ("classroom", (15, 36, 11)),
    ("questions", (16, 3, 28)),
    ("shopping", (17, 24, 5)),
    ("online", (18, 6, 34)),
    ("pronunciation", (19, 28, 30)),
    ("daily routine", (20, 37, 9)),
    ("mistakes", (21, 50, 38)),
    ("study abroad", (22, 1, 47)),
    ("exam", (23, 29, 30, 45, 46)),
    ("travel", (24, 22, 17)),
    ("writing", (25, 45, 10)),
    ("accusative", (26, 40, 12)),
    ("dative", (27, 40, 12)),
    ("speaking", (28, 3, 4, 19)),
    ("lesen", (29, 23, 48)),
    ("hören", (30, 46, 33)),
    ("word order", (31, 35, 10)),
    ("hobbies", (32, 28, 49)),
    ("music", (33, 30, 19)),
    ("ai tutor", (34, 6, 18)),
    ("study buddy", (34, 6, 18)),
    ("connector", (35, 31, 39)),
    ("classes", (36, 11, 47)),
    ("relative clauses", (39, 31, 12)),
    ("prepositions", (40, 26, 27)),
    ("adjective", (41, 12, 50)),
    ("modal verbs", (42, 13, 31)),
    ("konjunktiv", (43, 38, 45)),
    ("perfekt", (44, 9, 10)),
    ("books", (48, 29, 5)),
    ("learning", (6, 18, 49, 47)),
)

CATEGORY_IMAGES = (
    ("vocabulary", (5, 13, 15, 17, 24)),
    ("grammar", (12, 26, 27, 31, 35, 39, 40, 41, 42, 50)),
    ("speaking", (3, 4, 14, 16, 28, 32)),
    ("exam", (23, 29, 30, 45, 46)),
    ("writing", (25, 31, 45)),
    ("academy", (11, 36, 47, 49)),
    ("falowen", (6, 18, 34, 47)),
)


def cover_path(number: int) -> str:
    """Return a repo-local SVG URL, using 1-based catalogue numbers."""
    if not 1 <= number <= len(IMAGE_SLUGS):
        raise ValueError(f"Invalid blog cover number: {number}")
    return f"{IMAGE_BASE}/{IMAGE_SLUGS[number - 1]}.svg"


def choose_cover(title: str, category: str = "", rotation: int = 0) -> str:
    """Choose a relevant, rotating cover without external image calls."""
    topic = title.casefold()
    for needle, choices in TOPIC_IMAGES:
        if needle in topic:
            return cover_path(choices[rotation % len(choices)])
    cat = category.casefold()
    for needle, choices in CATEGORY_IMAGES:
        if needle in cat:
            return cover_path(choices[rotation % len(choices)])
    return cover_path((rotation % len(IMAGE_SLUGS)) + 1)


def verify_catalogue(root: Path = Path(".")) -> list[str]:
    """Paths not present on disk; useful for the CI test."""
    return [
        str(root / cover_path(n).lstrip("/"))
        for n in range(1, len(IMAGE_SLUGS) + 1)
        if not (root / cover_path(n).lstrip("/")).is_file()
    ]
