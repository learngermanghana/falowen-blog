(function () {
  var fallback = '/assets/img/falowen-blog-default.svg';

  function attachFallback(img) {
    if (!img || img.dataset.falowenFallbackReady === 'true') return;
    img.dataset.falowenFallbackReady = 'true';
    img.addEventListener('error', function () {
      if (img.src.indexOf(fallback) === -1) {
        img.src = fallback;
        img.removeAttribute('srcset');
      }
    });

    if (img.complete && img.naturalWidth === 0) {
      img.src = fallback;
      img.removeAttribute('srcset');
    }
  }

  function run() {
    document.querySelectorAll('img').forEach(attachFallback);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', run);
  } else {
    run();
  }
})();
