# Install Prompt — agent-setup (Claude Code edition)

> **Read this carefully. You are Claude Code, installing a memory + governance system into the user's project.**

This is the Claude Code–specific variant of `INSTALL_PROMPT.md`. It assumes the tool is Claude Code (no tool
detection, no adapters), installs **Advanced Mode** (`full/agent/`), and creates **no domain agents** — only the
canonical blank agent template ships, and agents are grown later via `/create-agent`. If the user might not be on
Claude Code, or wants Simple Mode or install-time domain agents, use the general `INSTALL_PROMPT.md` instead.

This document is the install procedure. Follow it step by step. Do not skip steps. Do not improvise.

## Source

Reference repo: **https://github.com/kukebab/agent-setup**

Fetch its contents (web fetch or git clone). You need only **`full/`** — a single `agent/` folder
(`memory/`, `rules/`, `skills/`, `agents/`, `hooks/`, `scripts/`) plus thin root `AGENTS.md`/`CLAUDE.md` stubs.
The whole `agent/` folder is copied to the target project root, so paths become `agent/memory/STATE.md`,
`agent/rules/...`, etc. Don't drop the `agent/` prefix.

The bundle builds on Karpathy's LLM wiki pattern, plus operational state, governance, and the
`/mine-learnings` trace→learnings loop.

---

## Procedure

### Step 1 — Inspect the user's project

Before doing anything, gather context. Look at:

- `README.md`, `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod` — anything signaling tech stack and project type
- Existing Claude Code config: `.claude/` (settings, skills, agents), `CLAUDE.md`, `AGENTS.md`
- Existing memory layer: `memory/` or `agent/` directories, any markdown files at root that look like state docs
- Project size: rough line count, number of directories, single-domain or multi-domain

Then ask the user (in plain words):

- What's this project? One sentence.
- Who works on it? Solo / small team / multiple roles?
- What are your top 1–3 priorities right now?
- Do you already have any AI memory / notes system in place?

Report back a 5–10 line summary of what you found.

### Step 2 — Plan the install

Show the user a concrete plan before any file action:

```
Install plan for [project name]:

Mode: Advanced (Claude Code)

Files to install — everything nests under one agent/ folder:
  - agent/AGENTS.md (canonical schema — the router)
  - agent/VERSION.md (installed schema version, for future updates)
  - agent/memory/STATE.md, agent/memory/INDEX.md
  - agent/memory/learnings/ (split: mistakes/patterns/decisions/constraints/archive + README)
  - agent/memory/inbox/learnings-candidates.md (the /mine-learnings review queue)
  - agent/memory/projects/ (per-project / per-client live state)
  - agent/memory/{wiki,daily,outputs,raw}/
  - agent/rules/ (behavioral policies)
  - agent/skills/ (reusable workflows, incl. review-learnings + mine-learnings + create-agent)
  - agent/agents/template/ (canonical blank agent — copied as-is, stays blank)
  - agent/hooks/ (session-start, commit-memory-reminder)
  - agent/scripts/context.sh, agent/scripts/mine_learnings.py (+ tests), agent/scripts/git-hooks/
  - AGENTS.md, CLAUDE.md (root) — thin stubs pointing at agent/AGENTS.md
  - .claude/skills/<name>/ — copy of each agent/skills/<name>/, so Claude Code
    auto-discovers them as native skills

Domain agents: NONE created now. agent/agents/template/ is installed blank; when a domain
owner emerges, run /create-agent — it copies the template, fills it, and registers the
agent in .claude/agents/.

Files I'll preserve (won't touch):
  - [list anything pre-existing that I'll leave alone]

Conflict handling for any pre-existing match:
  - I'll ask per-file: skip / merge / backup-and-replace
  - Default = skip

Project-specific customization I'll do:
  - Replace Acme Notes priorities in agent/memory/STATE.md with: [your priorities]
  - Replace Acme example wiki with: [your topics, or empty wiki/ ready for ingest]

Proceed?
```

**Wait for explicit confirmation.** Don't assume silence = yes.

### Step 3 — Install files

For each file:

1. **If destination doesn't exist** → copy from `full/`, then customize
2. **If destination exists** → ASK the user (skip / merge / backup-and-replace) — never silent overwrite
3. **After copy** → replace Acme Notes references with the user's actual project context

#### File-by-file customization rules

**`agent/memory/STATE.md`:**
- Replace the Acme Notes priorities table with the user's actual priorities (from Step 1)
- Set `Last updated: YYYY-MM-DD` to today
- Replace team section ("Maya / Alex") with the user's actual team
- Remove all references to Bluefin, Tessera, Acme Notes specifics

