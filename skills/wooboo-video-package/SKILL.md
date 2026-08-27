---
name: wooboo-video-package
description: Package an existing video with Wooboo AI when the user wants automatic titles, templates, identity text, background music, or a polished packaged video rather than generative video creation.
---

# Wooboo AI Video Package

Use `wooboo video-package bootstrap` first to confirm readiness, billing, limits, catalog revision, and default templates. Use `templates` and `music` when the user wants a specific style or track.

The duration is the source video's measured duration in seconds and is required for the server-side cost precheck.

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

The CLI uploads one video, submits the task, waits for completion, and optionally downloads the result. Use `list`, `status`, `download`, or `delete` for existing tasks. Do not substitute the retired long-video workflow.
