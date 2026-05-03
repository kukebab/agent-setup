# Memory — Top-level Index

Quick map of what's in `memory/`. Your AI agent reads this at session start to know where to look.

## Live state (read these first every session)

- [`STATE.md`](STATE.md) — current priorities, blockers, status
- [`learnings.md`](learnings.md) — mistakes (don't repeat), wins (remember), patterns
- [`USER.md`](USER.md.template) — optional: user's personal context, preferences, work patterns
- [`clients/`](clients/) — per-client state files

## Knowledge layers (Karpathy)

- [`raw/`](raw/) — immutable source dumps. Never edit, never rename
- [`wiki/`](wiki/) — topic pages, cross-linked. See [`wiki/INDEX.md`](wiki/INDEX.md) for catalog
- [`outputs/`](outputs/) — generated deliverables (specs, research, drafts, reports)

## Time series

- [`daily/`](daily/) — append-only event log per day. Latest day = freshest context

## How to navigate

For a specific question, read in this order:

1. `STATE.md` — what are we focused on right now?
2. `wiki/INDEX.md` → relevant `wiki/*.md` page — what do we already know?
3. Latest `daily/*.md` — what happened recently?
4. `clients/<client>.md` if it's a client question
5. `outputs/` if it's a deliverable that already exists

Don't re-read everything. The index files (this one + `wiki/INDEX.md`) are the only "always read" pages. Drill from there.
