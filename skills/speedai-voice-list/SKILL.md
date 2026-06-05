---
name: speedai-voice-list
description: Query the current user's Speed AI cloned voice list and digital-human voice configuration through the speedai CLI.
---

# Speed AI Voice List

Use this skill when the Agent needs to find available cloned voices or select a `voiceRecordId` for audio or digital-human generation.

Do not query the upstream provider directly. The Speed AI backend is the source of truth for user-owned voices.

## Required Flow

1. Ensure `speedai` is installed.
2. If the user is not logged in, run `speedai login web --open`.
3. Query voices with `speedai voice list`.
4. Use the returned `voices[].id` value as `--voice-record-id` in later commands.

## Commands

```bash
speedai voice list
```

## Response To User

Summarize the useful fields:

- `id`: voice record id used by CLI commands
- `voiceName`: display name
- `voiceId`: provider voice id
- `cloneStatus`: clone status
- `createdAt`: creation time

Prefer the most recent successfully cloned voice when the user does not specify one.

