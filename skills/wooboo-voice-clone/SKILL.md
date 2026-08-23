---
name: wooboo-voice-clone
description: Clone a reusable voice through the Wooboo AI system with user authorization, points billing, OSS direct upload, and task tracking.
---

# Wooboo AI Voice Clone

Use the `wooboo` CLI as the system entrypoint. This skill is Agent-agnostic and works with Codex, OpenClaw, Hermes, or any Agent that can run local commands.

## Required flow

1. Ensure `wooboo` is installed.
2. If authorization is missing, run `wooboo login web --open`.
3. Run `wooboo voice clone` with a local speech sample.
4. Wait for `cloneStatus` to become `ready`, `failed`, or `migration_pending`.
5. Report `item.id`; digital-human text drive uses it as `--voice-record-id`.

```bash
wooboo voice clone \
  --audio /path/to/sample.wav \
  --name "我的音色" \
  --language zh
```

Windows PowerShell:

```powershell
wooboo voice clone `
  --audio C:\path\to\sample.wav `
  --name "我的音色" `
  --language zh
```

`--prefix` is a backward-compatible alias for `--name`. Do not use or request upstream provider credentials. If the system returns an error, surface it instead of bypassing Wooboo AI.
