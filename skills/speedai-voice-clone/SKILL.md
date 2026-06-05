---
name: speedai-voice-clone
description: Clone a voice through the Speed AI system using the logged-in user's authorization and points billing. Use when an Agent needs to create a reusable voice from a local audio file.
---

# Speed AI Voice Clone

Use the Speed AI CLI as the system entrypoint. Do not call the upstream voice-clone provider directly.

This skill is Agent-agnostic and can be used by Codex, OpenClaw, Hermes, or any Agent runtime that can read local skill files and execute shell commands.

## Required Flow

1. Ensure `speedai` is installed.
2. If the user is not logged in, run `speedai login web --open`.
3. Clone the voice with `speedai voice clone`.
4. Report the returned voice record id. Later audio/video commands use this id as `--voice-record-id`.

## Commands

Login:

```bash
speedai login web --open
```

Clone:

```bash
speedai voice clone \
  --audio /path/to/sample.wav \
  --prefix "我的音色" \
  --language zh
```

Windows PowerShell:

```powershell
speedai voice clone `
  --audio C:\path\to\sample.wav `
  --prefix "我的音色" `
  --language zh
```

## Parameters

- `--audio`: Required local audio file. Use a clear speech sample.
- `--prefix`: Optional display name prefix for the cloned voice.
- `--language`: Optional language hint. Use `zh` for Chinese unless the user specifies another language.
- `--sex`: Optional provider sex value. Omit unless the user asks.

## Response To User

After cloning, report:

- Voice record id: `item.id`
- Provider voice id: `item.voiceId`
- Voice name: `item.voiceName`
- Clone status: `item.cloneStatus`

If cloning fails, surface the backend error. Do not retry with direct provider credentials.

