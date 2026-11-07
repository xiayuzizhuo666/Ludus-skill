---
name: ludus-china-accounting
description: "中国会计准则：准则选择、记账、报表、税务、审计."
version: 1.0.0
author: kylin985ti; Ludus extension packaging
license: PolyForm-Noncommercial-1.0.0
platforms: [windows, macos, linux]
metadata:
  ludus:
    tags: [accounting, china, bookkeeping, tax, audit, cas]
    related_skills: []
---

# Ludus-China-Accounting Skill

按中国《小企业会计准则》《企业会计准则》和中国注册会计师审计准则（CAS），处理建账、记账、报表、税务和审计任务。它是一个知识型总入口：先确认企业画像和适用准则，再路由到对应的子技能；不编造金额、税率、科目或审计证据。

## When to Use

- 建账、记账、做账、编制凭证、对账、月末结账。
- 资产负债表、利润表、现金流量表、毛利率/净利率分析。
- 增值税、企业所得税、个人所得税、汇算清缴、税率速查。
- 审计总控、风险评估、重要性水平、各科目实质性程序、审计调整、审计报告。
- 不适用：需要持证会计师出具正式鉴证意见、需要直接向税务系统申报、需要读取企业真实账套但用户没有提供数据的场景。

## Prerequisites

- 上游 26 个技能已随包分发：`references/_vendor/accounting/skills/`。
- 不需要网络和脚本依赖；所有内容为纯 Markdown。
- 需要用户提供企业画像和资料：规模/年收入、纳税人类型、准则、会计期间、币种、金额单位，以及流水、发票、合同、银行对账单、工资表、折旧表等。
- 如果工作区有 `memory/accounting-ledger.md`，先读；只有用户确认后才更新。

## How to Run

1. 先读 `references/INDEX.md`，确认任务属于准则、记账、报表、税务还是审计。
2. 读 `references/_vendor/accounting/skills/china-accounting/SKILL.md`（总入口）和对应的 `china-*` 子技能。
3. 按 `## Procedure` 先确认企业画像和准则，再给方案。
4. 用 `read_file` 读子技能；用 `write_file`/`patch` 生成本地工作底稿；不要把真实财务数据写进公开文件。
5. 输出后按 `## Verification` 自检，并列出「待补资料」和「需 CPA/税务师复核」事项。

## Quick Reference

| 任务 | 读取 |
|---|---|
| 总入口、路由表 | `references/_vendor/accounting/skills/china-accounting/SKILL.md` |
| 判断小企业准则还是企业准则 | `references/_vendor/accounting/skills/china-accounting-framework/SKILL.md` |
| 科目表与科目编码 | `references/_vendor/accounting/skills/china-chart-of-accounts/SKILL.md` |
| 记账凭证、借贷平衡 | `references/_vendor/accounting/skills/china-journal-entry/SKILL.md` |
| 月末计提、摊销、结转、结账 | `references/_vendor/accounting/skills/china-month-end-close/SKILL.md` |
| 资产负债表 | `references/_vendor/accounting/skills/china-balance-sheet/SKILL.md` |
| 利润表 | `references/_vendor/accounting/skills/china-profit-loss/SKILL.md` |
| 现金流量表 | `references/_vendor/accounting/skills/china-cash-flow/SKILL.md` |
| 增值税 | `references/_vendor/accounting/skills/china-vat-accounting/SKILL.md` |
| 企业所得税 | `references/_vendor/accounting/skills/china-income-tax/SKILL.md` |
| 个人所得税 | `references/_vendor/accounting/skills/china-individual-tax/SKILL.md` |
| 税率速查 | `references/_vendor/accounting/skills/china-tax-rates-reference/SKILL.md` |
| 审计总控 | `references/_vendor/accounting/skills/china-audit-master/SKILL.md` |
| 审计报告 | `references/_vendor/accounting/skills/china-audit-report/SKILL.md` |
| 完整路由表 | `references/INDEX.md` |
| 路径与数据连续性 | `references/PATHS.md` |
| 能力边界与缺口 | `references/GAPS.md` |
| 空白总账模板 | `templates/accounting-ledger.md` |

## Procedure

