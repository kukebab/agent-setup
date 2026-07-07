# Learnings candidates — review queue

This is the **review queue** populated by `/mine-learnings` (engine: `scripts/mine_learnings.py`).
Each entry below is a **CANDIDATE** mined from a session transcript — a detected user-correction or a
repeated tool failure, formatted into the `mistakes.md` schema (`Wrong / Correct / Why / Trigger`).

**Nothing here is auto-promoted.** These are proposals, not approved learnings. The miner writes ONLY to this
file and physically refuses to touch `memory/learnings/`.

Promote / discard flow is via `/mine-learnings`: you review each candidate per-item and decide
PROMOTE → `memory/learnings/mistakes.md` (or `patterns.md`) / DISCARD. Approved entries are moved into the
learnings file by the skill; the handled candidate is then removed from this queue.

---

_No candidates yet. Run `/mine-learnings` (or `python scripts/mine_learnings.py`) to populate._
