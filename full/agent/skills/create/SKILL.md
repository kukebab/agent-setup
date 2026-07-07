---
name: create
description: Create new skills or agents. Trigger when user says "make a skill", "create an agent", "turn this into a skill", "automate this", "save this workflow", "I keep doing this".
---

# /create

Bootstrap new skills or agents. Use when a workflow is stable enough to be reusable.

## When to use

User signals:

- "make a skill for X"
- "turn this into a skill"
- "I keep doing this — automate it"
- "create an agent for Y"
- "save this workflow"

Internal signal: you've watched the user do the same workflow 2+ times.

## When NOT to use

- One-off tasks (skill needs reuse value)
- Workflows still being figured out (skills should be stable, not WIP)
- Things better solved by a script/tool than a skill

## Decision: skill or agent?

**Skill** = a workflow the AI does (e.g. ingesting a URL, running a lint, drafting a spec).

**Agent** = a domain-specialized subagent with persistent state (e.g. backend-dev that owns sync/billing code).

Quick test:

- Is it a procedure? → skill
- Does it own a code area with ongoing state? → agent
- Is it both? → start as a skill, promote to agent if state grows

## Procedure — creating a skill

### 1. Define the trigger

What phrases / contexts should activate this skill? Be specific:

```
Trigger phrases:
- "trigger 1"
- "trigger 2"

Trigger contexts:
- when X happens
- before Y
```

### 2. Write the SKILL.md

File: `agent/skills/<name>/SKILL.md`

Template:

```markdown
---
name: <kebab-case-name>
description: [what + when, including trigger phrases]
---

# /<name>

[1-paragraph description]

## When to use
- [trigger 1]
- [trigger 2]

## When NOT to use
- [explicit anti-trigger]

## Procedure
### 1. [step]
### 2. [step]

## Anti-patterns
- [common mistake]
```

Keep under 300 lines. Skills are loaded into context.

### 3. Test it

Tell the user:

```
Created /skill-name. Try it next time you say "[trigger phrase]".

If it doesn't activate when you expect, tell me — we'll refine the description.
```

## Procedure — creating an agent

### 1. Confirm scope

What does this agent own? Specifically:

- Which directories? (`api/`, `frontend/`, etc.)
- Which concerns? (deployment, testing, security, etc.)
- What does it NOT touch?

If scope is fuzzy, push back. Agents need clear boundaries.

### 2. Create the definition file

`agent/agents/<name>.md` — frontmatter + system prompt + dispatch rules.

Use `agent/agents/backend-dev.md` as template.

### 3. Create the state folder

`agent/agents/<name>/` with 4 files:

- `STATUS.md` — start with empty events log + first entry "Agent created YYYY-MM-DD"
- `MEMORY.md` — empty, will fill as lessons emerge
- `PROJECT_MAP.md` — describe the directories/files this agent owns
- `RULES.md` — start minimal. Add hard rules as they're established.

### 4. Wire into routing

Update main schema (`AGENTS.md`) "Agent routing" table:

```markdown
| New domain | new-agent-name |
```

### 5. Confirm to user

```
Created agent: <name>
Owns: [list]
State: agent/agents/<name>/

Dispatch this agent for: [domain]
```

## Anti-patterns

- Creating skills for things done once — wait for 2+ use case
- Skills without specific triggers — they never activate
- Agents without clear boundaries — they overlap and conflict
- Copy-pasting existing skills without adapting — they should serve a real use
- Creating a skill instead of just doing the task — skills are infrastructure, not procrastination
