---
name: ludus-wechat
description: "公众号一条龙：选题、写作、配图、排版、上传草稿."
version: 1.0.0
author: WeChat Suite Contributors; Ludus extension packaging
license: PolyForm-Noncommercial-1.0.0
platforms: [windows, macos, linux]
metadata:
  ludus:
    tags: [wechat, official-account, writing, publishing, china]
    related_skills: []
---

# Ludus-WeChat Skill

把公众号的选题、写作、配图、排版和草稿上传串成一条可恢复的流水线。它只做到“草稿箱”：配图和上传前必须用户确认，永不自动群发；没有凭据时只做到排版，不假装发布成功。

## When to Use

- 用户说“公众号一条龙”“从选题到草稿”“写一篇并发布到公众号”。
- 用户要做公众号选题、标题、框架、成稿、配图提示词、HTML 排版或草稿上传。
- 用户要求按某种文风写公众号文章；内置 7 种风格，见写作技能的 `writing_style.md`。
- 不适用：自动群发、定时发布、素材库管理、刷量或伪造数据。

## Prerequisites

- Node.js 18+、Python 3.8+。
- 配图需要 `ZHIPU_API_KEY`；脚本用标准库 HTTP 调用智谱图片 API，无需额外 SDK。脚本会自动读取 `<ARTICLES_DIR>/image.env`（如果存在），也可 `--env-file` 指定。没有密钥就跳过配图或让用户手动提供图片。
- 上传草稿需要 `WECHAT_APPID`、`WECHAT_APP_SECRET`，并把当前公网 IP 加入公众号后台白名单。
- 建议设置 `WECHAT_ARTICLES_DIR`（文章/配图/HTML/状态文件目录）和 `WECHAT_CONFIG`（可写的配置文件路径，默认在用户配置目录，不在技能目录内）。
- 上游内容已随包分发：`references/_vendor/wechat/skills/`；配置说明见 `references/_vendor/wechat/docs/CONFIG.md`。

## How to Run

1. 读 `references/INDEX.md` 和 `references/PATHS.md`，确认 vendor 根和命令路径。
2. 按 `## Procedure` 的 Stage 0–7 执行；每个阶段结束更新 `<ARTICLES_DIR>/pipeline-state.json`。
3. 选题、写作、配图、排版用 `terminal` 运行对应脚本；读写文件用 `read_file`/`write_file`。
4. 上传草稿是外部副作用，必须再次确认；用 `scripts/run_wechat.py` 或显式传 `--config`，不要把真实密钥写进文章或状态文件。
5. 完成后告诉用户去公众号后台设置封面、预览、手动发布。

## Quick Reference

| 阶段 | 读取/运行 |
|---|---|
| 一条龙调度规则 | `references/_vendor/wechat/skills/wechat-pipeline/SKILL.md` |
| 选题 | `references/_vendor/wechat/skills/wechat-topic-selector/SKILL.md` |
| 写作六阶段 | `references/_vendor/wechat/skills/wechat-article-writer/SKILL.md` |
| 写作风格 | `references/_vendor/wechat/skills/wechat-article-writer/writing_style.md` |
| 排版与发布 | `references/_vendor/wechat/skills/wechat-publisher/SKILL.md` |
| 配置说明 | `references/_vendor/wechat/docs/CONFIG.md` |
| 配置模板 | `templates/wechat-config.example.json` |
| 排版增强（手机预览/长截图/校验） | `references/_vendor/wechat-enhancements/wechat-article-pipeline/README.md` |
| 路径与命令 | `references/PATHS.md` |

## Procedure

1. **Stage 0 预检（完成标准：Node/Python 版本、配置、文章目录、IP 白名单都已确认或明确缺失）**
   - `node --version`、`python --version`。
   - 配图：`ZHIPU_API_KEY`；上传：`WECHAT_APPID`/`WECHAT_APP_SECRET` 或 `WECHAT_CONFIG`。
   - 设置 `WECHAT_ARTICLES_DIR`；未设置就用 `./articles`，并告诉用户实际路径。
2. **Stage 1 选题（完成标准：用户已选定一个主题）**
   - 用户已有主题：直接用，进入 Stage 2。
   - 只有方向：运行
     `python references/_vendor/wechat/skills/wechat-topic-selector/topic_selector.py -d "方向" --top 3 --output "<ARTICLES_DIR>/topic_results.json"`
   - 展示 3 个选题（标题、角度、匹配度、理由），等用户选一个。
3. **Stage 2 写作（完成标准：标题、框架、成稿三个确认点都过了）**
   - 读 `references/_vendor/wechat/skills/wechat-article-writer/SKILL.md`，按其六阶段执行。
   - 标题必须给 5–10 个选项；框架先给结构；成稿 2500–3000 字；保存为 `<ARTICLES_DIR>/YYYYMMDD_标题关键词.md`；生成 `<ARTICLES_DIR>/YYYYMMDD_标题关键词_配图提示词.md`。
   - 写作风格从 `references/_vendor/wechat/skills/wechat-article-writer/writing_style.md` 选择（7 种内置风格）。
4. **Stage 3 成稿评审（完成标准：用户明确说可以进入配图和排版）**
   - 展示最终标题、3 行摘要、字数、小节结构、配图提示词清单。
   - 询问“可以进入配图和排版吗？需要改哪里？”；用户确认后更新 `stage=images`。
