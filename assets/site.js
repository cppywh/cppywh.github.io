(() => {
  'use strict';
  const search = document.getElementById('note-search');
  if (search) {
    const filters = [...document.querySelectorAll('[data-filter]')];
    const rows = [...document.querySelectorAll('.note-row')];
    let category = '全部';
    const update = () => {
      const query = search.value.trim().toLocaleLowerCase();
      let count = 0;
      for (const row of rows) {
        const visible = (category === '全部' || row.dataset.category === category) && row.dataset.search.toLocaleLowerCase().includes(query);
        row.hidden = !visible;
        count += Number(visible);
      }
      document.getElementById('result-count').textContent = `${count} 篇手记`;
      document.querySelector('.empty-state').hidden = count > 0;
      for (const filter of filters) filter.setAttribute('aria-pressed', String(filter.dataset.filter === category));
    };
    filters.forEach(button => button.addEventListener('click', () => { category = button.dataset.filter; update(); }));
    search.addEventListener('input', update);
    document.querySelector('.reset-search').addEventListener('click', () => { category = '全部'; search.value = ''; update(); search.focus(); });
  }
  let toastTimeout;
  function notify(message) {
    const toast = document.querySelector('.toast');
    toast.textContent = message;
    toast.classList.add('visible');
    clearTimeout(toastTimeout);
    toastTimeout = setTimeout(() => toast.classList.remove('visible'), 2600);
  }
  document.querySelectorAll('.copy-code').forEach(button => button.addEventListener('click', async () => {
    const code = button.closest('.code-block').querySelector('code').textContent;
    try {
      await navigator.clipboard.writeText(code);
      notify('代码已复制');
    } catch {
      const range = document.createRange();
      range.selectNodeContents(button.closest('.code-block').querySelector('code'));
      const selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      notify('已选中代码，请使用系统复制快捷键');
    }
  }));
  const progress = document.querySelector('.reading-progress');
  if (progress) {
    const links = [...document.querySelectorAll('.toc nav a')];
    const sections = links.map(link => document.getElementById(link.hash.slice(1)));
    let scheduled = false;
    const updateReading = () => {
      const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
      progress.style.width = `${maxScroll > 0 ? Math.min(100, Math.max(0, window.scrollY / maxScroll * 100)) : 0}%`;
      let current = 0;
      sections.forEach((section, index) => { if (section.getBoundingClientRect().top <= 150) current = index; });
      links.forEach((link, index) => { link.classList.toggle('active', index === current); if (index === current) link.setAttribute('aria-current', 'location'); else link.removeAttribute('aria-current'); });
      scheduled = false;
    };
    const schedule = () => { if (!scheduled) { scheduled = true; requestAnimationFrame(updateReading); } };
    addEventListener('scroll', schedule, { passive: true });
    addEventListener('resize', schedule);
    updateReading();
  }
})();
