# Install Prompt — agent-os-starter

> **Read this carefully. You are an AI agent installing a memory + governance system into the user's existing project.**

This document is the install procedure. Follow it step by step. Do not skip steps. Do not improvise.

## Source

Reference repo: **https://github.com/bruceorchestrator/agent-os-starter**

Fetch its contents (via web fetch, git clone, or your equivalent). Two modes ship there:

- **`starter/`** (Simple Mode) — 12 files: `memory/` + `AGENTS.md`/`CLAUDE.md`
- **`full/`** (Advanced Mode) — ~50 files: adds `agent-os/{rules,agents,skills,hooks}/` + `adapters/` + `scripts/`

Both build on Karpathy's LLM wiki pattern. Advanced Mode adds operational state, agent state, and governance.

---

## Procedure

### Step 0 — Classify the target

Before installing, look at the current directory.

**If this is an existing project** (has package config, source files, README with content) → continue to Step 1.

**If this is an empty or near-empty directory** → ASK the user which mode they want:

1. **New project bootstrap** — they have an idea but no code yet. Help them write a minimal `README.md` with the project name + one-line description, run `git init` if needed, then continue from Step 1 using their stated priorities.

2. **Personal knowledge wiki** — no project at all (note-taking, research, reading, learning, vision tracking, knowledge garden). This is closer to Karpathy's original use case.
   - Install **Simple Mode only** (`starter/`)
   - Skip Steps 1 and 2 — there's no "project" to inspect or mode to choose
   - In Step 4 customization: skip project/team/client/priority items entirely
   - Reframe `memory/STATE.md` from "Current State / Priorities" to **"Current Focus"** — what you're learning, exploring, or thinking about right now. No team table, no blockers, no priority levels — just a few bullets describing your current attention.
   - Keep all of: `wiki/`, `raw/`, `outputs/`, `daily/`, `learnings.md`, `AGENTS.md`/`CLAUDE.md`
   - Do NOT install Advanced Mode (`agent-os/rules/`, `agents/`, `hooks/`, `scripts/git-hooks/`) — those are project-ops oriented and will feel heavy here
   - User's role is "LLM-wiki gardener", not "project owner"

3. **Wait, I'll bring an existing project here first** — pause. Acknowledge and stop until they're ready.

Once the user picks, proceed accordingly.

---

### Step 1 — Inspect the user's project

Before doing anything destructive, gather context.

Look at:
- `README.md`, `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod` — anything signaling tech stack and project type
- Existing AI tooling: `.claude/`, `.cursor/`, `.codex/`, `.aider.conf.yml`, `.windsurfrules`, `CLAUDE.md`, `AGENTS.md`, `CONVENTIONS.md`
- Existing memory layer: `memory/` directory, any of its subdirs, any markdown files at project root that look like state docs
- Project size: rough line count, number of directories, single-domain or multi-domain

Then ask the user (in plain words):

- What's this project? One sentence.
- Who works on it? Solo / small team / multiple roles?
- What are your top 1–3 priorities right now?
- Do you already have any AI memory / notes system in place?

Report back to the user a 5–10 line summary of what you found.

### Step 2 — Choose Simple or Advanced

Based on Step 1, recommend a mode:

- **Simple Mode** if:
  - Solo or 1–2 people working
  - User is new to AI memory systems
  - User wants to test the pattern before committing
  - No multi-domain agent dispatch needed yet

- **Advanced Mode** if:
  - Multi-person team
  - Multiple AI agents working in parallel (or planned)
  - Codebase has clear domain boundaries (backend, frontend, infra, etc.)
  - Codebase >5k lines or growing fast
  - User explicitly asks for governance, hooks, or pre-commit checks

**If unclear → recommend Simple Mode.** They can graduate later by copying `full/agent-os/` over their starter setup.

State your recommendation, ask the user to confirm or override.

### Step 3 — Plan the install

Show the user a concrete plan before any file action:

```
Install plan for [project name]:

Mode: [Simple | Advanced]

Files to install:
  - memory/STATE.md (will customize for your project)
  - memory/learnings.md (empty MISTAKES section)
  - memory/wiki/INDEX.md
  - memory/daily/YYYY-MM-DD.md (today's first entry)
  - memory/{outputs,raw}/README.md
  - AGENTS.md (canonical schema)
  - CLAUDE.md (mirror for Claude Code)
  [Advanced only:]
  - agent-os/rules/ (9 behavioral policies)
  - agent-os/skills/ (9 reusable workflows)
  - agent-os/agents/<role>/ (4-file state per domain agent)
  - agent-os/hooks/ (session-start, commit-memory-reminder)
  - adapters/<your-tool>/
  - scripts/context.sh, scripts/git-hooks/

Files I'll preserve (won't touch):
  - [list anything pre-existing that I'll leave alone]

Conflict handling for any pre-existing match:
  - I'll ask per-file: skip / merge / backup-and-replace
  - Default = skip

Project-specific customization I'll do:
  - Replace Acme Notes priorities in STATE.md with: [your priorities]
  - Replace Acme example wiki with: [your topics, or empty wiki/ ready for ingest]
  [Advanced only:]
  - Replace example backend-dev PROJECT_MAP with: [your stack]

Proceed?
```

