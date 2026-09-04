---
name: wooboo-video-package
description: 通过挖宝AI包装已有视频，适用于添加自动标题、模板、身份文案、背景音乐或生成精加工成片，不用于生成新镜头。
---

# 挖宝AI视频智能包装

## 参数补全与追问

- 先从用户消息、对话上下文和已提供的附件中提取参数；能够安全推断时直接使用，不重复询问。
- 生成包装成片必须有可访问的源视频；用户没有提供时，先请用户提供视频。
- 标题和源视频实际时长是提交所需参数。标题可以从用户需求中确定，视频时长可以从本地素材读取；只有无法确定时才追问用户。
- 模板、音乐和身份文案是可选项。用户未提出要求时不要追问；用户明确要求但存在多个可用选择时，先列出选项并请用户选择。
- 如果同时缺少多个必要信息，合并成一次简短提问。

先查看当前可用模板和音乐：

```bash
wooboo video-package bootstrap
wooboo video-package templates
wooboo video-package music
```

生成时需要提供源视频的实际时长：

```bash
wooboo video-package generate \
  --video ./source.mp4 \
  --title "3分钟看懂AI工作流" \
  --duration-seconds 86.4 \
  --style-id <template-id> \
  --music-id <music-id> \
  --identity-name "胡老师" \
  --identity-desc "AI产品顾问"
```

可以使用 `list`、`status` 和 `download` 查询或下载已有任务。只有用户明确要求时才使用 `delete`。

完成后报告任务 ID、状态、成片地址和本地下载路径。
