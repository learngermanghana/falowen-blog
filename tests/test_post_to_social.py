import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from PIL import Image
from unittest.mock import patch

from scripts.post_to_social import load_image_bytes, main, parse_front_matter, post_url, publish_linkedin


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

        self.assertIn("[linkedin] Dry run: verified", output.getvalue())

    @patch.dict(
        "os.environ",
        {
            "LINKEDIN_ACCESS_TOKEN": "token",
            "LINKEDIN_AUTHOR_URN": "urn:li:person:author",
        },
        clear=True,
    )
    @patch("scripts.post_to_social.upload_linkedin_image", return_value="urn:li:image:test")
    @patch("scripts.post_to_social.post_json")
    def test_publish_linkedin_sends_current_posts_api_request(self, mock_post_json, mock_upload) -> None:
        mock_post_json.return_value = (201, "")

        publish_linkedin("New post", "https://example.com/post", dry_run=False)

        mock_post_json.assert_called_once_with(
            "https://api.linkedin.com/rest/posts",
            {
                "author": "urn:li:person:author",
                "commentary": "New post\n\nRead more: https://example.com/post",
                "visibility": "PUBLIC",
                "distribution": {
                    "feedDistribution": "MAIN_FEED",
                    "targetEntities": [],
                    "thirdPartyDistributionChannels": [],
                },
                "lifecycleState": "PUBLISHED",
                "isReshareDisabledByAuthor": False,
                "content": {
                    "media": {
                        "id": "urn:li:image:test",
                        "altText": "New post",
                    }
                },
            },
            {
                "Authorization": "Bearer token",
                "X-Restli-Protocol-Version": "2.0.0",
                "Linkedin-Version": "202607",
            },
        )

    @patch.dict(
        "os.environ",
        {
            "LINKEDIN_ACCESS_TOKEN": "token",
            "LINKEDIN_AUTHOR_URN": "urn:li:person:author",
        },
        clear=True,
    )
    @patch("scripts.post_to_social.upload_linkedin_image")
    @patch("scripts.post_to_social.post_json")
    def test_publish_linkedin_adds_native_image_media(
        self,
        mock_post_json,
        mock_upload_linkedin_image,
    ) -> None:
        mock_post_json.return_value = (201, "")
        mock_upload_linkedin_image.return_value = "urn:li:image:thumbnail"

        publish_linkedin(
            "German lesson",
            "https://blog.falowen.app/german-lesson/",
            dry_run=False,
            title="German Lesson",
            description="Learn a useful German grammar topic.",
            image_url="/assets/img/german-lesson.svg",
            site_url="https://blog.falowen.app",
        )

        mock_upload_linkedin_image.assert_called_once_with(
            "/assets/img/german-lesson.svg",
            "https://blog.falowen.app",
            "token",
            "urn:li:person:author",
            "202607",
        )
        payload = mock_post_json.call_args.args[1]
        self.assertEqual(
            {"media": {"id": "urn:li:image:thumbnail", "altText": "German Lesson"}},
            payload["content"],
        )

    @patch.dict(
        "os.environ",
        {
            "LINKEDIN_ACCESS_TOKEN": "token",
            "LINKEDIN_AUTHOR_URN": "urn:li:person:author",
            "LINKEDIN_VERSION": "202606",
        },
        clear=True,
    )
    @patch("scripts.post_to_social.upload_linkedin_image", return_value="urn:li:image:test")
    @patch("scripts.post_to_social.post_json")
    def test_publish_linkedin_allows_version_override(self, mock_post_json, mock_upload) -> None:
        mock_post_json.return_value = (201, "")

        publish_linkedin("New post", "https://example.com/post", dry_run=False)

        headers = mock_post_json.call_args.args[2]
        self.assertEqual("202606", headers["Linkedin-Version"])

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
                "---\n"
                "title: Test Post\n"
                "excerpt: A useful test excerpt.\n"
                "image: /assets/img/test.svg\n"
                "permalink: /test-post/\n"
                "---\n"
                "Useful body text.",
                encoding="utf-8",
            )
            with patch(
                "sys.argv",
                ["post_to_social.py", "--post", str(post_path), "--linkedin-only"],
            ):
                result = main()

        self.assertEqual(0, result)
        mock_linkedin.assert_called_once_with(
            "Test Post\n\nA useful test excerpt.",
            "https://falowen.com/test-post/",
            False,
            title="Test Post",
            description="A useful test excerpt.",
            image_url="/assets/img/test.svg",
            site_url="https://falowen.com",
        )
        mock_instagram.assert_not_called()
        mock_medium.assert_not_called()



class ThumbnailFormatTests(unittest.TestCase):
    @patch("scripts.post_to_social.get_bytes")
    def test_webp_image_is_converted_to_jpeg_for_linkedin(self, mock_get_bytes) -> None:
        photo = io.BytesIO()
        Image.new("RGBA", (5, 6), (10, 90, 140, 110)).save(photo, "WEBP")
        mock_get_bytes.return_value = (photo.getvalue(), "image/webp")

        data, content_type = load_image_bytes(
            "https://blog.falowen.app/assets/images/falowen-study-buddy-ai-example.webp",
            "https://blog.falowen.app",
        )

        self.assertEqual("image/jpeg", content_type)
        self.assertTrue(data.startswith(b"\xff\xd8"))
        with Image.open(io.BytesIO(data)) as converted:
            self.assertEqual("JPEG", converted.format)
            self.assertEqual((5, 6), converted.size)

    @patch("scripts.post_to_social.get_bytes")
    def test_webp_magic_detected_when_server_returns_octet_stream(self, mock_get_bytes) -> None:
        photo = io.BytesIO()
        Image.new("RGB", (4, 4), (10, 20, 30)).save(photo, "WEBP")
        mock_get_bytes.return_value = (photo.getvalue(), "application/octet-stream")

        data, content_type = load_image_bytes("https://example.com/photo", "https://example.com")

        self.assertEqual("image/jpeg", content_type)
        self.assertTrue(data.startswith(b"\xff\xd8"))

    @patch("scripts.post_to_social.get_bytes")
    def test_existing_jpeg_stays_supported_without_reencoding(self, mock_get_bytes) -> None:
        photo = io.BytesIO()
        Image.new("RGB", (4, 4), (10, 20, 30)).save(photo, "JPEG")
        mock_get_bytes.return_value = (photo.getvalue(), "image/jpeg")

        data, content_type = load_image_bytes("https://example.com/thumbnail.jpg", "https://example.com")

        self.assertEqual("image/jpeg", content_type)
        self.assertEqual(photo.getvalue(), data)


class PublishedPostMetadataTests(unittest.TestCase):
    def test_ai_post_uses_head_consumed_fields_and_one_layout_h1(self) -> None:
        root = Path(__file__).resolve().parents[1]
        post = (root / "_posts/2026-10-15-ai-german-tutor-writing-feedback-ghana.md").read_text()
        metadata = parse_front_matter(post)
        self.assertIn("AI German Tutor", metadata["title"])
        self.assertIn("Ghana", metadata["title"])
        self.assertIn("West Africa", metadata["description"])
        self.assertEqual(metadata["description"], metadata["excerpt"])
        self.assertNotIn("\nseo:\n", post)
        self.assertFalse(metadata["_body"].startswith("# "))
        self.assertIn("<h1", (root / "_layouts/post.html").read_text())


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