**Wait for explicit confirmation.** Don't assume silence = yes.

### Step 4 — Install files

For each file in the chosen mode:

1. **If destination doesn't exist** → copy from starter, then customize
2. **If destination exists** → ASK the user (skip / merge / backup-and-replace) — never silent overwrite
3. **After copy** → replace Acme Notes references with the user's actual project context

#### File-by-file customization rules

**`memory/STATE.md`:**
- Replace the Acme Notes priorities table with the user's actual priorities (from Step 1)
- Set `Last updated: YYYY-MM-DD` to today
- Replace team section ("Maya / Alex") with the user's actual team
- Remove all references to Bluefin, Tessera, Acme Notes specifics

**`memory/learnings.md`:**
- Keep the format spec at top (it's the reusable scaffold)
- **Empty** the MISTAKES, WINS, and PATTERNS sections (or migrate from existing user notes if any)
- Do NOT keep the Acme Notes example mistakes — those are example data

**`memory/wiki/`:**
- Do NOT keep `sync-engine.md`, `billing-flows.md`, `design-partner-program.md`, `onboarding-funnel.md` — those are Acme Notes example pages
- Either:
  - (a) Leave `wiki/` with just an empty `INDEX.md` (user will populate via `/ingest`)
  - (b) Generate stub pages for 1–3 topics the user actually cares about (ask them)

**`memory/daily/YYYY-MM-DD.md`:**
- Create today's file with a single "Actions" entry: "Installed agent-os pattern via INSTALL_PROMPT.md"
- Do NOT keep the Acme example day

**`memory/clients/*.md` (Advanced only):**
- Do NOT keep `bluefin-coffee.md`, `tessera-studio.md`
- If the user has actual clients/customers, ask them and create stubs
- Otherwise, leave the directory empty

**`memory/outputs/specs/*.md` and `outputs/research/*.md` (Advanced only):**
- Do NOT keep the Acme example spec or research output
- Leave subdirectories empty (just `outputs/README.md` retained)

**`AGENTS.md` and `CLAUDE.md` (root) — CRITICAL:**
- Change line 1 title from `# Acme Notes — AI Agent Schema (...)` to `# <project-name> — AI Agent Schema (...)`
- These files describe the schema for the user's project — they must use the user's project name everywhere
- Search for any other "Acme Notes" mentions in body and either remove (if installer instructions) or replace with project name (if descriptive)
- Both files have identical content — keep them in sync

**`agent-os/agents/backend-dev.md` (Advanced only):**
- Update the `description:` frontmatter field — currently says "for Acme Notes", replace with "for <project-name>" or just "for this project"
- The system prompt now references `PROJECT_MAP.md` generically (no hardcoded Acme paths) — usually no edit needed, just verify
- If renaming the agent (e.g. `backend-dev` → `backend` or `api-eng`), rename the `.md` file AND the state folder

**`agent-os/agents/backend-dev/` state folder (Advanced only):**
- `PROJECT_MAP.md` — REPLACE with the user's actual stack and directory structure (this is critical; the source's `<!-- REPLACE WITH YOUR STACK -->` marker tells you exactly where)
- `STATUS.md` — clear all Acme entries; write one fresh event line: `Agent created YYYY-MM-DD via agent-os install`
- `MEMORY.md` — empty out Acme gotchas; leave header + "Empty until non-obvious gotchas are discovered."
- `RULES.md` — review each rule. Generic rules (like "production migrations during low-traffic windows") apply universally; project-specific ones may need to be adapted. If you see leftover specifics from the bundled example, fix them.

