# Project Conventions (Aider)

This project uses the **agent-os** pattern. The canonical schema is in `AGENTS.md` — read it for the full schema.

## Quick reference

- **Memory layer:** `memory/` — read `STATE.md` + `learnings.md` MISTAKES + `wiki/INDEX.md` at session start.
- **Behavioral rules:** `agent-os/rules/` — auto-loaded policies (verification, testing, file size, cost).
- **Skills:** `agent-os/skills/` — reusable workflows.
- **Agents:** `agent-os/agents/` — domain specialists with persistent state.

## Aider-specific tips

- Run `aider --read AGENTS.md --read memory/STATE.md` at start to auto-load context.
- The `commit-memory-reminder.sh` hook is Claude Code-specific and won't fire here. Compensate with manual updates to `memory/daily/` after each commit.
- For research outputs and specs, save to `memory/outputs/` (Aider works fine with this — just write the files).

## Where to find things

| Looking for | Read |
|---|---|
| What this project is | `AGENTS.md` § Identity, § Memory protocol |
| Current priorities | `memory/STATE.md` |
| Past mistakes to avoid | `memory/learnings.md` |
| Code map | `agent-os/agents/<role>/PROJECT_MAP.md` |
| When to dispatch which agent | `AGENTS.md` § Agent dispatch |
| How to do X | Search `agent-os/skills/` |

When in doubt about how to behave: `AGENTS.md` is the schema.
