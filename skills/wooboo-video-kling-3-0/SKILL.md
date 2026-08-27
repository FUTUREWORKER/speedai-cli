---
name: wooboo-video-kling-3-0
description: Generate Kling 3.0 videos through the Wooboo AI system with user authorization, dynamic model selection, OSS direct upload, points billing, and creation history.
---

# Wooboo AI Kling 3.0 Video

Use `wooboo video generate --series kling`. Do not call Kling or another upstream provider directly.

The current backend can expose `t2v`, `i2v`, `first_last_frame`, `r2v`, and `video_edit`. Run `wooboo video models` and use only modes and duration limits returned for the selected model.

Text to video:

```bash
wooboo video generate \
  --series kling \
  --mode t2v \
  --prompt "电影感品牌短片，镜头缓慢推进，产品主体稳定" \
  --duration-seconds 5
```

For image-to-video use `--mode i2v --first-frame`; for first/last frame use `--mode first_last_frame --first-frame ... --last-frame ...`; for editing use `--mode video_edit --edit-video ...` and optional reference images.

Reference generation with mixed local media:

```bash
wooboo video generate \
  --series kling \
  --mode r2v \
  --prompt "保持人物与产品一致，参考动作视频生成品牌短片" \
  --reference-image /path/to/person.png \
  --reference-image /path/to/product.png \
  --reference-video /path/to/motion.mp4 \
  --output-dir ./generated-videos
```

Kling accepts at most one video reference; when a video is present, use no more than four reference images. It does not accept voice or audio references in the current platform contract.

Report the task ID, status, video URL, and downloaded path. Surface platform errors directly.
