# 公众号包路由表

## 阶段 → 技能

| 阶段 | 子技能 | 读取/运行 |
|---|---|---|
| 一条龙调度 | `wechat-pipeline` | `references/_vendor/wechat/skills/wechat-pipeline/SKILL.md` |
| 选题 | `wechat-topic-selector` | `references/_vendor/wechat/skills/wechat-topic-selector/SKILL.md` |
| 写作 | `wechat-article-writer` | `references/_vendor/wechat/skills/wechat-article-writer/SKILL.md` |
| 写作风格 | 七种内置风格 | `references/_vendor/wechat/skills/wechat-article-writer/writing_style.md` |
| 排版与草稿 | `wechat-publisher` | `references/_vendor/wechat/skills/wechat-publisher/SKILL.md` |

## 命令速查

| 动作 | 命令 |
|---|---|
| 选题 | `python references/_vendor/wechat/skills/wechat-topic-selector/topic_selector.py -d "方向" --top 3 --output "<ARTICLES_DIR>/topic_results.json"` |
| 配图 | `python references/_vendor/wechat/skills/wechat-article-writer/scripts/generate_images.py --input "<ARTICLES_DIR>/prompts.jsonl" --out "<ARTICLES_DIR>/images"` |
| 排版 | `node references/_vendor/wechat/skills/wechat-publisher/scripts/md-to-wechat-html.js --input "<ARTICLES_DIR>/文章.md" --output "<ARTICLES_DIR>/文章.html" --style warm` |

> 排版脚本的 `--style` 只接受 `warm|professional|daily|lively`；不要传写作风格编号。配图脚本自动读取 `<ARTICLES_DIR>/image.env`，也可 `--env-file`。
| 草稿上传（推荐包装器） | `python scripts/run_wechat.py --html "<ARTICLES_DIR>/文章.html" --title "标题" --author "作者"` |
| 草稿上传（直接脚本） | `node references/_vendor/wechat/skills/wechat-publisher/scripts/upload-draft.js --html "<ARTICLES_DIR>/文章.html" --title "标题" --author "作者" --config "<WECHAT_CONFIG>"` |

## 配置与模板

| 内容 | 文件 |
|---|---|
| 配置说明 | `references/_vendor/wechat/docs/CONFIG.md` |
| 公众号环境变量示例 | `references/_vendor/wechat/config/wechat.env.example` |
| 图片环境变量示例 | `references/_vendor/wechat/config/image.env.example` |
| 公众号配置文件模板 | `templates/wechat-config.example.json` |
| 路径与 cwd 契约 | `references/PATHS.md` |

## 排版增强

| 能力 | 文件 |
|---|---|
| 手机 390px 预览截图 | `references/_vendor/wechat-enhancements/wechat-article-pipeline/tools/capture_mobile_screenshot.py` |
| 长截图拼接 | `references/_vendor/wechat-enhancements/wechat-article-pipeline/tools/stitch_screenshot.py` |
| 公众号 HTML 渲染 | `references/_vendor/wechat-enhancements/wechat-article-pipeline/tools/render_wechat.py` |
| 公开输出脱敏 | `references/_vendor/wechat-enhancements/wechat-article-pipeline/tools/sanitize_public_output.py` |
| 增强说明 | `references/_vendor/wechat-enhancements/wechat-article-pipeline/README.md` |

增强工具只做二次检查，不替代上游 `wechat-pipeline` 的阶段与确认点。

## 非目标

- 不自动群发。
- 不做定时发布、素材库管理、刷量。
- 不伪造作者身份、头衔、业绩或数据来源。
- 不把 AppID/AppSecret/API Key 写进文章、状态文件或技能文档。