1. **确认企业画像（完成标准：五项信息都有，或已列清单让用户补）**
   - 企业规模 / 年收入；增值税纳税人类型（小规模/一般纳税人）；是否公开市场、有外部融资、有子公司；会计期间、币种、金额单位；现有资料。
   - 缺数据就列清单，不要用假设数字填空。
2. **先定准则（完成标准：明确写出小企业会计准则或企业会计准则，并说明依据）**
   - 读 `references/_vendor/accounting/skills/china-accounting-framework/SKILL.md`。
   - 小企业准则和企业准则不能混用；有外部融资、子公司、公开市场的，优先按企业准则判断。
3. **路由到子技能（完成标准：已读对应 `SKILL.md`，不是凭记忆答）**
   - 记账理账：科目表、凭证、月末结账、三大报表、盈利分析。
   - 税务：增值税、企业所得税、个人所得税、税率速查。
   - 审计：总控、风险评估、重要性、各科目实质性程序、审计调整、审计报告。
4. **执行（完成标准：输出满足本包的硬规则）**
   - 不编造金额、科目、税率、政策条款、审计证据或报表数字。
   - 记账凭证必须借贷平衡；摘要、附件、凭证号、日期齐全。
   - 报表必须勾稽：资产 = 负债 + 所有者权益；净利润与未分配利润变动勾稽；现金净增加额与现金余额变动勾稽。
   - 税务先确认纳税人身份，再谈进项抵扣、征收率、优惠和申报周期。
   - 审计按「风险评估 → 重要性 → 实质性程序 → 调整 → 报告」推进；不伪造函证、监盘或审计证据。
5. **输出（完成标准：格式与结尾清单齐全）**
   - 凭证：日期、摘要、科目编码与名称、借方金额、贷方金额、附件、凭证号。
   - 报表：项目、本期数、上期数、变动、备注。
   - 税务：税种、计税依据、税率/征收率、应纳税额、申报期。
   - 审计：程序、样本、发现、结论、调整建议、证据索引。
   - 结尾列：采用的准则和口径、关键假设、待补资料、需要 CPA/税务师复核的事项。
6. **自检（完成标准：逐条通过 `## Verification`）**

## Pitfalls

1. **准则混用。** 小企业准则和企业准则的科目、报表格式、递延所得税处理不同；先定准则再记账。
2. **用假设数字填空。** 缺流水、发票、对账单时，列清单让用户补，不要编。
3. **凭证不平。** 每张凭证借贷必须相等；先校验再输出。
4. **报表不勾稽。** 资产=负债+所有者权益；净利润与未分配利润变动；现金净增加额与现金余额变动。
5. **把税率当永久有效。** 税率、优惠、申报期会变；不确定时标「需复核」，并提醒以财政部、国家税务总局最新文件为准。
6. **替 CPA 出意见。** 税务申报和审计意见必须由持证专业人士复核；不自动申报、不自动出具审计报告。
7. **泄露企业数据。** 不把真实账目、客户名称、金额写进公开文件或提交到版本库。

## Verification

- [ ] 已确认企业画像五项信息，或已列出待补清单。
- [ ] 已明确写出适用准则和判断依据。
- [ ] 已读取对应的 `china-*` 子技能，而不是凭记忆答。
- [ ] 凭证借贷平衡；摘要、附件、凭证号、日期齐全。
- [ ] 报表三项勾稽全部通过。
- [ ] 税务标明计税依据、税率/征收率、申报期；不确定项标「需复核」。
- [ ] 审计标明程序、样本、发现、证据；没有伪造证据。
- [ ] 结尾列出准则口径、关键假设、待补资料、需 CPA/税务师复核事项。
- [ ] 没有把真实企业敏感数据写进公开文件。

## Boundaries

- 本技能包是知识参考，不构成会计、税务或审计鉴证意见。
- 税率、准则和优惠政策以最新官方文件为准；不确定时明确标注「需复核」。
- 不自动报税、不自动出具审计报告、不自动对外发送财务数据。
- 需要正式审计意见、税务鉴证或申报时，交由持证会计师、税务师或审计师完成。
- 上游内容的许可见 `references/_vendor/accounting/LICENSE` 和 `references/_vendor/accounting/THIRD-PARTY-NOTICES.md`。
