// Runs before first paint: apply a saved Day/Night choice, otherwise follow the OS.
const themeKey = 'agent-johnny5-theme';
const root = document.documentElement;
try {
  const saved = localStorage.getItem(themeKey);
  if (saved === 'light' || saved === 'dark') root.dataset.theme = saved;
} catch {}

document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.querySelector('#theme-toggle');
  const prefersLight = matchMedia('(prefers-color-scheme: light)');
  const isDay = () => (root.dataset.theme || (prefersLight.matches ? 'light' : 'dark')) === 'light';
  const render = () => {
    toggle.setAttribute('aria-pressed', String(isDay()));
    document.querySelector('meta[name="theme-color"]').content = getComputedStyle(root).getPropertyValue('--bg').trim();
  };
  toggle.addEventListener('click', () => {
    root.dataset.theme = isDay() ? 'dark' : 'light';
    try { localStorage.setItem(themeKey, root.dataset.theme); } catch {}
    render();
  });
  prefersLight.addEventListener('change', render);
  render();
});
