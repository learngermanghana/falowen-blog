"""Checks for the 50-cover Falowen Blog image library."""
import re
import unittest
from pathlib import Path
from xml.etree import ElementTree

from scripts.blog_image_library import (
    IMAGE_SLUGS,
    choose_cover,
    cover_path,
    verify_catalogue,
)
from scripts.generate_daily_calendar_post import pick_day_config, resolve_image_url

ROOT = Path(__file__).resolve().parents[1]


class BlogImageLibraryTests(unittest.TestCase):
    def test_all_50_distinct_local_covers_exist_and_are_valid_svg(self):
        self.assertEqual(len(IMAGE_SLUGS), 50)
        self.assertEqual(len(set(IMAGE_SLUGS)), 50)
        self.assertEqual(verify_catalogue(ROOT), [])
        for position in range(1, 51):
            path = ROOT / cover_path(position).lstrip("/")
            self.assertEqual(ElementTree.parse(path).getroot().tag, "{http://www.w3.org/2000/svg}svg")
            data = path.read_text(encoding="utf-8")
            self.assertIn("<text ", data, str(path))
            self.assertLess(len(data.encode("utf-8")), 150_000)

    def test_topic_selection_returns_relevant_rotating_covers(self):
        self.assertEqual(choose_cover("German Alphabet for Beginners"), cover_path(2))
        self.assertEqual(choose_cover("German Alphabet for Beginners", rotation=1), cover_path(5))
        self.assertEqual(choose_cover("How to Speak German", "Speaking"), cover_path(3))
        self.assertEqual(choose_cover("Falowen AI Tutor"), cover_path(34))
        self.assertTrue(choose_cover("A generic topic", "German Grammar").startswith("/assets/img/blog-library/"))

    def test_calendar_generator_uses_local_images_for_every_day(self):
        for day in range(1, 181):
            config = pick_day_config(day)
            self.assertIsNotNone(config)
            path = resolve_image_url(day, config)
            self.assertTrue(path.startswith("/assets/img/blog-library/"), (day, path))
            self.assertTrue((ROOT / path.lstrip("/")).is_file(), (day, path))

    def test_explicit_local_cover_is_respected(self):
        self.assertEqual(
            resolve_image_url(2, {"title": "Alphabet", "image_url": "/photos/approved-photo.jpg"}),
            "/photos/approved-photo.jpg",
        )

    def test_recently_affected_posts_have_distinct_local_covers(self):
        posts = [
            "2026-08-12-how-to-join-learn-language-education-academy-and-start-learning-german.md",
            "2026-08-19-german-numbers-1-to-20-made-easy.md",
            "2026-08-26-how-to-talk-about-your-family-in-german.md",
            "2026-09-02-5-mistakes-beginners-make-when-learning-german.md",
            "2026-09-09-how-to-talk-about-your-hobbies-in-german.md",
            "2026-09-16-20-basic-german-words-every-student-must-know.md",
            "2026-09-23-der-die-das-explained-simply.md",
            "2026-09-30-common-german-pronunciation-tips-for-beginners.md",
            "2026-10-07-how-falowen-supports-your-german-learning-journey.md",
            "2026-10-18-practise-goethe-german-exams-online-ai-falowen.md",
        ]
        seen = set()
        for post in posts:
            content = (ROOT / "_posts" / post).read_text(encoding="utf-8")
            match = re.search(r"^image:\s*(/assets/img/blog-library/[\w-]+\.svg)$", content, re.M)
            self.assertIsNotNone(match, post)
            image = match.group(1)
            self.assertNotIn(image, seen, post)
            self.assertTrue((ROOT / image.lstrip("/")).is_file(), post)
            self.assertRegex(content, r"(?m)^image_alt:\s*\S+")
            seen.add(image)


if __name__ == "__main__":
    unittest.main()
