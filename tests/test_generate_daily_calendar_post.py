import unittest
from datetime import date

from scripts.generate_daily_calendar_post import (
    build_body,
    compute_day_number,
    pick_day_config,
)


class DailyCalendarPostTests(unittest.TestCase):
    def test_compute_day_number_uses_start_day_as_day_one(self) -> None:
        self.assertEqual(compute_day_number(date(2026, 4, 15), date(2026, 4, 15)), 1)
        self.assertEqual(compute_day_number(date(2026, 4, 16), date(2026, 4, 15)), 2)

    def test_pick_day_config_only_returns_in_30_day_range(self) -> None:
        self.assertIsNotNone(pick_day_config(1))
        self.assertIsNotNone(pick_day_config(30))
        self.assertIsNone(pick_day_config(0))
        self.assertIsNone(pick_day_config(31))

    def test_build_body_contains_unique_daily_message(self) -> None:
        day_1 = pick_day_config(1)
        day_2 = pick_day_config(2)
        assert day_1 is not None
        assert day_2 is not None

        body_1 = build_body(1, day_1)
        body_2 = build_body(2, day_2)

        self.assertIn("Day 1/30 reminder", body_1)
        self.assertIn("Day 2/30 reminder", body_2)
        self.assertIn("## Reading lesson (short and practical)", body_1)
        self.assertIn("## Mini examples you can copy", body_1)
        self.assertIn("## 5-minute revision plan", body_1)
        self.assertNotEqual(body_1, body_2)


if __name__ == "__main__":
    unittest.main()
