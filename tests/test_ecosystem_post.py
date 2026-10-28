from __future__ import annotations

from datetime import date
from pathlib import Path
import unittest
from unittest.mock import patch

from scripts import generate_ecosystem_post as campaign


class EcosystemCalendarTests(unittest.TestCase):
    def test_calendar_is_eight_unique_tuesday_friday_slots(self) -> None:
        self.assertEqual(8, len(campaign.CALENDAR))
        dates = [date.fromisoformat(value) for value in campaign.CALENDAR]
        self.assertEqual(sorted(dates), dates)
        self.assertTrue(all(value.weekday() in (1, 4) for value in dates))

    def test_each_post_has_a_real_local_image_and_valid_cta(self) -> None:
        permitted_hosts = (
            "https://www.falowen.app",
            "https://exams.falowen.app",
            "https://music.falowen.app",
        )
        slugs = set()
        for post_date, spec in campaign.CALENDAR.items():
            self.assertTrue(spec["target"].startswith(permitted_hosts))
            self.assertTrue(Path(spec["image"].lstrip("/")).is_file(), post_date)
            self.assertIn(spec["image"].split(".")[-1].lower(), ("jpeg", "jpg", "png"))
            self.assertTrue(spec["cta"])
            slug = campaign.slugify(spec["title"])
            self.assertNotIn(slug, slugs)
            slugs.add(slug)
            metadata = campaign.render_front_matter(post_date, spec, slug)
            self.assertIn("image: /photos/", metadata)
            self.assertIn("permalink: /" + slug + "/", metadata)

    def test_no_generated_post_outside_explicit_dates(self) -> None:
        with patch.object(campaign, "POSTS_DIR", Path("/an/unused/directory")):
            with patch("sys.argv", ["generate_ecosystem_post.py", "--date", "2026-12-01"]):
                self.assertEqual(campaign.main(), 0)


if __name__ == "__main__":
    unittest.main()
