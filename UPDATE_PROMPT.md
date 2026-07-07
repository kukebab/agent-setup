# Update Prompt — agent-setup

> **Read this carefully. You are an AI agent updating an existing agent-os install to a newer version of the schema.**

This document is for a project that **already has** `agent/` installed (Advanced Mode). If the
project has no `agent/` folder yet, use `INSTALL_PROMPT.md` instead — this is not a fresh install.

## Source

Reference repo: **https://github.com/kukebab/agent-setup**

Fetch its `CHANGELOG.md` and `full/agent/` contents.

---

## Procedure

### Step 1 — Read the currently installed version

Read `agent/VERSION.md` in the target project. Note its `Schema version:` date. If the file
doesn't exist, the install predates version stamping — treat the schema version as unknown
and ask the user whether to do a full diff against the current `full/agent/` instead of a
changelog-based delta.

### Step 2 — Fetch the latest CHANGELOG.md

Fetch `CHANGELOG.md` from the source repo. Find entries dated **after** the installed schema
version. If there are none, tell the user they're already up to date and stop.

### Step 3 — Summarize pending changes

For each pending changelog entry, summarize in plain language what changed and which files or
directories it touches. Show this to the user before changing anything:

```
Pending updates for [project name] (currently on schema version YYYY-MM-DD):

2026-MM-DD:
  - [change 1] — touches: [files/dirs]
  - [change 2] — touches: [files/dirs]

Apply all? Or pick specific ones?
```

**Wait for explicit confirmation.** The user's `agent/` has been customized with real project
content (priorities, learnings, agent state) — never blind-overwrite.

### Step 4 — Apply selected changes

For structural changes (renamed/moved directories, new files):
1. Diff the user's current `agent/<path>` against the source repo's `full/agent/<path>`
2. If the user's file is unmodified from the old template, it's safe to replace/move
3. If the user's file has real customization, merge carefully — preserve their content, apply
   only the structural/mechanical part of the change (e.g., a path reference update, a new
   section in a rules file)
4. Never overwrite `memory/STATE.md`, `memory/learnings/`, `memory/projects/`, `memory/daily/`,
   `memory/wiki/`, or any agent `STATUS.md`/`MEMORY.md` — those are the user's live data, not
   template content. If a changelog entry claims to touch these, treat it as a structural
   move/rename only, never a content replacement.

For behavioral/documentation-only changes (a rule clarified, a skill's procedure improved):
- Compare the user's file to the new template version
- If the user hasn't customized that file, replace it
- If they have, show the diff and ask whether to take the new version, keep theirs, or merge

### Step 5 — Bump the version stamp

Update `agent/VERSION.md`:
- `Schema version:` → the newest changelog entry date you applied
- `Last synced:` → today's date

If the user chose to skip some pending entries, note in `agent/VERSION.md` (or tell the user
directly) that some updates were deliberately deferred, so a future update pass doesn't assume
they were applied.

### Step 6 — Verify

Run `bash agent/scripts/context.sh` — should still print cleanly. If any path in `agent/rules/`,
`agent/skills/`, `agent/hooks/`, or `agent/scripts/` changed, spot-check that cross-references
between files still resolve (no stale `agent-os/` or bare `memory/`-without-`agent/` references
left behind from a partial merge).

### Step 7 — Summarize

```
Update complete.

Applied:
  - [list of changelog entries applied]

Skipped (deferred):
  - [list, if any]

Schema version: OLD_DATE → NEW_DATE

Verification:
  ✓ agent/scripts/context.sh runs cleanly
```

---

## Critical rules (do not violate)

1. **NEVER overwrite live project data** (`memory/STATE.md`, `memory/learnings/`,
   `memory/projects/`, `memory/daily/`, `memory/wiki/`, agent `STATUS.md`/`MEMORY.md`) — these
   are the user's, not template content, even if a changelog entry touches the surrounding
   structure.
2. **NEVER apply an update silently.** Always show the pending changelog entries and wait for
   confirmation, same as a fresh install.
3. **NEVER guess at a merge.** If a file has been customized and the update is non-trivial
   (not a pure path rename), show the user both versions and ask how to reconcile.
4. **ALWAYS bump `agent/VERSION.md`** after applying changes, even partial ones — otherwise the
   next update pass will re-propose already-applied changes.

## Ground truth

`CHANGELOG.md` in the source repo is the authoritative list of what changed and when. If a
changelog entry is unclear, fetch the actual current file from `full/agent/` in the source repo
and diff it directly against the user's copy.
