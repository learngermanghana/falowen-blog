import unittest

from scripts.generate_post import build_post


class BuildPostTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
