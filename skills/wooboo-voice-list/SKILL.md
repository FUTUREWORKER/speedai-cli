---
name: wooboo-voice-list
description: Query and select the current user's Wooboo AI cloned voices for digital-human text-driven video generation.
---

# Wooboo AI Voice List

Use the platform voice records as the source of truth. Do not query the upstream voice provider.

```bash
wooboo voice list
```

Use `voices[].id` as `--voice-record-id`. Prefer a voice whose `cloneStatus` is `ready`. Report the display name, record ID, provider voice ID, language, and clone status when they are available.

Delete only when the user explicitly asks:

```bash
wooboo voice delete <voice-record-id>
```
