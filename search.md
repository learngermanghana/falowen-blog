---
layout: null
title: All Blog Posts
permalink: /search/
sitemap: false
---
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="robots" content="noindex,follow">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="canonical" href="{{ '/blogs/' | absolute_url }}">
  <meta http-equiv="refresh" content="1;url={{ '/blogs/' | relative_url }}">
  <title>Redirecting to All Blog Posts · Falowen</title>
  <script>
    // The old standalone search was retired. Preserve an existing ?q= filter
    // so indexed links and bookmarks still land on matching blog articles.
    (function () {
      var query = new URLSearchParams(window.location.search).get('q');
      var destination = {{ '/blogs/' | relative_url | jsonify }};
      if (query) destination += '?q=' + encodeURIComponent(query);
      window.location.replace(destination);
    })();
  </script>
</head>
<body>
  <p>Search has moved to <a href="{{ '/blogs/' | relative_url }}">All Blog Posts</a>.</p>
</body>
</html>
