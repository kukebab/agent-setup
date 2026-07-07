# Changelog

Notable changes to the agent-os-starter pattern (`starter/` and `full/` modes). This is a
changelog for the **pattern itself**, not for any project that has installed it.

Each entry is dated `YYYY-MM-DD`. If you have this pattern installed in a project, compare
the "Schema version" in your project's `agent/VERSION.md` against the dates below — entries
newer than your installed version are changes you haven't applied yet. See `UPDATE_PROMPT.md`
for the update procedure.

## 2026-07-08

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