**`agent-os/rules/identity.md.template` and `language.md.template`:**
- Leave as templates (don't rename to `.md`) unless user explicitly asks
- These contain "Acme Notes" example sections intentionally — they're illustrative inside templates, do not remove
- Mention as optional in the final summary

**`scripts/context.sh`:**
- Comment example uses `<client-name>` placeholder — no change needed
- If you see any specific client name in examples, replace with `<client-name>` placeholder

**Final cleanup after install — run a residue check:**

```bash
grep -irE "acme notes|bluefin|tessera|maya( chen)?|alex( rivera)?" . --exclude-dir=.git
```

After customization, this should return only:
- Lines in `agent-os/agents/README.md` describing the bundled example (intentional)
- Lines in `agent-os/rules/identity.md.template` "Filled-in example" section (intentional)
- Lines containing Maya/Alex only if those are the user's real project names
- Nothing else.

If it returns more, you missed a customization step. Go back and fix.

### Step 5 — Verify

Run: `bash scripts/context.sh`

Expected output: STATE + INDEX + learnings + latest daily + recent commits, no errors.

If errors:
- `memory/STATE.md` missing → check Step 4
- `Permission denied` → `chmod +x scripts/context.sh`
- Other → diagnose and fix before proceeding

### Step 6 — Wire up the tool adapter

Detect from Step 1 which AI tool the user has, and wire the appropriate adapter:

| Tool detected | Action |
|---|---|
| Claude Code (`.claude/` or CLAUDE.md present) | `CLAUDE.md` at root is enough; suggest `.claude/settings.json` hook config (see `agent-os/hooks/README.md`) |
| Codex / OpenCode (`.codex/` or AGENTS.md present) | `AGENTS.md` at root is enough |
| Cursor (`.cursor/` present) | Also create `.cursor/rules/main.mdc` (copy from `adapters/cursor/`) |
| Aider (`.aider.conf.yml` present) | Also create `CONVENTIONS.md` (copy from `adapters/aider/`) |
| Windsurf (`.windsurfrules` present) | Also create `.windsurfrules` (copy from `adapters/windsurf/`) |
| Multiple / unclear | Both `AGENTS.md` and `CLAUDE.md` cover ~95%. Leave as is unless user specifies. |

### Step 7 — Wire up git hooks (Advanced only, only if git repo)

```bash
git config core.hooksPath scripts/git-hooks
```

This activates the staleness check on `git commit`.

If the project already uses `core.hooksPath` for something else, do NOT overwrite — tell the user the conflict and let them decide.

### Step 8 — Summarize

Output to the user:

```
Installation complete.

Mode: [Simple | Advanced]
Tool: [detected tool]

Files installed:
  - [list — one bullet per file/dir]

Files preserved (untouched):
  - [list]

Customizations applied:
  - STATE.md priorities → [user's priorities]
  - [other replacements]

Verification:
  ✓ scripts/context.sh runs cleanly
  ✓ AGENTS.md at root, AI should auto-load on next session
  [Advanced: ✓ git hooks wired]

Next:
  1. Open the project in your AI tool — verify AGENTS.md is auto-loaded
  2. Try saying "morning" or "what's on my plate today?" — your AI should read STATE.md
  3. As you work, share URLs/files — your AI runs the Karpathy ingest into memory/
  4. Read AGENTS.md once yourself — it's the constitution your AI is following
  [Advanced:]
  5. Optional: rename agent-os/rules/identity.md.template → identity.md to define your AI's persona
  6. Optional: rename memory/USER.md.template → USER.md to add personal context
  7. Optional: customize agent-os/agents/<role>/PROJECT_MAP.md to match your code structure
```

---

## Critical rules (do not violate)

1. **NEVER overwrite existing files without asking.** Default to skip. Confirm explicitly per file.
2. **NEVER paste Acme Notes content into the user's project.** Acme is example data; replace it everywhere.
3. **NEVER skip the verification step (Step 5).** A silent install can leave broken state.
4. **NEVER guess.** If something's unclear (which directories are theirs, what their stack is, what their priorities are) → ASK.
5. **ALWAYS preserve user's existing AI config files.** `.claude/settings.json`, `.cursor/rules/*`, etc. — back up before touching, never delete.
6. **ALWAYS use the user's actual project context.** The whole point is THEIR project, not Acme.

## If the user already has a `memory/` directory

Three cases, in order of likelihood:

1. **Empty `memory/`** → just install
2. **`memory/` with agent-os-style files** (`STATE.md`, `daily/`, `learnings.md`, etc.) → MERGE: copy only files that don't exist. Never overwrite existing content.
3. **`memory/` with custom format** (different structure) → ASK: "your existing `memory/` has [describe what you see]. Adopt the agent-os pattern (I'll back yours up to `memory.backup-YYYYMMDD/`), or only add the missing pieces?"

Default: NEVER destroy existing memory. The user's notes are sacred.

## If the user disagrees with a step

The user is in charge. If they say:
- "Skip the wiki" → skip the wiki
- "I don't want adapters for Cursor" → skip cursor adapter
- "Use a different agent name than backend-dev" → rename
- "I don't want git hooks" → skip Step 7

The pattern is modular. Components are independent.

## If you hit something you don't understand

STOP. Ask the user. Examples of things to ask:

- "Which directories in your project are 'backend' vs 'frontend'?" (for PROJECT_MAP)
- "Who are your key clients or customers?" (for `clients/` if Advanced)
- "What are your top 3 priorities right now?" (for STATE.md)
- "Your preferred response language?" (for language.md template)
- "Do you want me to keep the example backend-dev agent, or skip it?"

Don't guess. The cost of asking is 30 seconds. The cost of guessing wrong is restarting.

## Ground truth

This document is a guide. The reference is the agent-os-starter repo itself. If anything here is unclear, fetch the actual file from the repo and follow its structure.
