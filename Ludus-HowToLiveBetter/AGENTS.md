# AGENTS.md — Ludus-HowToLiveBetter

先读 `skills/leisure/ludus-howtolivebetter/SKILL.md`，再读 `references/INDEX.md` 和 `references/PATHS.md`。

## 硬规则

- 不要把 `references/_vendor/` 里的上游文件改写成“更适合 Ludus”的版本；适配只放在入口 SKILL.md、INDEX.md、PATHS.md 和 `scripts/` 薄包装器。
- 不要重排上游目录；书里的 `book/`、`docs/`、`index.html` 都相对于 `references/_vendor/hltb/` 解析。
- 不要提交真实密钥、`.env`、`.wechat-config.json`、企业账目、客户材料或案件材料。
- 修改后运行 `python tests/validate.py` 和 `python tests/smoke.py`。
- 入口 `description` 必须 ≤60 字符，`name` 必须等于目录名，正文必须含 `## When to Use`。
- 只增不改：新增内容放 `references/_vendor/<enhancement>/` 或包根文档，不覆盖上游同名文件。

## 许可

书籍正文 CC BY 4.0，代码 MIT；保留作者署名、来源链接和修改声明。增强项目 `how-to-survive-unemployment` 为 MIT + CC BY 4.0。
