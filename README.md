# iris / 学习手记

浅色个人学习博客第一版。继续使用现有 `cppywh.github.io` 仓库，页面兼容 GitHub Pages。

此版本用于 GitHub Pages 发布。首页现有一篇真实的[中文医考后训练实验记录](research/medical-grpo/)，另有三篇排版示例。公开文章只使用脱敏后的文字、图和汇总数据；原始 notebook、逐题输出与权重不在仓库中。

## 本地预览

在此目录运行：

```powershell
python -m http.server 8765 --bind 127.0.0.1
```

打开 http://127.0.0.1:8765 。也可以直接打开 `index.html`；复制代码在部分浏览器中需要 localhost 安全上下文。

## 修改与重新生成

- `tools/build_site.py`：网站页面模板、文章入口和三篇示例文章。
- `research/medical-grpo/README.md`：这一项目的唯一公开笔记；`tools/render_research_note.py` 将它渲染为单篇网页。旧章节网址会跳到文中对应位置。
- `tools/requirements.txt`：渲染 Markdown 所需的 Python 依赖。
- `assets/style.css`：浅色主题与移动端样式。
- `assets/site.js`：分类、搜索、代码复制、目录高亮和阅读进度。
- `index.html`、`notes.html`、`about.html`：生成的页面。
- 三个 `*-notebook.html`：示例文章页。
- `404.html`：GitHub Pages 错误页。

修改模板或医学项目笔记后，在仓库目录执行：

```powershell
python -m pip install -r tools/requirements.txt
python tools/build_site.py
```

生成的 HTML 会在下次构建时被覆盖；请修改脚本或 Markdown 内容源。

## 后续发布

全站目前仍保留 `noindex,nofollow`。页面可通过链接访问，但不会主动请求搜索引擎收录；若以后决定开放索引，应在模板中统一调整并重新生成。

HTML/CSS/JS 已可直接由 GitHub Pages 托管，`.nojekyll` 用于按静态文件提供。发布前确认仓库 Pages 指向的分支和目录；部署沿用仓库已有的 GitHub Pages 设置。

这版是静态预览，没有登录、在线编辑器、评论或数据上传接口。


## iris 壁纸主题

站内名字为 iris（ywh → 鸢尾花），GitHub 链接仍保留真实账号。

`assets/theme.js` 将四张壁纸与浅色主题配对。首次访问随机选择，刷新消耗一个随机候选；一轮内不重复，下一轮不与上一张相同。站内导航保留当前主题，首页色点可手动选择，“换一张”无需刷新。使用 sessionStorage 仅保存当前标签页的主题及候选列表；如果浏览器禁用存储，仍能换主题，但跨刷新不重复的保证失效。

壁纸为用户提供的 Wallhaven 链接，原图本地保存，无远程图片 API 依赖，也不修改原图或署名：

- 6kqzl6：https://wallhaven.cc/w/6kqzl6 — 雕塑 / 雾紫
- kxp797：https://wallhaven.cc/w/kxp797 — 机械 / 冰蓝；来源页列出 Abdallah Talaat，原作：https://www.deviantart.com/abdallahtalat/art/Seraphim-Nexus-1148588696
- 837ymk：https://wallhaven.cc/w/837ymk — 几何 / 钴蓝
- w5m6yr：https://wallhaven.cc/w/w5m6yr — 晶体 / 湖青

来源记录不表示版权转让。四张壁纸按用户提供的链接选用，并随网站发布；页脚提供当前壁纸来源链接。
