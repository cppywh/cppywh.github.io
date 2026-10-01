"""Build a static literature shelf and browser-native PDF readers."""
import json
from html import escape
from urllib.parse import quote


def build_literature(root, shell):
    papers = json.loads((root / 'literature/catalog.json').read_text(encoding='utf-8'))
    cards = []
    seen = set()
    for paper in papers:
        slug = paper['id']
        if not slug.replace('-', '').isalnum() or slug in seen:
            raise ValueError(f'Invalid or duplicate paper ID: {slug}')
        seen.add(slug)
        if not (root / paper['file']).is_file():
            raise FileNotFoundError(paper['file'])
        title = escape(paper['title'])
        pdf = quote(paper['file'], safe='/')
        reader = f'paper-{slug}.html'
        tags = ' · '.join(paper['tags'])
        search = escape(paper['name'] + ' ' + paper['title'] + ' ' + tags, quote=True)
        cards.append(f'''<article class="paper-card" data-paper-search="{search}"><div class="eyebrow">{escape(tags)} · {paper['pages']} 页 · {escape(paper['status'])}</div><h2>{escape(paper['name'])}</h2><p>{title}</p><div class="paper-actions"><a href="{reader}">快速阅读 →</a><a href="{pdf}" target="_blank" rel="noopener">打开 PDF ↗</a><a href="{pdf}" download>下载</a></div></article>''')
        body = f'''<div class="page-wrap"><a class="back-link" href="literature.html">← 返回文献架</a><section class="page-intro"><div class="eyebrow">PAPER / {escape(paper['name'])}</div><h1>{escape(paper['name'])}</h1><p>{title}</p><div class="paper-actions"><a href="{pdf}" target="_blank" rel="noopener">独立打开 PDF ↗</a><a href="{pdf}" download>下载原文</a><a href="reading/llm-quantization/">量化阅读笔记 →</a></div></section><iframe class="paper-reader" src="{pdf}#view=FitH" title="{title}" loading="lazy"></iframe><p>若设备无法显示内嵌 PDF，请使用上方“独立打开 PDF”。搜索、缩放和页码跳转由浏览器的 PDF 阅读器提供。</p></div>'''
        (root / reader).write_text(shell(paper['name'], 'literature', body, paper['title']), encoding='utf-8')
    body = f'''<div class="page-wrap"><section class="page-intro"><div class="eyebrow">THE READING SHELF</div><h1>文献架<span class="title-dot">。</span></h1><p>把原文放在手边，把理解留在笔记里。</p><a href="reading/llm-quantization/">LLM Quantization · 我的阅读笔记 →</a></section><label class="paper-search">搜索文献<input id="paper-search" type="search" placeholder="标题、关键词、量化、高效微调…"></label><p id="paper-count" role="status" aria-live="polite">{len(papers)} 篇文献</p><div class="paper-grid">{''.join(cards)}</div><p id="paper-empty" hidden>没有找到匹配文献，试试其他关键词。</p></div>'''
    page = shell('文献架', 'literature', body)
    page = page.replace('</head>', '<script src="assets/literature.js" defer></script></head>')
    (root / 'literature.html').write_text(page, encoding='utf-8')
