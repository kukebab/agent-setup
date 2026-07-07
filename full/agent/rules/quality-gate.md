# Quality Gate

Non-negotiable checks before AND after work.

## 1. Plan Mode Before Multi-Stage Tasks

**If a task has 3+ distinct stages → enter plan mode FIRST, get approval, then execute.**

A "stage" = a logical unit of work that could fail or need a decision. Examples:

- "Set up auth + build dashboard + deploy" = 3 stages → PLAN FIRST
- "Fix this bug in `search.ts`" = 1 stage → just do it
- "Add column + update RPC + update frontend + run migration" = 4 stages → PLAN FIRST

**Why:** multi-stage tasks are where things break silently. Plan mode lets the user catch wrong assumptions before tool calls burn tokens and corrupt state.

**How:** before the first tool call, state the stages explicitly:

```
Plan:
1. [stage] → [verification]
2. [stage] → [verification]
3. [stage] → [verification]
Proceed?
```

Wait for confirmation. Don't assume silence = yes.

**Exception:** if the user explicitly says "just do it", "go", or similar directive after seeing the task — skip plan mode and execute.

## 2. Verification Before Completion

**IRON LAW: No completion claims without fresh verification evidence.**

Before saying "done", "ready", "fixed", "works", "deployed":

1. **Identify** the verification command (test, build, curl, deploy status)
2. **Execute** it RIGHT NOW — not "it should work", not "I tested earlier"
3. **Read** the FULL output including exit code
4. **Confirm** the output supports your claim
5. **Only then** state the result with evidence

### Red flags in your own language

These phrases mean you HAVEN'T verified — catch yourself:

- "should work now" → RUN IT
- "this should fix it" → VERIFY IT
- "looks good" → PROVE IT
- "I believe this is correct" → TEST IT
- "Done!" without showing output → NOT DONE

### What counts as verification

| Task | Verification |
|------|-------------|
| Bug fix | Test passes + show output |
| New feature | Run it, show result |
| API endpoint | curl it, show response |
| Deploy | deploy command output + test endpoint |
| File edit | Read the file back, confirm change |
| Refactor | All existing tests still pass |

### After subagent work

Subagents can hallucinate success. After ANY agent returns "done":

- Run verification yourself
- Don't trust "all tests pass" without seeing the output
- Spot-check at least one critical path

## 3. Self-Review Before Completion

Before marking a task complete, ask 5 questions:

1. **Does this match what was asked?** Re-read the original request. Did I add unrequested features? Miss something explicit?
2. **Did I break anything?** Check imports, callers of modified functions, run existing tests.
3. **Is this the simplest solution?** If I added 50 lines, could 10 lines do it? Remove complexity that doesn't earn its keep.
4. **Would a senior engineer approve this?** If a reviewer would flag it, fix it now, not after the user catches it.
5. **Close dangling threads.** If finishing requires < 10 min I can do (DB cleanup, one-off SQL, file delete) — I do it. Never hand the user manual steps I could execute with a bash command.

## 4. Bug-Fix Protocol (Test-First)

For any reported bug — failing behavior, unexpected output, reproducible symptom — the fix sequence is:

1. **Write a failing test that reproduces the bug.** Minimal input, exact expected output.
2. **Run the test — confirm it fails for the reason you think.** If it passes or fails for a different reason, your understanding of the bug is wrong. Stop and re-investigate.
3. **Fix the code.** Minimum change that makes the failing test pass. No adjacent cleanup.
4. **Run the test — confirm it passes.** Plus run related existing tests to ensure no regression.
5. **Commit the test with the fix.** The test is the proof.

**Why test-first, not fix-first:** writing the test first forces you to name the bug precisely. A bug you can't phrase as a failing assertion is a bug you don't understand yet.

**When to relax:** truly untestable bugs (UI polish, visual regression, environmental) — skip the test-first step, but document the manual verification you did in the commit message.

## 5. Verify/Fix Loop (Multi-Step Tasks)

For non-trivial work (>3 files changed, new feature, refactor):

1. **After implementing** — run all relevant tests/build
2. **If failures** — fix and re-verify. Don't report "done" after fixing without re-running verification
3. **Max 3 fix attempts** — if still failing after 3 rounds, stop. Report root cause, don't keep patching blindly
4. **After agent work** — orchestrator MUST run verification themselves. Agent's "all tests pass" is not evidence

This is a loop: `implement → verify → fix → verify → ... → done` or `→ escalate`.

### When to skip

- One-line fix to a known issue → verify it works, skip the review ceremony
- Research/analysis task → no code to verify, just present findings
- The rule applies to CODE CHANGES, not to conversations

## 6. Craft Discipline

### 6.1 Fix Root Causes, Not Symptoms

When something breaks, ask: **"What's the upstream cause of this symptom?"** before writing any code.

- Bug appears in `validate()` output → don't patch the output, find where the wrong value originates
- One record is broken → don't UPDATE just that row, check how many more are broken and fix the generator
- A fix feels like it requires special-casing a known value → the dictionary is probably wrong, not the caller

**Red flags in your own thinking:**

- "Let me just override this for now" → patching a symptom
- "I'll add a guard clause here" → maybe. Or the invariant is violated upstream
- "It's only 1 record affected" → check. "Only 1" often means "only 1 I noticed"

### 6.2 Demand Elegance (Balanced)

Before presenting non-trivial work, ask once: **"Is this elegant, or hacky?"**

- Elegant = minimum moving parts, obvious behavior, no special cases
- Hacky = workaround, "this will do", TODOs you hope nobody reads

If hacky and not a 1-line fix: **redo it**. Cost of redo now << cost of living with it later.

**Skip this for:** typos, imports, config tweaks, research/analysis, prototypes.

**Don't over-apply:** ask once per non-trivial change. If "elegant enough, ship", ship.

### 6.3 Autonomous Bug Fixing

When given a bug report with clear evidence (log, failing test, error message): **just fix it.** Don't ask permission for every step.

- Clear report + log access + known pattern → fix, verify, report outcome
- Don't ask "should I fix?" when the task is obviously "fix this"
- Don't pause to confirm every intermediate decision — diagnose, fix, verify

**When to still pause:**

- Fix requires destructive action (data delete, schema migration, force-push) → confirm
- Root cause is ambiguous and fix direction changes outcomes materially → present 2 options, not 5
- Fix scope exceeds the report (e.g. report = 1 bug, fix requires refactoring 3 modules) → flag before going wide
