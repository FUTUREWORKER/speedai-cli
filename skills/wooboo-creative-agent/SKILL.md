---
name: wooboo-creative-agent
description: 通过挖宝AI CLI 与已发布的创作 Agent 对话，适用于创意策划、文案、图片或视频任务编排以及带附件的创作请求。
---

# 挖宝AI创作 Agent

用户需要创意策划、文案、图片或视频创作协助时，使用已发布的创作 Agent。

## 参数补全与追问

- 当前消息已经包含明确任务时，直接将其作为对话内容，不重复询问。
- 发起对话必须有任务描述或至少一个可访问的附件；两者都没有时，先请用户说明需求或提供附件。
- 新任务不需要对话 ID；只有用户明确要求继续既有对话但没有提供或无法确定对话时，才查询现有对话并请用户选择。
- 附件、IP 分身和超时时间不是普通请求的必填项；用户未提出时不要追问。
- 如果同时缺少多个必要信息，合并成一次简短提问。

开始新对话：

```bash
wooboo agent bootstrap creative-agent
wooboo agent chat creative-agent --text "为这个新品写短视频脚本，并生成封面图"
```

继续已有对话或添加附件：

```bash
wooboo agent chat creative-agent \
  --conversation-id <conversation-id> \
  --file ./brief.docx \
  --text "结合附件继续完善方案"
```

用户选择了 IP 分身时添加 `--ip-clone-id`。需要查看或管理对话时，可使用 `conversations`、`messages`、`clear` 和 `cancel`。

完成后返回 Agent 回复；如果生成了图片或视频任务，同时报告任务 ID、状态和结果地址。
