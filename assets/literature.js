'use strict';
const paperSearch = document.getElementById('paper-search');
paperSearch.addEventListener('input', () => {
  const query = paperSearch.value.trim().toLocaleLowerCase();
  let count = 0;
  document.querySelectorAll('[data-paper-search]').forEach(card => {
    card.hidden = !card.dataset.paperSearch.toLocaleLowerCase().includes(query);
    if (!card.hidden) count++;
  });
  document.getElementById('paper-count').textContent = `${count} 篇文献`;
  document.getElementById('paper-empty').hidden = count > 0;
});
