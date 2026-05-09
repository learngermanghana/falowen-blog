import unittest
from datetime import date

from scripts.generate_daily_calendar_post import (
    build_body,
    build_post,
    compute_day_number,
    pick_day_config,
    resolve_image_url,
)


class DailyCalendarPostTests(unittest.TestCase):
    def test_compute_day_number_uses_start_day_as_day_one(self) -> None:
        self.assertEqual(compute_day_number(date(2026, 4, 15), date(2026, 4, 15)), 1)
        self.assertEqual(compute_day_number(date(2026, 4, 16), date(2026, 4, 15)), 2)

    def test_pick_day_config_only_returns_in_180_day_range(self) -> None:
        day_1 = pick_day_config(1)
        self.assertIsNotNone(day_1)
        assert day_1 is not None
        self.assertEqual(day_1["content_type"], "promo_essay")
        self.assertIsNotNone(pick_day_config(30))
        self.assertIsNone(pick_day_config(0))
        day_31 = pick_day_config(31)
        self.assertIsNotNone(day_31)
        assert day_31 is not None
        self.assertEqual(day_31["slug"], day_1["slug"])
        self.assertIsNone(pick_day_config(181))

    def test_build_body_uses_content_type_specific_template(self) -> None:
        day_1 = pick_day_config(1)
        day_2 = pick_day_config(2)
        day_21 = pick_day_config(21)
        assert day_1 is not None
        assert day_2 is not None
        assert day_21 is not None

        body_1 = build_body(1, day_1)
        body_2 = build_body(2, day_2)
        body_21 = build_body(21, day_21)

        self.assertIn("Register now at Learn Language Education Academy", body_1)
        self.assertIn("**Rule:**", body_2)
        self.assertIn("**Common mistake:**", body_2)
        self.assertIn("1. **Start small and consistent**", body_21)
        self.assertIn("Day 21/180 CTA:", body_21)
        self.assertNotEqual(body_1, body_2)

    def test_resolve_image_url_falls_back_to_repo_image_for_unsplash_search_pages(self) -> None:
        day_2 = pick_day_config(2)
        assert day_2 is not None
        image_url = resolve_image_url(2, day_2)
        self.assertIn("raw.githubusercontent.com/learngermanghana/falowen-blog/main/photos/", image_url)

    def test_build_post_appends_level_test_and_standard_closing(self) -> None:
        day_1 = pick_day_config(1)
        assert day_1 is not None
        body = build_body(1, day_1)
        post_md = build_post(1, day_1, body, date(2026, 4, 15))
        self.assertIn("## Level", post_md)
        self.assertIn("## Quick Test", post_md)
        self.assertIn(
            "Are you interested learning german. check our available classes here https://www.learngermanghana.com/classes",
            post_md,
        )


if __name__ == "__main__":
    unittest.main()
