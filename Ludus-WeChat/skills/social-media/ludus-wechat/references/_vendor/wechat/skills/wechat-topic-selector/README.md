# 微信公众号选题助手

基于热榜内容拆解与方向匹配，生成带匹配度、标题和写作大纲的公众号选题。

## 依赖

- Python 3.8+
- `curl`（百度、CSDN 热榜）
- `mcporter`（可选，微博、GitHub 热榜）

无第三方 Python 依赖。

## 用法

```bash
python3 topic_selector.py --direction "AI 技术"
python3 topic_selector.py -d "职场成长" --platform weibo,baidu
python3 topic_selector.py -d "产品经理" --top 5 --output topic_results.json
```

## 输出

终端打印选题详情，同时把 JSON 结果写入 `--output` 指定的文件（默认 `topic_results.json`）。

## 已知限制

- 知乎条目为内置示例数据，不保证实时。
- 微博、GitHub 依赖 `mcporter`；不可用时自动跳过。
- 百度、CSDN 通过 Jina Reader 抓取，网络异常时自动跳过。

## 来源与许可

- 上游项目：https://github.com/lucianaib0318/wechat-auto-publish
- 许可证：MIT，见 `LICENSE`
