import unittest
from unittest.mock import patch

from scripts.generate_repo_update_story import build_story_body, normalize_commit


class GenerateRepoUpdateStoryTests(unittest.TestCase):
    @patch("scripts.generate_repo_update_story.fetch_commit_details")
    def test_normalize_commit_extracts_message_and_changed_files(self, mock_fetch_details) -> None:
        mock_fetch_details.return_value = {
            "files": [
                {
                    "filename": "src/trainer/session.py",
                    "status": "modified",
                    "additions": 12,
                    "deletions": 3,
                },
                {
                    "filename": "README.md",
                    "status": "added",
                    "additions": 25,
                    "deletions": 0,
                },
            ]
        }

        item = {
            "sha": "abcdef1234567890",
            "html_url": "https://github.com/x/y/commit/abcdef",
            "commit": {
                "message": "feat: add streak tracker\n\nextra details",
                "author": {"name": "Falowen Bot", "date": "2026-03-15T12:30:00Z"},
            },
        }

        normalized = normalize_commit(item, max_files=1)

        self.assertEqual(normalized["message"], "feat: add streak tracker")
        self.assertEqual(normalized["short_sha"], "abcdef1")
        self.assertEqual(normalized["author"], "Falowen Bot")
        self.assertEqual(len(normalized["changed_files"]), 1)
        self.assertEqual(normalized["changed_files"][0]["filename"], "src/trainer/session.py")

    def test_build_story_body_lists_commit_and_file_highlights(self) -> None:
        body = build_story_body(
            [
                {
                    "message": "feat: improve writing trainer feedback",
                    "date": "2026-03-15T09:00:00Z",
                    "author": "Maintainer",
                    "sha": "123456789",
                    "short_sha": "1234567",
                    "url": "https://github.com/example/commit/1234567",
                    "changed_files": [
                        {
                            "filename": "docs/guide.md",
                            "status": "modified",
                            "additions": 10,
                            "deletions": 2,
                        }
                    ],
                }
            ]
        )

        self.assertIn("## Commit highlights", body)
        self.assertIn("feat: improve writing trainer feedback", body)
        self.assertIn("`1234567`", body)
        self.assertIn("`docs/guide.md`", body)


if __name__ == "__main__":
    unittest.main()
