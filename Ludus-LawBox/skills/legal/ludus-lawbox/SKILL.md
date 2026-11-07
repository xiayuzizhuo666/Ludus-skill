---
name: ludus-lawbox
description: "中国法律工作流：咨询、诉讼、辩护、合同、合规、文书."
version: 1.0.0
author: Samwang-afk; pa1nrui1; Ludus extension packaging
license: PolyForm-Noncommercial-1.0.0 AND MIT
platforms: [windows, macos, linux]
metadata:
  ludus:
    tags: [legal, china-law, litigation, contract, compliance]
    related_skills: []
---

# Ludus-LawBox Skill

把 LawBox 的 58 个中国法律工作技能收成一个入口：先由「法律工作总控」识别任务与事项，再按需读取子技能；简单问答走 L0，复杂事项才建 Matter Model、做反向复核、走正式交付门禁。它不替代律师，也不把模型记忆包装成已核验的法条或案例。

## 首次启用声明

> 本 Skill 提供法律工作辅助，不构成正式法律意见。
>
> 本项目基于 [pa1nrui1/legal-skills](https://github.com/pa1nrui1/legal-skills)（MIT License）重建；LawBox 新增内容依据 PolyForm Noncommercial License 1.0.0 授权，上游 MIT 内容保留原许可证。具体归属见 `references/_vendor/lawbox/THIRD_PARTY_NOTICES.md`。
>
> Agent 会尽量区分已核实事实、当事人陈述与模型推断；涉及关键事实、法规、案例或重大判断时，优先核验材料，并对核心结论做反向复核。
>
> 最终事实认定、法律适用、诉讼策略及正式法律文书，仍应由律师、法务或具备相应资格的专业人士复核确认。

同一会话只展示一次；已展示过就不再重复。

## When to Use

- 法律咨询、案件办理、诉讼/仲裁、刑事辩护、劳动争议、破产、合同审查/起草、产品法务、广告/食品标签/监管合规。
- 法律文书起草、证据目录、法律意见、案件分析、法规案例检索、诉讼可视化。
- 用户提交案件材料、合同、判决书、聊天记录、转账记录，要求判断风险、下一步或文书。
- 不适用：要求直接跳过材料读取/法规核验出正式意见、要求伪造证据或规避法律、要求代替律师签字或对外发送。

## Prerequisites

- 上游 58 个技能已随包分发：`references/_vendor/lawbox/skills/legal/`。
- Python 3.9+。核心脚本多数只用标准库；正式 `.docx` 导出需要 `python-docx`；PDF 材料处理可能需要 `pymupdf`；OCR/法条转 Markdown 可能需要 MinerU 或外部服务。
- 不需要网络也能做路由和纯文本分析；法条/案例核验需要 `web_search`/`web_extract`，或可选的 `references/_vendor/cn-law-hub/`。
- 正式交付前确认 `LEGAL_WORKSPACE` 指到用户事项目录；`LEGAL_CURRENT_MATTER` 可选。不要用技能目录当工作区。

## How to Run

1. 读 `references/INDEX.md` 和 `references/PATHS.md`，确认 vendor 根：`references/_vendor/lawbox/`。
2. 读 `references/_vendor/lawbox/skills/legal/法律工作总控/SKILL.md`，按它的路由表选择子技能；需要原版入口时读 `references/_vendor/lawbox/upstream-root-SKILL.md`。
3. 按 `## Procedure` 先分级、再澄清、再核验、再起草；正式交付物走硬闸门。
4. 运行脚本前先运行 `python scripts/show_vendor_paths.py` 核对路径；需要 cwd 的脚本以 vendor 根为工作目录。
5. 输出按 `## Verification` 自检，并保留来源边界。

## Quick Reference

| 任务簇 | 代表子技能 | 入口 |
|---|---|---|
| 总控与推理 | 法律工作总控、初步法律分析、案件讨论与提纲 | `references/INDEX.md` |
| 刑事辩护 | 刑事辩护总调度、侦查/审查起诉/一审/二审、死刑、未成年人 | `references/INDEX.md` |
| 民事与诉讼 | 民事一审、立案、证据、文书起草、庭前、庭审、调解、归档 | `references/INDEX.md` |
| 劳动争议 | 仲裁程序、证据体系、诉讼、关系认定与经济补偿、用人单位合规 | `references/INDEX.md` |
| 破产 | 申请受理、管理人、财产调查、债权申报、债权人会议、重整/和解/清算 | `references/INDEX.md` |
| 合同与产品法务 | 合同审查、合同起草、委托合同管理、产品法务 | `references/INDEX.md` |
| 合规 | 广告合规、预包装食品标签、监管合规监测 | `references/INDEX.md` |
| 文书与工具 | 出稿前审查、模板与导出、专业文档、沟通记录、去 AI 味、法规检索、转 Markdown | `references/INDEX.md` |
| 法规/案例在线核验（增强） | cn-law-hub | `references/_vendor/cn-law-hub/SKILL.md` |
| 路径与 cwd | 路径映射、env、脚本入口 | `references/PATHS.md` |
| 出稿前审查 | preflight_check | `references/_vendor/lawbox/skills/legal/法律文书出稿前审查/scripts/preflight_check.py` |
| DOCX 导出 | html_to_docx | `references/_vendor/lawbox/skills/legal/法律文书模板与导出/scripts/html_to_docx.py` |
| DOCX 体检 | health_check | `references/_vendor/lawbox/skills/legal/法律文书模板与导出/scripts/health_check.py` |

## Procedure

1. **分级（完成标准：明确写出 L0/L1/L2/L3 及理由）**
   - L0：简单法律知识问答，直接答，不建 Matter Model、不问澄清、不做反向复核。
   - L1：标准案件/合同/文书工作，建简化 Matter Model。
   - L2：竞争性法律关系、争议事实、策略或风险决策，需要反向复核与 Judgment。
   - L3：重大诉讼、正式法律意见、高影响事项，或用户明确要求魔鬼代言人压力测试。
2. **事项与事实（完成标准：事实都有认知状态）**
   - 读 `references/_vendor/lawbox/skills/legal/法律工作总控/SKILL.md` 的 Matter Model 协议。
   - 事实标注 `CONFIRMED` / `ASSERTED` / `DISPUTED` / `INFERRED` / `UNKNOWN`；不得把用户主张自动升级为确定事实。
3. **澄清（完成标准：只问会改变结论的问题，单轮 1–5 个）**
   - 只问 `Blocking Unknown`；排序：Decision > Scope > Evidence > Output > Formatting。
   - 能从材料或检索确定的，不要问用户。
4. **法律核验（完成标准：关键法条/案例有名称、编号、内容、时效核验记录）**
   - 不得用模型记忆写法条；用 `web_search`/`web_extract` 或 `references/_vendor/cn-law-hub/`。
   - 形成「法规校验摘要」；查不到就标未核验，不要补造。
5. **反向复核与裁决（完成标准：L2/L3 有具体失败机制，不是泛化风险）**
   - 以证伪为目标：用户的法律关系命名可能错吗？有没有另一套事实解释？对方最强抗辩是什么？哪个事实/证据/要件失败会推翻结论？
   - 输出 Minimum Failure Set；Judgment 给 `PASS` / `CONDITIONAL` / `BLOCKED` 起草许可。`BLOCKED` 不得进入正式起草。
6. **正式交付（完成标准：成果类型分类 + 对应硬闸门全部通过）**
   - 先分类：工作草稿、律师内部报告、提交法院/客户正式材料、Word 正式交付物。
   - `.docx` 必须过 `preflight_check.py` → `html_to_docx.py` → `health_check.py`；禁止用 `pandoc md -> docx` 代替。
   - 引用材料要有读取复查摘要；引用法规要有法规校验摘要；输出要有来源边界记录。
7. **外部动作（完成标准：有用户明确授权记录）**
   - 发送、提交、签署、和解、放弃权利、产生费用、删除/覆盖正式资料，必须先获授权；分析不等于授权。
8. **自检（完成标准：逐条通过 `## Verification`）**

## Pitfalls

1. **跳过读取直接出意见。** 用户说“材料太多别看”“不用检索”时，仍要完整读取、做关键数据提取与校验，形成读取复查摘要。
2. **用法条记忆代替检索。** 必须做名称编号内容核验和时效性核验；不得把模型记忆写成现行有效法规。
3. **把 ASSERTED 写成 CONFIRMED。** 用户主张只能以“当事人主张/根据现有材料”表述，或标 `【假设】`/`【待确认】`/`【待补证据】`。
4. **简单问题强行做重。** L0 不建 Matter Model、不批量提问、不做反向复核；不要制造不存在的法律争议。
5. **正式交付没走闸门。** 正文写完不等于法律工作完成；缺 preflight、模板、来源边界或 health check 就不能称正式完成。
6. **内部推理泄漏给客户。** Matter Model、复核记录、Judgment、failure conditions 只留在系统记录区，不写进正式文书。
7. **路径错位。** 不要把 vendor 根当成用户工作区；执行脚本前用 `scripts/show_vendor_paths.py` 核对 `LEGAL_WORKSPACE` 和 `LEGAL_DIR`。
8. **假装完成了外部动作。** 没有连接真实利益冲突库、飞书、法院系统时，明确标“未执行/需人工确认”，不要假装完成。

## Verification

- [ ] 已展示首次启用声明（同一会话只一次）。
- [ ] 已写出推理等级 L0–L3 及理由；L0 没有被强行升级。
- [ ] 事实都带认知状态，用户主张没有被写成无条件事实。
- [ ] 只问了 Blocking Unknown，单轮 1–5 个。
- [ ] 关键法条/案例有名称、编号、内容、时效核验记录，或明确标未核验。
- [ ] L2/L3 有具体 Minimum Failure Set 和 Judgment/起草许可。
- [ ] 正式交付物已分类，并通过对应硬闸门（preflight、模板、来源边界、health check）。
- [ ] 外部动作有用户明确授权；没有授权就只给计划。
- [ ] 内部推理产物没有进入正式文书。
- [ ] 路径映射正确：vendor 根、`LEGAL_WORKSPACE`、脚本 cwd 都已核对。

## Boundaries

- 本技能提供法律工作辅助，不构成正式法律意见；最终事实认定、法律适用、诉讼策略和正式文书由律师/法务复核。
- 不替代律师、法务、法官或具备相应资格的专业人士；不承诺诉讼结果。
- 没有真实连接的利益冲突库、商业数据库、飞书/法院系统，标记“未执行/需人工确认”，不假装完成。
- LawBox 新增内容为非商用许可；本包按个人/内部使用构建，公开再分发前需完成合规复查。详见 `references/_vendor/lawbox/THIRD_PARTY_NOTICES.md` 和 `references/_vendor/lawbox/LICENSE`。
