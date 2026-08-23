---
name: wooboo-image-generation
description: Generate or edit images with any enabled Wooboo AI image model through user authorization, dynamic model configuration, points billing, OSS storage, and creation history.
---

# Wooboo AI Image Generation

Use the `wooboo` CLI instead of calling an image-model provider directly. This skill is compatible with Codex, OpenClaw, Hermes, and other command-capable Agents.

1. Run `wooboo image models` when the requested model or supported specification is unclear.
2. If authorization is missing, run `wooboo login web --open`.
3. Submit a new task for every new generation request.
4. Omit quality and aspect ratio unless the user specifies them; the CLI will use the selected model's current default variant.

```bash
wooboo image generate --prompt "高级棚拍产品图，主体清晰，电影感灯光"
```

With an explicit model and reference image:

```bash
wooboo image generate \
  --model gpt-image-2 \
  --prompt "保留主体，把场景改成高级摄影棚" \
  --reference-image /path/to/reference.png \
  --aspect-ratio 1:1 \
  --output-dir ./generated-images
```

Report the record ID, final status, selected model/quality, image URL, and downloaded path. Never bypass platform points or history.
