# Ludus 外接扩展技能包

四个 Ludus 外接扩展包，每个包只注册一个入口技能，上游子技能全部放在 `references/_vendor/` 下按需读取。

| 包 | 入口技能 | 领域 | 许可 |
|---|---|---|---|
| `Ludus-HowToLiveBetter` | `leisure/ludus-howtolivebetter` | 日常生活咨询与决策 | CC BY 4.0 + MIT |
| `Ludus-LawBox` | `legal/ludus-lawbox` | 中国法律咨询与工作流 | PolyForm NC + MIT；非商用 |
| `Ludus-china-accounting-suite` | `finance/ludus-china-accounting` | 中国会计准则、记账、报税、审计 | MIT |
| `Ludus-WeChat` | `social-media/ludus-wechat` | 公众号运营、写作、排版、草稿发布 | MIT + ISC（写作技能为自写实现） |

## 快速安装

每个包都有独立安装器，目标目录是 Ludus 的 skills 目录：

```bash
python Ludus-HowToLiveBetter/install.py --target "$HOME/.ludus/skills"
python Ludus-LawBox/install.py --target "$HOME/.ludus/skills"
python Ludus-china-accounting-suite/install.py --target "$HOME/.ludus/skills"
python Ludus-WeChat/install.py --target "$HOME/.ludus/skills"
```

Windows PowerShell：

```powershell
python Ludus-HowToLiveBetter/install.py --target "$env:USERPROFILE\.ludus\skills"
python Ludus-LawBox/install.py --target "$env:USERPROFILE\.ludus\skills"
python Ludus-china-accounting-suite/install.py --target "$env:USERPROFILE\.ludus\skills"
python Ludus-WeChat/install.py --target "$env:USERPROFILE\.ludus\skills"
```

安装器会校验入口 frontmatter、引用路径和敏感内容；目标已存在时备份到 `<skills 目录的父目录>/skill-backups/`，不会把备份放进 `skills/`。

## 验证

```bash
for p in Ludus-HowToLiveBetter Ludus-LawBox Ludus-china-accounting-suite Ludus-WeChat; do
  python "$p/tests/validate.py"
  python "$p/tests/smoke.py"
done
```

四个入口技能都已通过 Ludus 的 hard frontmatter validator 和 advisory linter（本机临时 venv 中运行）。

## 结构

```text
Ludus-<Domain>/
├── skills/<category>/<name>/SKILL.md     # 唯一入口
├── skills/<category>/<name>/references/
│   ├── INDEX.md                          # 任务 → 子技能路由
│   ├── PATHS.md                          # vendor 根、cwd、env 契约
│   └── _vendor/                          # 上游快照 + 增强项目
├── install.py
├── manifest.json
├── README.md
├── AGENTS.md
├── LICENSE
├── THIRD-PARTY-NOTICES.md
└── tests/
```

`_vendor/` 以下划线开头，Ludus 不会把其中的 `SKILL.md` 当成独立技能，advisory linter 也不会把大量参考文件算成 `references-sprawl`。

## 许可与分发

- `Ludus-HowToLiveBetter`：书籍正文 CC BY 4.0，代码 MIT；再分发需保留作者署名与来源链接。含 `how-to-survive-unemployment`（MIT + CC BY 4.0）。
- `Ludus-china-accounting-suite`：上游 MIT；可再分发，保留上游 `LICENSE`。
- `Ludus-LawBox`：LawBox 新增内容 PolyForm Noncommercial 1.0.0，上游 legal-skills 为 MIT；含 `cn-law-hub`（Apache-2.0）。**公开仓库保留 NC 许可与声明；商业使用需另行取得授权。**
- `Ludus-WeChat`：本包 MIT，`wechat-publisher` ISC；`wechat-article-writer` 已替换为本包自写 MIT 实现，不再包含上游无许可证版本。

每个包的 `THIRD-PARTY-NOTICES.md` 记录了上游仓库、快照/commit、许可证、复制范围和修改说明。

## 不含什么

- 不含真实 AppID、AppSecret、API Key、企业账目、客户材料或案件材料。
- 不会自动群发公众号文章；只提交草稿。
- 不替代律师、会计师、税务师、医生或审计师的专业判断。
