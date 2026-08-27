---
name: wooboo-ip-clone
description: Create, update, inspect, or attach photo, video, and voice assets to a Wooboo AI IP clone for later agent and video-generation use.
---

# Wooboo AI IP Clone

List existing clones before creating a duplicate. A clone requires a name, company name, and business description.

```bash
wooboo ip-clone create --name "胡老师" --company "未来工作室" --business "AI产品培训与咨询"
wooboo ip-clone list
```

Attach one current asset per type with `wooboo ip-clone upload <id> --type photo|video|voice --file <path>`. Uploading the same type replaces the previous asset. Use `parse-file --file profile.txt` or a DOCX to extract clone fields before creation when appropriate.

Creating, changing, replacing assets, or deleting a clone mutates the user's platform data; do it only when requested and report the returned clone or asset ID.
