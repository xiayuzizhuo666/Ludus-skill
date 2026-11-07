# Ludus-HowToLiveBetter

把《高性价比人生指南》的 34 节、772 条建议封装成一个 Ludus 技能：先查书里的条目，再按成本、收益和证据等级排序回答。

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

- “每天通勤两小时值不值？”
- “朋友让我替他担保，签不签？”
- “被裁了之后先做什么、能领什么？”
- “这个体检项目要不要做？”

## 结构

```text
Ludus-HowToLiveBetter/
├── skills/leisure/ludus-howtolivebetter/SKILL.md
├── skills/leisure/ludus-howtolivebetter/references/INDEX.md
├── skills/leisure/ludus-howtolivebetter/references/PATHS.md
├── skills/leisure/ludus-howtolivebetter/references/_vendor/...
├── install.py
├── manifest.json
├── README.md
├── AGENTS.md
├── LICENSE
├── THIRD-PARTY-NOTICES.md
└── tests/
```

## 许可

新增封装/入口/路由与适配内容 PolyForm Noncommercial 1.0.0；书籍正文 CC BY 4.0；上游代码/增强 MIT + CC BY 4.0。必须保留作者署名与来源链接。

非商用；商业使用新增内容需取得授权。上游组件仍按原许可证授权；必须保留 `LICENSE`、`LICENSE-CODE` 和 `THIRD-PARTY-NOTICES.md` 中的署名与许可声明。

商业授权请联系：https://github.com/xiayuzizhuo666 。

上游归属与修改说明见 `THIRD-PARTY-NOTICES.md`；上游原始许可证在各自的 `references/_vendor/.../LICENSE`。
