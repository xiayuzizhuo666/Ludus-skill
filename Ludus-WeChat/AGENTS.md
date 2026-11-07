# AGENTS.md — Ludus-WeChat

先读 `skills/social-media/ludus-wechat/SKILL.md`，再读 `references/INDEX.md` 和 `references/PATHS.md`。

## 硬规则

- 不要把 `references/_vendor/` 里的上游文件改写成“更适合 Ludus”的版本；适配只放在入口 SKILL.md、INDEX.md、PATHS.md 和 `scripts/` 薄包装器。
- 不要重排上游目录；`skills/wechat-*/` 的相对路径和 `__dirname` 依赖原目录布局；不要重排。
- 不要提交真实密钥、`.env`、`.wechat-config.json`、企业账目、客户材料或案件材料。
- 修改后运行 `python tests/validate.py` 和 `python tests/smoke.py`。
- 入口 `description` 必须 ≤60 字符，`name` 必须等于目录名，正文必须含 `## When to Use`。
- 只增不改：新增内容放 `references/_vendor/<enhancement>/` 或包根文档，不覆盖上游同名文件。

## 许可

新增封装/入口与自写写作技能 PolyForm NC；`wechat-publisher` 为 ISC；`wechat-topic-selector` 为 MIT；增强项目 MIT；保留原许可证；商业使用新增内容需授权。
