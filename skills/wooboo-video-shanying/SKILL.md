---
name: wooboo-video-shanying
description: 通过挖宝AI“闪影”生成视频，适用于文生视频以及结合图片、视频、音频、文档或公开网页的全能参考创作。
---

# 挖宝AI闪影视频生成

使用 `wooboo` CLI 调用“闪影”系列，模型选择和结果说明均使用挖宝AI系统名称。

## 参数补全与追问

- 先从用户消息、对话上下文和已提供的附件中提取参数；能够安全推断时直接使用，不重复询问。
- 必须有明确的视频画面或动作要求。用户没有说明要生成什么时，先追问创作内容。
- 纯文字创作使用文生视频；用户要求参考生成时，根据其素材自动选择全能参考模式。
- 用户明确要求参考某张图片、视频、音频、文档或网页，但没有提供相应素材或可访问链接时，先请用户补充。
- 时长、比例、分辨率和输出目录不是阻塞参数；用户未指定时使用当前默认值。
- 如果同时缺少多个必要信息，合并成一次简短提问。

提交前运行 `wooboo video models`，确认闪影当前启用的模式、时长、分辨率和素材限制。

文生视频：

```bash
wooboo video generate \
  --series "闪影" \
  --mode t2v \
  --prompt "电影感城市夜景，镜头缓慢推进" \
  --duration-seconds 10
```

全能参考生成可以重复传入图片、视频或音频：

```bash
wooboo video generate \
  --series "闪影" \
  --mode r2v \
  --prompt "参考人物、运镜和旁白节奏制作品牌短片" \
  --reference-image ./person.png \
  --reference-video ./motion.mp4 \
  --reference-audio ./voice.mp3 \
  --duration-seconds 15 \
  --output-dir ./generated-videos
```

还可以使用一个 `--reference-file` 或一个 `--reference-link`，两者不能同时使用。用户未指定规格时使用平台当前默认值；所有限制以 `wooboo video models` 返回结果为准。

完成后报告任务 ID、状态、视频地址和本地下载路径；失败时直接反馈挖宝AI返回的错误。
