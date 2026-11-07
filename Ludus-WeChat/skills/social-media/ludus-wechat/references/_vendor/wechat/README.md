# 微信公众号技能包（vendored）

本目录是 `Ludus-WeChat` 的 vendored 上游快照，只保留一条龙、选题、写作、发布四个技能和配置说明。

安装与使用请看包根 `README.md` 和 `SKILL.md`；路径契约见 `references/PATHS.md`。

## 包含

| 目录 | 作用 | 许可 |
|---|---|---|
| `skills/wechat-pipeline/` | 一条龙调度入口 | MIT（本包新增） |
| `skills/wechat-topic-selector/` | 热榜选题 | MIT |
| `skills/wechat-article-writer/` | 六阶段写作、标题、框架、风格、配图提示词 | PolyForm NC（本包自写替换） |
| `skills/wechat-publisher/` | Markdown → 公众号 HTML、草稿提交 | ISC |

`khazix-writer` 上游没有 LICENSE，已移除，不在本包中。
