---
name: wooboo-video-wan3
description: Generate Flash/Wan3 videos with the Wooboo AI CLI when a request needs text-to-video or all-in-one references including images, videos, audio, a document, or a public web link.
---

# Wooboo AI Wan3 Video

Use `wooboo video models` to confirm the currently enabled `wan3.0-video` or `wan3.0-video-prime` model and its variants. Submit through Wooboo AI so authorization, points, OSS storage, queues, refunds, and creation history remain in the platform.

Use `t2v` for text-only generation and `r2v` for all-in-one reference generation. Wan3 does not accept first-frame or last-frame roles.

```bash
wooboo video generate --series wanx --model wan3.0-video --mode t2v --prompt "电影感城市夜景" --duration-seconds 10
```

For all-in-one reference, repeat image, video, or audio flags as needed. A reference file and public link are mutually exclusive.

```bash
wooboo video generate \
  --series wanx \
  --model wan3.0-video-prime \
  --mode r2v \
  --prompt "参考人物、运镜和旁白节奏制作品牌短片" \
  --reference-image ./person.png \
  --reference-video ./motion.mp4 \
  --reference-audio ./voice.mp3 \
  --duration-seconds 15 \
  --resolution 1080P \
  --audio
```

Use `--reference-file` for one supported document or `--reference-link` for one public web page. Respect the model limits returned by `wooboo video models`; do not call the upstream provider directly.
