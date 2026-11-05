# Resume Forge · 中文简历 agent skill

一个可安装的 [Agent Skill](https://agentskills.io)：装上之后，你的 AI 编码 agent 会写中文简历、会套 A4 排版、会自己导出 PDF 并**验页数**，而不是给一份"看起来很专业"的 Markdown 让你自己排版。

内置 4 套 A4 模板（单页 / 双页、彩色 / 黑白）、Chrome 导出脚本、PDF 验版脚本，以及简历写作规则。适用于 Claude Code、Codex、Cursor、Pi、Freebuff、OpenCode、Gemini CLI 等所有支持 Agent Skills 的工具。

```text
你：帮我把这份简历按这个 JD 改一版，出 PDF
agent：审计问题清单 → 重写正文（不新增事实）→ 套模板 → 导出 → 报页数与填充率
```

## 安装

```bash
# 全局装（推荐，所有项目可用；会提示你选装到哪些 agent）
npx skills add wangliang01/resume-forge-skill -g

# 只装到 Claude Code
npx skills add wangliang01/resume-forge-skill -a claude-code -g

# 装进当前项目（.claude/skills/ 或 .agents/skills/，可随仓库共享）
npx skills add wangliang01/resume-forge-skill
```

仓库名是 `resume-forge-skill`，装进去的 skill 名是 **`resume-forge`**，所以落地目录是 `…/skills/resume-forge/`。

`npx skills add` 需要 Node.js 22+，支持 70+ 个 agent（完整清单见 [vercel-labs/skills › docs/agents.md](https://github.com/vercel-labs/skills/blob/main/docs/agents.md)）。

**手动安装**（不想用 npx，或工具不在清单里）：把 `skills/resume-forge/` 整个目录复制到对应位置即可——一个 skill 就是一个含 `SKILL.md` 的目录。

| 工具 | 全局目录 | 项目目录 |
|---|---|---|
| Claude Code | `~/.claude/skills/resume-forge/` | `.claude/skills/resume-forge/` |
| Codex、Pi、Cursor、Freebuff、Gemini CLI、Copilot、Amp、OpenCode 等 | `~/.agents/skills/resume-forge/` | `.agents/skills/resume-forge/` |
| 其他（Kiro、Goose、Windsurf …） | 各自 `*/skills/` 目录 | 同左 |

```bash
git clone https://github.com/wangliang01/resume-forge-skill.git /tmp/rf
mkdir -p ~/.agents/skills && cp -r /tmp/rf/skills/resume-forge ~/.agents/skills/
```

**完全不支持 skills 的老工具**：把 `SKILL.md` 的内容贴进 `AGENTS.md` / `CLAUDE.md`，并把 `references/`、`scripts/`、`assets/` 放在同目录下，然后把文中 `$SKILL_DIR` 换成实际路径。语义一样，只是少了按需加载。

装完你可以先说一句「列出可用的 skill」确认 agent 认到了它。

## 装上之后怎么用

直接说人话，触发词已经写进 skill 的 description：

| 你说 | 它会做 |
|---|---|
| 「优化我的简历，出一版 PDF」 | 建事实表 → 审计 → 重写 → 套 `classic` → 导出 → 验版 |
| 「按这个 JD 改简历，投的是资深前端」 | 按 JD 调关键词与项目重点，只改文案不动事实 |
| 「简历导出成 3 页了，第 3 页只有两行」 | 按分页排查顺序调字号 / 行高 / 断页，重导并报填充率 |
| 「给我一个中文简历模板，我自己填」 | 直接给 `assets/templates/<style>/index.html` 并说明怎么改 |

它会遵守的硬规矩（写在 `SKILL.md` 的铁律里）：**不编造项目和数据、指标只搬不改、不写自我评价、平台专属文案不进简历**；缺的事实标 `.todo` 占位符留给你补。

## 它替你做什么

| 步骤 | 产出 / 硬指标 |
|---|---|
| 1 建事实表 | 年限、头衔、团队规模、公司性质的来源与冲突逐条列出 |
| 2 审计 | 一句话结论 + 3~6 个"为什么会被刷 + 怎么改" |
| 3 选模板 | 从 4 套里按经验年限和投递方向选，说明理由 |
| 4 重写正文 | 结构固定：概述 → 核心能力 → 核心项目 → 工作经历 → 教育 |
| 5 自审 | 每个数字回原文找出处，编造的直接删 |
| 6 套模板 | 只换 `<body>` 文字，不动 CSS |
| 7 导出 PDF | Chrome headless，自动处理中文路径与页眉页脚 |
| 8 验版 | 页数 == 期望；首页填充 ≥ 90%、末页 ≥ 60%；无孤立标题；已删内容确不存在 |

验版用的是 `scripts/check_pdf.py`：它把每页渲染成 PNG 并算填充率，页数或留白不对就直接判失败，agent 必须调完再交。**没有跑过验版的 PDF 不算交付。**

## 模板

| 模板 | 风格 | 页数 | 适合 |
|---|---|---|---|
| **[classic](skills/resume-forge/assets/templates/classic/index.html)** | 单栏 · 深松石绿 | 2 页 | 5~15 年技术岗，通用投递，最稳 |
| **[mono](skills/resume-forge/assets/templates/mono/index.html)** | 黑白极简 · 无彩色 | 2 页 | 黑白打印、外企、设计感团队 |
| **[navy](skills/resume-forge/assets/templates/navy/index.html)** | 藏青页眉色块 · 双栏技能 | 2 页 | 大厂 / 管理岗 / 想让简历"重"一点 |
| **[sidebar](skills/resume-forge/assets/templates/sidebar/index.html)** | 左信息栏 · 双栏 | 1 页 | 3~8 年经验，一页交代完 |

<p>
  <img src="previews/classic-p1.png" width="24%" alt="classic 模板第 1 页">
  <img src="previews/mono-p1.png" width="24%" alt="mono 模板第 1 页">
  <img src="previews/navy-p1.png" width="24%" alt="navy 模板第 1 页">
  <img src="previews/sidebar-p1.png" width="24%" alt="sidebar 模板第 1 页">
</p>

第二页（含断页效果）：[classic-p2](previews/classic-p2.png) · [mono-p2](previews/mono-p2.png) · [navy-p2](previews/navy-p2.png)

样例 PDF 在 [`samples/`](samples)：classic 2 页（94.5% / 81.3%）、mono 2 页（94.2% / 64.3%）、navy 2 页（94.6% / 66.8%）、sidebar 1 页（87.2%）。

> 模板里的姓名、公司、数据全部是虚构示例（陈思远 / 星岸科技 / 云际数据），仓库里没有任何真实个人信息。

## 目录结构

```text
skills/resume-forge/
├── SKILL.md                                  入口：铁律、9 步流程、决策点
├── references/
│   ├── rewrite-rules.md                      简历结构、bullet 句型、禁止项、诚实口径
│   ├── layout-spec.md                        排版规格与分页调参手册
│   ├── verify-checklist.md                   导出验收清单与常见故障
│   └── template-guide.md                     给人看的手册：改内容 / 调密度 / 换配色 / 打印
├── scripts/
│   ├── export_pdf.sh                         Chrome headless 导出（macOS / Linux / Windows）
│   └── check_pdf.py                          页数 / 填充率 / 关键词 / PNG 预览
└── assets/templates/{classic,mono,navy,sidebar}/index.html
samples/*.pdf                                  每套模板导出的完整样例
previews/*.png                                 README 预览图
```

`SKILL.md` 只讲流程，细节按需读 `references/`——这是 skills 的渐进加载约定，agent 不会一上来吞掉几万字。

## 不用 agent 也能用

模板就是纯 HTML + CSS，零构建：

```bash
cp skills/resume-forge/assets/templates/classic/index.html 我的简历.html
# 改 <body> 里的文字，然后：
bash skills/resume-forge/scripts/export_pdf.sh 我的简历.html 我的简历.pdf
python skills/resume-forge/scripts/check_pdf.py 我的简历.pdf --expect 2 --render
```

浏览器手动导出：Chrome 打开 → `Ctrl/Cmd + P` → 另存为 PDF → 边距「默认」→ 勾选「背景图形」→ 缩放 100% → 关掉页眉页脚。

## 常见问题

| 现象 | 原因 | 解决 |
|---|---|---|
| `npx skills add` 装完只有 `SKILL.md`，没有脚本和模板 | 仓库把 `SKILL.md` 放在根目录，CLI 会当成单文件 skill | 本仓库用 `skills/resume-forge/` 布局，正常安装是整目录 |
| agent 认不到 skill | 装到了别的 agent 目录 | `npx skills add wangliang01/resume-forge-skill -a claude-code`，或确认目录里有 `SKILL.md` |
| 导出成 3 页，第 3 页只有几行 | 字号/行高偏大，或边距叠加 | 调 `--base-pt` / `--lh`，见 `template-guide.md`「调密度与页数」 |
| 第 1 页底部大片空白 | 某个项目被整块推到下一页 | 把 `.item` 的 `break-inside` 设成 `auto`（模板默认） |
| 色块 / 左侧栏打印不出来 | 没勾「背景图形」 | 勾选 `Background graphics` |
| 导出报「拒绝访问 (0x5)」 | Chrome 不接受中文输出路径 | 用 `scripts/export_pdf.sh`，或先输出 `out.pdf` 再改名 |
| 换了电脑页数变了 | 中文 fallback 字体不同 | 装 [Noto Sans SC](https://fonts.google.com/noto/specimen/Noto+Sans+SC)，或接受字宽差异 |
| Codex 里看不到 skill | 需要开 skills 特性 | `codex --enable skills`（实验特性） |

## English

Resume Forge is an installable agent skill for building Chinese-language resumes: audit → rewrite → apply one of four A4 templates → export PDF via headless Chrome → verify page count and page fill ratio. Install with `npx skills add wangliang01/resume-forge-skill -g` (Claude Code, Codex, Cursor, Pi, Freebuff, and 70+ other agents), or copy `skills/resume-forge/` into your agent's skills directory. Sample persona data is fictional. MIT licensed.

## License

[MIT](LICENSE)。模板与脚本可自由商用、修改、二次分发，无需署名。
