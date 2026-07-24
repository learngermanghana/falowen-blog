import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from scripts.post_to_social import main, post_url, publish_linkedin


class PublishLinkedInTests(unittest.TestCase):
    @patch.dict(
        "os.environ",
        {
            "LINKEDIN_ACCESS_TOKEN": "token",
            "LINKEDIN_AUTHOR_URN": "urn:li:person:author",
        },
        clear=True,
    )
    def test_publish_linkedin_uses_linkedin_author_urn(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            publish_linkedin("Hello world", "https://example.com/post", dry_run=True)

        self.assertIn("[linkedin] Dry run: would publish post", output.getvalue())

    @patch.dict(
        "os.environ",
        {
            "LINKEDIN_ACCESS_TOKEN": "token",
            "LINKEDIN_AUTHOR_URN": "urn:li:person:author",
        },
        clear=True,
    )
    @patch("scripts.post_to_social.post_json")
    def test_publish_linkedin_sends_publish_request(self, mock_post_json) -> None:
        mock_post_json.return_value = (201, '{"id":"123"}')

        publish_linkedin("New post", "https://example.com/post", dry_run=False)

        mock_post_json.assert_called_once_with(
            "https://api.linkedin.com/v2/ugcPosts",
            {
                "author": "urn:li:person:author",
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": "New post\n\nRead more: https://example.com/post"
                        },
                        "shareMediaCategory": "NONE",
                    }
                },
                "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
            },
            {
                "Authorization": "Bearer token",
                "X-Restli-Protocol-Version": "2.0.0",
            },
        )

    @patch.dict(
        "os.environ",
        {
            "LINKEDIN_ACCESS_TOKEN": "token",
            "LINKEDIN_PERSON_URN": "urn:li:person:legacy",
        },
        clear=True,
    )
    def test_publish_linkedin_falls_back_to_legacy_person_urn(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            publish_linkedin("Hello world", "https://example.com/post", dry_run=True)

        self.assertIn("[linkedin] Dry run: would publish post", output.getvalue())

    @patch("scripts.post_to_social.publish_medium")
    @patch("scripts.post_to_social.publish_instagram")
    @patch("scripts.post_to_social.publish_linkedin")
    def test_linkedin_only_mode_does_not_call_other_socials(
        self,
        mock_linkedin,
        mock_instagram,
        mock_medium,
    ) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            post_path = Path(temp_dir) / "2026-07-24-test-post.md"
            post_path.write_text(
                "---\ntitle: Test Post\npermalink: /test-post/\n---\nUseful body text.",
                encoding="utf-8",
            )
            with patch(
                "sys.argv",
                ["post_to_social.py", "--post", str(post_path), "--linkedin-only"],
            ):
                result = main()

        self.assertEqual(0, result)
        mock_linkedin.assert_called_once()
        mock_instagram.assert_not_called()
        mock_medium.assert_not_called()


class PostUrlTests(unittest.TestCase):
    def test_post_url_uses_front_matter_permalink_when_available(self) -> None:
        url = post_url(
            "https://falowen.com/",
            Path("_posts/2026-04-16-german-alphabet-for-complete-beginners.md"),
            {"permalink": "/german-alphabet-for-complete-beginners/"},
        )

        self.assertEqual("https://falowen.com/german-alphabet-for-complete-beginners/", url)

    def test_post_url_falls_back_to_slug_from_filename(self) -> None:
        url = post_url(
            "https://falowen.com",
            Path("_posts/2026-04-16-german-alphabet-for-complete-beginners.md"),
        )

        self.assertEqual("https://falowen.com/german-alphabet-for-complete-beginners/", url)


if __name__ == "__main__":
    unittest.main()
