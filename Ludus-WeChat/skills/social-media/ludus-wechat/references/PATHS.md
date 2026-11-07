# 路径、cwd 与配置契约

## 根目录

```text
<技能目录>/
├── SKILL.md
├── references/
│   ├── INDEX.md
│   ├── PATHS.md
│   └── _vendor/
│       ├── wechat/                      # 上游 5 个技能 + 配置 + 文档
│       └── wechat-enhancements/         # 排版增强
├── scripts/
│   └── run_wechat.py
└── templates/
    └── wechat-config.example.json
```

## 路径映射

| 上游文档里的路径 | 本包实际路径 |
|---|---|
| `skills/wechat-pipeline/` | `references/_vendor/wechat/skills/wechat-pipeline/` |
| `skills/wechat-topic-selector/` | `references/_vendor/wechat/skills/wechat-topic-selector/` |
| `skills/wechat-article-writer/` | `references/_vendor/wechat/skills/wechat-article-writer/` |
| `skills/wechat-publisher/` | `references/_vendor/wechat/skills/wechat-publisher/` |
| `config/` | `references/_vendor/wechat/config/` |

上游 `wechat-pipeline/SKILL.md` 假设“当前目录是本技能目录”。在本包里，凡是需要 cwd 的命令，先把 cwd 设为 `references/_vendor/wechat/`；或者按 `INDEX.md` 的命令使用从技能目录出发的相对路径。

## 配置路径

- `WECHAT_ARTICLES_DIR`：文章、配图、HTML、`pipeline-state.json` 的目录；建议设为工作区下的 `articles/`。
- `WECHAT_CONFIG`：公众号配置文件路径；必须是可写路径，不要放在 `references/_vendor/` 下。
- 推荐默认位置：
  - Windows：`%LOCALAPPDATA%/ludus-wechat/wechat-config.json`
  - macOS/Linux：`$XDG_CONFIG_HOME/ludus-wechat/wechat-config.json`，未设置时 `~/.config/ludus-wechat/wechat-config.json`
- `scripts/run_wechat.py` 会在未设置 `WECHAT_CONFIG` 时使用上述默认路径，并把 `--config` 传给 `upload-draft.js`。
- 配置模板：`templates/wechat-config.example.json`；复制后填写，不要把真实密钥提交到版本库。

## 环境变量

| 变量 | 用途 | 必填 |
|---|---|---|
| `WECHAT_APPID` | 公众号 AppID | 上传时必填 |
| `WECHAT_APP_SECRET` | 公众号 AppSecret | 上传时必填 |
| `WECHAT_AUTHOR` | 草稿作者名 | 可选 |
| `WECHAT_ARTICLES_DIR` | 文章/配图/HTML/状态文件目录 | 建议设置 |
| `WECHAT_CONFIG` | 自定义配置文件路径 | 可选 |
| `WECHAT_DEFAULT_STYLE` | 默认视觉风格 | 可选 |
| `WECHAT_SIGNATURE` | 文末落款 | 可选 |
| `ZHIPU_API_KEY` | 智谱 AI 图片生成密钥 | 配图时必填 |

## 安全规则

- 不把 AppID/AppSecret/API Key 写进文章、`pipeline-state.json`、技能文档或公开仓库。
- 不把真实 `.wechat-config.json` 复制进 `references/_vendor/`。
- 生成图片（有成本）和上传草稿（外部副作用）前必须得到用户明确确认。
- 只提交草稿，不自动群发。
