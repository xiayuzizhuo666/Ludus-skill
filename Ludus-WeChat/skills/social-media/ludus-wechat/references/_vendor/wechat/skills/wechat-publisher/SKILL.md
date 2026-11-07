---
name: wechat-publisher
description: 将已完成的文章排版并提交到微信公众号草稿箱，负责 Markdown→公众号 HTML、图片上传和草稿提交，不负责选题与写作。触发词：发公众号、上传草稿箱、发布文章到公众号、公众号排版、wechat publish。
trigger-words: [发公众号, 上传草稿箱, 发布文章到公众号, 公众号排版, wechat publish]
metadata:
  version: 1.0.0
  source: https://clawhub.ai
  license: ISC
---

# 微信公众号发布技能

## 边界

- ✅ 本技能只做：Markdown/文本 → 公众号 HTML → 上传图片 → 提交草稿箱
- ❌ 本技能不做：选题、写作、内容生成（由 `../wechat-article-writer/SKILL.md` 负责）
- 输入：已完成的文章内容 + 配图文件 + 标题/作者
- 输出：公众号草稿箱中的可发布草稿

## 前置配置

AppID/Secret 的读取优先级：

1. 命令行参数 `--appid` / `--secret`
2. 环境变量 `WECHAT_APPID` / `WECHAT_APP_SECRET`
3. `scripts/.wechat-config.json`（本地文件，已在 `.gitignore` 中排除）

首次使用任选一种：

```bash
# 方式一：环境变量
export WECHAT_APPID=your-appid
export WECHAT_APP_SECRET=your-appsecret

# 方式二：保存到本地配置
node scripts/upload-draft.js --appid your-appid --secret your-appsecret --save-config
```

其他前置条件：

- 调用微信 API 的公网 IP 必须加入公众号后台的 IP 白名单。
- 不要把真实 AppID/Secret 写入 SKILL.md、README 或提交到版本库。
- 本技能只提交草稿，**永远不要自动群发**；发布动作由用户在公众号后台确认。

## 发布流程（6 步）

> 以下命令假设当前目录是本技能目录（`skills/wechat-publisher`）。

### Step 1: 确认输入

确认文章 Markdown/HTML、标题、作者、封面图和正文图片都已就绪。缺少标题或正文时停止，不要自行编造。

### Step 2: 转换 HTML

```bash
node scripts/md-to-wechat-html.js --input article.md --output article.html --style warm
```

`--style` 只接受 `daily`、`warm`、`professional`、`lively`；数字编号已废弃，传入会报错。

### Step 3: 上传正文图片

```bash
curl -F "media=@image.png" "https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token=TOKEN"
```

把返回的微信图床 URL 替换到 HTML 中所有对应 `<img src>`。封面图可选：

```bash
curl -F "media=@cover.jpg" "https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=TOKEN&type=image"
```

返回 `media_id`。`upload-draft.js` 不处理封面；可以在公众号后台手动设置，或调用 `draft/add` 时传入 `thumb_media_id`。

### Step 4: 转换后必检

- [ ] 全文搜索 `<ol` / `</ol>`：如有，说明行首“数字+点”被误解析为列表，回到 Markdown 修正
- [ ] 全文搜索 `<style`：所有样式必须内联
- [ ] 全文搜索 `<h1`：标题由公众号系统渲染，正文不允许出现
- [ ] 所有图片 `src` 已替换为微信图床 URL
- [ ] 正文大小 < 2MB

### Step 5: 提交草稿

```bash
node scripts/upload-draft.js --html article.html --title "标题" --author "作者"
```

脚本会读取配置、获取 `access_token`，并调用 `POST /cgi-bin/draft/add` 提交草稿。

### Step 6: 通知用户

上传成功后通知用户：公众号后台 → 内容与互动 → 草稿箱 → 检查排版、设置封面 → 预览确认后手动发布。

## 排版规范（公众号 HTML 标准）

### 视觉风格系统

| 风格名 | 配色 | 适用写作风格 |
|:-------|:-----|:-------------|
| `daily`（日报风） | 品牌蓝 #0EA5E9 + 橙 #f59e0b | ⑥资讯日报主义（默认） |
| `warm`（温暖风） | 暖橙红 #E8633C + 琥珀 | ①情感共鸣主义、⑦情感叙事文风 |
| `professional`（专业风） | 深蓝 #1E40AF + 棕橙 | ②干货教程、③观点评论、⑤深度长文 |
| `lively`（活泼风） | 紫色 #7C3AED + 橙 | ④轻松幽默主义 |

### 全局规则

- **所有样式必须内联**，禁止 `<style>` 标签和 CSS class。
- 正文不含 `<h1>` 标题（标题由公众号自动显示），开头用摘要引导块代替。

### 元素规范

