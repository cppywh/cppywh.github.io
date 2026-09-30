// Markdown数学插件先保护LaTeX，再由本地KaTeX渲染；代码块不参与。
document.addEventListener("DOMContentLoaded", () => {
  if (!window.katex) return;
  document.querySelectorAll(".prose .math").forEach(element => {
    const source = element.textContent;
    try {
      katex.render(source, element, {
        displayMode: element.classList.contains("block"),
        throwOnError: true, trust: false, strict: "ignore"
      });
    } catch (error) {
      element.classList.add("math-error");
      element.title = "公式渲染失败：" + error.message;
      console.error("Formula render failed", error);
    }
  });
});
