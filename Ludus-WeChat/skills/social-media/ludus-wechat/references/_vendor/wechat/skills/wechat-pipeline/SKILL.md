---
name: wechat-pipeline
description: 微信公众号一条龙调度技能。把选题、写作、配图、排版、草稿上传串成可恢复的流程，适合 OpenClaw、Hermes、Claude Code、Codex 等能读取本地文件的 Agent。触发词：公众号一条龙、写并发布公众号、从选题到草稿、公众号全流程、wechat pipeline。
trigger-words: [公众号一条龙, 写并发布公众号, 从选题到草稿, 公众号全流程, wechat pipeline]
metadata:
  version: 1.0.0
  license: PolyForm-Noncommercial-1.0.0
---

# 微信公众号一条龙

## 这个技能解决什么

> 下文命令假设当前目录是本技能目录（`skills/wechat-pipeline`）。如果 Agent 的工作目录不同，把 `../` 换成本机实际的 `skills/` 根目录，或直接使用绝对路径。

用户只说一句“帮我写篇公众号并发到草稿箱”时，Agent 需要自己完成：

```
选题 → 写作 → 配图提示词 → 生成配图 → 排版 → 上传草稿 → 用户后台发布
```

本技能是调度入口。具体执行细节分别由三个子技能提供：

| 阶段 | 子技能 | 读取文件 |
|---|---|---|
| 选题 | wechat-topic-selector | `../wechat-topic-selector/SKILL.md` |
| 写作 | wechat-article-writer | `../wechat-article-writer/SKILL.md` |
| 发布 | wechat-publisher | `../wechat-publisher/SKILL.md` |

**不要凭记忆复述子技能内容**，执行到对应阶段时先读对应文件。

---

## 何时触发

- “公众号一条龙”“从选题到草稿”“写一篇并发布到公众号”
- “帮我找选题，然后写成文章发草稿箱”
- 用户同时提到“公众号”和“发布/草稿箱”，但没有指定只做某一步

只写文章不发：直接用 `wechat-article-writer`。
只排版发布：直接用 `wechat-publisher`。
只找选题：直接用 `wechat-topic-selector`。

---

## 前置检查（Stage 0）

> Windows 下把下文命令中的 `python3` 换成 `python`。

按顺序检查，缺什么补什么，不要跳过：

1. **Node.js 18+**：`node --version`（排版和发布脚本需要）
2. **Python 3.8+**：`python3 --version` 或 `python --version`（选题和配图脚本需要）
3. **依赖安装**：
   - 配图：`ZHIPU_API_KEY`（脚本使用标准库 HTTP）
   - 选题：无 Python 依赖；百度/CSDN 需要 `curl`；微博/GitHub 需要可选 `mcporter`
4. **公众号配置**：`WECHAT_APPID`、`WECHAT_APP_SECRET`，或 `skills/wechat-publisher/scripts/.wechat-config.json`
5. **图片配置**：`ZHIPU_API_KEY`，或可写的 `image.env`（不要放进 vendor）
6. **文章目录**：`WECHAT_ARTICLES_DIR`，未设置则用 `./articles`
7. **IP 白名单**：提醒用户把当前公网 IP 加入公众号后台白名单

配置示例见包裹根目录 `config/wechat.env.example`、`config/image.env.example`、`skills/wechat-article-writer/scripts/image.env.example`；实际 `image.env` 写到可写目录，不要放进 vendor。

---

## 产物与状态文件

所有产物放在 `ARTICLES_DIR`：

```
articles/
├── pipeline-state.json
├── YYYYMMDD_文章标题关键词.md
├── YYYYMMDD_文章标题关键词_配图提示词.md
├── YYYYMMDD_文章标题关键词.html
└── images/
    ├── cover.png
    ├── info1.png
    └── cta.png
```

`pipeline-state.json` 用于跨会话、跨 Agent 恢复：

```json
{
  "stage": "review",
  "direction": "AI 技术",
  "selected_topic": "选题标题",
  "title": "最终标题",
  "articles_dir": "C:/path/to/articles",
  "article_md": "C:/path/to/articles/20261105_xxx.md",
  "image_prompts": "C:/path/to/articles/20261105_xxx_配图提示词.md",
  "article_html": null,
  "images": [],
  "wechat_media_id": null,
  "updated_at": "2026-11-05T23:00:00+08:00"
}
```

规则：

- 每完成一个阶段就更新 `stage` 和时间。
- 路径写绝对路径，方便另一个 Agent 接手。
- 不要把 AppID/Secret/API Key 写进状态文件。
- 新会话接手时先读状态文件，不要从零重来。

`stage` 取值：`topic` → `writing` → `review` → `images` → `format` → `draft` → `done`。

---

## Stage 1：选题

**两种情况：**

### A. 用户已有明确主题

跳过热榜，直接进入写作阶段的 `01-topic.md`，把用户主题当作已确认选题。

### B. 用户只有方向

```bash
cd ../wechat-topic-selector
python3 topic_selector.py -d "AI 技术" --top 3 --output "<ARTICLES_DIR>/topic_results.json"
```

读取结果，向用户展示 3 个选题（标题、角度、匹配度、推荐理由），**等用户选一个**再进入下一阶段。

