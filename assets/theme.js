/* Four user-selected wallpapers. Shuffle without repeats; retain on navigation. */
(() => {
  'use strict';
  const palettes = [
    {id:'6kqzl6',name:'雕塑 · 雾紫',bg:'#f8f6f9',ink:'#393441',muted:'#686071',accent:'#796085',soft:'#eee7f0',line:'#dfd5e4',mark:'#668379',wash:'#e8e1ee',veil:'.72',position:'50% 50%',quote:'把好奇种下，等理解开花。'},
    {id:'kxp797',name:'机械 · 冰蓝',bg:'#f3f9fa',ink:'#29434a',muted:'#526d75',accent:'#2b7483',soft:'#e2f0f2',line:'#cddfe3',mark:'#8d7899',wash:'#dbeef2',veil:'.56',position:'65% 50%',quote:'在代码与想象之间，慢慢理解。'},
    {id:'837ymk',name:'几何 · 钴蓝',bg:'#f7faff',ink:'#283e56',muted:'#556b83',accent:'#2468a0',soft:'#e5eef9',line:'#d1deef',mark:'#7598aa',wash:'#e1ebf9',veil:'.55',position:'50% 50%',quote:'把复杂拆开，让理解一块一块生长。'},
    {id:'w5m6yr',name:'晶体 · 湖青',bg:'#f0f7fa',ink:'#29444c',muted:'#4b6974',accent:'#28768c',soft:'#dfeef3',line:'#c9dfe8',mark:'#6d7eab',wash:'#d4e9f0',veil:'.82',position:'50% 50%',quote:'每一次尝试，都折射出一点新的光。'}
  ];
  const assetBase = new URL('wallpapers/', document.currentScript.src);
  const storageKey = 'iris-wallpapers-v1';
  let saved = {};
  try { saved = JSON.parse(sessionStorage.getItem(storageKey) || '{}') || {}; } catch {}
  let index = Number.isInteger(saved.index) && saved.index >= 0 && saved.index < palettes.length ? saved.index : -1;
  let remaining = Array.isArray(saved.remaining) ? [...new Set(saved.remaining.filter(i => Number.isInteger(i) && i >= 0 && i < palettes.length && i !== index))] : [];
  const navigation = performance.getEntriesByType('navigation')[0]?.type || 'navigate';
  const root = document.documentElement;
  function save() { try { sessionStorage.setItem(storageKey,JSON.stringify({index,remaining})); } catch {} }
  function chooseNext() {
    if (!remaining.length) {
      remaining = palettes.map((_,i) => i);
      for (let i = remaining.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [remaining[i],remaining[j]] = [remaining[j],remaining[i]];
      }
      if (remaining[0] === index) [remaining[0],remaining[1]] = [remaining[1],remaining[0]];
    }
    index = remaining.shift();
    save();
  }
  function syncLabels() {
    const palette = palettes[index];
    document.querySelectorAll('[data-season-quote]').forEach(el => { el.textContent = palette.quote; });
    document.querySelectorAll('[data-palette-label]').forEach(el => { el.textContent = palette.name; });
    document.querySelectorAll('[data-theme-index]').forEach(el => el.setAttribute('aria-pressed',String(Number(el.dataset.themeIndex) === index)));
    document.querySelectorAll('[data-wallpaper-source]').forEach(el => { el.href = `https://wallhaven.cc/w/${palette.id}`; el.textContent = `壁纸来源 ↗`; el.setAttribute('aria-label',`${palette.name}壁纸来源（新窗口）`); });
  }
  function apply() {
    const palette = palettes[index];
    root.dataset.palette = palette.id;
    for (const [key,value] of Object.entries({bg:palette.bg,ink:palette.ink,muted:palette.muted,blue:palette.accent,'blue-soft':palette.soft,line:palette.line,rust:palette.mark,'theme-wash':palette.wash,'wallpaper-veil':palette.veil,'wallpaper-position':palette.position})) root.style.setProperty(`--${key}`,value);
    root.style.setProperty('--wallpaper',`url("${new URL(`${palette.id}.jpg`,assetBase).href}")`);
    root.style.setProperty('--seed-tilt', `${index * 13 - 20}deg`);
    syncLabels();
  }
  if (index < 0 || navigation === 'reload') chooseNext();
  apply();
  document.addEventListener('DOMContentLoaded', () => {
    syncLabels();
    document.querySelectorAll('[data-theme-index]').forEach(button => button.addEventListener('click', () => {
      const chosen = Number(button.dataset.themeIndex);
      if (!Number.isInteger(chosen) || chosen < 0 || chosen >= palettes.length || chosen === index) return;
      index = chosen;
      remaining = palettes.map((_,i) => i).filter(i => i !== index);
      save(); apply();
    }));
    document.querySelectorAll('[data-next-theme]').forEach(button => button.addEventListener('click', () => { chooseNext(); apply(); }));
  });
})();
