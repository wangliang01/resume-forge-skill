#!/usr/bin/env bash
# 导出 A4 简历 PDF（Chrome headless），处理 Windows 中文路径与页眉页脚问题。
# 用法: bash export_pdf.sh <输入.html> <输出.pdf>
set -euo pipefail

IN="${1:?用法: export_pdf.sh <输入.html> <输出.pdf>}"
OUT="${2:?用法: export_pdf.sh <输入.html> <输出.pdf>}"
[ -f "$IN" ] || { echo "输入文件不存在: $IN" >&2; exit 1; }

# ---------- 定位 Chrome ----------
CHROME="${CHROME:-}"
if [ -z "$CHROME" ]; then
  for c in \
    "/c/Program Files/Google/Chrome/Application/chrome.exe" \
    "/c/Program Files (x86)/Google/Chrome/Application/chrome.exe" \
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
    "$(command -v google-chrome || true)" \
    "$(command -v chromium || true)" \
    "$(command -v chrome || true)"
  do
    [ -n "$c" ] && [ -x "$c" ] && CHROME="$c" && break
  done
fi
[ -n "$CHROME" ] || { echo "找不到 Chrome，请用 CHROME=/path/to/chrome 指定" >&2; exit 1; }

# ---------- 路径转 file:// URL ----------
# Windows/Git Bash 下 /c/Users/... 或 /tmp/... 都不是 Chrome 能解析的路径，
# 先用 cygpath 转成 C:/Users/... 形式再拼 file:///
to_native() {
  if command -v cygpath >/dev/null 2>&1; then
    cygpath -m "$1"
  else
    printf '%s' "$1"
  fi
}
abs_in="$(cd "$(dirname "$IN")" && pwd)/$(basename "$IN")"
native_in="$(to_native "$abs_in")"
url="file:///${native_in#/}"
# 中文与空格：Chrome 接受未编码路径，仅把空格转义
url="${url// /%20}"

# ---------- 输出到 ASCII 临时名再改名 ----------
# Chrome 的 --print-to-pdf 不接受中文输出路径（报 拒绝访问 0x5）
out_dir="$(cd "$(dirname "$OUT")" && pwd)"
tmp="$out_dir/.forge_tmp_$$.pdf"
rm -f "$tmp"

if ! "$CHROME" --headless=new --disable-gpu --no-pdf-header-footer \
      --print-to-pdf="$(to_native "$tmp")" "$url" >/dev/null 2>&1; then
  : # Chrome 有时返回非零但已写出文件，统一在下面按文件存在性判断
fi

[ -f "$tmp" ] || { echo "导出失败：未生成 PDF" >&2; echo "  HTML: $url" >&2; echo "  Chrome: $CHROME" >&2; exit 1; }

mv -f "$tmp" "$OUT"
echo "已导出: $OUT ($(wc -c < "$OUT" | tr -d ' ') bytes)"
