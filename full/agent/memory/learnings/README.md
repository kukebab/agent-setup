# learnings/

**Behavior-changing rules** — split from a single `learnings.md` once it outgrew one file (Advanced Mode).
These change how the agent behaves; they are NOT project state (that's `projects/`) or evidence (that's `outputs/`).

| File | Holds | Lifecycle |
|---|---|---|
| `mistakes.md` | Recent corrections (last ~60–90 days) still likely to repeat | Append after every user correction. Promote to a PATTERN if the same root cause repeats 2+ times. |
| `patterns.md` | Durable rules graduated from repeated mistakes + insights ("what works") | Always-on. Stays unless invalidated. |
| `decisions.md` | Decision log — what we chose and why | Append when a non-obvious decision is made. |
| `constraints.md` | Hard "always / never" rules (curated, inviolable) | Rare edits. Only when a new inviolable rule is established. |
| `archive.md` | Stale lessons + historical wins (no longer triggering) | Where `/review-learnings` moves entries that have gone quiet. |

**Why split?** A single append-only `learnings.md` works for the first month or two, then degrades: every session
loads the whole file (token cost), stale entries drown active ones (signal-to-noise), and repeated mistakes never
graduate into canonical rules. Splitting by *lifecycle* keeps the hot file (`mistakes.md`) small and signal-dense.

> **Simple Mode keeps a single `memory/learnings.md`** with MISTAKES / PATTERNS / WINS sections — don't carry this
> directory into a solo setup until you actually outgrow one file. This split is the Advanced-Mode shape.

## Session start

Read `mistakes.md` (the hot file) every session — those are the corrections most likely to recur. `patterns.md`
and `constraints.md` are the durable layer; skim on demand. `archive.md` is history — search it, don't auto-load it.

## Feeding the queue

`/mine-learnings` reads a session transcript and proposes candidate entries into `inbox/learnings-candidates.md`.
You review each one and promote it here (or discard). The miner never writes to this directory — promotion is always
human-in-the-loop. See `agent/skills/mine-learnings/SKILL.md`.