| 元素 | 标签 | 内联样式 |
|------|------|----------|
| 摘要块 | `<section>` | `margin:10px 0 15px;padding:15px 20px;background:#f7f8fa;border-left:4px solid #0EA5E9;font-size:15px;color:#555;line-height:1.6;` |
| 正文段落 | `<p>` | `margin:3px 0;font-size:16px;line-height:1.75;color:#333;` |
| 加粗 | `<strong>` | 不加额外样式（禁止用 `<span>` 或 class 模拟加粗） |
| 关键词高亮 | `<strong>` | `<strong style="color:#0EA5E9;">关键句</strong>` |
| 二级标题 | `<h2>` | `font-size:20px;font-weight:bold;color:#111;margin-top:15px;margin-bottom:5px;padding-left:12px;border-left:4px solid #0EA5E9;` |
| 三级标题 | `<h3>` | `font-size:17px;font-weight:bold;color:#222;margin-top:12px;margin-bottom:3px;` |
| 分割线 | `<hr>` | `border:none;border-top:1px solid #eee;margin:8px 0;`（禁止用 div 模拟） |
| 引用块 | `<blockquote>` | `margin:3px 0;padding:12px 18px;background:#f7f8fa;border-left:4px solid #0EA5E9;color:#555;font-style:italic;` |
| 图片容器 | `<p>` | `text-align:center;margin:3px 0;` |
| 图片 | `<img>` | `max-width:100%;display:block;margin:0 auto;border-radius:12px;` |
| 落款 | `<p>` | `margin-top:20px;padding-top:10px;border-top:1px solid #eee;font-size:14px;color:#999;text-align:center;line-height:2;` |

### 关键词颜色高亮规则

纯加粗在黑字中不够突出，必须对关键词/关键句加颜色。

| 用途 | 颜色 | 写法 |
|------|------|------|
| 核心观点/金句 | 品牌蓝 #0EA5E9 | `<strong style="color:#0EA5E9;">关键句</strong>` |
| 重要数据/数字 | 橙色 #f59e0b | `<strong style="color:#f59e0b;">40%</strong>` |
| 警示/冲突 | 红色 #ef4444 | `<strong style="color:#ef4444;">警示内容</strong>` |
| 正面/增长 | 绿色 #10b981 | `<strong style="color:#10b981;">增长数据</strong>` |
| 普通加粗 | 默认黑色 | `<strong>普通强调</strong>` |

- 每段最多高亮 1-2 处，不要全篇彩色。
- 不要在一句话里混用多种颜色。
- 普通强调仍然用无颜色的 `<strong>`。

### 落款

落款内容由账号运营者提供，禁止编造身份、头衔、业绩或“个人观点，不构成投资建议”等话术。

- 优先读取环境变量 `WECHAT_SIGNATURE`。
- 未配置时省略落款，不要使用别人的品牌署名。

```html
<p style="margin-top:20px;padding-top:10px;border-top:1px solid #eee;font-size:14px;color:#999;text-align:center;line-height:2;">{{WECHAT_SIGNATURE}}</p>
```

### 禁止事项

- ❌ 使用 `<style>` 标签或 CSS class
- ❌ 使用 `<h1>`（标题由公众号系统渲染）
- ❌ 使用 base64 图片（使用外部图床 URL 或在公众号素材库上传）
- ❌ 使用 `<span class="bold">` 模拟加粗（必须用 `<strong>`）
- ❌ 使用 `<div>` 模拟分割线（必须用 `<hr>`）
- ❌ 自动群发或未经用户确认发布

### 有序列表识别规则

转换器只把“数字 + 点 + 空格”（如 `1. `）识别为有序列表。以下写法不会被识别为列表，可以安全使用：

| 写法 | 结果 |
|---|---|
| `1、第一个要点` | 普通段落 |
| `2026.05.01·星期六` | 普通段落 |
| `0.1秒后，外骨骼...` | 普通段落 |
| `10.第一个要点` | 普通段落（点后无空格） |

如果正文确实需要有序列表，用 `1. `（点后带空格），转换器会生成一个完整的 `<ol>`。

## 文章结构模板

参考 `assets/article-template.html`，标准结构为：

```
摘要引导块（section）
正文段落...
图片
引用块
正文段落...
分割线
二级标题 + 图片 + 正文段落...
...（重复章节）
分割线
二级标题“写在最后” + 结尾段落...
落款（可选）
```

## 脚本工具

| 脚本 | 用途 |
|---|---|
| `scripts/md-to-wechat-html.js` | Markdown → 公众号内联样式 HTML |
| `scripts/visual-styles.js` | 4 种视觉风格配置 |
| `scripts/upload-draft.js` | 提交草稿到公众号草稿箱 |

仅使用 Node.js 内置模块，无需安装额外依赖。

## 常见错误

| 现象 | 原因 | 处理 |
|---|---|---|
| `40164 invalid ip` | 服务器 IP 不在白名单 | 公众号后台加入 IP 白名单 |
| `40001 invalid credential` | AppSecret 错误或已重置 | 重新获取 AppSecret |
| `40007 invalid media_id` | 封面 media_id 无效 | 重新上传封面素材 |
| HTML 出现 `<ol>` | 行首数字+点 | 按上表修正 Markdown 后重新转换 |
| 草稿里图片裂开 | 未替换为微信图床 URL | 重新上传图片并替换 `src` |

## 来源与许可

本技能基于 magicx 的 `magicx-wechat-publisher`（ISC © magicx）整理，已做去个人化与可移植化修改。完整归属与许可见包裹根目录 `THIRD-PARTY-NOTICES.md`。
