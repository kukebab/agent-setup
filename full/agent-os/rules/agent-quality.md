# Agent Quality Protocol

When dispatching subagents for non-trivial tasks (>1 file, >20 lines of change), discipline matters. This rule defines that discipline.

## Dispatch Rules

1. **Plan before dispatch** — break work into tasks of 2-5 min each. Specify exact file paths, what changes, how to verify.
2. **One agent = one focused scope** — don't ask one agent to do 5 unrelated things. Split by domain.
3. **Parallel dispatch when independent** — if tasks don't share files/state, run concurrently.

## Execution Rules

4. **Silent execution** — agents must NOT narrate ("Now I will read..."). Execute silently, report result with evidence.
5. **Failure protocol** — on failure: state what broke, root cause, what was attempted. Halt. No speculative "maybe try X".

## Token Efficiency

Agents waste budget when they re-explore code they already mapped. `PROJECT_MAP.md` exists to prevent this.

6. **PROJECT_MAP first** — Before any Read/Grep/Glob, check the agent's `PROJECT_MAP.md` for the file's role + location. If a file isn't there, ask the orchestrator before exploring.

7. **Grep before Read for large files** (>500 lines). If you know the symbol, `grep -n "def foo\|class Foo"` then Read a targeted 30-50 line window via `Read offset+limit`.

   **By file size:**
   - ≤ 300 lines: Read whole file
   - 300–1000 lines: Grep to find section, Read with `offset+limit`
   - 1000+ lines: Grep twice (structure + target), Read only windows

8. **No redundant re-reads.** After you've read a file section, don't re-read it. If unsure, scroll back, don't re-fetch.

9. **Edit in batches.** If making 3 edits to the same file, emit all 3 `Edit` calls in one message. Each intermediate Read is waste.

## Memory-Loop Scaling

Memory-loop updates (daily + learnings + STATUS + memory + project map) are mandatory for *significant* work, but scale down for minor fixes:

| Commit class | Minimum updates |
|---|---|
| **Structural** (new file/module/migration) | FULL: daily + PROJECT_MAP (new file entry) + STATUS (event line) + MEMORY only if non-obvious gotcha + learnings only if mistake/pattern |
| **Feature / bug fix** (30+ lines, new behavior) | daily (1-2 bullets) + STATUS (event line). Skip PROJECT_MAP/MEMORY unless non-obvious gotcha |
| **Minor** (<30 lines, single-file tweak, typo, config bump) | daily (1 bullet) ONLY. Skip everything else |

## Verification After Agent Dispatch (IRON LAW)

**Agents can hallucinate success. The orchestrator (main session) MUST verify before reporting "done" to the user.**

### Mandatory triggers — verification is non-negotiable when:

- Agent modified **>1 file** OR **>30 lines of code**
- Agent claimed "tests pass" / "build succeeds" / "deployed" / "all green"
- Agent ran any of: tests, build, type check, deploy, DB migration
- Agent touched: auth, security, migrations, billing, anything sensitive
- Agent's task ran **>10 minutes** OR returned >500 words of summary
- The work is being reported to the user as "shipped" / "deployed" / "complete"

If ANY trigger applies → run verification before saying "done".

### Verification checklist

| What agent did | Verification I run myself |
|---|---|
| Modified Python | `pytest <relevant test file> -v` — full output, exit 0 |
| Modified TS/TSX | `npm run build` OR `npm run typecheck` — show 0 errors |
| Added endpoint | `curl <endpoint>` with realistic payload, check 200 + body shape |
| Added cron/job | check schedule registered |
| DB migration | dry-run first; check generated SQL is what was intended |
| Wrote/edited config | Read the file myself, confirm exact change |
| Wrote a doc / memory file | Read the file myself, confirm structure |
| Refactored code | Run existing test suite — baseline must still pass |
| Spot-check at minimum 1 critical file | Read one of the modified files — confirm change |

### Red flags in my own language

When I write any of these phrases, **stop, run the verification, replace with evidence**:

- "Agent shipped X" → did I see the output? exit code?
- "All tests pass" → did I see the output myself?
- "Deployed successfully" → did I curl it?
- "Build succeeds" → did I run build myself?
- "Looks good" / "Should work" / "I believe this is correct" → all violation tells
- "Subagent handled it" → not enough; subagents lie

## State Management (for agents with a folder)

Agents with `agents/<name>/` manage 4 files. Different files, different purposes:

| File | Purpose | When to update |
|------|---------|----------------|
| `STATUS.md` | Events log + current state + TODO. "What happened, what's next." | After EVERY significant task |
| `MEMORY.md` | Long-term lessons, gotchas, patterns, decisions with rationale. "What future-me needs to know." | When you discover something non-obvious worth remembering |
| `PROJECT_MAP.md` | Where the code lives. File/module responsibilities. | When architecture changes |
| `RULES.md` | Hard rules: always-do / never-do, with reasoning. | Rarely — when a new rule is established from painful experience |

### After agent work — mandatory

1. **Always update STATUS.md** — every significant task gets an entry.
2. **Update MEMORY.md only when you learned something non-obvious** — ask: "If a new agent picked this up tomorrow, would this gotcha save them hours?" If yes, record. If "did X and it worked as expected" — don't pollute.
3. **Update PROJECT_MAP.md only for structural changes.**
4. **Update RULES.md only when establishing a new inviolable rule.** Rare.

### Test for MEMORY.md worthiness

Record if ANY:
- Hit unexpected error, fix required reading docs/experimenting
- Platform behavior differs from official docs
- Naming/schema convention that's non-obvious but load-bearing
- A decision that looks arbitrary but has specific reasoning

DO NOT record:
- "Task completed successfully"
- Information already in RULES or main schema
- Obvious things ("use HTTPS")
- Ephemeral details (specific commit hashes)
