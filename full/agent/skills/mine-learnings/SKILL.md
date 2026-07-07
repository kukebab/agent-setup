---
name: mine-learnings
description: Mine an AI coding-session transcript for candidate learnings — detect user-correction turns (+ the assistant's pivot) and repeated tool failures, format each into the mistakes.md schema, and queue them for review. Proposes candidates, NEVER auto-writes mistakes.md. Use when the user says "mine learnings", "learn from this session", "what did I do wrong", "review the session", or at end-of-session. Human-in-the-loop — the user approves each candidate before it lands in mistakes.md.
allowed-tools: Read Write Edit Bash Grep
---

# /mine-learnings

Close the loop **trace → learnings**. The engine reads a session transcript (JSONL), detects (a) user-correction
turns + the assistant's pivot and (b) repeated tool failures, formats each as a `mistakes.md`-schema candidate,
dedups against existing `mistakes.md`, and writes them to the review queue `agent/memory/inbox/learnings-candidates.md`.
This skill then walks the user through the candidates — they approve, and approved entries land in
`agent/memory/learnings/mistakes.md`.

Sibling of `/review-learnings` (curation) and `/lint` (wiki health). Same philosophy: **PROPOSES, never auto-applies.**

## Critical rule

**The miner writes ONLY to `agent/memory/inbox/learnings-candidates.md`.** It physically refuses any path under
`agent/memory/learnings/` (hard guard in `append_to_queue`). Promotion to `mistakes.md` happens HERE, per-item, only
after the user confirms. Never auto-promote. Never batch-apply.

## When to use

- The user says: "mine learnings", "learn from this session", "what did I do wrong", "review the session"
- End of a working session (also referenced from `/endday`) — mine the current session before it's gone
- After a session with visible back-and-forth corrections or a tool that kept failing

## Procedure

### 1. Run the engine

Default = the newest Claude Code transcript for this project. For other tools, pass `--transcript PATH`.

```bash
python agent/scripts/mine_learnings.py --no-llm        # zero setup, offline
python agent/scripts/mine_learnings.py                 # polish candidates via OpenRouter (needs OPENROUTER_API_KEY)
```

Options:
- `--no-llm` — skip the LLM formatting pass (offline / free; raw candidates).
- `--dry-run` — print candidates, do NOT write the queue (use to preview).
- `--transcript PATH` — mine a specific transcript (required for non-Claude-Code tools).
- `--session-id ID` — label for the queue block.
- `--queue PATH` — override the queue file (default `agent/memory/inbox/learnings-candidates.md`).

The script prints a summary line (`turns=… corrections=… tool_failures=… → candidates=…`) and the rendered
block, then appends to the queue unless `--dry-run`.

### 2. Read the queue

Read `agent/memory/inbox/learnings-candidates.md`. The newest mined block is at the bottom. Each candidate has
`Wrong / Correct / Why / Trigger` and a `[source]` tag (`correction` or `tool_failure`).

### 3. Present each candidate to the user (per-item)

For EACH candidate, show it and ask for a decision:

```
Candidate N [correction] — <title>
  Wrong:   <...>
  Correct: <...>
  Why:     <...>
  Trigger: <...>

→ PROMOTE to mistakes.md / PROMOTE to patterns.md / DISCARD ?
```

Do not proceed to the next item until the user decides this one. Recall-favoring detection means some candidates
will be noise — DISCARD is expected and fine.

### 4. Apply confirmed decisions

For each **PROMOTE → mistakes.md**: append to `agent/memory/learnings/mistakes.md` in the canonical format (use `Edit`
to add at the top of the entries, after the format block):

```markdown
## YYYY-MM-DD — <short title>
**Wrong:** <what the AI did>
**Correct:** <what it should have done>
**Why:** <reason>
**Trigger:** <when to recall this lesson>
```

For **PROMOTE → patterns.md** (a recurring root cause, 2+×): add a Rule/Why/Trigger entry to
`agent/memory/learnings/patterns.md` instead (mirror `/review-learnings` format).

For **DISCARD**: leave it; just remove the candidate block from the queue.

After processing, **remove the handled candidate blocks** from `agent/memory/inbox/learnings-candidates.md` (keep the
header). Promoted entries now live in `agent/memory/learnings/`; discarded ones are gone.

### 5. Confirm to the user

```
Mined <session>: <N> candidates.
Promoted to mistakes.md: <a>
Promoted to patterns.md: <b>
Discarded: <c>
Queue cleared.
```

## How detection works (for context)

- **User correction** — only a genuine typed user turn (`type:"user"`, content is a string, no `toolUseResult`,
  `promptSource=="typed"`) that matches a correction marker (`wrong, not that, redo, revert, stop, no, …`) and isn't
  a known negative phrase (`no problem`, `cannot`, `known issue`). Tool output (role `user` but a `tool_result`) is
  NEVER a correction. Add markers for your own language in `CORRECTION_MARKERS`.
- **Repeated tool failure** — `tool_result` blocks with `is_error==true`, grouped by tool name + error class;
  ≥2 of the same pair → one candidate.

Engine: `agent/scripts/mine_learnings.py`. Tests: `agent/scripts/test_mine_learnings.py` (15 tests, no network).

## Anti-patterns

- **Auto-promoting candidates** — never. Each goes through the user.
- **Editing `mistakes.md` from the script** — impossible by design (guard); do it here via `Edit` only after confirmation.
- **Treating tool errors as corrections** — they're not; the parser separates them.
- **Skipping the per-item review** — the review IS the value, same as `/review-learnings`.
