---
name: review-learnings
description: Curate the agent/memory/learnings/ directory — group repeated mistakes, promote to patterns.md, archive stale entries to archive.md. Proposes changes, NEVER auto-applies. Use when user says "review learnings", "curate learnings", "audit mistakes", "promote patterns", or when agent/memory/learnings/mistakes.md exceeds ~300 lines (size trigger from /morning or /lint).
allowed-tools: Read Write Edit Bash Grep
---

# /review-learnings

Curate `agent/memory/learnings/` — keep `mistakes.md` short, active, and signal-dense. Move old or redundant entries
out without losing them.

This is the **lifecycle** skill for operational memory. Run periodically (when `mistakes.md` grows past ~300 lines)
or when noticeable noise creeps in. Sibling of `/mine-learnings`, which *feeds* the queue; this skill *curates*
what's already promoted.

## When to use

- User says: "review learnings", "curate learnings", "audit mistakes", "promote patterns"
- `/morning` or `/lint` flags `agent/memory/learnings/mistakes.md` > 300 lines
- After a big project milestone (lessons accumulated; consolidate before next phase)
- When repeated mistakes blur into similar-looking entries

## Critical rule

**This skill PROPOSES changes. It does NOT auto-apply.** Mistakes encode painful context — losing nuance is worse
than keeping noise. Every promotion / archive / merge requires user confirmation per item.

## The agent/memory/learnings/ directory (read this first)

```
agent/memory/daily/                         = raw event log, append-only (never curate)
agent/memory/learnings/mistakes.md   = active corrections (curated, ~300 lines, the hot file)
agent/memory/learnings/patterns.md   = repeated mistakes compressed into durable rules
agent/memory/learnings/decisions.md  = decision log (what we chose and why)
agent/memory/learnings/constraints.md= hard always/never rules (rarely touched)
agent/memory/learnings/archive.md    = old lessons + wins, searchable but NOT auto-loaded
```

## Procedure

### 1. Read

Read `agent/memory/learnings/mistakes.md` and `agent/memory/learnings/patterns.md` end-to-end. Note the `mistakes.md` line count.

### 2. Identify candidates (3 categories)

For each MISTAKE entry, classify:

**🔼 PROMOTE → patterns.md**
- Same root cause repeats in 2+ entries (e.g. 3 separate "agent claimed prod state without checking" stories)
- Suggest a canonical compressed rule for `patterns.md` that supersedes the individual stories

**📦 ARCHIVE → archive.md**
- Last triggered date >60–90 days ago AND no recent commit history shows the trigger condition was hit
- Old enough that it's history, not active guidance

**🔗 MERGE**
- 2+ entries describe variations of the same incident class with no meaningfully different lesson
- Propose a canonical merged entry keeping the strongest specifics from each

### 3. Output the proposal (do not edit yet)

Present to user:

```markdown
# Learnings curation proposal — YYYY-MM-DD

Current: mistakes.md = N lines / M entries · patterns.md = L rules.

## 🔼 PROMOTE (N candidates)

### Candidate 1 → new rule in patterns.md
**Stories to compress:** [list 2-3 entry titles]
**Proposed rule:**
> [compressed canonical rule — 3-5 lines]
**Confirm?** [y/n]

## 📦 ARCHIVE (N candidates)

### Candidate 1
**Entry:** "2026-01-XX — [title]"
**Reason:** Last trigger condition hit 90+ days ago, no recent recurrence
**Confirm archive?** [y/n]

## 🔗 MERGE (N candidates)

### Candidate 1
**Entries to merge:** [list]
**Proposed merged entry:**
> [text]
**Confirm?** [y/n]
```

Show the proposal. **Stop and wait** for the user to go through each item.

### 4. Apply user-confirmed changes

For each ✅ confirmed item:

**PROMOTE:**
- Add the new rule to `agent/memory/learnings/patterns.md`
- Move the source MISTAKE entries from `mistakes.md` to `agent/memory/learnings/archive.md` (append, original date preserved)

**ARCHIVE:**
- Move entry from `mistakes.md` to `agent/memory/learnings/archive.md` (append, original date preserved)

**MERGE:**
- Replace source entries with the merged canonical version in `mistakes.md`
- Append the originals to `agent/memory/learnings/archive.md` for traceability

### 5. Confirm to user

```
Curation done.

Before: mistakes.md N lines / M entries · patterns.md L rules
After:  mistakes.md N' lines / M' entries · patterns.md L+X rules

Promoted: N      Archived: N (now in archive.md)      Merged: N

mistakes.md is back under target.
```

## Anti-patterns

- **Auto-applying without confirmation** — never. The user owns this curation.
- **Deleting entries entirely** — always move to `archive.md`. Lessons are precious data.
- **Aggressive promotion** — only promote when the same root cause clearly repeats 2+ times with the same lesson. One-offs stay in `mistakes.md`.
- **Archiving recent mistakes** — keep at minimum the last 60 days in `mistakes.md`, even if they look similar to old entries.
- **Skipping the proposal step** — the proposal IS the value. Without user judgment, automation drifts.

## Why this matters

`agent/memory/learnings/mistakes.md` is loaded into AI sessions for pattern recall. Every line costs tokens AND attention.
A 700-line file with 60% noise produces worse pattern recall than a 300-line curated one. Curation is signal compression.

`agent/memory/daily/` is the raw event log — keep it append-only.
`mistakes.md` is the active layer — keep it short.
`patterns.md` is the durable layer — promote here.
`archive.md` is history — searchable, not auto-loaded.
