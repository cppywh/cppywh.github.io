@echo off
chcp 65001 >nul
cd /d "%~dp0"
if exist ".venv\Scripts\python.exe" (
  ".venv\Scripts\python.exe" tools\publish.py
) else (
  python tools\publish.py
)
if errorlevel 1 (
  echo 上传失败，请查看上方错误。修改和提交均已保留。
) else (
  echo 推送完成，GitHub Pages 稍后更新网站。
)
pause