**`agent/memory/learnings/`:**
- Keep `README.md` + the per-file scaffolds (`mistakes.md`, `patterns.md`, `decisions.md`, `constraints.md`,
  `archive.md`); **empty** the Acme example entries from each, leaving the format/intro blocks
- Keep `agent/memory/inbox/learnings-candidates.md` as the seeded (empty) queue
- Do NOT keep the Acme Notes example lessons — those are example data

**`agent/memory/wiki/`:**
- Do NOT keep `sync-engine.md`, `billing-flows.md`, `design-partner-program.md`, `onboarding-funnel.md` —
  those are Acme Notes example pages
- Either: (a) leave `wiki/` with just an empty `INDEX.md` (user will populate via `/ingest`), or
  (b) generate stub pages for 1–3 topics the user actually cares about (ask them)

**`agent/memory/daily/YYYY-MM-DD.md`:**
- Create today's file with a single "Actions" entry: "Installed agent-os pattern via INSTALL_PROMPT_CLAUDE_CODE.md"
- Do NOT keep the Acme example day

**`agent/memory/projects/*.md`:**
- Do NOT keep `bluefin-coffee.md`, `tessera-studio.md`
- If the user has actual projects/customers, ask them and create stubs; otherwise leave the directory empty

**`agent/memory/outputs/specs/*.md` and `outputs/research/*.md`:**
- Do NOT keep the Acme example spec or research output; leave subdirectories empty (just `outputs/README.md` retained)

**`AGENTS.md` and `CLAUDE.md` (root):**
- These are thin stubs — leave their content as-is (they just point at `agent/AGENTS.md`)
- The actual schema customization happens in **`agent/AGENTS.md`**: change the line 1 title from
  `# Acme Notes — ...` to `# <project-name> — ...`, and search the body for any other "Acme Notes"
  mentions to remove or replace

**`agent/agents/template/` — the blank agent. CRITICAL:**
- Copy the folder **exactly as-is**: `agent.md.template` + the 4 state files (`STATUS.md`, `MEMORY.md`,
  `PROJECT_MAP.md`, `RULES.md`), all `<placeholder>`-marked
- Do NOT fill any placeholder, do NOT rename `agent.md.template`, do NOT customize dates or stack markers —
  it is a copy source, not an agent, and must stay blank
- Do NOT copy anything from it into `.claude/agents/` — it is never dispatched
- Do NOT create any domain agents during install. When the user is ready, `/create-agent` copies the template,
  fills the copy, wires the `agent/AGENTS.md` dispatch table, and registers the copy in `.claude/agents/`
- If the user asks for domain agents *during* this install, that's out of this prompt's scope — finish the
  install, then run `/create-agent` per domain

