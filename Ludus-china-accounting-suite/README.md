# Ludus-china-accounting-suite

按中国《小企业会计准则》《企业会计准则》和 CAS 审计准则，处理建账、记账、报表、税务与审计任务。

## 安装

```bash
python install.py --target "$HOME/.ludus/skills"
```

Windows PowerShell：

```powershell
python install.py --target "$env:USERPROFILE\.ludus\skills"
```

也可以先设置 `LUDUS_HOME`，再运行 `python install.py`。安装器会校验入口技能、引用路径和敏感内容；目标已存在时备份到 `<skills 目录的父目录>/skill-backups/`。

## 验证

```bash
python tests/validate.py
python tests/smoke.py
```

## 使用

在 Ludus 里直接描述任务，例如：

- “按小企业会计准则给这家公司建账。”
- “把 6 月流水做成记账凭证和利润表。”
- “小规模纳税人二季度增值税怎么算？”
- “做一次应收账款审计，并给出调整建议。”

## 结构

```text
Ludus-china-accounting-suite/
├── skills/finance/ludus-china-accounting/SKILL.md
├── skills/finance/ludus-china-accounting/references/INDEX.md
├── skills/finance/ludus-china-accounting/references/PATHS.md
├── skills/finance/ludus-china-accounting/references/_vendor/...
├── install.py
├── manifest.json
├── README.md
├── AGENTS.md
├── LICENSE
├── THIRD-PARTY-NOTICES.md
└── tests/
```

## 许可

新增封装/入口/路由内容 PolyForm Noncommercial 1.0.0；上游 25 个技能 MIT。

非商用；商业使用新增内容需取得授权。上游技能仍按 MIT 授权；保留上游 `LICENSE` 与 `THIRD-PARTY-NOTICES.md`。

上游归属与修改说明见 `THIRD-PARTY-NOTICES.md`；上游原始许可证在各自的 `references/_vendor/.../LICENSE`。
