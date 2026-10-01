# 文献架维护

文献目录数据保存在 `catalog.json`，PDF 当前保留在网站根目录，不复制原文件。

添加论文时：

1. 将 PDF 放入网站（以后可集中放在 `literature/pdfs/`）。
2. 在 `catalog.json` 添加一项，填写唯一的英文 `id`、简称 `name`、完整 `title`、相对于网站根目录的 `file`、`pages`、`tags` 和阅读状态 `status`。
3. 在网站根目录运行 `.\.venv\Scripts\python.exe tools/build_site.py`。
4. 检查 `literature.html` 和对应阅读页面。双击网站根目录的 `上传网站.cmd`，或者运行 `.\.venv\Scripts\python.exe tools/publish.py`，即可构建、提交并推送全部网站更新（包含新 PDF）。

`tools/build_literature.py` 是构建模块，直接运行不会上传。只检查构建、不提交或推送可运行 `.\.venv\Scripts\python.exe tools/publish.py --check`。上传脚本失败时保留所有修改和已有提交，修复错误后可再次运行。

阅读状态由自己维护，例如“待读”“阅读中”“已读”。论文阅读笔记编辑 `reading/llm-quantization/LLM Quantization.md`，与 PDF 分开保存。

公开发布后 PDF 可被访问和下载；只收录可以公开分享的文件。
