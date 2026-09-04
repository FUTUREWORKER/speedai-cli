---
name: wooboo-video-lingguang
description: 通过挖宝AI“灵光”生成视频，适用于文生视频、单图生视频和多图参考视频创作。
---

# 挖宝AI灵光视频生成

使用 `wooboo` CLI 调用“灵光”系列，模型选择和结果说明均使用挖宝AI系统名称。

## 参数补全与追问

- 先从用户消息、对话上下文和已提供的附件中提取参数；能够安全推断时直接使用，不重复询问。
- 必须有明确的视频画面或动作要求。用户没有说明要生成什么时，先追问创作内容。
- 纯文字创作使用文生视频；用户提供一张起始图片时使用单图生视频；用户要求结合多张图片时使用多图参考。
- 单图生视频缺少起始图片，或多图参考缺少参考图片时，先请用户提供相应图片。
- 时长、比例和输出目录不是阻塞参数；用户未指定时使用当前默认值。
- 如果同时缺少多个必要信息，合并成一次简短提问。

提交前运行 `wooboo video models`，确认灵光当前启用的模式、时长、比例和参考图数量限制。

文生视频：

```bash
wooboo video generate \
  --series "灵光" \
  --mode t2v \
  --prompt "一只可爱的品牌吉祥物在明亮展厅中向镜头挥手" \
  --duration-seconds 5
```

单图生视频：

```bash
wooboo video generate \
  --series "灵光" \
  --mode i2v \
  --prompt "让图片中的角色自然挥手，保持脸部和服装一致" \
  --first-frame /path/to/image.png \
  --duration-seconds 5
```

多图参考生成：

```bash
wooboo video generate \
  --series "灵光" \
  --mode r2v \
  --prompt "保持人物和产品外观一致，在简洁舞台上完成展示动作" \
  --reference-image /path/to/person.png \
  --reference-image /path/to/product.png \
  --duration-seconds 5 \
  --output-dir ./generated-videos
```

灵光的参考生成只使用图片，不使用视频、音频、文档或网页参考。用户未指定规格时使用平台当前默认值。

完成后报告任务 ID、状态、视频 URL 和本地下载路径。失败时直接反馈挖宝AI返回的错误。
