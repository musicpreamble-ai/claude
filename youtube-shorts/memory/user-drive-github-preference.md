---
name: user-drive-github-preference
description: "User prefers deliverables saved to a GitHub repo (musicpreamble-ai/claude) instead of Google Drive; I couldn't write to their Drive folder from this environment"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 7d165d56-8b25-451a-b5a3-f7db3e329b35
  modified: 2026-11-15T19:05:27.544Z
---

The user asked me to save all work in a Google Drive folder (https://drive.google.com/drive/folders/1JyLvZUtOK1HjuJ3O0-2R3Er_G-M_ASxu), but this environment has **no Google Drive authentication**, so a scripted upload failed (Drive API returns 403; rclone needs the user to create their own OAuth client_id, which requires their Google Cloud console action).

The user then pivoted: they created a **public GitHub repo `musicpreamble-ai/claude`** and asked me to push everything there instead.

**Why:** GitHub push works from this environment via `git` + HTTPS (no OAuth dance needed if credentials are available). Drive doesn't.

**How to apply:** For this user, default to saving/pushing deliverables to the GitHub repo `https://github.com/musicpreamble-ai/claude.git` (folder for this project = the `shorts-design/` package). If they mention Google Drive again, remind them Drive needs their own OAuth client_id and offer GitHub instead.
