from __future__ import annotations

import argparse
import json
import mimetypes
import os
import re
from pathlib import Path
from urllib import error, parse, request


def env_value(*names: str) -> str | None:
    for name in names:
        raw = os.getenv(name)
        if raw is None:
            continue
        value = raw.strip()
        if not value:
            continue
        # GitHub Actions commonly masks missing/misconfigured secrets as "***".
        # Treat any all-asterisk value as absent to avoid invalid auth headers.
        if set(value) == {"*"}:
            continue
        if value.startswith("${{") and value.endswith("}}"):
            continue
        if value:
            return value
    return None


def parse_front_matter(markdown_text: str) -> dict[str, str]:
    if not markdown_text.startswith("---\n"):
        raise ValueError("Post does not start with YAML front matter.")

    try:
        _, fm_block, body = markdown_text.split("---\n", 2)
    except ValueError as exc:
        raise ValueError("Could not parse front matter block.") from exc

    data: dict[str, str] = {}
    for line in fm_block.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')

    data["_body"] = body.strip()
    return data


def slug_from_filename(path: Path) -> str:
    name = path.stem
    return re.sub(r"^\d{4}-\d{2}-\d{2}-", "", name)


def post_url(site_url: str, post_path: Path, front_matter: dict[str, str] | None = None) -> str:
    if front_matter:
        permalink = front_matter.get("permalink", "").strip()
        if permalink:
            normalized = permalink if permalink.startswith("/") else f"/{permalink}"
            return f"{site_url.rstrip('/')}{normalized}"

    return f"{site_url.rstrip('/')}/{slug_from_filename(post_path)}/"


def excerpt_from_body(body: str, max_len: int = 220) -> str:
    cleaned = re.sub(r"[#*_`>\-]", "", body)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    if len(cleaned) <= max_len:
        return cleaned
    return cleaned[: max_len - 1].rstrip() + "…"


def post_json(url: str, payload: dict, headers: dict[str, str]) -> tuple[int, str]:
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(url, data=data, method="POST")
    for k, v in headers.items():
        req.add_header(k, v)
    req.add_header("Content-Type", "application/json")

    try:
        with request.urlopen(req) as resp:  # noqa: S310 - trusted URLs from APIs
            return resp.status, resp.read().decode("utf-8")
    except error.HTTPError as exc:
        response_body = exc.read().decode("utf-8", errors="replace")
        details = response_body.strip() or exc.reason or "No response body"
        raise RuntimeError(
            f"HTTP {exc.code} from {url}: {details[:1200]}"
        ) from exc


def get_bytes(url: str) -> tuple[bytes, str]:
    req = request.Request(
        url,
        headers={
            "User-Agent": "FalowenLinkedInPublisher/1.0",
            "Accept": "image/jpeg,image/png,image/gif,image/svg+xml,*/*;q=0.5",
        },
    )
    try:
        with request.urlopen(req) as resp:  # noqa: S310 - image URL comes from post front matter
            content_type = resp.headers.get_content_type() or "application/octet-stream"
            return resp.read(), content_type
    except error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace").strip() or exc.reason
        raise RuntimeError(
            f"Could not download LinkedIn thumbnail from {url}: HTTP {exc.code} {details[:500]}"
        ) from exc


def put_bytes(url: str, data: bytes, headers: dict[str, str]) -> int:
    req = request.Request(url, data=data, method="PUT")
    for k, v in headers.items():
        req.add_header(k, v)
    try:
        with request.urlopen(req) as resp:  # noqa: S310 - upload URL is issued by LinkedIn
            return resp.status
    except error.HTTPError as exc:
        response_body = exc.read().decode("utf-8", errors="replace")
        details = response_body.strip() or exc.reason or "No response body"
        raise RuntimeError(
            f"HTTP {exc.code} while uploading LinkedIn image: {details[:1200]}"
        ) from exc


