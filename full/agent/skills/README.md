# Skills

Reusable workflows your AI agent can invoke. Each skill is just markdown — `SKILL.md` — that the agent reads and acts on.

This pattern is borrowed from [Karpathy's `program.md`](https://github.com/karpathy/autoresearch) approach: a lightweight markdown file that defines a workflow.

## How skills are invoked

Different tools have different mechanisms:

- **Claude Code:** typing `/skill-name` (slash command), or the AI invoking it via `Skill` tool when context matches the description
- **Codex / OpenCode:** the AI reads `SKILL.md` when relevant context appears
- **Cursor / Aider:** the AI reads on user request or matching trigger phrase

The descriptions in each skill's frontmatter list the trigger phrases that should activate it.

## Bundled skills

### Core memory operations (Karpathy)

- **`ingest/`** — save external source to `agent/memory/raw/`, update `agent/memory/wiki/`, log in `agent/memory/daily/`
- **`lint/`** — wiki health check (mechanical script + semantic pass + `agent/memory/learnings/mistakes.md` size check)
- **`review-learnings/`** — curate the `agent/memory/learnings/` lifecycle: promote repeated mistakes in `mistakes.md` to `patterns.md`, move stale entries to `archive.md`. Proposes changes, never auto-applies.
- **`mine-learnings/`** — mine a session transcript for candidate learnings (detected corrections + repeated tool failures) → `agent/memory/inbox/learnings-candidates.md` review queue. Human approves each before it lands in `mistakes.md`. Engine: `agent/scripts/mine_learnings.py` (+ tests).

### Session loop

- **`morning/`** — start-of-day context load + plan (flags bloated `agent/memory/learnings/mistakes.md`)
- **`endday/`** — end-of-day session save

### Memory writers (workflows that produce agent/memory/outputs/)

- **`call-debrief/`** — extract decisions and action items from call transcripts
- **`create-spec/`** — generate structured spec before non-trivial work
- **`web-researcher/`** — deep research with web search, save to `agent/memory/outputs/research/`

### Meta (agent infrastructure)

- **`create/`** — bootstrap new skills or agents
- **`swarm/`** — decompose a task into parallel subagents

## Adding your own skills

Trigger: you've done the same workflow 2+ times AND it has clear reuse value AND the pattern is stable.

Then run `/create` (the meta skill) — or copy an existing `SKILL.md` as a template.

Each skill should be:

- Under ~300 lines (skills are loaded into context — keep them tight)
- Specific about WHEN to use it (description triggers)
- Clear about WHAT it does (numbered procedure)
- Honest about WHAT IT WON'T DO (anti-patterns section)

Bundled skills follow this pattern. Use them as templates.
