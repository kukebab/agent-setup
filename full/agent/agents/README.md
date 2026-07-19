# Agents

Domain-specialized subagents. Each agent owns a part of the codebase and maintains its own operational state.

## Why have multiple agents

A single AI agent works fine for small projects. As complexity grows, splitting by domain helps:

- **Different concerns, different context** — backend agent doesn't need to know UI conventions
- **Token efficiency** — each agent loads only its own state, not everything
- **Continuity** — when you return to backend work, the backend agent remembers where you left off
- **Parallelism** — independent tasks can run as parallel agent dispatches

## When to add an agent

Default to not pre-creating agents. Add one when:

- You've done 3+ tasks in the same domain
- A clear "owner area" emerges (frontend, backend, infra, data, etc.)
- Cross-domain context-switching is costing you time

Exception: if you already know your project has clear domain boundaries at install time (an existing multi-person team, an established backend/frontend split), it's fine to install one or more of the bundled templates upfront instead of waiting to grow into them — that's what the install-time "which agents do you want" prompt is for.

For small projects, one main agent (no `agent/agents/` folder) is fine.

## Anatomy of an agent

Each agent is defined by:

- **A definition file** — `agent/agents/<name>.md` — role, when to dispatch, system prompt
- **A state folder** — `agent/agents/<name>/` — 4 files maintaining operational memory:
  - `STATUS.md` — events log + current state + TODO. Updated after every significant task.
  - `MEMORY.md` — long-term lessons, gotchas, decisions with rationale.
  - `PROJECT_MAP.md` — where the code lives, file responsibilities. Updated on structural changes.
  - `RULES.md` — hard rules: always-do / never-do, with reasoning. Rare additions.

## Operating rules

- **Code must be written via subagent dispatch, not by the orchestrator directly.** The main session plans and verifies; the agent (subagent) does the actual reading/writing of code. See `agent/rules/agent-quality.md` § Dispatch Rules.
- **`PROJECT_MAP.md` is mandatory, not optional.** Check it before any Read/Grep/Glob so the agent isn't re-exploring code it already mapped, and keep it updated whenever the code structure changes (new file/module, moved responsibility). An agent with a stale or empty `PROJECT_MAP.md` is wasting tokens re-discovering what should already be recorded.

## Bundled templates

Four ready-to-install role templates ship here. Pick the ones that match your project — installers ask which of these you want (see `INSTALL_PROMPT.md`).

- **`backend-dev.md`** + **`backend-dev/`** — the one **worked example**, filled in for the fictional Acme Notes project (Next.js + Postgres). Stack-specific paths clearly marked `<!-- REPLACE WITH YOUR STACK -->` in PROJECT_MAP — use it to see what a filled-in agent looks like, then replace the specifics.
- **`frontend-dev.md`** + **`frontend-dev/`** — blank template. UI components, client-side state, styling, frontend routing.
- **`infra.md`** + **`infra/`** — blank template. CI/CD, deploy pipelines, environment config, observability.
- **`data-eng.md`** + **`data-eng/`** — blank template. ETL/pipelines, analytics schemas, data warehouse.

The three blank templates have no example content — their `PROJECT_MAP.md` has the `<!-- REPLACE WITH YOUR STACK -->` marker and placeholder paths, and `STATUS.md`/`MEMORY.md`/`RULES.md` start empty.

## Adding your own agent (not in the bundled list)

Run `/create-agent` (`agent/skills/create-agent/SKILL.md`) — it walks through scope, definition,
empty state folder, and routing, and defines when the state files get updated afterwards. Or manually:

1. Pick a clear scope (e.g. `mobile-dev`, `security`)
2. Copy `backend-dev.md` and `backend-dev/` (or any bundled template) as a starting point
3. Adapt the system prompt and project map to your domain
4. Reference the new agent from your main schema (`AGENTS.md`) under "Agent routing"

## Agent routing

The main schema (`AGENTS.md`) should have a routing table that says "for tasks in domain X, dispatch agent Y". Without that, the orchestrator doesn't know when to use which agent.

Example:

```markdown
## Agent routing

| Task type | Agent |
|---|---|
| Backend (sync, billing, API) | backend-dev |
| Frontend (UI, editor, mobile) | frontend-dev |
| Data analysis | data-eng |
```