降级：`mcporter` 不可用时微博/GitHub 会跳过；知乎是示例数据。不要把这些平台失败当成整体失败。

---

## Stage 2：写作

读取 `../wechat-article-writer/SKILL.md`，严格按其六阶段执行：

1. 阶段 01 选题定位（用户已选主题则快速确认）
2. 阶段 02 标题优化：**必须给 5-10 个标题选项**，等用户选
3. 阶段 03 框架搭建：先给结构，等用户确认
4. 阶段 04 全文撰写：2500-3000 字
5. 阶段 05 保存：写入 `ARTICLES_DIR/YYYYMMDD_标题关键词.md`
6. 阶段 06 生成配图提示词：写入同目录 `_配图提示词.md`

写作风格从 `../wechat-article-writer/writing_style.md` 选择（7 种内置风格）。

**门禁：** 标题、框架、成稿三个点都要让用户确认，不要一口气写到底再问。

---

## Stage 3：成稿评审

把以下内容展示给用户：

- 最终标题
- 文章摘要（3 行以内）
- 字数
- 小节结构
- 配图提示词清单

询问：“可以进入配图和排版吗？需要改哪里？”

用户确认后更新 `stage=images`。

---

## Stage 4：配图

1. 读取 `_配图提示词.md`，转成 `prompts.jsonl`（每行一个 JSON：`id`、`size`、`prompt`）。
2. 先询问用户是否调用 API 生成图片（会产生费用）。
3. 用户确认后执行：

```bash
cd ../wechat-article-writer
python3 scripts/generate_images.py --input "<ARTICLES_DIR>/prompts.jsonl" --out "<ARTICLES_DIR>/images"
```

4. 检查输出：至少要有封面图；正文信息图 2-3 张；结尾引导图可选。
5. 失败重试：单张失败不影响其他张，记录失败项并告知用户，不要静默跳过。

没有图片 API 时，可以让用户手动提供图片，或跳过配图直接排版。

---

## Stage 5：排版

读取 `../wechat-publisher/SKILL.md` 的排版规范，然后：

```bash
cd ../wechat-publisher
node scripts/md-to-wechat-html.js --input "<ARTICLES_DIR>/文章.md" --output "<ARTICLES_DIR>/文章.html" --style warm
```

风格选择：

- 情感/故事/卡兹克文风 → `warm`
- 干货/教程/观点/深度长文 → `professional`
- 资讯日报 → `daily`
- 轻松幽默 → `lively`

转换后逐项检查：

- [ ] 没有 `<style`、`<h1`、class
- [ ] 没有意外的 `<ol`
- [ ] 图片 `src` 稍后会替换为微信图床 URL
- [ ] HTML < 2MB

---

## Stage 6：上传草稿

**这是外部副作用操作，执行前必须让用户明确确认。**

1. 获取 access_token（脚本会自动做）。
2. 上传正文图片到微信图床，替换 HTML 中的 `src`。
3. 提交草稿：

```bash
cd ../wechat-publisher
node scripts/upload-draft.js --html "<ARTICLES_DIR>/文章.html" --title "标题" --author "作者"
```

4. 记录返回的 `media_id` 到状态文件，更新 `stage=draft`。
5. 告诉用户：公众号后台 → 内容与互动 → 草稿箱 → 设置封面 → 预览 → 手动发布。

---

## Stage 7：完成

用户确认草稿无误后，把 `stage` 更新为 `done`。把最终产物路径列给用户。

**不要自动群发**，不要在用户未确认时点击发布。

---

## 失败处理

| 失败 | 处理 |
|---|---|
| `mcporter` 不存在 | 跳过微博/GitHub，使用百度/CSDN/知乎或用户提供素材 |
| 热榜抓取为空 | 让用户给主题，直接进入写作 |
| 图片 API 失败 | 保留提示词，重试单张；仍失败则让用户手动配图 |
| `40164 invalid ip` | 让用户把公网 IP 加入公众号白名单 |
| `40001 invalid credential` | 检查 AppSecret，必要时重置 |
| HTML 出现 `<ol>` | 回到 Markdown 修正行首“数字+点”，重新转换 |
| 内容超过 2MB | 压缩图片或拆分文章 |
| 草稿图片裂开 | 图片未替换为微信图床 URL，重新上传并替换 |

---

## 安全规则

- 不把 AppID/Secret/API Key 写入文章、状态文件或技能文档。
- 不把真实配置复制进可分享的包裹。
- 生成图片（有成本）和上传草稿（外部可见）前都要用户确认。
- 不自动发布，不伪造作者身份、头衔、业绩或数据来源。
- 用户要求“只写不发”时，到 Stage 3 结束即可。

---

## 给其他 Agent 的交接说明

本技能不依赖某个客户端的私有工具，只需要：

- 能读本地文件
- 能执行 `node` / `python`
- 能发起 HTTPS 请求（脚本内部完成）

接手时：

1. 读 `ARTICLES_DIR/pipeline-state.json`
2. 从 `stage` 继续，不要重复已完成阶段
3. 读对应子技能的 `SKILL.md`
4. 保持同样的用户确认点

如果当前 Agent 不支持技能自动发现，直接把本文件内容作为系统提示或任务说明加载即可。
