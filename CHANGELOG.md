# Changelog

Notable changes to the agent-setup pattern (`starter/` and `full/` modes). This is a
changelog for the **pattern itself**, not for any project that has installed it.

Each entry is dated `YYYY-MM-DD`. If you have this pattern installed in a project, compare
the "Schema version" in your project's `agent/VERSION.md` against the dates below — entries
newer than your installed version are changes you haven't applied yet. See `UPDATE_PROMPT.md`
for the update procedure.

## 2026-07-19

- **New `INSTALL_PROMPT_CLAUDE_CODE.md` — Claude Code–specific installer.** A variant of
  `INSTALL_PROMPT.md` that skips tool detection and adapters (assumes Claude Code), installs
  Advanced Mode only, and creates **no domain agents**: `agent/agents/template/` is copied blank
  and stays blank — `<placeholder>` markers untouched, nothing registered in `.claude/agents/` —
  with `/create-agent` as the only path to real agents afterwards. Skills are still copied into
  `.claude/skills/` for native discovery. Use the general `INSTALL_PROMPT.md` for other tools,
  Simple Mode, or install-time domain agents.
- **Advanced Mode: the four bundled agent templates are removed.** `backend-dev` (the Acme worked
  example), `frontend-dev`, `infra`, and `data-eng` — definition files and state folders — are gone
  from `full/agent/agents/`. `agent/agents/template/` (next entry) is now the only thing shipping
  there: every agent is created by copying it, at install time (INSTALL_PROMPT Step 2.5 now asks
  "do you want any domain agents created now?" instead of offering a fixed menu) or later via
  `/create-agent`. All references updated across `INSTALL_PROMPT.md`, `INSTALL.md`,
  `EXAMPLE_TOUR.md`, `README`s, the `agent/AGENTS.md` dispatch table, skills, `install.sh`, and the
  repo meta-docs (`AGENTS.md`/`CLAUDE.md`).
- **Advanced Mode: canonical blank agent at `agent/agents/template/`.** New folder holding the
  agent file structure as a copy source: `agent.md.template` (definition) + the 4 state files
  (`STATUS.md`, `MEMORY.md`, `PROJECT_MAP.md`, `RULES.md`), all `<placeholder>`-marked. It is not
  an installable agent — it ships with every Advanced install (the bundle is copied wholesale) so
  new agents are created locally by **copy-first-then-fill**: `cp -R agent/agents/template
  agent/agents/<name>`, move `agent.md.template` to `agent/agents/<name>.md`, then fill
  placeholders in the copy only. `/create-agent` now mandates this flow (never write agent files
  from scratch, never edit `template/` itself); `agent/agents/README.md` documents the folder;
  `INSTALL_PROMPT.md` routes custom-domain agents through `template/` instead of "build from
  `backend-dev`". `check-staleness.py` now skips `agent/agents/template/` — its `YYYY-MM-DD`
  placeholders are by design and shouldn't produce per-commit warnings (tested on a fake project:
  template excluded, real agents still hard-blocked on stale dates).
- **`/create-agent` now registers the agent in both locations.** Creation ends with the definition
  file existing twice: `agent/agents/<name>.md` (source of truth, next to the `<name>/` state
  folder) and a copy at `.claude/agents/<name>.md` for Claude Code's native subagent discovery.
  The skill verifies the memory links before copying — the definition must reference its state
  files by full path from the project root (`agent/agents/<name>/STATUS.md` etc.), which is what
  lets the `.claude/agents/` copy find its memory; the state folder itself is never duplicated.
  The template's instruction comment and `agent/agents/README.md` § "Adding an agent" document the
  same step.

## 2026-07-18

- **Advanced Mode: new `/create-agent` skill** (`full/agent/skills/create-agent/`). Dedicated skill
  for creating domain agents. Two ideas it encodes: (1) new agents are born **empty** — the 4 state
  files (`STATUS.md`, `MEMORY.md`, `PROJECT_MAP.md`, `RULES.md`) start as bare skeletons and are
  never pre-filled with speculation; (2) an explicit trigger table for filling them afterwards —
  on user request, when a task in the agent's domain completes, when the code structure changes,
  when general requirements get clarified, and when the user's general wishes/preferences become
  clearer — so the agent keeps its project map and state current instead of going stale. The
  existing `/create` meta-skill now routes agent creation to `/create-agent` instead of carrying
  its own copy of the procedure; `agent/agents/README.md`, `agent/skills/README.md`, and the
  skills routing table in `agent/AGENTS.md` reference the new skill.

