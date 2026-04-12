
(function () {
  const input = document.getElementById('search-input');
  const rows = Array.from(document.querySelectorAll('[data-search-row]'));
  if (!input) return;
  input.addEventListener('input', () => {
    const kw = input.value.trim().toLowerCase();
    rows.forEach((row) => {
      const text = (row.getAttribute('data-search-row') || '').toLowerCase();
      row.style.display = !kw || text.includes(kw) ? '' : 'none';
    });
  });
})();
