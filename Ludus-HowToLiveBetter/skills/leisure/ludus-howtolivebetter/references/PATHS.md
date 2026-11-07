# 路径与引用规则

## 根目录

本技能目录：

```text
<技能目录>/
├── SKILL.md
├── references/
│   ├── INDEX.md
│   ├── PATHS.md
│   └── _vendor/
│       ├── hltb/                 # 《高性价比人生指南》正文快照
│       └── hltb-enhancements/    # 失业/被裁增强
└── scripts/
    └── extract_ratio.py
```

## 路径映射

| 文档里写的 | 实际位置 |
|---|---|
| 书里的 `README.md` | `references/_vendor/hltb/README.md` |
| 书里的 `book/` | `references/_vendor/hltb/book/` |
| 书里的 `docs/` | `references/_vendor/hltb/docs/` |
| 书里的 `index.html` | `references/_vendor/hltb/index.html` |
| 增强项目的 `guides/` | `references/_vendor/hltb-enhancements/how-to-survive-unemployment/guides/` |
| 增强项目的 `playbooks/` | `references/_vendor/hltb-enhancements/how-to-survive-unemployment/playbooks/` |
| 增强项目的 `templates/` | `references/_vendor/hltb-enhancements/how-to-survive-unemployment/templates/` |

## 读取顺序

1. `references/INDEX.md`：先定位节或长文。
2. `references/_vendor/hltb/README.md`：看「这本书想回答的问题」表，确认节号。
3. `references/_vendor/hltb/book/`：读节正文；用 `search_files` 找 `^### ` 和关键词。
4. `references/_vendor/hltb/docs/`：读长文。
5. `references/_vendor/hltb-enhancements/how-to-survive-unemployment/`：只在失业/被裁场景补充。

## 网络

默认完全离线。只有正文文件缺失时，才用 `terminal` 浅克隆 `https://github.com/eternity4719/HowToLiveBetter.git`，或按节用 `web_extract` 取 `raw.githubusercontent.com` 文件。取不到就如实告诉用户，不要凭印象复述书的内容。

## 排序脚本

```bash
python scripts/extract_ratio.py
```

它只读取 `references/_vendor/hltb/index.html`，打印匹配 `COST_W` 和 `e.ratio` 的行。不要凭记忆写档位；没有输出就说明 `index.html` 缺失，改为只列成本标签。