## 2026-07-08

- **Claude Code: skills and agents are now copied into `.claude/skills/` and `.claude/agents/`.**
  Previously, Advanced Mode's `agent/skills/<name>/` and `agent/agents/<name>.md` were only
  reachable by Claude Code reading `AGENTS.md`/`CLAUDE.md` as prose — they weren't visible to
  Claude Code's native skill/subagent auto-discovery. `full/install.sh` now copies each
  `agent/skills/<name>/` into `.claude/skills/<name>/` and each `agent/agents/<name>.md`
  (excluding `README.md`) into `.claude/agents/<name>.md` when Claude Code is detected.
  `INSTALL_PROMPT.md` and `INSTALL.md` document the same step for AI-driven and manual installs.
  Also fixed a latent bug in `install.sh`'s `copy_dir_safe` helper that failed when the
  destination's parent directory didn't exist yet (surfaced by this change).
- **Fixed broken state-folder references in the 4 bundled agent templates.** Each
  `agent/agents/<name>.md` referenced its state folder with a bare relative path
  (`state-folder: backend-dev/`, `` `backend-dev/PROJECT_MAP.md` ``, etc.). That only resolved
  correctly when the `.md` was read from inside `agent/agents/` — it broke for the copy now placed
  at `.claude/agents/<name>.md` (previous entry), which has no `agent/agents/` context to resolve
  against. All 4 templates (`backend-dev`, `frontend-dev`, `infra`, `data-eng`) now reference their
  state folder by full path from the project root (`agent/agents/<name>/`), so the link holds
  regardless of which copy of the `.md` a subagent is dispatched from. The state folder itself is
  not duplicated — it stays under `agent/agents/<name>/` as the single copy.

- **`full/agent/agents/`: added 3 blank agent role templates** — `frontend-dev`, `infra`,
  `data-eng` — alongside the existing `backend-dev` worked example. Each ships a `<name>.md`
  definition file and a `<name>/` state folder (`STATUS.md`, `MEMORY.md`, `PROJECT_MAP.md`,
  `RULES.md`), all blank/generic with the `<!-- REPLACE WITH YOUR STACK -->` marker in
  `PROJECT_MAP.md` — no Acme Notes content, unlike `backend-dev`.
- **`INSTALL_PROMPT.md`: new Step 2.5 — "Choose which agents to install" (Advanced Mode only).**
  The installer now explicitly asks the user which of the 4 bundled agents (or a custom domain)
  to install, instead of only ever handling `backend-dev`. Default recommendation is still to
  install none and grow into agents organically — this is an opt-in for users who already know
  their domain boundaries at install time.

## 2026-07-07

- **`full/`: consolidated the install target into a single `agent/` folder.** Previously,
  installing Advanced Mode into a project scattered `memory/`, `agent-os/{rules,skills,hooks,agents}/`,
  and `scripts/` across the project root. Now everything lives under one `agent/` folder:
  `agent/{memory,rules,skills,hooks,agents,scripts}/` — the `agent-os/` middle layer is gone,
  its four subdirectories are now direct children of `agent/`.
- **Root `AGENTS.md`/`CLAUDE.md` are now thin stub pointers**, not full copies of the schema.
  The canonical router moved to `agent/AGENTS.md`. This also removes the old requirement to
  keep two full copies (`AGENTS.md` + `CLAUDE.md`) in sync — there's only one canonical copy now.
- **Added `agent/VERSION.md` version stamping.** `install.sh` stamps the installed schema
  version (derived from this changelog's newest entry date) and the install date. This is what
  future updates diff against.
- **Added `UPDATE_PROMPT.md`** — a paste-into-AI procedure for updating an existing install to
  a newer version of this schema, parallel to `INSTALL_PROMPT.md` for fresh installs.
- `full/scripts/install.sh` moved to `full/install.sh` (it's source-repo tooling, not part of
  the bundle copied into a target project).
