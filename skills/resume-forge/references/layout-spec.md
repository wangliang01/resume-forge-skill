# 排版规格与分页调参手册

## 一、基线规格

| 项 | 值 | 说明 |
|---|---|---|
| 纸张 | A4 210×297mm | `@page{ size:A4; margin:13mm 15mm 12mm }` |
| 容器 | 单一流式 `<div class="page">` | **不要**用多个 `.page` 写死分页 |
| 正文字号 | 9.5pt | 9.2pt 以下中文会糊成一团，10pt 以上容易溢出 3 页 |
| 行高 | 1.68 | 1.72 以上 2 页内容会变 3 页 |
| 姓名 | 23pt / 700 / 字距 .18em | 字距是中文姓名的主要气质来源 |
| 区块标题 | 10.5pt / 700 / 字距 .12em | 标题后接 flex 细线，避免"标题+横线"画歪 |
| 项目标题 | 10.2pt / 700 | 与正文差 0.7pt 足够，靠字重区分 |
| 时间 | 8.2pt / 700 / 主色 / tabular-nums | 数字等宽，时间轴才对齐 |
| 主色 | `#14655f`（深松石） | 单强调色；要纯黑白版就把 `--accent` 改成 `--ink` |
| 分隔线 | `#dfe3e8` / 1px | 只用细线，不用投影和色块 |
| 项目间距 | `margin-bottom:9pt` | 段落呼吸感的唯一来源 |

## 二、打印与屏幕双轨

```css
@page{ size:A4; margin:13mm 15mm 12mm; }
@media print{
  html,body{ background:#fff; }
  .page{ width:auto; padding:0; margin:0; background:#fff; }
}
@media screen{ body{ padding:10mm 0; } .page{ box-shadow:0 2px 14px rgba(20,30,40,.12); } }
```

**关键**：屏幕上的纸张宽度/内边距必须归零，让 `@page` 独占边距控制，否则两份边距叠加，第一页顶部会被吃掉。

## 三、断页控制

```css
.item           { break-inside:avoid; }   /* 一个项目不被劈成两半 */
.sec-title      { break-after:avoid; }    /* 标题不留在页底做孤儿 */
ul.bullets li   { break-inside:avoid; }   /* 单条 bullet 不被劈开 */
```

`break-after:avoid` 只对"标题紧跟的下一个块"生效，Chrome 支持有限，所以**永远要在 PDF 里目检页首**，不能只信 CSS。

## 四、分页失衡排查顺序

现象：页数不对，或某页底部大片空白。**一次只改一个变量，改完重新导出验版。**

1. **第 1 页 < 90% 填充** → 说明有个大块（通常是某个项目 `break-inside:avoid`）整块被推到下一页。
   - 首选：略降字号（9.6 → 9.5pt）或行高（1.72 → 1.68）；
   - 次选：缩短该项目的一句话描述；
   - 不要：去掉该项目的 `break-inside:avoid`（会劈开项目，比留白更难看）。
2. **多出第 3 页且内容不足 10%** → 说明还在用写死的 `.page` 硬分页，或 `.page` 上仍有 padding 与 `@page` 叠加。改成单一流式容器。
3. **末页 < 60%** → 内容量约 1.5 页。两个正当选择：接受留白（推荐，末页留白是常态），或删掉最弱的一个项目；不要加"兴趣爱好"填空。
4. **标题落在页底** → 给 `.sec-title` 加 `break-after:avoid`，仍不行则把该 section 整体 `break-inside:avoid`。
5. **中英文混排 justify 拉出大空隙** → 给正文 `letter-spacing:.005em`，或对短段落放弃 justify。

实测参考（2 页版，12 年经验，约 1.7 页内容量）：

| 字号/行高 | 结果 |
|---|---|
| 9.5pt / 1.68 | 2 页，p1 95%，p2 70% ✅ |
| 9.8pt / 1.72 | 2 页，但 p1 82%、p2 95%（大块被推到 p2）❌ |
| 9.5pt / 1.66 + 写死 `.page` | 3 页（第三页 4% 空壳）❌ |

结论：字号不是越大越好，**页面填充均衡**比字号绝对大小更影响"是否专业"。

## 五、字体

```css
font-family:"Noto Sans SC","Microsoft YaHei","Segoe UI",sans-serif;
```

- 中文优先 Noto Sans SC（思源黑体），其次微软雅黑；Windows 上两者字宽差异会改变行数，换机器一定要重导 PDF。
- 不引入 webfont（headless 导出时网络请求不稳定）。
- `-webkit-font-smoothing:antialiased` 让屏幕预览更接近 PDF 观感。

## 六、视觉层级预算

一份简历最多 3 层强调，超出就变花：

1. 主色 + 字重（项目标题、关键数字）
2. 灰阶（次要信息 `#5a636f`、极弱信息 `#8d959f`）
3. 结构（细线、时间轴、圆角标签）

禁止：多色强调、渐变底、图标堆砌、表格式技能条、色块分区。
