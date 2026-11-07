# 配置说明

## 1. 公众号配置

从公众号后台获取：

1. 登录公众号后台
2. 设置与开发 → 基本配置
3. 记录 AppID 和 AppSecret
4. 把当前公网 IP 加入 IP 白名单

配置方式（优先级从高到低）：

1. 命令行参数 `--appid` / `--secret`
2. 环境变量 `WECHAT_APPID` / `WECHAT_APP_SECRET`
3. `skills/wechat-publisher/scripts/.wechat-config.json`

生成配置文件：

```bash
node skills/wechat-publisher/scripts/upload-draft.js \
  --appid "your-appid" \
  --secret "your-appsecret" \
  --save-config
```

配置文件格式：

```json
{
  "appid": "your-appid",
  "secret": "your-appsecret",
  "author": "你的作者名"
}
```

## 2. 文章目录

```bash
export WECHAT_ARTICLES_DIR="/absolute/path/to/articles"
```

Windows PowerShell：

```powershell
$env:WECHAT_ARTICLES_DIR = "C:\path\to\articles"
```

未设置时默认 `./articles`。目录不存在会自动创建。

## 3. 图片生成配置

从 https://open.bigmodel.cn/ 获取密钥。

方式一（推荐）：

```bash
export ZHIPU_API_KEY="your-key"
```

方式二：

```bash
cp skills/wechat-article-writer/scripts/image.env.example "<ARTICLES_DIR>/image.env"
```

然后填写 `ZHIPU_API_KEY`，并 source 该文件或直接设置环境变量。默认模型 `cogview-3`，尺寸按提示词文件里的 `size`。不要把真实密钥写进技能目录。

## 4. 视觉风格

```bash
export WECHAT_DEFAULT_STYLE="warm"
```

可选：`daily`、`warm`、`professional`、`lively`。

映射建议：

| 内容类型 | 风格 |
|---|---|
| 情感、故事、卡兹克文风 | `warm` |
| 干货、教程、观点、深度长文 | `professional` |
| 资讯日报 | `daily` |
| 轻松幽默 | `lively` |

## 5. 落款

```bash
export WECHAT_SIGNATURE="你的账号名 — 一句话介绍"
```

未设置时省略落款。不要使用他人的品牌署名。

## 6. 安全

- 真实密钥只放在环境变量或本地配置文件中。
- `.wechat-config.json` 和 `image.env` 已被 `.gitignore` 排除。
- 不要通过聊天、截图或文章内容传输密钥。
- 如果密钥曾出现在公开位置，立即在公众号后台重置 AppSecret，并更换图片 API Key。
