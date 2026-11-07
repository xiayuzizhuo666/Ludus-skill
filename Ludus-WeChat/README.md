# Ludus-WeChat

把公众号选题、写作、配图、排版和草稿上传串成一条可恢复的流水线；只提交草稿，永不自动群发。

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

- “帮我写一篇公众号，一条龙，方向是 AI 技术，写完发到草稿箱。”
- “给我三个公众号选题，要适合职场读者。”
- “把这篇 Markdown 排成公众号 HTML。”
- “只写不发，先给我标题和框架。”

## 结构

```text
Ludus-WeChat/
├── skills/social-media/ludus-wechat/SKILL.md
├── skills/social-media/ludus-wechat/references/INDEX.md
├── skills/social-media/ludus-wechat/references/PATHS.md
├── skills/social-media/ludus-wechat/references/_vendor/...
├── install.py
├── manifest.json
├── README.md
├── AGENTS.md
├── LICENSE
├── THIRD-PARTY-NOTICES.md
└── tests/
```

## 许可

新增封装/入口与自写写作技能 PolyForm Noncommercial 1.0.0；`wechat-topic-selector` MIT；`wechat-publisher` ISC；增强项目 MIT。

非商用；商业使用新增内容需取得授权。上游组件仍按原许可证授权；保留 `wechat-publisher` 的 ISC 声明。

上游归属与修改说明见 `THIRD-PARTY-NOTICES.md`；上游原始许可证在各自的 `references/_vendor/.../LICENSE`。
