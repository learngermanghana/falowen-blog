---
layout: page
title: Search
permalink: /search/
---

<input type="text" id="search-input" placeholder="Search German lessons, grammar, exams, vocabulary...">
<ul id="results-container" class="search-results"></ul>

<script src="https://cdn.jsdelivr.net/npm/simple-jekyll-search@1.11.1/dest/simple-jekyll-search.min.js"></script>
<script>
  var searchInput = document.getElementById('search-input');
  var search = SimpleJekyllSearch({
    searchInput: searchInput,
    resultsContainer: document.getElementById('results-container'),
    json: '/search.json',
    searchResultTemplate: '<li><a href="{url}">{title}</a><span> — {date}</span></li>',
    noResultsText: '<li>No matching lessons found.</li>',
    limit: 20,
    fuzzy: true
  });

  var initialQuery = new URLSearchParams(window.location.search).get('q');
  if (initialQuery) {
    searchInput.value = initialQuery;
    search.search(initialQuery);
  }
</script>