def load_image_bytes(image_ref: str, site_url: str) -> tuple[bytes, str]:
    if image_ref.startswith(("http://", "https://")):
        data, content_type = get_bytes(image_ref)
    else:
        local_path = Path(image_ref.lstrip("/"))
        if local_path.is_file():
            data = local_path.read_bytes()
            content_type = mimetypes.guess_type(local_path.name)[0] or "application/octet-stream"
        else:
            resolved = parse.urljoin(f"{site_url.rstrip('/')}/", image_ref)
            data, content_type = get_bytes(resolved)

    leading = data[:512].lstrip().lower()
    is_svg = (
        "svg" in content_type.lower()
        or parse.urlparse(image_ref).path.lower().endswith(".svg")
        or b"<svg" in leading
    )
    if is_svg:
        try:
            import cairosvg
        except ImportError as exc:  # pragma: no cover - dependency is installed in GitHub Actions
            raise RuntimeError(
                "SVG LinkedIn thumbnails require CairoSVG. Install it with `pip install cairosvg`."
            ) from exc
        data = cairosvg.svg2png(bytestring=data)
        content_type = "image/png"

    allowed_types = {"image/jpeg", "image/png", "image/gif"}
    if content_type.lower() not in allowed_types:
        raise RuntimeError(
            f"LinkedIn thumbnail format is unsupported: {content_type}. Use JPG, PNG, GIF, or SVG."
        )

    return data, content_type.lower()


def linkedin_headers(token: str, linkedin_version: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {token}",
        "X-Restli-Protocol-Version": "2.0.0",
        "Linkedin-Version": linkedin_version,
    }


def upload_linkedin_image(
    image_ref: str,
    site_url: str,
    token: str,
    author_urn: str,
    linkedin_version: str,
) -> str:
    headers = linkedin_headers(token, linkedin_version)
    status, body = post_json(
        "https://api.linkedin.com/rest/images?action=initializeUpload",
        {"initializeUploadRequest": {"owner": author_urn}},
        headers,
    )
    if status != 200:
        raise RuntimeError(f"LinkedIn image upload initialization failed with status {status}.")

    try:
        value = json.loads(body)["value"]
        upload_url = value["uploadUrl"]
        image_urn = value["image"]
    except (KeyError, TypeError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"LinkedIn image upload returned an unexpected response: {body[:500]}") from exc

    image_bytes, content_type = load_image_bytes(image_ref, site_url)
    upload_status = put_bytes(
        upload_url,
        image_bytes,
        {
            "Authorization": f"Bearer {token}",
            "Content-Type": content_type,
        },
    )
    if upload_status not in {200, 201}:
        raise RuntimeError(f"LinkedIn image upload failed with status {upload_status}.")

    return image_urn


def publish_linkedin(
    text: str,
    article_url: str,
    dry_run: bool,
    *,
    title: str | None = None,
    description: str | None = None,
    image_url: str | None = None,
    site_url: str = "https://blog.falowen.app",
) -> None:
    token = env_value("LINKEDIN_ACCESS_TOKEN")
    author_urn = env_value("LINKEDIN_AUTHOR_URN", "LINKEDIN_PERSON_URN")
    if not token or not author_urn:
        print(
            "[linkedin] Skipped: missing LINKEDIN_ACCESS_TOKEN or "
            "(LINKEDIN_AUTHOR_URN or LINKEDIN_PERSON_URN)"
        )
        return

    linkedin_version = env_value("LINKEDIN_VERSION") or "202607"
    commentary = f"{text}\n\nRead more: {article_url}"
    payload: dict = {
        "author": author_urn,
        "commentary": commentary,
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": [],
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False,
    }

    # LinkedIn's Posts API does not scrape URLs for article previews. We must
    # explicitly send article metadata and upload the thumbnail image first.
    if title or description or image_url:
        article: dict[str, str] = {
            "source": article_url,
            "title": title or text.splitlines()[0][:200],
            "description": description or "",
        }
        if image_url and not dry_run:
            article["thumbnail"] = upload_linkedin_image(
                image_url,
                site_url,
                token,
                author_urn,
                linkedin_version,
            )
        payload["content"] = {"article": article}

    if dry_run:
        print("[linkedin] Dry run: would publish post")
        return

    status, body = post_json(
        "https://api.linkedin.com/rest/posts",
        payload,
        linkedin_headers(token, linkedin_version),
    )
    print(f"[linkedin] Published (status={status}): {body[:160]}")


