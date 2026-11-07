# Ludus-LawBox

把 LawBox 的 58 个中国法律工作技能收成一个入口：先由「法律工作总控」识别任务与事项，再按需读取子技能；简单问答走 L0，复杂事项才建 Matter Model、做反向复核、走正式交付门禁。

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

- “这是客户发来的微信、借条和转账记录，帮我判断现在起诉最大的风险。”
- “我是乙方，帮我审这份 SaaS 服务合同。”
- “员工主动离职，公司还需要付经济补偿吗？”
- “帮我起草一份民事起诉状，并列出证据目录。”

## 结构

```text
Ludus-LawBox/
├── skills/legal/ludus-lawbox/SKILL.md
├── skills/legal/ludus-lawbox/references/INDEX.md
├── skills/legal/ludus-lawbox/references/PATHS.md
├── skills/legal/ludus-lawbox/references/_vendor/...
├── install.py
├── manifest.json
├── README.md
├── AGENTS.md
├── LICENSE
├── THIRD-PARTY-NOTICES.md
└── tests/
```

## 许可

LawBox 新增内容 PolyForm Noncommercial 1.0.0；上游 legal-skills 为 MIT；`cn-law-hub` 为 Apache-2.0。

**非商用许可**。LawBox 新增内容为 PolyForm Noncommercial 1.0.0；公开仓库保留 NC 许可与声明，商业使用需另行取得授权。

上游归属与修改说明见 `THIRD-PARTY-NOTICES.md`；上游原始许可证在各自的 `references/_vendor/.../LICENSE`。
