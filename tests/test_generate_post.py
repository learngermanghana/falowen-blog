import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from scripts.generate_post import (
    build_post,
    dated_permalink_slug,
    topic_already_published,
)


class BuildPostTests(unittest.TestCase):
    def test_dated_permalink_slug_appends_publish_date(self) -> None:
        self.assertEqual(
            dated_permalink_slug("a2-german-connectors-writing-guide", "2026-03-22"),
            "a2-german-connectors-writing-guide-2026-03-22",
        )

    def test_build_post_uses_category_argument(self) -> None:
        md = build_post(
            title="Test title",
            excerpt="Test excerpt",
            category="Guides",
            tags=["falowen", "german"],
            image_url="https://example.com/image.jpg",
            image_alt="alt text",
            permalink_slug="test-title",
            seo_title="SEO title",
            seo_description="SEO description",
            body="Body text",
            publish_date="2026-02-16",
        )

        self.assertIn("categories: [Guides]", md)

    def test_build_post_uses_explicit_parameters_for_front_matter(self) -> None:
        md = build_post(
            title="A title",
            excerpt="Custom excerpt",
            category="News",
            tags=["a", "b"],
            image_url="https://example.com/custom-image.jpg",
            image_alt="custom alt",
            permalink_slug="custom-slug",
            seo_title="Custom SEO title",
            seo_description="Custom SEO description",
            body="  Main body text  ",
            publish_date="2026-02-16",
        )

        self.assertIn('excerpt: "Custom excerpt"', md)
        self.assertIn("image: https://example.com/custom-image.jpg", md)
        self.assertIn('image_alt: "custom alt"', md)
        self.assertIn("permalink: /custom-slug/", md)
        self.assertIn('  title: "Custom SEO title"', md)
        self.assertIn('  description: "Custom SEO description"', md)
        self.assertTrue(md.endswith("Main body text\n"))

    def test_topic_already_published_detects_dated_or_base_permalink(self) -> None:
        with TemporaryDirectory() as tmp_dir:
            posts_dir = Path(tmp_dir)
            existing = posts_dir / "2026-02-23-a1-daily-vocabulary.md"
            existing.write_text(
                "---\n"
                'title: "A1: Daily Vocabulary with Examples and Mini Routines"\n'
                "permalink: /a1-daily-vocabulary-guide-2026-02-23/\n"
                "---\n",
                encoding="utf-8",
            )

            with patch("scripts.generate_post.POSTS_DIR", posts_dir):
                found = topic_already_published(
                    "a1-daily-vocabulary-guide",
                    "A1: Daily Vocabulary with Examples and Mini Routines",
                )

            self.assertEqual(found, existing)

    def test_topic_already_published_returns_none_for_new_topic(self) -> None:
        with TemporaryDirectory() as tmp_dir:
            posts_dir = Path(tmp_dir)
            (posts_dir / "2026-02-23-a1-daily-vocabulary.md").write_text(
                "---\n"
                'title: "A1: Daily Vocabulary with Examples and Mini Routines"\n'
                "permalink: /a1-daily-vocabulary-guide-2026-02-23/\n"
                "---\n",
                encoding="utf-8",
            )

            with patch("scripts.generate_post.POSTS_DIR", posts_dir):
                found = topic_already_published(
                    "b2-discussion-writing-ai-guide",
                    "B2: Write Discussions About AI with Precise Arguments",
                )

            self.assertIsNone(found)


if __name__ == "__main__":
    unittest.main()
