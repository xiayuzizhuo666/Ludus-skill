# 中国会计准则财务技能包

基于中国《小企业会计准则》《企业会计准则》和中国注册会计师审计准则（CAS）整理的可移植技能包，覆盖**准则选择 → 记账理账 → 报表 → 税务 → 审计**的完整流程。

- 上游来源：https://github.com/kylin985ti/china-accounting-skills
- 上游快照：`main @ 9ace803`
- 上游许可：MIT © 2026 kylin985ti
- 本包版本：`1.0.0`

## 包含内容

- **25 个上游技能**：11 个记账理账、12 个审计、2 个参考资料
- **1 个总入口技能** `china-accounting`：先判断企业画像，再路由到对应子技能
- **安装器与校验器**：`install.mjs`、`validate.mjs`
- **文档与模板**：安装说明、使用说明、空白会计总账模板
- 上游技能正文未修改，仅做目录扁平化和打包适配

## 技能清单

### 记账理账（11）

| 技能 | 功能 |
|---|---|
| `accounting-framework` | 判断适用小企业会计准则还是企业会计准则 |
| `chart-of-accounts` | 小企业 66 科目 / 企业准则 167 科目 |
| `journal-entry` | 编制记账凭证、借贷平衡校验 |
| `month-end-close` | 月末计提、摊销、结转、对账、结账 |
| `balance-sheet` | 资产负债表（两套准则版本） |
| `profit-loss` | 利润表（两套准则版本） |
| `cash-flow` | 现金流量表 |
| `gross-net-margin` | 毛利率、净利率、营业利润率分析 |
| `vat-accounting` | 增值税、价税分离、进项抵扣、数电发票 |
| `income-tax` | 企业所得税、预缴、汇算清缴、递延所得税 |
| `individual-tax` | 个人所得税、工资代扣、经营所得 |

### 审计（12）

| 技能 | 功能 |
|---|---|
| `audit-master` | 审计项目总控、全流程编排 |
| `risk-assessment` | 风险评估、重大错报风险 |
| `materiality` | 重要性水平计算 |
| `cash-audit` | 货币资金实质性程序 |
| `receivables-audit` | 应收账款实质性程序 |
| `inventory-audit` | 存货实质性程序 |
| `fixed-assets-audit` | 固定资产实质性程序 |
| `payables-audit` | 应付账款实质性程序 |
| `revenue-audit` | 收入实质性程序 |
| `expenses-audit` | 费用实质性程序 |
| `audit-adjustments` | 审计调整分录 |
| `audit-report` | 审计报告、意见类型 |

### 参考资料（2）

| 技能 | 功能 |
|---|---|
| `coa-reference` | 两套准则科目表双向对照 |
| `tax-rates-reference` | 2025-2026 常用税率速查 |

完整描述见 `manifest.json`。

## 安装

```bash
node install.mjs --list
node install.mjs --agent claude
node install.mjs --agent openclaw
node install.mjs --agent hermes
node install.mjs --agent codex
node install.mjs --agent opencode
node install.mjs --target "/path/to/skills"
```

安装器会复制 `skills/` 下的所有目录；目标已存在同名技能时默认备份为 `<name>.bak-<时间戳>`。

### 各 Agent 默认目录

| Agent | 默认目录 |
|---|---|
| OpenClaw | `~/.openclaw/workspace/skills/` |
| Claude Code | `~/.claude/skills/` |
| Codex | `~/.codex/skills/` |
| Hermes（Windows） | `%LOCALAPPDATA%\hermes\skills\` |
| Hermes（macOS/Linux） | `~/.local/share/hermes/skills/` |
| OpenCode | `~/.config/opencode/skills/` |

其他 Agent 用 `--target` 指定技能目录。本包是纯知识技能，没有脚本依赖；安装器本身只依赖 Node.js。

## 使用

在 Agent 里直接描述任务即可，总入口会路由：

- “按小企业会计准则给这家公司建账”
- “把 6 月流水做成记账凭证和利润表”
- “小规模纳税人二季度增值税怎么算”
- “做一次应收账款审计，并给出调整建议”
- “帮我判断我们该用哪套会计准则”

建议第一次使用时提供：

1. 企业规模、年收入、行业
2. 增值税纳税人类型（小规模/一般纳税人）
3. 是否有外部融资、子公司、公开市场
4. 会计期间、币种、金额单位
5. 现有资料：流水、发票、合同、银行对账单、工资表、折旧表

输出约定：记账凭证用借贷表格，报表带本期/上期/变动，税务标明计税依据和税率，审计标明程序、样本、发现和证据。

## 会计总账模板

`templates/accounting-ledger.md` 是空白模板，可复制到工作区：

```bash
cp templates/accounting-ledger.md ~/.openclaw/workspace/memory/accounting-ledger.md
```

模板包含企业档案、准则选择、科目表版本、凭证历史、报表快照、税务记录和审计项目。不要把真实财务数据提交到版本库或公开分享。

## 校验

```bash
node validate.mjs
```

会检查：

- 25 个上游技能是否齐全
- 每个技能是否有 `SKILL.md`
- frontmatter `name` 是否与目录匹配（允许 `china-` 前缀）
- 总入口引用的子技能文件是否存在
- JS 语法
- 是否残留 API Key、个人绝对路径等敏感内容

## 与上游的差异

- 上游是 `business/`、`audit/`、`shared/` 嵌套结构；本包扁平化为 `skills/china-*/SKILL.md`，便于 OpenClaw/Hermes 等只扫描一层目录的 Agent 自动发现。
- 目录名使用 `china-` 前缀，但 frontmatter 的 `name` 保留上游原值（如 `accounting-framework`），因为技能正文之间按这个名字互相引用。支持按 frontmatter 名称发现的 Agent 不受影响。
- 新增 `china-accounting` 总入口路由技能。
- 新增安装器、校验器、README、AGENTS.md、docs 和空白总账模板。
- 未修改 25 个上游技能正文。

## 免责声明

本技能包提供的信息仅供参考和学习用途，不构成会计、税务或审计鉴证意见。所有财务处理、税务申报和审计意见应由持证会计师（CPA）、税务师或审计师复核确认。税率、准则和优惠政策以最新官方文件为准。因使用本技能包产生的任何后果由使用者自行承担。

## License

MIT，见 `LICENSE`。上游技能 © 2026 kylin985ti；打包脚本和文档同样采用 MIT。
