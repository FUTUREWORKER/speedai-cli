---
name: wooboo-voice-clone
description: 通过挖宝AI使用本地语音样本克隆可复用音色，并获得用于数字人视频的音色记录。
---

# 挖宝AI音色克隆

使用 `wooboo voice clone` 提交本地语音样本。

## 参数补全与追问

- 克隆音色必须有可访问的本地语音样本；用户没有提供时，先请用户提供音频。
- 用户未指定音色名称时使用“我的音色”，不要为名称单独追问。
- 语言能够从用户要求或语音用途中明确判断时直接填写；无法判断时使用当前默认值，不为此阻塞提交。
- 如果同时缺少多个必要信息，合并成一次简短提问。

## 使用流程

1. 未登录时运行 `wooboo login web --open`。
2. 使用清晰的本地语音样本创建音色。
3. 等待克隆完成。
4. 返回音色名称和记录 ID；生成数字人视频时把该 ID 传给 `--voice-record-id`。

```bash
wooboo voice clone \
  --audio /path/to/sample.wav \
  --name "我的音色" \
  --language zh
```

Windows PowerShell：

```powershell
wooboo voice clone `
  --audio C:\path\to\sample.wav `
  --name "我的音色" `
  --language zh
```

失败时直接反馈挖宝AI返回的错误。
