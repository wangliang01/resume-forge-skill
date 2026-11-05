# 导出与验版清单

`$SKILL_DIR` = 本 skill 的安装目录（如 `~/.claude/skills/resume-forge`、`~/.agents/skills/resume-forge`）。

## 一、导出命令

```bash
bash "$SKILL_DIR/scripts/export_pdf.sh" resume.html "我的简历-v1.0.pdf"
```

等价的裸命令（无脚本时用）：

```bash
"/c/Program Files/Google/Chrome/Application/chrome.exe" \
  --headless=new --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="out.pdf" "file:///C:/path/to/resume.html"
```

macOS：`"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"`。

## 二、Windows 上的三个坑

1. **中文输出路径会失败**：`--print-to-pdf="…\简历-v1.0.pdf"` 报 `Failed to write file … 拒绝访问 (0x5)`。
   解决：先输出 ASCII 名 `out.pdf`，再用 `mv` 改名。
2. **必须 `--no-pdf-header-footer`**，否则每页顶部/底部会印上 `file:///…` 和日期页码。
3. **`file:///` 三次斜杠 + 正斜杠路径**，中文目录可以直接用，只有输出路径有编码问题。

## 三、验版命令

```bash
python "$SKILL_DIR/scripts/check_pdf.py" "我的简历-v1.0.pdf" --expect 2 --render
```

脚本输出：页数、每页填充率、每页首行/末行文本、关键词命中、PNG 预览文件。

## 四、验收口径（全部通过才算完成）

| # | 检查 | 阈值 | 不过怎么办 |
|---|---|---|---|
| 1 | 页数 | == 期望值 | 见 `layout-spec.md` 排查顺序 |
| 2 | 第 1 页填充率 | ≥ 90%（单页 PDF ≥ 75%） | 有大块被整块推到下一页，微调字号/行高 |
| 3 | 末页填充率 | ≥ 60% | 内容不足，接受留白或删最弱项目 |
| 4 | 页首是否有孤立标题 | 无 | 看渲染出的 PNG，加 `break-after:avoid` |
| 5 | 已删除内容确实不存在 | grep 为 False | 内容改动没同步到 HTML |
| 6 | 占位符是否还在 | 人工确认 | 要么补数，要么明确告知用户保留 |

第 5 项常用关键词模式（按本次实际删除内容替换）：

```bash
python -c "import fitz;t=''.join(p.get_text() for p in fitz.open('简历.pdf'));print('近 N 年' in t, '个人优势' in t)"
```

或直接用脚本参数：

```bash
python "$SKILL_DIR/scripts/check_pdf.py" "我的简历-v1.0.pdf" --expect 2 --absent "近 N 年" "个人优势"
```

## 五、目检要点（渲染 PNG 后看）

1. 顶部：姓名与右侧岗位是否在同一基线；页眉双色分隔线是否水平；联系方式分隔符是否居中。
2. 正文：bullet 的短横标记是否与首行文字垂直居中对齐；中英混排行尾是否出现大洞。
3. 断页处：下一页第一个元素是否是完整项目（不是孤立标题、不是半条 bullet）。
4. 数字：所有 `→` 箭头两侧是否等距；时间轴年月是否左对齐成一列。
5. 末页：留白是否落在教育背景之后（合理），而不是落在中间（不合理）。

## 六、交付前最后一遍

- [ ] md、html、pdf 三个文件内容一致（改一处必须同步三处）
- [ ] 版本号已递增，旧 PDF 未被同名覆盖丢失（需要留档就先 `mv` 备份）
- [ ] 中间产物已清理（`out.pdf`、`preview_p*.png`）
- [ ] 向用户报告：改动摘要 + 实际页数与填充率数字 + 待补占位符 + 待确认口径
