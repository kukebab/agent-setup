# Install Prompt — agent-setup

> **Read this carefully. You are an AI agent installing a memory + governance system into the user's project or knowledge workspace.**

This document is the install procedure. Follow it step by step. Do not skip steps. Do not improvise.

## Source

Reference repo: **https://github.com/kukebab/agent-setup**

Fetch its contents (via web fetch, git clone, or your equivalent). Two modes ship there:

- **`starter/`** (Simple Mode) — 18 files: `memory/` (single `learnings.md`) + `AGENTS.md`/`CLAUDE.md`. Installs at the target project **root** — `memory/STATE.md`, `memory/learnings.md`, etc.
- **`full/`** (Advanced Mode) — ~60 files: a single `agent/` folder (`memory/`, `rules/`, `skills/`, `agents/`, `hooks/`, `scripts/`) plus thin root `AGENTS.md`/`CLAUDE.md` stubs and `adapters/`. Installs the whole `agent/` folder at the target project root — so paths become `agent/memory/STATE.md`, `agent/rules/...`, etc. Also adds the `/mine-learnings` trace→learnings loop and version tracking (`agent/VERSION.md` + the source repo's `CHANGELOG.md`).

Both build on Karpathy's LLM wiki pattern. Advanced Mode adds operational state, agent state, and governance.

**Path convention in this document:** Simple Mode paths are written bare (`memory/STATE.md`) since they land at the project root. Advanced Mode paths are written with the `agent/` prefix (`agent/memory/STATE.md`) since the whole bundle nests under one folder. Don't drop the prefix when installing Advanced Mode.

---

## Procedure

### Step 0 — Classify the target

Before installing, look at the current directory.

**If this is an existing project** (has package config, source files, README with content) → continue to Step 1.

**If this is an empty or near-empty directory** → ASK the user which mode they want:

1. **New project bootstrap** — they have an idea but no code yet. Help them write a minimal `README.md` with the project name + one-line description, run `git init` if needed, then continue from Step 1 using their stated priorities.

2. **Personal knowledge wiki** — no project at all (note-taking, research, reading, learning, vision tracking, knowledge garden). This is closer to Karpathy's original use case.
   - Install **Simple Mode only** (`starter/`)
   - Skip the project-inspection parts of Steps 1 and 2 — there's no codebase to inspect or mode to choose
   - Still show a short Step 3 plan and wait for confirmation before writing files
   - In Step 4 customization: skip project/team/client/priority items entirely
   - Reframe `memory/STATE.md` from "Current State / Priorities" to **"Current Focus"** — what you're learning, exploring, or thinking about right now. No team table, no blockers, no priority levels — just a few bullets describing your current attention.
   - Keep all of: `wiki/`, `raw/`, `outputs/`, `daily/`, `learnings.md`, `AGENTS.md`/`CLAUDE.md`
   - Do NOT install Advanced Mode (the `agent/` bundle's `rules/`, `agents/`, `hooks/`, `scripts/git-hooks/`) — those are project-ops oriented and will feel heavy here
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

**If unclear → recommend Simple Mode.** They can graduate later by copying `full/agent/` over their starter setup (their existing `memory/` merges into `agent/memory/`).

State your recommendation, ask the user to confirm or override.

### Step 2.5 — Choose which agents to install (Advanced Mode only)

`full/agent/agents/` ships 4 ready-to-install role templates:

- **`backend-dev`** — the worked example (filled in for the fictional Acme Notes project, Next.js + Postgres). Useful as a reference for what a filled-in agent looks like; stack-specific parts are still Acme's until you customize them.
- **`frontend-dev`**, **`infra`**, **`data-eng`** — blank templates (no example content, just the `<!-- REPLACE WITH YOUR STACK -->` structure).

Ask the user explicitly: **"Which of these domain agents do you want installed — backend-dev, frontend-dev, infra, data-eng, none of them, or a different domain name?"**

- **Default recommendation if the user is unsure: install none yet.** The pattern's default is to grow into agents organically as domain ownership becomes clear (see `agent/agents/README.md` § "When to add an agent") — don't pre-create agents just because they're available.
- Installing one or more upfront is the right call if the user already has clear domain boundaries (existing multi-person team, established backend/frontend split, etc.) — this is the exception, not the default.
- If the user names a domain that isn't one of the 4 bundled templates (e.g. "mobile-dev", "security"), that's fine — build it from the `backend-dev.md`/`backend-dev/` structure per `agent/agents/README.md` § "Adding your own agent", blank (not Acme-filled) like the other blank templates.

For each agent selected, in Step 4 you will: copy its `<name>.md` definition file, copy its `<name>/` state folder (`STATUS.md`, `MEMORY.md`, `PROJECT_MAP.md`, `RULES.md`), customize both, and add a row for it to `agent/AGENTS.md`'s "Agent dispatch" table.

### Step 3 — Plan the install

Show the user a concrete plan before any file action:

```
Install plan for [project name]:

Mode: [Simple | Advanced]

Files to install (Simple Mode — paths at project root):
  - memory/STATE.md (will customize for your project)
  - memory/learnings.md — single file, empty MISTAKES section
  - memory/wiki/INDEX.md
  - memory/daily/YYYY-MM-DD.md (today's first entry)
  - memory/{outputs,raw}/README.md
  - AGENTS.md (canonical schema)
  - CLAUDE.md (mirror for Claude Code)

[Advanced only — everything below nests under one agent/ folder:]
  - agent/AGENTS.md (canonical schema — the router)
  - agent/VERSION.md (installed schema version, for future updates)
  - agent/memory/STATE.md, agent/memory/INDEX.md
  - agent/memory/learnings/ (split: mistakes/patterns/decisions/constraints/archive + README)
  - agent/memory/inbox/learnings-candidates.md (the /mine-learnings review queue)
  - agent/memory/projects/ (per-project / per-client live state)
  - agent/memory/{wiki,daily,outputs,raw}/
  - agent/rules/ (behavioral policies)
  - agent/skills/ (reusable workflows, incl. review-learnings + mine-learnings)
  - agent/agents/<selected-agents>.md + agent/agents/<selected-agents>/ (4-file state per agent chosen in Step 2.5 — may be none)
  - agent/hooks/ (session-start, commit-memory-reminder)
  - agent/scripts/context.sh, agent/scripts/mine_learnings.py (+ tests), agent/scripts/git-hooks/
  - AGENTS.md, CLAUDE.md (root) — thin stubs pointing at agent/AGENTS.md
  - adapters/<your-tool>/ (written outside agent/, wherever your tool auto-loads from)
  [Claude Code only:]
  - .claude/skills/<name>/ — copy of each agent/skills/<name>/ (or agent-os/skills/<name>/ in Simple Mode), so Claude Code auto-discovers them as native skills
  - .claude/agents/<name>.md — copy of each installed agent/agents/<name>.md (Advanced only), so Claude Code auto-discovers them as native subagents

Files I'll preserve (won't touch):
  - [list anything pre-existing that I'll leave alone]

Conflict handling for any pre-existing match:
  - I'll ask per-file: skip / merge / backup-and-replace
  - Default = skip

Project-specific customization I'll do:
  - Replace Acme Notes priorities in STATE.md with: [your priorities]
  - Replace Acme example wiki with: [your topics, or empty wiki/ ready for ingest]
  [Advanced only:]
  - Agents to install: [none | backend-dev | frontend-dev | infra | data-eng | custom: <name>] (from Step 2.5)
  - Replace each installed agent's PROJECT_MAP with: [your stack]

Proceed?
```

**Wait for explicit confirmation.** Don't assume silence = yes.

### Step 4 — Install files

For each file in the chosen mode:

1. **If destination doesn't exist** → copy from starter, then customize
2. **If destination exists** → ASK the user (skip / merge / backup-and-replace) — never silent overwrite
3. **After copy** → replace Acme Notes references with the user's actual project context

#### File-by-file customization rules

**`memory/STATE.md`** (Simple) / **`agent/memory/STATE.md`** (Advanced):
- Replace the Acme Notes priorities table with the user's actual priorities (from Step 1)
- Set `Last updated: YYYY-MM-DD` to today
- Replace team section ("Maya / Alex") with the user's actual team
- Remove all references to Bluefin, Tessera, Acme Notes specifics

**`memory/learnings.md` (Simple Mode) / `agent/memory/learnings/` (Advanced Mode):**
- **Simple Mode** keeps a single `learnings.md`: keep the lifecycle table (MISTAKES / PATTERNS / WINS), **empty** the sections, drop the Acme example mistakes. Do NOT create `learnings.archive.md` preemptively.
- **Advanced Mode** keeps the `agent/memory/learnings/` directory: keep `README.md` + the per-file scaffolds (`mistakes.md`, `patterns.md`, `decisions.md`, `constraints.md`, `archive.md`); **empty** the Acme example entries from each, leaving the format/intro blocks. Keep `agent/memory/inbox/learnings-candidates.md` as the seeded (empty) queue.
- Either way: do NOT keep the Acme Notes example lessons — those are example data.

**`memory/wiki/` (Simple) / `agent/memory/wiki/` (Advanced):**
- Do NOT keep `sync-engine.md`, `billing-flows.md`, `design-partner-program.md`, `onboarding-funnel.md` — those are Acme Notes example pages
- Either:
  - (a) Leave `wiki/` with just an empty `INDEX.md` (user will populate via `/ingest`)
  - (b) Generate stub pages for 1–3 topics the user actually cares about (ask them)

**`memory/daily/YYYY-MM-DD.md` (Simple) / `agent/memory/daily/YYYY-MM-DD.md` (Advanced):**
- Create today's file with a single "Actions" entry: "Installed agent-os pattern via INSTALL_PROMPT.md"
- Do NOT keep the Acme example day

**`agent/memory/projects/*.md` (Advanced only):**
- Do NOT keep `bluefin-coffee.md`, `tessera-studio.md`
- If the user has actual projects/customers, ask them and create stubs
- Otherwise, leave the directory empty

**`agent/memory/outputs/specs/*.md` and `outputs/research/*.md` (Advanced only):**
- Do NOT keep the Acme example spec or research output
- Leave subdirectories empty (just `outputs/README.md` retained)

**`AGENTS.md` and `CLAUDE.md` (root) — CRITICAL:**
- **Simple Mode:** these ARE the full schema. Change line 1 title from `# Acme Notes — AI Agent Schema (...)` to `# <project-name> — AI Agent Schema (...)`, and search the body for any other "Acme Notes" mentions to remove or replace with the project name. Both files have identical content — keep them in sync.
- **Advanced Mode:** the root `AGENTS.md`/`CLAUDE.md` are thin stubs — leave their content as-is (they just point at `agent/AGENTS.md`), no per-project customization needed. The actual schema customization happens in **`agent/AGENTS.md`**: change line 1 title the same way, search its body for "Acme Notes" mentions, and keep it as the single canonical copy — there is no `agent/CLAUDE.md` to sync separately.

**For each agent selected in Step 2.5 (Advanced only) — copy and customize its `<name>.md` + `<name>/` folder:**

- Copy `agent/agents/<name>.md` and `agent/agents/<name>/` (all 4 state files) from the source repo
- If the requested domain isn't one of the 4 bundled templates, build it from `backend-dev.md`/`backend-dev/` per `agent/agents/README.md` § "Adding your own agent" — blank, not Acme-filled
- Add a row for it to `agent/AGENTS.md`'s "Agent dispatch" table

**`<name>.md`:**
- Update the `description:` frontmatter field — for `backend-dev` it currently says "for Acme Notes", replace with "for <project-name>" or just "for this project" (the 3 blank templates are already generic — verify, don't assume)
- The system prompt references `PROJECT_MAP.md` by its full path from project root (`agent/agents/<name>/PROJECT_MAP.md`) — no hardcoded Acme paths in any of the 4 templates, usually no edit needed, just verify
- If renaming the agent (e.g. `backend-dev` → `backend` or `api-eng`), rename the `.md` file AND the state folder, AND update every `agent/agents/backend-dev/` path reference inside the `.md` (the `state-folder:` frontmatter, the "State files" section, and the system prompt's PROJECT_MAP line) to the new name — these are full paths, not symlinks, so they don't update themselves

**`<name>/` state folder:**
- `PROJECT_MAP.md` — REPLACE with the user's actual stack and directory structure (this is critical; the `<!-- REPLACE WITH YOUR STACK -->` marker tells you exactly where — every bundled template has one, not just backend-dev)
- `STATUS.md` — for `backend-dev`: clear all Acme entries; write one fresh event line: `Agent created YYYY-MM-DD via agent-os install`. For the blank templates: replace the `YYYY-MM-DD` placeholders with today's date, keep "No events yet."
- `MEMORY.md` — for `backend-dev`: empty out Acme gotchas, leave header + "Empty until non-obvious gotchas are discovered." The blank templates are already in this state — verify, don't duplicate the note.
- `RULES.md` — review each rule. Generic rules (like "production migrations during low-traffic windows") apply universally; project-specific ones may need to be adapted. For `backend-dev`, fix any leftover Acme specifics; the blank templates' starter rules are already generic but still worth a sanity check against the user's actual stack.

**`agent/rules/identity.md.template` and `language.md.template`:**
- Leave as templates (don't rename to `.md`) unless user explicitly asks
- These contain "Acme Notes" example sections intentionally — they're illustrative inside templates, do not remove
- Mention as optional in the final summary

**`agent/scripts/context.sh`:**
- Comment example uses `<client-name>` placeholder — no change needed
- If you see any specific client name in examples, replace with `<client-name>` placeholder

**`agent/VERSION.md` (Advanced only):**
- Set `Schema version:` to the newest dated entry in the source repo's `CHANGELOG.md`
- Set `Installed:` and `Last synced:` to today's date
- This is what a future `UPDATE_PROMPT.md` run will diff against — don't skip it

**`.claude/skills/` and `.claude/agents/` (Claude Code only):**
- Claude Code auto-discovers skills from `.claude/skills/<name>/SKILL.md` and subagents from `.claude/agents/<name>.md` — reading `AGENTS.md`/`CLAUDE.md` alone is not enough for those to show up as native `/slash-commands` or dispatchable subagents.
- Copy every `agent/skills/<name>/` (Simple Mode: `agent-os/skills/<name>/`) into `.claude/skills/<name>/` — same `SKILL.md` content, just duplicated at the path Claude Code scans. Skip `skills/README.md` (it's an index, not a skill).
- For each agent installed in Step 2.5 (Advanced only), copy its `agent/agents/<name>.md` definition file into `.claude/agents/<name>.md`. Do NOT copy `agent/agents/README.md` or the `<name>/` state folders — Claude Code only reads the single `.md` definition from `.claude/agents/`, the state folder stays under `agent/agents/<name>/` where the agent's own system prompt points it.
- These are copies, not symlinks — if you later rename or edit a skill/agent under `agent/`, re-copy into `.claude/` to keep them in sync. Mention this in the final summary.

**Final cleanup after install — run a residue check:**

```bash
grep -irE "acme notes|bluefin|tessera|maya( chen)?|alex( rivera)?" . --exclude-dir=.git
```

After customization, this should return only:
- Lines in `agent/agents/README.md` describing the bundled example (intentional)
- Lines in `agent/rules/identity.md.template` "Filled-in example" section (intentional)
- Lines containing Maya/Alex only if those are the user's real project names
- Nothing else.

If it returns more, you missed a customization step. Go back and fix.

### Step 5 — Verify

Run: `bash scripts/context.sh` (Simple) or `bash agent/scripts/context.sh` (Advanced)

Expected output: STATE + INDEX + learnings + latest daily + recent commits, no errors.

If errors:
- `memory/STATE.md` (Simple) / `agent/memory/STATE.md` (Advanced) missing → check Step 4
- `Permission denied` → `chmod +x scripts/context.sh` (Simple) / `chmod +x agent/scripts/context.sh` (Advanced)
- Other → diagnose and fix before proceeding

### Step 6 — Wire up the tool adapter

Detect from Step 1 which AI tool the user has, and wire the appropriate adapter:

| Tool detected | Action |
|---|---|
| Claude Code (`.claude/` or CLAUDE.md present) | `CLAUDE.md` at root is enough for the AI to *read* the schema (Advanced: it's a stub pointing at `agent/AGENTS.md`) — but Claude Code also natively auto-discovers skills and subagents from specific folders, so additionally: copy each `agent/skills/<name>/` (Simple: `agent-os/skills/<name>/`) into `.claude/skills/<name>/`, and copy each installed `agent/agents/<name>.md` (Advanced only — skip `README.md`) into `.claude/agents/<name>.md`. This makes `/morning`, `/endday`, `backend-dev`, etc. available as first-class Claude Code skills/subagents, not just prose inside AGENTS.md. Also suggest `.claude/settings.json` hook config (see `agent/hooks/README.md`) |
| Codex / OpenCode (`.codex/` or AGENTS.md present) | `AGENTS.md` at root is enough |
| Cursor (`.cursor/` present) | Also create `.cursor/rules/main.mdc` (copy from `adapters/cursor/`) |
| Aider (`.aider.conf.yml` present) | Also create `CONVENTIONS.md` (copy from `adapters/aider/`) |
| Windsurf (`.windsurfrules` present) | Also create `.windsurfrules` (copy from `adapters/windsurf/`) |
| Multiple / unclear | Both `AGENTS.md` and `CLAUDE.md` cover ~95%. Leave as is unless user specifies. |

### Step 7 — Wire up git hooks (Advanced only, only if git repo)

```bash
git config core.hooksPath agent/scripts/git-hooks
```

This activates the staleness check on `git commit`.

If the project already uses `core.hooksPath` for something else, do NOT overwrite — tell the user the conflict and let them decide.

**First commit after install:** the staleness hook hard-blocks a commit when a current-state file's body changed but its `Last updated:` / `## Current State as of` date is older than today. On the very first commit, every installed file counts as "changed", so any example date left in the past (e.g. the Acme `2026-05-03`) will block. This is why Step 4 bumps `STATE.md` (and any `PROJECT_MAP.md` / `STATUS.md` you keep) to today's date. If you've customized faithfully it just passes; if you're committing the template as-is to start, use `STALENESS_SKIP=1 git commit ...` for that first commit only.

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
  ✓ scripts/context.sh runs cleanly [Advanced: agent/scripts/context.sh]
  ✓ AGENTS.md at root, AI should auto-load on next session [Advanced: it's a stub pointing at agent/AGENTS.md]
  [Advanced: ✓ git hooks wired, ✓ agent/VERSION.md stamped]
  [Claude Code: ✓ skills copied to .claude/skills/, ✓ agents copied to .claude/agents/ (if any installed)]

Next:
  1. Open the project in your AI tool — verify AGENTS.md is auto-loaded
  2. Try saying "morning" or "what's on my plate today?" — your AI should read STATE.md
  3. As you work, share URLs/files — your AI runs the Karpathy ingest into memory/ [Advanced: agent/memory/]
  4. Read AGENTS.md once yourself — it's the constitution your AI is following [Advanced: read agent/AGENTS.md, the root one is just a pointer]
  [Advanced:]
  5. Optional: rename agent/rules/identity.md.template → identity.md to define your AI's persona
  6. Optional: rename agent/memory/USER.md.template → USER.md to add personal context
  7. [If any agents installed] Double-check agent/agents/<name>/PROJECT_MAP.md matches your actual code structure
  8. To pull in future updates to this pattern, paste UPDATE_PROMPT.md into your AI later
```

---

## Critical rules (do not violate)

1. **NEVER overwrite existing files without asking.** Default to skip. Confirm explicitly per file.
2. **NEVER paste Acme Notes content into the user's project.** Acme is example data; replace it everywhere.
3. **NEVER skip the verification step (Step 5).** A silent install can leave broken state.
4. **NEVER guess.** If something's unclear (which directories are theirs, what their stack is, what their priorities are) → ASK.
5. **ALWAYS preserve user's existing AI config files.** `.claude/settings.json`, `.cursor/rules/*`, etc. — back up before touching, never delete.
6. **ALWAYS use the user's actual project context.** The whole point is THEIR project, not Acme.

## If the user already has a `memory/` directory (Simple) or `agent/` directory (Advanced)

Three cases, in order of likelihood:

1. **Empty** → just install
2. **Existing agent-os-style files** (`STATE.md`, `daily/`, `learnings.md` or `learnings/`, etc.) → MERGE: copy only files that don't exist. Never overwrite existing content.
3. **Custom format** (different structure) → ASK: "your existing `memory/`/`agent/` has [describe what you see]. Adopt the agent-os pattern (I'll back yours up to `memory.backup-YYYYMMDD/` or `agent.backup-YYYYMMDD/`), or only add the missing pieces?"

Default: NEVER destroy existing memory. The user's notes are sacred.

## If the user disagrees with a step

The user is in charge. If they say:
- "Skip the wiki" → skip the wiki
- "I don't want adapters for Cursor" → skip cursor adapter
- "Use a different agent name than backend-dev" → rename
- "I don't want any agents yet" → skip Step 2.5 entirely, install none
- "I don't want git hooks" → skip Step 7

The pattern is modular. Components are independent.

## If you hit something you don't understand

STOP. Ask the user. Examples of things to ask:

- "Which directories in your project are 'backend' vs 'frontend'?" (for PROJECT_MAP)
- "Who are your key clients or customers?" (for `projects/` if Advanced)
- "What are your top 3 priorities right now?" (for STATE.md)
- "Your preferred response language?" (for language.md template)
- "Which agents do you want installed — backend-dev, frontend-dev, infra, data-eng, none, or something else?" (Step 2.5)

Don't guess. The cost of asking is 30 seconds. The cost of guessing wrong is restarting.

## Ground truth

This document is a guide. The reference is the agent-setup repo itself. If anything here is unclear, fetch the actual file from the repo and follow its structure.
