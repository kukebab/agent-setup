# Acme Notes — AI Agent Schema (Advanced Mode)

> Control plane for the agent-os pattern: memory protocol, agent dispatch, source-of-truth map, and pointers to rules, skills, and hooks. Based on [Karpathy's LLM wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f), extended with operational state and governance for working codebases.

This file is a router. It tells your AI agent **what to read, when, and where things live** — not the full content of rules. Detailed policies live in `agent/rules/`. Workflows live in `agent/skills/`. Domain ownership lives in `agent/agents/`.

## If you are an AI agent installing this into an existing project

1. Copy this entire `agent/` folder (this file plus `memory/`, `rules/`, `skills/`, `hooks/`, `agents/`, `scripts/`) into the target repo root, unmodified in structure.
2. Drop thin stub `AGENTS.md`/`CLAUDE.md` files at the target repo root pointing back here (see the source repo's `full/AGENTS.md` / `full/CLAUDE.md` for the stub template).
3. Preserve existing project files — never overwrite or delete without asking the user first.
4. Replace the Acme Notes example content with the user's real project context (priorities, learnings, wiki topics, agent definitions).
5. Run `bash install.sh` from the source repo's `full/` directory (or the equivalent for the user's tool) to wire up adapters, git hooks, and stamp `agent/VERSION.md`.

To update an existing install to a newer version of this schema, see `UPDATE_PROMPT.md` in the source repo.

---

## Identity

Optional persona layer. If `agent/rules/identity.md` exists (renamed from `.template`), read it for the AI's name, tone, and behavioral defaults. Otherwise use neutral defaults: helpful, peer-to-peer, concise.

Communication preferences live in `agent/rules/language.md` (also `.template` until renamed).

---

## Memory protocol

### Three layers (Karpathy) + live state

| Path | Purpose | Mutability |
|---|---|---|
| `agent/memory/raw/` | Immutable source dumps (articles, transcripts, scrapes) | Never edit, never rename |
| `agent/memory/wiki/` | Topic pages, cross-linked via `[[topic-name]]` | LLM-maintained |
| `agent/memory/outputs/` | Generated deliverables (specs, research, drafts) | Append + iterate |
| `agent/memory/STATE.md` | Current priorities, blockers | Update as state shifts |
| `agent/memory/learnings/` | `mistakes` / `patterns` / `decisions` / `constraints` / `archive` | Append `mistakes.md`; curate the rest |
| `agent/memory/projects/*.md` | Per-project / per-client live state | Update as relationships evolve |
| `agent/memory/inbox/` | Un-triaged capture + the `/mine-learnings` review queue | Drained as you triage |
| `agent/memory/daily/*.md` | Append-only event log per day | New section per session |
| `agent/memory/INDEX.md` | Navigation map | Update on structural changes |

### Operations

Three operations from Karpathy's pattern, implemented as skills:

- **Ingest** → `agent/skills/ingest/SKILL.md` — reflexive on URL/file/text share
- **Query** — implicit; read `agent/memory/wiki/INDEX.md` first, drill from there
- **Lint** → `agent/skills/lint/SKILL.md` — periodic wiki health check

### Session start protocol

Read in order at the start of every session:

1. `agent/memory/STATE.md` — current priorities and blockers
2. `agent/memory/learnings/mistakes.md` — past corrections (the hot file; read every session)
3. `agent/memory/INDEX.md` + `agent/memory/wiki/INDEX.md` — navigation maps
4. Latest `agent/memory/daily/*.md` — recent events
5. `agent/memory/projects/<active>.md` if a specific project/client is in scope

This is the minimum context to act. Don't re-read the whole wiki; drill from the indexes.

---

## Single source of truth

When a fact lives in multiple places, the table below defines which is authoritative. Mirrors must update in the same commit, never independently.

| Fact | Authoritative source | Read-only mirrors |
|---|---|---|
| Project priorities | `agent/memory/STATE.md` | client files reference it |
| Client live snapshot | `agent/memory/projects/<name>.md` | STATE.md row summarizes |
| Code paths + responsibilities | `agent/agents/<name>/PROJECT_MAP.md` | — |
| Agent operational status | `agent/agents/<name>/STATUS.md` | client/STATE rows summarize |
| Today's events | `agent/memory/daily/YYYY-MM-DD.md` | STATUS event line cross-references |
| Permanent learnings | `agent/memory/learnings/` (mistakes / patterns / decisions / constraints / archive) | — |
| Learning candidates (un-promoted) | `agent/memory/inbox/learnings-candidates.md` (`/mine-learnings` queue) | promoted into `agent/memory/learnings/` only after review |

**Rule:** when you touch one source, scan its mirrors for stale markers and bring them along in the same commit. Test counts, status flags, deadline dates, and "as of YYYY-MM-DD" markers drift fastest.

The pre-commit hook (`agent/scripts/git-hooks/check-staleness.py`) hard-blocks commits where a current-state file's body changed but the date marker is stale.

---

## Behavioral rules

Auto-loaded policies. Read each rule when its trigger context applies.

| Rule | When to consult | File |
|---|---|---|
| Verification before completion | Always — non-negotiable IRON LAW | `agent/rules/quality-gate.md` |
| Plan mode for multi-stage tasks | Tasks with 3+ stages | `agent/rules/quality-gate.md` §1 |
| Bug-fix protocol (test-first) | Any bug report | `agent/rules/quality-gate.md` §4 |
| Agent dispatch + memory loop | When dispatching subagents | `agent/rules/agent-quality.md` |
| Self-correction → agent/memory/learnings/mistakes.md | Any user correction | `agent/rules/self-monitor.md` |
| Test requirements | Engines, validators, security boundaries, bugs | `agent/rules/testing.md` |
| File-size triggers | Before adding code to existing files | `agent/rules/file-size-triggers.md` |
| LLM cost discipline | When designing LLM pipelines | `agent/rules/cost-aware-llm.md` |

Rules are policy. Don't restate them — refer to them.

---

## Agent dispatch

| Task scope | Agent | When NOT to use |
|---|---|---|
| `api/`, `sync/`, `db/migrations/`, `lib/billing/` | `backend-dev` | Frontend work; cross-cutting refactors |
| Trivial fixes, single-file edits | (main agent) | Multi-file structural changes |
| Cross-domain refactors | (main agent — orchestrate) | When scope is purely single-domain |

Each domain agent maintains 4 files in `agent/agents/<name>/`: STATUS, MEMORY, PROJECT_MAP, RULES. See `agent/agents/README.md`.

**Size gate (hard rule):** ≤ 10 lines / 1 file → never dispatch an agent. Multi-file or >30 lines or deploy pipeline → dispatch the matching specialist. 10–30 lines → judgment.

---

## Skills

Reusable workflows. Invoked by trigger phrase or `/skill-name`.

| Skill | Trigger | What it does |
|---|---|---|
| `/morning` | Start of day, "morning" | Load context, propose plan |
| `/endday` | End of day, "wrap up" | Save context for next session |
| `/ingest` | URL/file/text shared | Karpathy ingest → agent/memory/raw/ + agent/memory/wiki/ + agent/memory/daily/ |
| `/lint` | "lint", "audit memory" | Wiki health check (mechanical + semantic) |
| `/create-spec` | "spec", before 2+ hour task | Generate structured spec → agent/memory/outputs/specs/ |
| `/call-debrief` | Transcript pasted, audio dropped | Extract decisions/actions → agent/memory/outputs/call-debriefs/ |
| `/web-researcher` | "research", "investigate", "compare" | Multi-source research → agent/memory/outputs/research/ |
| `/create` | "make a skill", "automate this" | Bootstrap new skill or agent |
| `/swarm` | "parallel agents", "decompose" | Multi-agent task decomposition |
| `/review-learnings` | "review learnings", file > target size | Curate `agent/memory/learnings/` — promote to patterns, archive stale |
| `/mine-learnings` | "mine learnings", end of session | Mine the session transcript → candidate learnings into the review queue (human-approved before promotion) |

See `agent/skills/README.md` and individual `SKILL.md` files for full procedures.

---

## Hooks

Runtime enforcement. Fire automatically at events.

| Hook | When | What |
|---|---|---|
| `session-start.sh` | Session start | Auto-loads `STATE.md` + recent context via `agent/scripts/context.sh` |
| `commit-memory-reminder.sh` | After successful `git commit` | Nudges memory updates per commit class |
| `agent/scripts/git-hooks/pre-commit` | Before `git commit` | PII block + staleness check (hard-blocks 3 patterns) |

See `agent/hooks/README.md` and `agent/scripts/git-hooks/README.md` for wiring.

---

## File-size discipline

Before adding code to an existing file, run `wc -l <file>`:

- < 500 lines → edit freely
- 500–1000 → ask user about split if introducing new concern
- 1000–2000 → no new features without explicit approval
- > 2000 → stop, decompose first

Full rule + cohesion exceptions: `agent/rules/file-size-triggers.md`.

---

## References

- **[Karpathy's LLM wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)** — the foundational pattern
- **[agent-os-starter](https://github.com/bruceorchestrator/agent-os-starter)** — this repo
- **`agent/memory/INDEX.md`** — top-level navigation
- **`agent/rules/`** — behavioral policies (read on demand, per the rules table above)
- **`agent/skills/`** — workflows (invoked by trigger or slash command)
- **`agent/agents/`** — domain specialists with persistent state
- **`agent/VERSION.md`** — installed schema version; compare against the source repo's `CHANGELOG.md` to find pending updates

---

## When to update this file

Add to AGENTS.md ONLY when:

- A new agent is added to dispatch map
- A new rule warrants a row in the rules table
- A new skill is added to skills routing
- The source-of-truth map needs a new fact

DO NOT add to AGENTS.md:

- Rule content (lives in `agent/rules/<name>.md`)
- Skill procedures (lives in `agent/skills/<name>/SKILL.md`)
- Code examples
- Detailed conventions

Keep this file under 250 lines. If it grows past that, extract content into the layered system below it.