**`agent/rules/identity.md.template` and `language.md.template`:**
- Leave as templates (don't rename to `.md`) unless user explicitly asks
- These contain "Acme Notes" example sections intentionally — illustrative inside templates, do not remove
- Mention as optional in the final summary

**`agent/VERSION.md`:**
- Set `Schema version:` to the newest dated entry in the source repo's `CHANGELOG.md`
- Set `Installed:` and `Last synced:` to today's date
- This is what a future `UPDATE_PROMPT.md` run will diff against — don't skip it

**`.claude/skills/`:**
- Claude Code auto-discovers skills from `.claude/skills/<name>/SKILL.md` — reading `CLAUDE.md` alone is not
  enough for them to show up as native `/slash-commands`
- Copy every `agent/skills/<name>/` into `.claude/skills/<name>/` — same `SKILL.md` content, duplicated at the
  path Claude Code scans. Skip `skills/README.md` (it's an index, not a skill)
- These are copies, not symlinks — if a skill under `agent/skills/` is later edited, re-copy into `.claude/`.
  Mention this in the final summary
- `.claude/agents/` stays empty at install (no domain agents yet) — `/create-agent` populates it later

**Final cleanup after install — run a residue check:**

```bash
grep -irE "acme notes|bluefin|tessera|maya( chen)?|alex( rivera)?" . --exclude-dir=.git
```

After customization, this should return only:
- Lines in `agent/rules/identity.md.template` "Filled-in example" section (intentional)
- Lines containing Maya/Alex only if those are the user's real project names
- Nothing else.

If it returns more, you missed a customization step. Go back and fix.

### Step 4 — Verify

Run: `bash agent/scripts/context.sh`

Expected output: STATE + INDEX + learnings + latest daily + recent commits, no errors.

If errors:
- `agent/memory/STATE.md` missing → check Step 3
- `Permission denied` → `chmod +x agent/scripts/context.sh`
- Other → diagnose and fix before proceeding

Also verify Claude Code discovery: `.claude/skills/` contains one folder per skill (each with a `SKILL.md`),
and `agent/agents/template/agent.md.template` still has its `<placeholder>` markers (i.e., it was NOT filled).

### Step 5 — Wire up hooks

Suggest `.claude/settings.json` hook config (see `agent/hooks/README.md`). Never overwrite an existing
`.claude/settings.json` — show the user the snippet to merge instead.

If the project is a git repo:

```bash
git config core.hooksPath agent/scripts/git-hooks
```

This activates the staleness check on `git commit`. If the project already uses `core.hooksPath` for something
else, do NOT overwrite — tell the user the conflict and let them decide.

**First commit after install:** the staleness hook hard-blocks a commit when a current-state file's body changed
but its `Last updated:` / `## Current State as of` date is older than today. On the very first commit, every
installed file counts as "changed", so any example date left in the past will block. This is why Step 3 bumps
`STATE.md` to today's date. (`agent/agents/template/` is exempt — the staleness check skips it by design, its
`YYYY-MM-DD` placeholders are intentional.) If you're committing the template as-is to start, use
`STALENESS_SKIP=1 git commit ...` for that first commit only.

### Step 6 — Summarize

Output to the user:

```
Installation complete.

Mode: Advanced (Claude Code)

Files installed:
  - [list — one bullet per file/dir]

Files preserved (untouched):
  - [list]

Customizations applied:
  - agent/memory/STATE.md priorities → [user's priorities]
  - [other replacements]

Verification:
  ✓ agent/scripts/context.sh runs cleanly
  ✓ CLAUDE.md at root (stub → agent/AGENTS.md), auto-loaded next session
  ✓ skills copied to .claude/skills/
  ✓ agent/agents/template/ installed blank (no domain agents created)
  ✓ git hooks wired, agent/VERSION.md stamped

Next:
  1. Restart Claude Code in this project — verify CLAUDE.md is auto-loaded and /morning, /endday
     appear as skills
  2. Try saying "morning" or "what's on my plate today?" — Claude should read agent/memory/STATE.md
  3. As you work, share URLs/files — Claude runs the Karpathy ingest into agent/memory/
  4. Read agent/AGENTS.md once yourself — it's the constitution Claude is following
  5. When a domain owner emerges (3+ tasks in the same domain), run /create-agent — it copies
     agent/agents/template/ and registers the new agent in .claude/agents/
  6. Optional: rename agent/rules/identity.md.template → identity.md to define your AI's persona
  7. Optional: rename agent/memory/USER.md.template → USER.md to add personal context
  8. To pull in future updates to this pattern, paste UPDATE_PROMPT.md into Claude later
```

---

## Critical rules (do not violate)

1. **NEVER overwrite existing files without asking.** Default to skip. Confirm explicitly per file.
2. **NEVER paste Acme Notes content into the user's project.** Acme is example data; replace it everywhere.
3. **NEVER fill or rename anything inside `agent/agents/template/`.** It installs blank and stays blank —
   `/create-agent` copies it later; the template itself is never an agent.
4. **NEVER skip the verification step (Step 4).** A silent install can leave broken state.
5. **NEVER guess.** If something's unclear (which directories are theirs, what their stack is, what their
   priorities are) → ASK.
6. **ALWAYS preserve the user's existing Claude Code config.** `.claude/settings.json`, existing
   `.claude/skills/*`, `.claude/agents/*` — back up before touching, never delete.
7. **ALWAYS use the user's actual project context.** The whole point is THEIR project, not Acme.

## If the user already has an `agent/` directory

Three cases, in order of likelihood:

1. **Empty** → just install
2. **Existing agent-os-style files** (`memory/STATE.md`, `daily/`, `learnings/`, etc.) → MERGE: copy only files
   that don't exist. Never overwrite existing content.
3. **Custom format** (different structure) → ASK: "your existing `agent/` has [describe what you see]. Adopt the
   agent-os pattern (I'll back yours up to `agent.backup-YYYYMMDD/`), or only add the missing pieces?"

Default: NEVER destroy existing memory. The user's notes are sacred.

## If the user disagrees with a step

The user is in charge. If they say:
- "Skip the wiki" → skip the wiki
- "I don't want git hooks" → skip the git hooks part of Step 5
- "I want Simple Mode" / "I'm not on Claude Code" → switch to the general `INSTALL_PROMPT.md`

The pattern is modular. Components are independent.

## If you hit something you don't understand

STOP. Ask the user. Examples of things to ask:

- "Who are your key clients or customers?" (for `agent/memory/projects/`)
- "What are your top 3 priorities right now?" (for `agent/memory/STATE.md`)
- "Your preferred response language?" (for the language.md template)

Don't guess. The cost of asking is 30 seconds. The cost of guessing wrong is restarting.

## Ground truth

This document is a guide. The reference is the agent-setup repo itself. If anything here is unclear, fetch the
actual file from the repo and follow its structure.
