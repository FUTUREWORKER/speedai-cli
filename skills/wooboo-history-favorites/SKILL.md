---
name: wooboo-history-favorites
description: Query, download, delete, favorite, or unfavorite Wooboo AI creations when the user wants to manage previously generated platform media and records.
---

# Wooboo AI History and Favorites

Use `wooboo history list` to find record IDs and statuses across image, video, digital-human, agent, analysis, and video-package work.

```bash
wooboo history download <record-id> --output-dir ./downloads
wooboo favorite add --kind image --record-id <record-id>
wooboo favorite list
```

Deleting history or removing a favorite changes platform data. Run `history delete` or `favorite remove` only when the user explicitly requests it and use the exact ID returned by the platform. A favorite is an independent stored copy; deleting history and removing a favorite are different actions.
