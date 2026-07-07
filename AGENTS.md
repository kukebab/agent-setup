# agent-os-starter — How to Work Inside This Repo

> If you're an AI agent inside the `agent-os-starter` repo (not a user project that's installed it), this file tells you how to behave. It is **not** a project schema — it's a meta-doc for contributors.

If you got here by following an install link, you want [`INSTALL_PROMPT.md`](INSTALL_PROMPT.md), not this file.

## What this repo is

A starter kit for installing the **agent-os** pattern (Karpathy LLM wiki + operational governance) into other projects. The repo contains:

- Documentation: `README.md`, `INSTALL.md`, `INSTALL_PROMPT.md`, `EXAMPLE_TOUR.md`
- Two example modes: `starter/` (Simple) and `full/` (Advanced)
- A fictional example project (Acme Notes) that fills out the structure with realistic-feeling content

## Your job in this repo

You are **not** building Acme Notes. Acme Notes is example data. Treat it as illustrative content the same way a code template treats `// TODO: replace`.

You **are**:

- Maintaining the starter kit itself
- Updating documentation
- Fixing bugs in `install.sh`, `check-staleness.py`, `lint-wiki.py`
- Adding new tool adapters (`adapters/<tool>/`)
- Improving `INSTALL_PROMPT.md` based on real-world install tests
- Keeping `starter/` and `full/` in sync conceptually (Advanced is a superset, not a divergence)

## Critical: do NOT pollute starter/ or full/ with personal data

The whole point of this repo is "no personal references." When working here:

- Never insert real names, real client names, real revenue numbers, real domains
- The example project is **Acme Notes** (fictional B2B notes app); the team is **Maya Chen** (founder) + **Alex Rivera** (contractor); the design partners are **Bluefin Coffee** and **Tessera Studio**
- Before any commit that touches `starter/` or `full/`, run a scrub grep for personal-residue patterns (real names, real client names, real domain references) — should return zero hits. Maintain the scrub pattern list in your contributor checklist; do not embed the literal patterns in this doc (that defeats the scrub).

If the scrub finds anything, fix before committing.

## Working memory for this repo

This repo's own working memory lives in the **parent operating-os repo**, at `memory/outputs/agent-os-starter/CONTEXT.md`. That file holds the canonical Acme Notes context (team, priorities, partners, etc.) — refer back to it when populating example files to keep names and dates consistent.

The `agent-os-starter` repo itself does **not** have a `memory/` directory at root — that would conflict with users who install this pattern into their projects. The example `memory/` only exists inside `starter/` and `full/`.

## Repo layout

```
agent-os-starter/
├── README.md                ← human-facing pitch
├── INSTALL.md               ← human manual install
├── INSTALL_PROMPT.md        ← THE killer file — paste-into-AI installer
├── UPDATE_PROMPT.md         ← paste-into-AI updater for existing installs
├── CHANGELOG.md             ← dated log of changes to the pattern itself
├── EXAMPLE_TOUR.md          ← walkthrough of Acme Notes example
├── AGENTS.md                ← this file
├── CLAUDE.md                ← mirror of this file
├── LICENSE                  ← MIT
├── starter/                 ← Simple Mode template (12 files, Acme Notes example)
└── full/                    ← Advanced Mode template (~60 files, Acme Notes example)
    ├── AGENTS.md / CLAUDE.md    ← thin root stubs, copied to target project root
    ├── install.sh               ← installer (not copied into target)
    ├── adapters/                ← tool-specific shims (Cursor, Aider, Windsurf)
    └── agent/                   ← the whole bundle, copied wholesale to target's agent/
```

`starter/` and `full/` ARE the worked Acme Notes example — no separate `examples/` directory. Both modes contain the same fictional project at different complexity levels.

## When the user asks about the agent-os pattern

Refer them to:

- `README.md` — high-level pitch + credits
- `EXAMPLE_TOUR.md` — what it does day-to-day
- `starter/AGENTS.md` — Simple Mode example schema (the schema users actually copy)
- `full/agent/AGENTS.md` — Advanced Mode example schema (richer). `full/AGENTS.md` at the repo root is just a thin stub pointing at it — don't confuse the two.

Do not paraphrase those files inline — point at them.

## When the user asks to install agent-os

That's `INSTALL_PROMPT.md`'s job. Tell the user to:

1. Open **their own project** in their AI agent (Claude Code, Codex, Cursor, etc.)
2. Paste the contents of `INSTALL_PROMPT.md`
3. Their AI will inspect their project and install the adapted version

Do **not** try to install agent-os from inside this repo into itself. This repo is the source, not the destination.

## When the user asks to fix or extend the starter

Edit files in `starter/`, `full/`, `adapters/` as appropriate. Before committing:

1. Run scrub grep (above)
2. If you changed `install.sh` or `check-staleness.py`, test on a fake project structure
3. If you changed schema in `starter/AGENTS.md`, sync the corresponding `starter/CLAUDE.md` mirror. For `full/`, the canonical schema is `full/agent/AGENTS.md` (no mirror to keep in sync); only the tiny root stubs `full/AGENTS.md` / `full/CLAUDE.md` need to stay identical to each other.
4. If you added a new rule, skill, or agent — update the relevant `README.md` index
5. If the change is user-visible (new file, moved path, changed behavior), add a dated entry to `CHANGELOG.md`

## Conventions

- Markdown only for documentation. No HTML in docs.
- Code in `scripts/`: bash + Python 3 (no exotic deps; standard library only).
- Line widths: ~120 chars max in docs, no hard wrap.
- Frontmatter (`---` blocks) only where the loading tool requires it (Cursor `.mdc`, skill files).
- Never assume a specific tech stack in `starter/` or `full/AGENTS.md` — they're stack-agnostic.

## Things to NOT do

- Don't add a `memory/` directory at the repo root (would conflict with installs)
- Don't add a `.claude/` directory at repo root (same reason)
- Don't bake a specific stack into `starter/` or schema files — only the example `backend-dev` agent in `full/` may have stack-specific paths, and only with the `<!-- REPLACE WITH YOUR STACK -->` marker
- Don't add rules with names matching personal patterns to `full/agent/rules/` — keep them universal
- Don't merge changes that would expand `full/agent/AGENTS.md` past ~250 lines — it's a router, not a rule dump (full content lives in `full/agent/rules/`)

## License

MIT. PRs welcome.
