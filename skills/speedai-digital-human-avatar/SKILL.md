---
name: speedai-digital-human-avatar
description: Create, list, or delete reusable Wooboo AI digital-human avatars from local training videos through the speedai CLI.
---

# Wooboo AI Digital Human Avatar

Use this skill before digital-human generation when no ready avatar record exists.

Create and wait for training:

```bash
speedai avatar create \
  --video /path/to/avatar-training.mp4 \
  --title "品牌主理人"
```

List avatars:

```bash
speedai avatar list
```

Use an item whose `status` is `ready`; pass its `id` as `--avatar-record-id`. Non-H.264 video may be converted by the platform. Report `failed` errors directly and never submit the training file to an upstream provider.

Delete only on explicit user request:

```bash
speedai avatar delete <avatar-record-id>
```