def publish_medium(title: str, content_markdown: str, article_url: str, dry_run: bool) -> None:
    token = env_value("MEDIUM_TOKEN")
    user_id = env_value("MEDIUM_USER_ID")
    if not token or not user_id:
        print("[medium] Skipped: missing MEDIUM_TOKEN or MEDIUM_USER_ID")
        return

    content = f"{content_markdown}\n\nOriginally published: [{article_url}]({article_url})"
    payload = {
        "title": title,
        "contentFormat": "markdown",
        "content": content,
        "publishStatus": "public",
    }
    if dry_run:
        print("[medium] Dry run: would publish article")
        return

    status, body = post_json(
        f"https://api.medium.com/v1/users/{parse.quote(user_id)}/posts",
        payload,
        {"Authorization": f"Bearer {token}"},
    )
    print(f"[medium] Published (status={status}): {body[:160]}")


def publish_instagram(caption: str, article_url: str, image_url: str | None, dry_run: bool) -> None:
    token = env_value("INSTAGRAM_ACCESS_TOKEN")
    account_id = env_value("INSTAGRAM_ACCOUNT_ID")
    if not token or not account_id:
        print("[instagram] Skipped: missing INSTAGRAM_ACCESS_TOKEN or INSTAGRAM_ACCOUNT_ID")
        return
    if not image_url:
        print("[instagram] Skipped: post has no `image:` URL in front matter")
        return

    final_caption = f"{caption}\n\nRead more: {article_url}"
    create_url = f"https://graph.facebook.com/v20.0/{account_id}/media"
    publish_url = f"https://graph.facebook.com/v20.0/{account_id}/media_publish"

    if dry_run:
        print("[instagram] Dry run: would create media container + publish")
        return

    container_payload = {
        "image_url": image_url,
        "caption": final_caption,
        "access_token": token,
    }
    status, body = post_json(create_url, container_payload, {})
    data = json.loads(body)
    creation_id = data.get("id")
    if not creation_id:
        raise RuntimeError(f"[instagram] Failed creating media container (status={status}): {body}")

    status2, body2 = post_json(publish_url, {"creation_id": creation_id, "access_token": token}, {})
    print(f"[instagram] Published (status={status2}): {body2[:160]}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Publish a blog post to social channels.")
    parser.add_argument("--post", required=True, help="Path to post markdown file in _posts/.")
    parser.add_argument("--site-url", default=os.getenv("SITE_URL", "https://falowen.com"))
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--linkedin-only",
        action="store_true",
        help="Publish only to LinkedIn. Useful for the dedicated LinkedIn workflow.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    post_path = Path(args.post)
    if not post_path.exists():
        raise FileNotFoundError(f"Post not found: {post_path}")

    fm = parse_front_matter(post_path.read_text(encoding="utf-8"))
    title = fm.get("title", post_path.stem)
    body = fm.get("_body", "")
    excerpt = fm.get("excerpt") or excerpt_from_body(body)
    image_url = fm.get("image")

    url = post_url(args.site_url, post_path, fm)

    publish_linkedin(
        f"{title}\n\n{excerpt}",
        url,
        args.dry_run,
        title=title,
        description=excerpt,
        image_url=image_url,
        site_url=args.site_url,
    )
    if args.linkedin_only:
        return 0

    publish_instagram(f"{title}\n\n{excerpt}", url, image_url, args.dry_run)
    publish_medium(title, body, url, args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
