#!/usr/bin/env python
"""简历 PDF 验版：页数、每页填充率、首末行、关键词命中、PNG 预览。

用法:
    python check_pdf.py 简历.pdf --expect 2 --render
    python check_pdf.py 简历.pdf --expect 2 --absent "近 N 年" "个人优势"
"""
import argparse
import sys

try:
    import fitz  # PyMuPDF
except ImportError:
    sys.exit("需要 PyMuPDF：pip install pymupdf")

A4_H = 842.0  # pt


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--expect", type=int, default=0, help="期望页数，0 表示不检查")
    ap.add_argument("--absent", nargs="*", default=[],
                    help="本应已被删除的关键词，命中即失败")
    ap.add_argument("--require", nargs="*", default=[],
                    help="必须出现的关键词，缺失即失败")
    ap.add_argument("--render", action="store_true", help="输出 preview_p*.png 供目检")
    args = ap.parse_args()

    doc = fitz.open(args.pdf)
    pages = len(doc)
    ok = True

    print(f"文件: {args.pdf}")
    print(f"页数: {pages}" + (f"（期望 {args.expect}）" if args.expect else ""))
    if args.expect and pages != args.expect:
        ok = False
        print("  ✗ 页数不符 —— 见 references/layout-spec.md 的分页失衡排查顺序")

    for i, page in enumerate(doc, 1):
        blocks = [b for b in page.get_text("blocks") if b[4].strip()]
        if not blocks:
            print(f"  p{i}: 空白页 ✗")
            ok = False
            continue
        top = min(b[1] for b in blocks)
        bottom = max(b[3] for b in blocks)
        fill = bottom / A4_H * 100
        first = blocks[0][4].strip().splitlines()[0][:28]
        last = blocks[-1][4].strip().splitlines()[-1][:28]
        # 双页：首页应接近满页、末页不应太空；单页：整页填充 ≥75% 即可（单页简历本就留白）
        if pages == 1:
            bad = fill < 75
        else:
            bad = (i == 1 and fill < 90) or (i == pages and fill < 60)
        flag = "✗" if bad else "✓"
        print(f"  p{i}: 填充 {fill:5.1f}%  底边 {bottom:5.0f}pt  {flag}")
        print(f"       首: {first!r}")
        print(f"       末: {last!r}")
        if flag == "✗":
            ok = False
            print("       → 双页：首页 <90% 说明有整块被推到下一页，末页 <60% 说明内容不足；单页：<75% 说明太空")
        if args.render:
            page.get_pixmap(dpi=110).save(f"preview_p{i}.png")

    text = "".join(p.get_text() for p in doc)
    for kw in args.absent:
        hit = kw in text
        print(f"  {'✗' if hit else '✓'} 不应出现 {kw!r}: {'出现' if hit else '未出现'}")
        ok = ok and not hit
    for kw in args.require:
        hit = kw in text
        print(f"  {'✓' if hit else '✗'} 必须出现 {kw!r}: {'找到' if hit else '缺失'}")
        ok = ok and hit

    print("\n结果:", "通过" if ok else "未通过")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
