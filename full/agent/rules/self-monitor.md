# Self-Monitoring & Self-Healing

## Part 0: Improvement Loop (MANDATORY)

**`agent/memory/learnings/mistakes.md` is the single source of truth for past mistakes across sessions.**
(Its siblings: `patterns.md` = durable rules, `decisions.md` = decision log, `constraints.md` = hard always/never, `archive.md` = stale lessons + wins. See `agent/memory/learnings/README.md`.)

### Read on session start

At the start of every session, read `agent/memory/learnings/mistakes.md`. These are past mistakes. Don't repeat them.

### Write after every user correction

When the user corrects you ("no", "wrong", "not that", "stop"):

1. Acknowledge the correction immediately — stop the wrong approach
2. **Append to `agent/memory/learnings/mistakes.md`** with this format:

```
## YYYY-MM-DD — Short title
**Wrong:** what I did
**Correct:** what I should have done
**Why:** reason it matters
**Trigger:** when to recall this lesson
```

3. The title + trigger matter most — they determine whether future-you will recall it

### What counts as a correction

- Any pushback on your approach (not just the word "no")
- You suggesting X, user saying "do Y instead"
- You marking done, user pointing out it's broken
- You repeating a past mistake (double-severity lesson)

### What does NOT go in mistakes.md

- Scope changes ("let's do X instead of Y") — that's a decision → `decisions.md`, not a mistake
- Clarifications ("I meant X") — that's ambiguity, not a correction
- One-off typos or trivial bugs — git history covers those

### Automated capture (optional)

`/mine-learnings` reads a session transcript and proposes candidate mistakes (detected corrections + repeated
tool failures) into `agent/memory/inbox/learnings-candidates.md`. You review each and promote it to `mistakes.md`.
It never writes `agent/memory/learnings/` directly — promotion is always human-in-the-loop. Run it at end-of-session to catch
corrections you logged in the moment but forgot to write down.

### Rotation

When `mistakes.md` grows past ~300 lines → run `/review-learnings`: promote repeated mistakes to `patterns.md`,
move lessons quiet for 60+ days to `archive.md`. Append-only during work; curation is a separate deliberate action.

## Part 1: Detection (In-Session)

Before each tool call, check:

1. **Am I repeating?** Same action that failed in the last 2 iterations → STOP
2. **Same file 3+ times?** Editing the same file 3+ times this session → step back, re-read, different approach
3. **Same bash command?** Running the same command with minor variations → diagnose root cause first

If any are true: STOP. State what you're stuck on. Propose a different approach.

### Anti-Pattern Detection

Watch for these signals:

- **Analysis paralysis** — researching for >10 minutes without action → pick one approach and try it
- **Over-engineering** — adding features not requested → stop, do only what was asked
- **Ignoring context** — not reading the schema or live state before executing → always read first

## Part 2: Action (Self-Healing)

### Activation Signals

1. **Deja vu** — solving a problem you've seen before → save the solution
2. **Repeated workflow** — same sequence 2+ times → create a skill
3. **Hard-won knowledge** — discovered something non-obvious → save to memory
4. **User correction** — user corrected you → update agent/memory/rules immediately
5. **Convention discovery** — found a codebase pattern → document it
6. **Explicit request** — user asks to improve/learn/remember

### Decision Matrix: What To Do

| Signal | Action | Where |
|--------|--------|-------|
| Solved a tricky problem | Save solution | Memory wiki |
| User corrected me | Update/remove incorrect info | agent/memory/learnings/mistakes.md |
| Found a codebase convention | Document | Memory or rules |
| Same workflow 2+ times | Create a skill | `agent/skills/` |
| Existing memory is stale | Edit or delete | Memory files |
| Built something complex | Extract reusable pattern | Skill or memory |

### Memory Rules

- Read existing memory first — never write blind
- Keep `agent/memory/INDEX.md` concise (only first ~200 lines auto-load reliably)
- Use INDEX as catalog; details in topic files
- Semantic organization (by topic, not by date)
- Remove outdated entries — stale memory is worse than no memory
- NEVER persist secrets, API keys, tokens

### Skill Creation Triggers

Create a new skill only when:

- A workflow has been done 2+ times
- Clear reuse value exists
- The pattern is stable (not still evolving)

## Part 3: Correction Protocol

When the user says "no", "wrong", "not that", "stop":

1. Acknowledge the correction immediately
2. Do NOT continue the same approach
3. Ask: should this become a permanent rule?
4. If yes → update `agent/rules/` accordingly + log to `agent/memory/learnings/mistakes.md`

## Known Failure Modes

Common patterns to watch for:

- **Dead URLs** — verify URLs before suggesting
- **Wrong API signatures** — check official docs (don't trust training data)
- **Scope creep** — only edit what was asked
- **Going in circles** — different angle every retry
- **Hallucinated details** — describe ONLY what is explicitly visible
- **No API preflight** — test endpoint with curl before writing integration code
