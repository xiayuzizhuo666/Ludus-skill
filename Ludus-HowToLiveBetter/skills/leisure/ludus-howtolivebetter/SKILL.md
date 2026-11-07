---
name: ludus-howtolivebetter
description: "人生性价比决策：先查书里条目，再按成本收益排序."
version: 1.0.0
author: eternity4719; Ludus extension packaging
license: PolyForm-Noncommercial-1.0.0
platforms: [windows, macos, linux]
metadata:
  ludus:
    tags: [life, decision, cost-benefit, evidence, china]
    related_skills: []
---

# Ludus-HowToLiveBetter Skill

把《高性价比人生指南》的 34 节、772 条建议作为本地知识库，回答“该不该、值不值、划不划算、出事了先做什么、能领什么、犯不犯法”这类具体人生决策。它只做两件事：先查书里的条目，再按书的成本、收益和证据等级排序；查不到就明说，不凭记忆补数字。

## When to Use

- 用户问某件具体人生事情“该不该做、值不值、划不划算、怎么选”。
- 用户问“出事了先做什么、能领哪笔钱、这么干犯不犯法”。
- 用户要求按性价比、成本、收益或证据强度比较若干选项。
- 不适用：纯情绪倾诉、需要专业诊断/诉讼代理/个性化投资建议的个案；先按 Boundaries 分流。

## Prerequisites

- 正文已随技能分发：`references/_vendor/hltb/book/`、`references/_vendor/hltb/docs/`、`references/_vendor/hltb/README.md`、`references/_vendor/hltb/index.html`。
- 默认不需要网络。只有正文缺失时才用 `terminal` 浅克隆上游仓库，或用 `web_extract` 取单节。
- 用 `read_file` 读条目、`search_files` 搜标题和关键词；不要用裸 shell 文本命令作为主要交互方式。

## How to Run

1. 先读 `references/INDEX.md`，按问题类型定位到节或长文。
2. 用 `search_files` 在 `references/_vendor/hltb/book/` 里找 `^### ` 标题和关键词，锁定 1–3 节。
3. 用 `read_file` 完整读取命中的条目，连同「备注」栏；不要只读标题。
4. 需要排序时运行 `scripts/extract_ratio.py`，它会从 `references/_vendor/hltb/index.html` 提取 `COST_W` 和 `e.ratio` 两行；照这两行计算，不凭记忆写档位。
5. 按 `## Procedure` 的答复结构输出，每条注明节号和条号。

## Quick Reference

| 需要 | 读取 |
|---|---|
| 问题 → 节的路由表 | `references/_vendor/hltb/README.md` |
| 某节全文 | `references/_vendor/hltb/book/` |
| 长文（结婚、应急、平台办证、换城市等） | `references/_vendor/hltb/docs/` |
| 性价比档算法 | `references/_vendor/hltb/index.html` + `scripts/extract_ratio.py` |
| 失业/被裁补充 | `references/_vendor/hltb-enhancements/how-to-survive-unemployment/README.md` |
| 路径与引用规则 | `references/PATHS.md` |

## Procedure

1. **安全分流（完成标准：已判断是否属于急症、自杀风险或正在进行的法律程序）**
   - 正在发生的急症（倒地没呼吸、大出血、火灾、溺水、触电、中毒、卒中或心梗症状）：先说打 120/119 和现场第一个动作，出处第 13 节；不要先讲性价比。
   - 提到自杀念头、活不下去：先给全国心理援助热线 12356，再按第 1、29 节说；不做劝导式分析，不评价动机。
   - 已被传唤、拘留、起诉：先指第 8 节对应条目，并说明本书只给通用口径，个案要找律师。
2. **定位（完成标准：锁定 1–3 节，并写出节号）**
   - 读 `references/_vendor/hltb/README.md` 的「这本书想回答的问题」表，把用户问题对上节。
   - 用 `search_files` 搜 `^### ` 标题；再用关键词在候选节里搜正文。
3. **抽条目（完成标准：每条都完整读到「备注」栏）**
   - 用 `read_file` 读取命中条目的完整段落；不要只读标题，不要把「备注」里的适用人群、争议、例外丢掉。
   - 条目里的 HTML 注释是成本标签：钱 0/少/多、时间 少/中/多、毅力 否/些/是、收益 大/中/小、口径 死亡率/金钱/时间/自由；有 `人群=` 时按用户处境过滤。
4. **排序（完成标准：已拿到 `COST_W`/`e.ratio` 两行，或明确说明没有 `index.html`）**
   - 运行 `python scripts/extract_ratio.py`；按 `COST_W` 计算三项成本，按 `e.ratio` 落到「极高/高/一般」。
   - `e.ratio` 的公式依赖 `e.level`（大/中/小）：脚本输出的 `e.ratio = ...` 行就是完整公式；按公式计算，不要只看成本分。`e.cs === 0` 表示三项成本都取最低档，不是“低成本”。
   - 先按性价比，同档按证据等级 A > B > C，再按与用户处境的贴合度。
   - 不同口径不排序：换钱的和换寿命的分开列，各排各的。
5. **作答（完成标准：五段齐全，每条有出处）**
   1. 一句话结论：划不划算、该不该做、第一步是什么。
   2. 先做这几条（3–7 条）：动作、花掉什么、换回什么、证据等级、出处「第 8 节第 17 条（借条和担保）」。
   3. 别做/不用做的：书里明确不值得或有反面证据的。
   4. 书里没写的：如实说；常识判断要标明是常识。
   5. 复查信号：什么时候再看一次，或什么信号出现就改主意。
6. **自检（完成标准：逐条通过下方 Verification）**

## Pitfalls

1. **没查到就编。** 书里没有的数字、DOI、法条条款号一律不加；查不到就说查不到。
2. **只读标题。** 「备注」里的适用人群、争议、例外是条目的一部分；漏掉会把条件丢掉。
3. **把不同口径混在一起排序。** 「总死亡率降 12%」和「每年省 500 元」不在一把尺子上。
4. **忘了政策时效。** 第 7、19、21、24、31、32 节里的金额、时限、名单带截至日期；答复要带日期并提醒自查官方渠道。
5. **把「法律支持你」只说成胜诉。** 要连过程成本一起说：要不要打官司、大概多久、律师费谁掏。
6. **对第 ④ 档受益人只写好处。** 救陌生人、替人担保、帮人转账要把被讹、被卷进案子、被报复的风险一起写。

## Verification

- [ ] 答复里的每个数字都能指回某一条正文；指不回去的已标为常识。
- [ ] 每条建议都有「第 X 节第 Y 条（标题关键词）」。
- [ ] 排序前已运行 `scripts/extract_ratio.py`，或已说明没有 `index.html` 并只列成本标签。
- [ ] 急症、自杀风险、在办法律程序已按安全分流处理。
- [ ] 政策金额、时限、名单带了截至日期。
- [ ] 没有引知乎、公众号、搜狐等二手转述；只给条目「来源」栏已有的链接。
- [ ] 争议条目说了反方证据；TODO 条目没有当结论用。

## Boundaries

- 本书给通用口径，不替代医生、律师、会计；具体病情、案件、税务按条目给方向并说明该找谁。
- 不给个性化投资建议；不替专业人士下判断。
- 书的观点和性价比档是作者判断；用户不同意时摆出书里的依据即可，不辩论。
- 失业/被裁增强内容来自 `AIPMAndy/how-to-survive-unemployment`（MIT + CC BY 4.0），与本书 `references/_vendor/hltb/docs/被裁了之后先做什么.md` 重叠时，以本书条目为第一优先，增强内容作补充。
