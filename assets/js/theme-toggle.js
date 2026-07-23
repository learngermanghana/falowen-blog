(function() {
  const storageKey = 'theme';
  const toggle = document.getElementById('theme-toggle');

  function apply(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    if (toggle) {
      const dark = theme === 'dark';
      toggle.textContent = dark ? '☀' : '☾';
      toggle.setAttribute('aria-label', dark ? 'Switch to light mode' : 'Switch to dark mode');
      toggle.setAttribute('title', dark ? 'Switch to light mode' : 'Switch to dark mode');
    }
  }

  let current = localStorage.getItem(storageKey);
  if (!current) {
    current = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }
  apply(current);

  if (toggle) {
    toggle.addEventListener('click', function() {
      current = current === 'dark' ? 'light' : 'dark';
      localStorage.setItem(storageKey, current);
      apply(current);
    });
  }
})();