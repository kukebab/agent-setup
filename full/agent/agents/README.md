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

Exception: if you already know your project has clear domain boundaries at install time (an existing multi-person team, an established backend/frontend split), it's fine to create one or more agents upfront from `template/` instead of waiting to grow into them — that's what the install-time "do you want any domain agents" prompt is for.

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

## The `template/` folder

`agent/agents/template/` is the canonical blank agent — a definition file (`agent.md.template`) plus
the 4 state files, all with `<placeholder>` markers. It is **not** an agent itself and is never
dispatched; it's the folder every new agent is copied from. Don't edit it when creating an agent —
fill only the copy. It ships with the bundle at install so `/create-agent` always has it locally.

## Adding an agent

Run `/create-agent` (`agent/skills/create-agent/SKILL.md`) — it copies `template/`, renames, fills
placeholders, wires routing, and defines when the state files get updated afterwards. Or manually:

1. Pick a clear scope (e.g. `mobile-dev`, `security`)
2. `cp -R agent/agents/template agent/agents/<name>` and move `agent.md.template` → `agent/agents/<name>.md`
3. Replace the `<placeholder>` markers; adapt the system prompt and project map to your domain
4. Claude Code: copy the definition into `.claude/agents/<name>.md` so it's discovered as a native subagent. Definition only — the state folder stays under `agent/agents/<name>/`; the definition's full `agent/agents/<name>/...` paths (state-folder, PROJECT_MAP reference) are the links that let the copy find its memory. Re-copy after editing the definition.
5. Reference the new agent from your main schema (`AGENTS.md`) under "Agent routing"

## Agent routing

The main schema (`AGENTS.md`) should have a routing table that says "for tasks in domain X, dispatch agent Y". Without that, the orchestrator doesn't know when to use which agent.

Example:

```markdown
## Agent routing

| Task type | Agent |
|---|---|
| Backend (API, DB, jobs) | `<your-backend-agent>` |
| Frontend (UI, styling) | `<your-frontend-agent>` |
```
