---
name: wooboo-digital-human-video
description: 使用已训练的数字人形象生成视频，支持“文字加克隆音色”和“本地音频驱动”两种方式。
---

# 挖宝AI数字人视频

使用 `wooboo digital-human generate` 生成数字人视频。

## 参数补全与追问

- 先根据用户提供的是文字还是音频判断驱动方式；两者都没有且无法从上下文判断时，询问用户要使用文字驱动还是音频驱动。
- 必须确定一个可用的数字人形象。先运行 `wooboo avatar list`；只有一个可用形象时直接使用，存在多个且无法从用户要求中确定时请用户选择，没有可用形象时请用户先提供训练视频创建形象。
- 文字驱动必须有播报文字和可用音色。先运行 `wooboo voice list`；只有一个可用音色时直接使用，存在多个且无法确定时请用户选择，没有可用音色时请用户先提供语音样本克隆音色。
- 音频驱动必须有可访问的本地音频；缺少时请用户提供。
- 标题、字幕设置和输出目录不是阻塞参数；用户未指定时使用当前默认值。
- 如果同时缺少多个必要信息，合并成一次简短提问。

## 准备素材

- 先通过 `wooboo avatar list` 选择可用的数字人形象。
- 文字驱动需要选择一个可用音色。
- 音频驱动需要提供本地音频文件。

## 文字驱动

```bash
wooboo digital-human generate \
  --drive-mode text \
  --avatar-record-id <avatar-record-id> \
  --voice-record-id <voice-record-id> \
  --text "大家好，欢迎来到挖宝AI。" \
  --subtitle \
  --output-dir ./generated-videos
```

## 音频驱动

```bash
wooboo digital-human generate \
  --drive-mode audio \
  --avatar-record-id <avatar-record-id> \
  --audio /path/to/drive-audio.mp3 \
  --title "声音驱动视频" \
  --output-dir ./generated-videos
```

完成后报告任务 ID、状态、视频地址和本地下载路径；失败时直接反馈挖宝AI返回的错误。
