---
name: speedai-audio-synthesis
description: Synthesize speech audio through the Speed AI system using a cloned voice record id, user authorization, points billing, and system history.
---

# Speed AI Audio Synthesis

Use the Speed AI CLI as the system entrypoint. Do not call the upstream voice-merge provider directly.

## Required Flow

1. Ensure `speedai` is installed.
2. If the user is not logged in, run `speedai login web --open`.
3. If no voice record id is known, run `speedai voice list`.
4. Synthesize audio with `speedai audio synthesize`.
5. Report the task id, status, audio URL, duration, points cost, and downloaded path when available.

## Commands

```bash
speedai audio synthesize \
  --text "大家好，欢迎来到极速 AI。" \
  --voice-record-id <voice-record-id> \
  --language zh \
  --speech-rate 1 \
  --pitch-rate 1 \
  --volume 50 \
  --output-dir ./generated-audio
```

Windows PowerShell:

```powershell
speedai audio synthesize `
  --text "大家好，欢迎来到极速 AI。" `
  --voice-record-id <voice-record-id> `
  --language zh `
  --speech-rate 1 `
  --pitch-rate 1 `
  --volume 50 `
  --output-dir .\generated-audio
```

## Parameters

- `--text`: Required speech text.
- `--voice-record-id`: Required Speed AI voice record id from `speedai voice list`.
- `--language`: Optional language hint. Use `zh` unless the user specifies another language.
- `--speech-rate`: Optional speech rate. Typical range is `0.5` to `2`.
- `--pitch-rate`: Optional pitch rate. Typical range is `0.5` to `2`.
- `--volume`: Optional volume. Typical range is `0` to `100`.
- `--prompt`: Optional voice instruction.
- `--output-dir`: Optional local audio download directory.

## Response To User

After generation, report:

- Audio task id
- Status
- Audio URL
- Audio duration
- Points cost
- Downloaded local path if present

If synthesis fails, surface the backend error. Do not silently fall back to provider direct calls.

