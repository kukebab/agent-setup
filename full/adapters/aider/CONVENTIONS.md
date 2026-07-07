# Project Conventions (Aider)

This project uses the **agent-os** pattern. The root `AGENTS.md` is a thin stub — the canonical schema is in `agent/AGENTS.md`, read that for the full schema.

## Quick reference

- **Memory layer:** `agent/memory/` — read `STATE.md` + `learnings/mistakes.md` MISTAKES + `wiki/INDEX.md` at session start.
- **Behavioral rules:** `agent/rules/` — auto-loaded policies (verification, testing, file size, cost).
- **Skills:** `agent/skills/` — reusable workflows.
- **Agents:** `agent/agents/` — domain specialists with persistent state.

## Aider-specific tips

- Run `aider --read AGENTS.md --read agent/memory/STATE.md` at start to auto-load context.
- The `commit-memory-reminder.sh` hook is Claude Code-specific and won't fire here. Compensate with manual updates to `agent/memory/daily/` after each commit.
- For research outputs and specs, save to `agent/memory/outputs/` (Aider works fine with this — just write the files).

## Where to find things

| Looking for | Read |
|---|---|
| What this project is | `agent/AGENTS.md` § Identity, § Memory protocol |
| Current priorities | `agent/memory/STATE.md` |
| Past mistakes to avoid | `agent/memory/learnings/mistakes.md` |
| Code map | `agent/agents/<role>/PROJECT_MAP.md` |
| When to dispatch which agent | `agent/AGENTS.md` § Agent dispatch |
| How to do X | Search `agent/skills/` |

When in doubt about how to behave: `agent/AGENTS.md` is the schema.
