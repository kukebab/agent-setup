---
name: create-agent
description: Create a new domain agent with empty state files that fill up as work happens. Trigger when user says "create an agent", "new agent", "add an agent for X", "make an agent". Also defines WHEN the agent's state must be updated afterwards.
---

# /create-agent

Bootstrap a new domain-specialized agent. The agent is born **empty** — its state files start as bare
skeletons and fill up as real work happens. This skill defines both the creation procedure and the
update triggers that keep the agent's project map and state current afterwards.

## When to use

- "create an agent for X"
- "new agent", "add an agent"
- `/create` decided the thing being automated is an agent, not a skill
- A domain has accumulated 3+ tasks and a clear owner area (see `agent/agents/README.md`)

## When NOT to use

- The workflow is a procedure, not an ownership area → make a skill instead (`/create`)
- Scope is fuzzy ("an agent for everything else") — push back until boundaries are clear
- The project is small enough that the main agent handles everything fine

## Procedure — creation

### 1. Confirm scope

Pin down before writing anything:

- Which directories does this agent own?
- Which concerns? (e.g. deployment, testing, a subsystem)
- What does it explicitly NOT touch?

If the user can't answer, the agent isn't ready to exist yet.

### 2. Create the definition file

`agent/agents/<name>.md` — frontmatter (`name`, `description`, `state-folder: agent/agents/<name>/`,
`model`, `effort`) + system prompt + dispatch rules. Copy `agent/agents/frontend-dev.md` as the
blank template (or `backend-dev.md` to see a filled-in example).

### 3. Create the state folder — empty

`agent/agents/<name>/` with the 4 state files, each a skeleton with headers only, no content:

- `STATUS.md` — one entry: "YYYY-MM-DD — Agent created". Current state: "Empty until first task."
- `MEMORY.md` — empty. Fills as lessons emerge.
- `PROJECT_MAP.md` — empty apart from the section headers. Fills as the agent explores its area.
- `RULES.md` — empty. Rules are added when established, never invented upfront.

Do NOT pre-populate these files with guesses. An empty file that fills from real work beats a
speculative one that has to be corrected later.

### 4. Wire into routing

Add a row to the "Agent routing" table in the main schema (`AGENTS.md`), and — if the tool supports
native subagents (e.g. Claude Code) — copy the definition file to its discovery location
(`.claude/agents/<name>.md`).

### 5. Confirm to user

```
Created agent: <name>
Owns: [list]
State: agent/agents/<name>/ (empty — fills as work happens)
```

## Procedure — keeping state filled (the important part)

The state files are only useful if they're updated. Update them at these triggers:

| Trigger | Update |
|---|---|
| User asks ("update your state", "save where we are") | All 4 files as needed — never refuse, never defer |
| A task in this agent's domain is completed | `STATUS.md` — new event entry, current state, TODO delta |
| Code structure changed (new file/module, moved responsibility) | `PROJECT_MAP.md` — same session, not "later" |
| General requirements got clarified (user pinned down what must be true) | `STATUS.md` current state + `RULES.md` if it's a hard always/never rule |
| General wishes/preferences became clearer (user revealed how they like things) | `MEMORY.md` — record the preference with its rationale |
| A lesson was learned the hard way (bug, gotcha, wrong assumption) | `MEMORY.md` |

Rules of thumb:

- **State updates happen in the same session as the trigger.** A "will update later" note is a lost update.
- **`PROJECT_MAP.md` is the map, `STATUS.md` is the position.** Map changes on structural change; position changes on every task.
- **Requirements vs wishes:** a requirement constrains what the agent must do (→ STATUS/RULES); a wish shapes how the agent should do it (→ MEMORY). When unsure, MEMORY.
- Keep entries short — one dated line beats a paragraph. These files are loaded into context.

## Anti-patterns

- Pre-filling state files with speculation "to be helpful" — they must reflect reality only
- Creating an agent before the domain has real recurring work — wait for the 3+ task signal
- Updating `STATUS.md` but forgetting `PROJECT_MAP.md` after structural changes — the map goes stale silently
- Writing requirements/wishes only in the conversation and not into state — next session starts blind
- Overlapping ownership with an existing agent — split or merge, never share a directory
