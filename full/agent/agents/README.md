# Agents

Domain-specialized subagents. Each agent owns a part of the codebase and maintains its own operational state.

## Why have multiple agents

A single AI agent works fine for small projects. As complexity grows, splitting by domain helps:

- **Different concerns, different context** — backend agent doesn't need to know UI conventions
- **Token efficiency** — each agent loads only its own state, not everything
- **Continuity** — when you return to backend work, the backend agent remembers where you left off
- **Parallelism** — independent tasks can run as parallel agent dispatches

## When to add an agent

Don't pre-create agents. Add one when:

- You've done 3+ tasks in the same domain
- A clear "owner area" emerges (frontend, backend, infra, data, etc.)
- Cross-domain context-switching is costing you time

For small projects, one main agent (no `agent/agents/` folder) is fine.

## Anatomy of an agent

Each agent is defined by:

- **A definition file** — `agent/agents/<name>.md` — role, when to dispatch, system prompt
- **A state folder** — `agent/agents/<name>/` — 4 files maintaining operational memory:
  - `STATUS.md` — events log + current state + TODO. Updated after every significant task.
  - `MEMORY.md` — long-term lessons, gotchas, decisions with rationale.
  - `PROJECT_MAP.md` — where the code lives, file responsibilities. Updated on structural changes.
  - `RULES.md` — hard rules: always-do / never-do, with reasoning. Rare additions.

## Example included

- **`backend-dev.md`** + **`backend-dev/`** — backend specialist for the Acme Notes example. Stack: Next.js + Postgres (clearly marked `<!-- REPLACE WITH YOUR STACK -->` in PROJECT_MAP).

## Adding your own agent

1. Pick a clear scope (e.g. `frontend-dev`, `data-eng`, `infra`)
2. Copy `backend-dev.md` and `backend-dev/` as a template
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
