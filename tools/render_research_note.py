"""Render the single public medical GRPO note and redirect its old section URLs."""

from __future__ import annotations

import re
from html import escape
from pathlib import Path
from urllib.parse import quote

from markdown_it import MarkdownIt


SECTION_REDIRECTS = {
    "design.html": "实验设计",
    "results.html": "主要结果",
    "explorations.html": "历史探索",
    "reproduction.html": "代码与复核",
}


def render_note(root: Path, shell, icon) -> None:
    """Read the project's README.md and build one article plus legacy redirects."""
    folder = root / "research" / "medical-grpo"
    content = (folder / "README.md").read_text(encoding="utf-8")
    title = content.splitlines()[0].removeprefix("# ").strip()
    content = re.sub(
        r"```mermaid\n.*?\n```",
        "![Qwen3 实验权重继承路线图](assets/route.svg)",
        content,
        flags=re.DOTALL,
    )

    md = MarkdownIt("commonmark", {"html": False}).enable("table")
    tokens = md.parse(content)
    if tokens and tokens[0].type == "heading_open" and tokens[0].tag == "h1":
        tokens = tokens[3:]

    headings = []
    for position, token in enumerate(tokens):
        if token.type == "heading_open" and token.tag in ("h2", "h3"):
            label = tokens[position + 1].content
            token.attrSet("id", label)
            if token.tag == "h2":
                headings.append(label)

    article = md.renderer.render(tokens, md.options, {})
    article = re.sub(
        r"<table>.*?</table>",
        lambda match: f'<div class="table-wrap">{match.group(0)}</div>',
        article,
        flags=re.DOTALL,
    )
    toc = "".join(
        f'<a href="#{quote(label)}"><span>{number:02d}</span>{escape(label)}</a>'
        for number, label in enumerate(headings, 1)
    )
    source_url = (
        "https://github.com/cppywh/cppywh.github.io/blob/main/"
        "research/medical-grpo/README.md"
    )
    body = (
        '<div class="reading-progress" aria-hidden="true"></div>'
        '<div class="page-wrap article-wrap">'
        '<a class="back-link" href="../../notes.html">← 返回学习手记</a>'
        '<header class="article-header">'
        '<div class="eyebrow">MEDICAL GRPO / 01</div>'
        f'<h1>{escape(title)}</h1>'
        '<p class="article-lead">从三奖励 GRPO、扩量 SFT 到直接 GRPO 与 DAPO 的一次实验复盘。</p>'
        '<div class="post-meta"><span>iris</span><span>实验记录</span>'
        '<span>基于公开汇总数据</span></div></header>'
        '<div class="article-layout"><article class="prose">'
        f'{article}'
        f'<p><a href="{source_url}" target="_blank" rel="noopener noreferrer">在 GitHub 查看 Markdown 原文 ↗</a></p>'
        '<div class="article-end"><span>— END —</span><p>记录到这里，下一步继续。</p></div>'
        '</article><aside class="toc"><div class="toc-inner">'
        '<span class="eyebrow">本页目录</span>'
        f'<nav aria-label="文章目录">{toc}</nav>'
        '<a class="back-top" href="#main">↑ 回到顶部</a>'
        '</div></aside></div></div>'
    )
    page = shell(title, "notes", "@@ARTICLE@@", title)
    for path in (
        "index.html", "notes.html", "about.html", "assets/favicon.svg",
        "assets/style.css", "assets/theme.js", "assets/site.js",
    ):
        page = page.replace(f'"{path}"', f'"../../{path}"')
    page = page.replace('class="inner-page"', 'class="inner-page research-note"', 1)
    (folder / "index.html").write_text(page.replace("@@ARTICLE@@", body), encoding="utf-8")

    # Keep shared links to the former section pages useful after consolidation.
    for old_page, section in SECTION_REDIRECTS.items():
        destination = f"index.html#{quote(section)}"
        redirect = (
            '<!doctype html><html lang="zh-CN"><meta charset="utf-8">'
            f'<meta http-equiv="refresh" content="0;url={destination}">'
            f'<link rel="canonical" href="{destination}">'
            f'<title>文章已合并 · {escape(title)}</title>'
            f'<p>文章已合并。<a href="{destination}">前往{escape(section)}</a></p></html>'
        )
        (folder / old_page).write_text(redirect, encoding="utf-8")

    print("Rendered one medical GRPO article with four legacy redirects.")
