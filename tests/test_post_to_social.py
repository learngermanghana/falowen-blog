import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from scripts.post_to_social import publish_linkedin


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
            "LINKEDIN_PERSON_URN": "urn:li:person:legacy",
        },
        clear=True,
    )
    def test_publish_linkedin_falls_back_to_legacy_person_urn(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            publish_linkedin("Hello world", "https://example.com/post", dry_run=True)

        self.assertIn("[linkedin] Dry run: would publish post", output.getvalue())


if __name__ == "__main__":
    unittest.main()
