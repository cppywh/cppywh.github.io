"""Render the public medical GRPO Markdown into the existing static article layout.

Run through build_site.py after installing markdown-it-py from tools/requirements.txt.
The Markdown files remain the content source; private experiment files are not read.
"""

from __future__ import annotations

import re
from html import escape
from pathlib import Path
from urllib.parse import quote

from markdown_it import MarkdownIt


PAGES = [
    ("00-project-overview.md", "index.html", "从格式学会到答题改进", "我从三奖励 GRPO、扩量 SFT 到直接 GRPO 与 DAPO 的一次实验复盘。"),
    ("01-experiment-design.md", "design.html", "实验设计", "题目怎样进入训练，分数怎样计算。"),
    ("02-main-results.md", "results.html", "主结果", "用同题的正确率、改对与改错题数检验训练效果。"),
    ("03-explorations-and-ablations.md", "explorations.html", "历史探索", "记录 V2、V3 和更早实验的负结果与限制。"),
    ("04-reproduction-and-code.md", "reproduction.html", "代码与复核", "说明公开证据、环境和再运行边界。"),
]


def render_all(root: Path, shell, icon) -> None:
    """Read five public Markdown files and write five navigable site pages."""
    folder = root / "research" / "medical-grpo"
    md = MarkdownIt("commonmark", {"html": False}).enable("table")
    targets = {source: output for source, output, _, _ in PAGES}

    for index, (source, output, short_title, lead) in enumerate(PAGES):
        content = (folder / source).read_text(encoding="utf-8")
        title = content.splitlines()[0].removeprefix("# ").strip()
        content = re.sub(r"(?m)^\[← [^\n]+\n\n", "", content)
        if source == "00-project-overview.md":
            content = re.sub(
                r"```mermaid\n.*?\n```",
                "![Qwen3 实验权重继承路线图](assets/route.svg)",
                content,
                flags=re.DOTALL,
            )

        tokens = md.parse(content)
        if tokens and tokens[0].type == "heading_open" and tokens[0].tag == "h1":
            tokens = tokens[3:]

        headings = []
        for position, token in enumerate(tokens):
            if token.type == "heading_open" and token.tag == "h2":
                label = tokens[position + 1].content
                token.attrSet("id", label)
                headings.append(label)

        article = md.renderer.render(tokens, md.options, {})
        for markdown_name, html_name in targets.items():
            article = article.replace(f'href="{markdown_name}', f'href="{html_name}')
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
        _, next_output, next_title, _ = PAGES[(index + 1) % len(PAGES)]
        source_url = (
            "https://github.com/cppywh/cppywh.github.io/blob/main/"
            f"research/medical-grpo/{source}"
        )
        body = (
            '<div class="reading-progress" aria-hidden="true"></div>'
            '<div class="page-wrap article-wrap">'
            '<a class="back-link" href="../../notes.html">← 返回学习手记</a>'
            '<header class="article-header">'
            f'<div class="eyebrow">MEDICAL GRPO / {index + 1:02d}</div>'
            f'<h1>{escape(title)}</h1><p class="article-lead">{escape(lead)}</p>'
            '<div class="post-meta"><span>iris</span><span>实验记录</span>'
            '<span>基于公开汇总数据</span></div></header>'
            '<div class="article-layout"><article class="prose">'
            f'{article}'
            f'<p><a href="{source_url}" target="_blank" rel="noopener noreferrer">在 GitHub 查看 Markdown 原文 ↗</a></p>'
            '<div class="article-end"><span>— END —</span><p>记录到这里，下一步继续。</p></div>'
            f'<a class="next-article" href="{next_output}"><span>继续阅读</span>'
            f'<strong>{escape(next_title)}</strong>{icon("arrow")}</a>'
            '</article><aside class="toc"><div class="toc-inner">'
            '<span class="eyebrow">本页目录</span>'
            f'<nav aria-label="文章目录">{toc}</nav>'
            '<a class="back-top" href="#main">↑ 回到顶部</a>'
            '</div></aside></div></div>'
        )
        page = shell(short_title, "notes", "@@ARTICLE@@", lead)
        for path in (
            "index.html", "notes.html", "about.html", "assets/favicon.svg",
            "assets/style.css", "assets/theme.js", "assets/site.js",
        ):
            page = page.replace(f'"{path}"', f'"../../{path}"')
        page = page.replace('class="inner-page"', 'class="inner-page research-note"', 1)
        page = page.replace("@@ARTICLE@@", body)
        (folder / output).write_text(page, encoding="utf-8")

    print(f"Rendered {len(PAGES)} medical GRPO article pages.")
