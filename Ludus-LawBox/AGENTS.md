# AGENTS.md — Ludus-LawBox

先读 `skills/legal/ludus-lawbox/SKILL.md`，再读 `references/INDEX.md` 和 `references/PATHS.md`。

## 硬规则

- 不要把 `references/_vendor/` 里的上游文件改写成“更适合 Ludus”的版本；适配只放在入口 SKILL.md、INDEX.md、PATHS.md 和 `scripts/` 薄包装器。
- 不要重排上游目录；必须保留 `references/_vendor/lawbox/skills/legal/<子技能>/scripts/` 的原始深度；`parents[2]` 依赖它。markdown 里的 `skills/legal/...` 以 `references/_vendor/lawbox/` 为根解析。
- 不要提交真实密钥、`.env`、`.wechat-config.json`、企业账目、客户材料或案件材料。
- 修改后运行 `python tests/validate.py` 和 `python tests/smoke.py`。
- 入口 `description` 必须 ≤60 字符，`name` 必须等于目录名，正文必须含 `## When to Use`。
- 只增不改：新增内容放 `references/_vendor/<enhancement>/` 或包根文档，不覆盖上游同名文件。

## 许可

LawBox 新增内容 PolyForm Noncommercial 1.0.0；上游 MIT 内容保留 MIT；`cn-law-hub` 为 Apache-2.0。公开仓库保留 NC 声明；商业使用需授权。
