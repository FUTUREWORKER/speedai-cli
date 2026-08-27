---
name: wooboo-viral-video-analysis
description: Analyze a Douyin video link with Wooboo AI when the user wants the original transcript, content structure, hooks, or viral-video breakdown.
---

# Wooboo AI Viral Video Analysis

Submit a public Douyin URL through the platform:

```bash
wooboo viral-video analyze --url "https://v.douyin.com/..."
```

The CLI waits for transcription and analysis, then returns the final record. Use `latest` or `status <id>` for an existing task. The platform charges points only according to its configured success workflow and stores the result in creation history. Do not download or call Douyin/model providers outside the Wooboo API.
