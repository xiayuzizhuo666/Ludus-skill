# 路径与数据连续性

## 根目录

```text
<技能目录>/
├── SKILL.md
├── references/
│   ├── INDEX.md
│   ├── PATHS.md
│   ├── GAPS.md
│   └── _vendor/accounting/
│       ├── skills/            # 26 个 china-* 技能
│       ├── docs/USAGE.md
│       ├── README.md
│       ├── LICENSE
│       └── THIRD-PARTY-NOTICES.md
└── templates/
    └── accounting-ledger.md
```

## 路径映射

| 文档里写的 | 实际位置 |
|---|---|
| 总入口 `china-accounting` | `references/_vendor/accounting/skills/china-accounting/SKILL.md` |
| 子技能 `china-*` | `references/_vendor/accounting/skills/china-*/SKILL.md` |
| 使用说明 | `references/_vendor/accounting/docs/USAGE.md` |
| 空白总账模板 | `templates/accounting-ledger.md` |

## 工作区与数据连续性

- `ACCOUNTING_WORKSPACE`：用户工作区根目录。`memory/accounting-ledger.md` 相对于它解析；未设置时以用户当前工作目录为根，不要用技能目录。
- 如果 `<ACCOUNTING_WORKSPACE>/memory/accounting-ledger.md` 存在，先读企业档案、历史凭证和报表快照。
- 只有用户确认后才更新；不要在无关对话中暴露企业敏感财务信息。
- 需要新建账套时，先把 `templates/accounting-ledger.md` 复制到 `<ACCOUNTING_WORKSPACE>/memory/accounting-ledger.md`，再填写企业档案和准则选择。

## 输出约定

- 记账凭证：日期、摘要、科目编码与名称、借方金额、贷方金额、附件、凭证号。
- 报表：项目、本期数、上期数、变动、备注。
- 税务：税种、计税依据、税率/征收率、应纳税额、申报期。
- 审计：程序、样本、发现、结论、调整建议、证据索引。

## 依赖与网络

- 本包无脚本、无第三方依赖、默认不需要网络。
- 税率、准则和优惠政策以财政部、国家税务总局等官方最新文件为准；不确定时标「需复核」。
