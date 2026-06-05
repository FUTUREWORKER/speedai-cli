---
name: speedai-digital-human-video
description: Generate a digital-human video through the Speed AI system from a portrait image, synthesized audio URL, and cloned voice record id.
---

# Speed AI Digital Human Video

Use the Speed AI CLI as the system entrypoint. Do not call the upstream digital-human provider directly.

Digital-human video generation requires an existing audio URL. If the user only provides text, first use the audio synthesis skill to create audio, then pass the resulting `audioUrl` and `audioDuration` to this skill.

## Required Flow

1. Ensure `speedai` is installed.
2. If the user is not logged in, run `speedai login web --open`.
3. Ensure a voice record id exists. If needed, run `speedai voice list` or clone a voice first.
4. Ensure speech audio exists. If needed, run `speedai audio synthesize` first.
5. Generate the digital-human video with `speedai digital-human generate`.
6. Report the task id, status, video URL, cover URL, and downloaded path when available.

## Commands

```bash
speedai digital-human generate \
  --image /path/to/portrait.png \
  --text "大家好，欢迎来到极速 AI。" \
  --voice-record-id <voice-record-id> \
  --audio-url <audio-url> \
  --audio-duration 12.3 \
  --language zh \
  --model XPro1.0 \
  --output-dir ./generated-videos
```

Windows PowerShell:

```powershell
speedai digital-human generate `
  --image C:\path\to\portrait.png `
  --text "大家好，欢迎来到极速 AI。" `
  --voice-record-id <voice-record-id> `
  --audio-url <audio-url> `
  --audio-duration 12.3 `
  --language zh `
  --model XPro1.0 `
  --output-dir .\generated-videos
```

## Parameters

- `--image`: Required portrait image path.
- `--text`: Required speech text matching the audio.
- `--voice-record-id`: Required Speed AI voice record id.
- `--audio-url`: Required audio URL, usually returned by `speedai audio synthesize`.
- `--audio-duration`: Required audio duration in seconds.
- `--language`: Optional language hint. Use `zh` unless the user specifies another language.
- `--model`: Optional digital-human model. Typical values: `XPro1.0` for fast mode, `XPro2.0` for standard mode.
- `--prompt`: Optional audio generation prompt snapshot.
- `--video-prompt`: Optional video behavior prompt.
- `--output-dir`: Optional local video download directory.

## Response To User

After generation, report:

- Digital-human task id
- Status
- Video URL
- Cover URL if present
- Downloaded local path if present

If generation fails, surface the backend error. Do not silently fall back to provider direct calls.

