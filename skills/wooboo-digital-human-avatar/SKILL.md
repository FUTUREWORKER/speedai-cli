---
name: wooboo-digital-human-avatar
description: 通过挖宝AI CLI 使用本地训练视频创建、查询或删除可复用的数字人形象。
---

# 挖宝AI数字人形象

没有可用的数字人形象时，先通过本地训练视频创建一个形象。

## 参数补全与追问

- 创建形象必须有可访问的本地训练视频；用户没有提供时，先请用户提供视频。
- 用户未指定形象名称时使用“我的形象”，不要为名称单独追问。
- 查询形象不需要额外参数，直接执行 `wooboo avatar list`。
- 删除形象必须由用户明确提出，并且需要确定具体的形象记录；无法唯一确定时先请用户选择。
- 如果同时缺少多个必要信息，合并成一次简短提问。

创建并等待完成：

```bash
wooboo avatar create \
  --video /path/to/avatar-training.mp4 \
  --title "品牌主理人"
```

查询已有形象：

```bash
wooboo avatar list
```

生成数字人视频时，选择一个可用形象，并将其记录 ID 作为 `--avatar-record-id`。

只有用户明确要求时才删除：

```bash
wooboo avatar delete <avatar-record-id>
```
