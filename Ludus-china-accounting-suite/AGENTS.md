# AGENTS.md — Ludus-china-accounting-suite

先读 `skills/finance/ludus-china-accounting/SKILL.md`，再读 `references/INDEX.md` 和 `references/PATHS.md`。

## 硬规则

- 不要把 `references/_vendor/` 里的上游文件改写成“更适合 Ludus”的版本；适配只放在入口 SKILL.md、INDEX.md、PATHS.md 和 `scripts/` 薄包装器。
- 不要重排上游目录；子技能之间的 `../china-*/SKILL.md` 相对路径依赖 `skills/` 目录整体保留，不要重排。
- 不要提交真实密钥、`.env`、`.wechat-config.json`、企业账目、客户材料或案件材料。
- 修改后运行 `python tests/validate.py` 和 `python tests/smoke.py`。
- 入口 `description` 必须 ≤60 字符，`name` 必须等于目录名，正文必须含 `## When to Use`。
- 只增不改：新增内容放 `references/_vendor/<enhancement>/` 或包根文档，不覆盖上游同名文件。

## 许可

原创会计内容（含封装/入口/26 个技能正文）PolyForm NC；上游 MIT 许可证文本保留；保留上游作者 kylin985ti 的版权声明；商业使用需授权。
