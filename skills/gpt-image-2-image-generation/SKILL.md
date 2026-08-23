---
name: gpt-image-2-image-generation
description: Generate or edit images with the Wooboo AI system's enabled gpt-image-2 model through the wooboo CLI, user authorization, points billing, OSS storage, and creation history.
---

# GPT Image 2 through Wooboo AI

Use `wooboo` as the system entrypoint. Do not call the upstream model directly or request a provider API key. This skill is Agent-agnostic and works with Codex, OpenClaw, Hermes, and similar runtimes.

If authorization is missing:

```bash
wooboo login web --open
```

Confirm that GPT Image 2 is enabled when necessary:

```bash
wooboo image models
```

Generate:

```bash
wooboo image generate \
  --model gpt-image-2 \
  --prompt "高级棚拍产品图，主体清晰，电影感灯光"
```

Edit from references:

```bash
wooboo image generate \
  --model gpt-image-2 \
  --prompt "保留主体，把背景改成高级摄影棚" \
  --reference-image /path/to/reference.png \
  --aspect-ratio 1:1 \
  --output-dir ./generated-images
```

Omit `--quality`, `--variant-key`, and `--aspect-ratio` unless the user requests a specific result; the CLI resolves the model's current enabled defaults. Report the record ID, status, result URL, and downloaded path. If the platform fails, surface the platform error and do not bypass points or creation history.

Credentials remain at `~/.wooboo-ai/credentials.json`. Never print or paste the token unless the user explicitly requests credential debugging.
