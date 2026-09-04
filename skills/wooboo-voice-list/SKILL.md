---
name: wooboo-voice-list
description: 查询并选择当前用户在挖宝AI中的克隆音色，用于文字驱动的数字人视频生成。
---

# 挖宝AI音色查询

本查询不需要用户补充参数，直接执行。查询结果只有一个可用音色时可直接选择；存在多个且后续任务无法从用户要求中确定时，再请用户选择。没有可用音色时，说明需要先提供语音样本创建音色。

查询当前用户已有的克隆音色：

```bash
wooboo voice list
```

选择一个可用音色，并将其记录 ID 作为数字人视频命令的 `--voice-record-id`。向用户展示音色名称、记录 ID、语言和当前状态。

只有用户明确要求时才删除：

```bash
wooboo voice delete <voice-record-id>
```
