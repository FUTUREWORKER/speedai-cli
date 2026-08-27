---
name: wooboo-creative-agent
description: Chat with a published Wooboo AI agent through the CLI when the user wants creative planning, copywriting, image/video task orchestration, IP-clone-aware answers, or file-assisted agent work.
---

# Wooboo AI Agent Chat

Use the published agent code requested by the user. For the platform creative agent, use `creative-agent`.

```bash
wooboo agent bootstrap creative-agent
wooboo agent chat creative-agent --text "为这个新品写短视频脚本，并生成封面图"
```

Continue a conversation with `--conversation-id`; add `--ip-clone-id` when the user selected a Wooboo IP clone; repeat `--file` for attachments. The CLI uses the platform NDJSON stream and returns the completed reply, billing, conversation, and task information.

Use `conversations`, `messages`, `clear`, and `cancel` only when the user asks to manage that state. Agent chat can consume points or create media tasks, so report the returned billing and task IDs and never claim an unsubmitted result exists.
