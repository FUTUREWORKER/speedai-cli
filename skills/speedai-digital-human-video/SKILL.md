---
name: speedai-digital-human-video
description: Generate a Wooboo AI digital-human video from a trained avatar using either text plus a cloned voice or a local drive-audio file.
---

# Wooboo AI Digital Human Video

Use `speedai` so authorization, points billing, OSS storage, task queues, and creation history remain inside the platform. This is an Agent-agnostic skill.

## Prerequisites

- A ready avatar record from `speedai avatar list` or `speedai avatar create`.
- Text mode: a ready voice record from `speedai voice list`.
- Audio mode: a local audio file.

## Text drive

```bash
speedai digital-human generate \
  --drive-mode text \
  --avatar-record-id <avatar-record-id> \
  --voice-record-id <voice-record-id> \
  --text "大家好，欢迎来到挖宝AI。" \
  --subtitle \
  --output-dir ./generated-videos
```

## Audio drive

```bash
speedai digital-human generate \
  --drive-mode audio \
  --avatar-record-id <avatar-record-id> \
  --audio /path/to/drive-audio.mp3 \
  --title "声音驱动视频" \
  --output-dir ./generated-videos
```

The CLI waits through `queued`, `running`, and `payment_pending`, then returns `succeeded` or `failed`. Report the task ID, billing state, points cost, video URL, and downloaded path.

Do not use the retired `speedai audio synthesize` workflow, old `--image`, or external `audioUrl` parameters.
