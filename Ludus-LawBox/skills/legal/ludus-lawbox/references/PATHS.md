# 路径、cwd 与环境变量

## 根目录

```text
<技能目录>/
├── SKILL.md
├── references/
│   ├── INDEX.md
│   ├── PATHS.md
│   └── _vendor/
│       ├── lawbox/                  # LawBox 上游快照（保留 skills/legal 原始深度）
│       └── cn-law-hub/              # 法规/案例在线核验增强
└── scripts/
    └── show_vendor_paths.py
```

## 关键映射

| LawBox 文档里写的 | 本包实际位置 |
|---|---|
| `skills/legal/...` | `references/_vendor/lawbox/skills/legal/...` |
| 根 `SKILL.md` | `references/_vendor/lawbox/upstream-root-SKILL.md` |
| `knowledge/lessons.md` | `references/_vendor/lawbox/knowledge/lessons.md` |
| `LICENSE` | `references/_vendor/lawbox/LICENSE` |
| `THIRD_PARTY_NOTICES.md` | `references/_vendor/lawbox/THIRD_PARTY_NOTICES.md` |

## 脚本为什么不用改路径

上游脚本从脚本文件本身推导目录。以 `法律文书出稿前审查/scripts/preflight_check.py` 为例：

```python
LEGAL_DIR = Path(__file__).resolve().parents[2]
```

如果脚本位于：

```text
<技能目录>/references/_vendor/lawbox/skills/legal/法律文书出稿前审查/scripts/preflight_check.py
```

那么：

- `parents[0]` = `scripts`
- `parents[1]` = `法律文书出稿前审查`
- `parents[2]` = `skills/legal`

正好是上游期望的 `LEGAL_DIR`。`LEGAL_DIR.parents[1]` 则是 `references/_vendor/lawbox`，也就是上游仓库根。因此**保留 `skills/legal/<子技能>/scripts/` 的原始深度即可，不要重排目录**。

## cwd 契约

- 运行任何接收相对路径的 LawBox 脚本时，把 cwd 设为 `references/_vendor/lawbox/`，或显式传绝对路径。
- 用户事项工作区通过 `LEGAL_WORKSPACE` 指定；不要用技能目录或 vendor 根当用户工作区。
- 正式交付物应放在用户工作区的业务文件区，系统记录放在 `_系统记录/`；`.cache` 只能当临时目录。

## 环境变量

| 变量 | 用途 | 建议 |
|---|---|---|
| `LEGAL_WORKSPACE` | 用户事项根目录 | 必设；脚本默认 `.` |
| `LEGAL_CURRENT_MATTER` | 当前事项文件 | 可选；默认 `_系统记录/当前事项.md` |
| `LEGAL_TEMPLATE_REGISTRY` | 模板登记表 | 可选 |
| `LEGAL_TEMPLATE_CLONE_MANIFEST` | 模板克隆清单 | 可选 |
| `LEGAL_CONTRACT_TEMPLATE_ROOT` | 合同模板根 | 可选 |
| `LEGAL_QC_PYTHON` | QC 使用的 Python | 可选 |
| `LEGAL_ALLOW_LEGACY_DOCX` | 允许旧版 DOCX 生成 | 默认不要开启 |

## 可选依赖

| 子技能/脚本 | 依赖 | 缺失时 |
|---|---|---|
| 正式 `.docx` 导出 | `python-docx` | 不能导出正式 Word；只出 HTML/草稿 |
| PDF 材料处理 | `pymupdf` | 不能读 PDF；让用户转文本或装依赖 |
| 法条转 Markdown / OCR | MinerU 或外部 OCR | 自动 OCR 不可用；手工粘贴或装依赖 |
| 法规/案例在线核验 | `cn-law-hub` 的 Python 依赖 + 网络 | 回退 `web_search`/`web_extract`，标未核验 |
| 旧版 DOCX 生成 | Node `docx` 包 | 不使用；走 `html_to_docx.py` |

## 增强项目

`references/_vendor/cn-law-hub/` 是 Apache-2.0 的可选法规/案例检索层：

- 读 `references/_vendor/cn-law-hub/SKILL.md` 了解命令和来源。
- 依赖见 `references/_vendor/cn-law-hub/requirements.txt`。
- 许可与 NOTICE 见 `references/_vendor/cn-law-hub/LICENSE`、`references/_vendor/cn-law-hub/NOTICE`。
- 不可用或失败时，不要假装核验完成；回退到 `web_search`/`web_extract` 并记录缺口。