5. **Stage 4 配图（完成标准：用户确认费用后生成，或明确跳过）**
   - 读 `_配图提示词.md`，转成 `prompts.jsonl`（每行 `id`、`size`、`prompt`）。
   - 先问用户是否调用图片 API（会产生费用）；确认后运行
     `python references/_vendor/wechat/skills/wechat-article-writer/scripts/generate_images.py --input "<ARTICLES_DIR>/prompts.jsonl" --out "<ARTICLES_DIR>/images"`
   - 至少检查封面图；正文信息图 2–3 张；单张失败不影响其他张，记录失败项。
6. **Stage 5 排版（完成标准：HTML 通过检查清单）**
   - 运行
     `node references/_vendor/wechat/skills/wechat-publisher/scripts/md-to-wechat-html.js --input "<ARTICLES_DIR>/文章.md" --output "<ARTICLES_DIR>/文章.html" --style warm`
   - 风格：情感/故事/叙事 → `warm`；干货/教程/观点 → `professional`；资讯日报 → `daily`；轻松幽默 → `lively`。`--style` 只用这四个命名风格，不要传 `writing_style.md` 的 1–7 编号。
   - 检查：没有 `<style`、`<h1`、class；没有意外 `<ol>`；图片 `src` 稍后替换为微信图床 URL；HTML < 2MB。
   - 可选增强：读 `references/_vendor/wechat-enhancements/wechat-article-pipeline/README.md`，用手机预览/长截图/公开输出脱敏工具做二次检查。
7. **Stage 6 上传草稿（完成标准：用户明确确认，且拿到 media_id）**
   - 这是外部副作用，执行前必须再次确认。
   - 推荐用包装器（自动把 `WECHAT_CONFIG` 指到可写路径）：
     `python scripts/run_wechat.py --html "<ARTICLES_DIR>/文章.html" --title "标题" --author "作者"`
   - 或直接运行
     `node references/_vendor/wechat/skills/wechat-publisher/scripts/upload-draft.js --html "<ARTICLES_DIR>/文章.html" --title "标题" --author "作者" --config "<WECHAT_CONFIG>"`
   - 记录返回的 `media_id` 到状态文件，更新 `stage=draft`。
   - 失败对照：`40164 invalid ip` → 公网 IP 加白名单；`40001 invalid credential` → 检查 AppSecret。
8. **Stage 7 完成（完成标准：用户确认草稿无误，stage=done）**
   - 告诉用户：公众号后台 → 内容与互动 → 草稿箱 → 设置封面 → 预览 → 手动发布。
   - 列出最终产物路径；不自动群发。

## Pitfalls

1. **自动群发。** 本技能只提交草稿；发布动作永远由用户在公众号后台完成。
2. **把密钥写进文章/状态文件。** AppID、AppSecret、API Key 只放环境变量或 `WECHAT_CONFIG`；状态文件只记路径和 `media_id`。
3. **默认配置写进技能目录。** `upload-draft.js` 默认读写 `__dirname/.wechat-config.json`；在 `references/_vendor/` 下不可写。用 `scripts/run_wechat.py` 或显式 `--config` 指到 `WECHAT_ARTICLES_DIR`/用户配置目录。
4. **HTML 出现 `<ol>`。** 回到 Markdown 修正行首“数字+点”，重新转换。
5. **图片裂开。** 草稿里的图片必须先上传到微信图床并替换 `src`；直接引用本地路径会裂。
6. **伪造作者/头衔/数据。** 不冒充作者本人，不编造业绩、案例或数据来源。
7. **没有凭据却声称上传成功。** 没有 AppID/Secret/IP 白名单时，停在 Stage 5，如实说明。

## Verification

- [ ] Stage 0 的 Node/Python、配置、文章目录、IP 白名单已确认或明确缺失。
- [ ] 标题、框架、成稿三个确认点都有用户确认记录。
- [ ] 配图前已确认费用；没有 `ZHIPU_API_KEY` 时已跳过或让用户手动配图。
- [ ] HTML 不含 `<style`、`<h1`、class 或意外 `<ol>`；小于 2MB。
- [ ] 上传前已得到用户明确确认；配置路径可写；密钥没有写进文章/状态文件。
- [ ] 已记录 `media_id`；已告诉用户去后台手动发布。
- [ ] 没有自动群发，没有伪造作者/头衔/数据。

## Boundaries

- 只提交草稿，不支持自动群发、定时发布、素材库管理。
- 选题里的知乎条目是示例数据，不保证实时；微博/GitHub 依赖可选的 `mcporter`，不可用时跳过。
- 百度/CSDN 通过 Jina Reader 抓取，网络异常时可能返回 0 条；此时让用户直接给主题。
- 配图脚本只依赖 Python 标准库和 `ZHIPU_API_KEY`；上传脚本依赖公众号 API 和 IP 白名单。
- 许可：本包原创内容 PolyForm Noncommercial 1.0.0；`wechat-publisher` 为 ISC；`wechat-article-writer` 为本包自写 PolyForm NC 实现，不包含上游无许可证版本。详见 `references/_vendor/wechat/THIRD-PARTY-NOTICES.md`。
