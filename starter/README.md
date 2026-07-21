# Simple Mode — `starter/`

Everything you need to give your AI agent persistent memory across sessions. Drop this folder into your project and your agent will know how to use it.

## What's here

```
AGENTS.md           — schema (your AI reads this first)
CLAUDE.md           — same content, mirrored for Claude Code
memory/
  STATE.md          — current priorities and blockers
  learnings.md      — mistakes, wins, patterns
  daily/            — append-only event log per day
  wiki/             — topic pages, cross-linked
    INDEX.md
  outputs/          — generated deliverables (specs, reports)
  raw/              — immutable source dumps
agent-os/
  skills/           — 4 core memory-loop workflows
    morning/        — load context, propose plan
    endday/         — save session, log corrections
    ingest/         — URL/file/text → raw/ + wiki/ + daily/
    lint/           — wiki health check (script + semantic)
```

18 files total. The example data is from a fictional product called **Acme Notes**. Replace it with your own as you go.

## How to use it

1. **Copy this `starter/` directory** into your own project (rename to whatever you want — `memory/` at project root works fine).
2. **Open the project in your AI agent** — Claude Code, Codex, Cursor, Aider, anything that reads markdown.
3. **Your agent reads `AGENTS.md` (or `CLAUDE.md`)** and learns the conventions automatically.
4. **Try `/morning`** to load context, **`/ingest`** when sharing a URL, **`/endday`** to save session, **`/lint`** monthly to check wiki health.
5. **Each session starts** with `STATE.md` + `learnings.md` + `wiki/INDEX.md` + latest `daily/*.md`.

## Why skills matter

Without `/morning`, `/endday`, `/ingest`, `/lint` — `memory/` is just static folders. The skills are what make the wiki actually update over time as you work. They're the minimum needed for the memory loop to function.

## When you outgrow this

Simple Mode is for projects where one or two people work with one or two AI agents. When you need:

- Multi-domain agent state (separate context per role: backend, frontend, etc. — grown from a blank agent template)
- Behavioral rules (auto-loaded policies, e.g. testing rules, cost-aware LLM routing)
- 5 more advanced skills (`/create-spec`, `/call-debrief`, `/web-researcher`, `/create`, `/swarm`)
- Hooks (runtime enforcement: session-start auto-load, commit memory reminders)
- Pre-commit governance (staleness checks, source-of-truth discipline)

→ See [Advanced Mode in `../full/`](https://github.com/kukebab/agent-setup/tree/main/full).

## Credits

Concrete instantiation of [Andrej Karpathy's LLM wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f). The pattern is his — this packaging is one way to use it on a real project.
