---
name: gpt-image-2-image-generation
description: Generate images through the Speed AI system using the logged-in user's authorization, points billing, OSS storage, and creation history. Use when an Agent should generate an image with gpt-image-2 or the Speed AI system image generator through the speedai CLI.
---

# GPT Image 2 System Image Generation

Use this skill as a Speed AI system entrypoint, not as a direct model-provider client.

This skill is Agent-agnostic. It can be used by Codex, OpenClaw, Hermes, or any other Agent runtime that supports reading local skill/instruction files and running shell commands.

Required flow:

1. Run the `speedai` CLI.
2. If not logged in, use `speedai login web --open` so the user authorizes in the H5 app.
3. Generate images by running `speedai image generate ...`.
4. Let the Speed AI backend handle model selection, points billing, OSS upload, queue processing, and creation history.

Do not call the upstream `gpt-image-2` provider directly for normal user requests. Direct provider calls bypass user authorization, points, and history.

## Commands

Login:

```bash
speedai login web --open
```

Generate:

```bash
speedai image generate \
  --prompt "A clean product photo of a matte black wireless speaker on a concrete table" \
  --aspect-ratio auto \
  --quality 1k
```

With references:

```bash
speedai image generate \
  --prompt "Turn the reference into a polished studio product render" \
  --reference-image /path/to/reference.png \
  --aspect-ratio 1:1 \
  --quality 1k
```

Windows PowerShell multiline example:

```powershell
speedai image generate `
  --prompt "A clean product photo of a matte black wireless speaker on a concrete table" `
  --aspect-ratio auto `
  --quality 1k
```

Account check:

```bash
speedai account
```

Default image download directory:

```bash
speedai config set output-dir ./generated-images
```

Logout:

```bash
speedai logout
```

## Environment

The installed CLI defaults to the production Speed AI service:

```text
https://speed.ycszai.com
```

For local development, pass explicit bases:

```bash
speedai --api-base http://127.0.0.1:3000 --h5-base http://127.0.0.1:5174 login web --open
```

Address priority:

1. Command-line `--api-base` / `--h5-base`
2. Environment variables `SPEEDAI_API_BASE` / `SPEEDAI_H5_BASE`
3. Persistent config `speedai config set api-base ...` / `speedai config set h5-base ...`
4. Production default `https://speed.ycszai.com`

## Parameters

- `--prompt`: Required image prompt.
- `--scene`: System image scene. Defaults to `图片生成`.
- `--aspect-ratio`: Passed to the Speed AI system endpoint. For `gpt-image-2`, use `auto`, `1:1`, `16:9`, or `9:16`.
- `--quality`: Passed to the Speed AI system endpoint. Typical values are `1k`, `2k`, `4k`, `standard`, or `hd`; backend variant rules remain authoritative.
- `--variant-key`: Optional model variant key. Omit unless the user asks or a prior bootstrap lookup establishes the correct value.
- `--model-config-id`: Optional model config id. Omit to use the system default model for the scene.
- `--reference-image`: Optional reference image path. May be passed multiple times; backend limits remain authoritative.
- `--output-dir`: Optional local download directory after the backend record succeeds. Overrides `SPEEDAI_OUTPUT_DIR` and `speedai config set output-dir ...`.

## Credentials

`speedai login web --open` creates an authorization grant in the API, opens `/cli/authorize?code=...` in H5, and waits for the logged-in user to approve it. The CLI stores the resulting system session token at:

```text
~/.speed-ai/credentials.json
```

Do not print or paste the token unless the user explicitly asks for debugging. Prefer `speedai account` to verify login state.

## Response To User

After generation, report:

- Record id
- Status
- Result image URL if present
- Downloaded local path if `--output-dir` was used

When a local path exists and the Agent UI supports local image rendering, render it:

```markdown
![generated image](C:/absolute/path/to/image.png)
```

If generation fails, surface the backend error. Do not silently fall back to direct provider calls or another model.

