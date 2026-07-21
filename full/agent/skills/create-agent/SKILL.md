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

### 2. Copy the template folder — FIRST, before any writing

The canonical blank agent lives in `agent/agents/template/`. Copy it, then rename the definition
file out of the state folder:

```bash
cp -R agent/agents/template agent/agents/<name>
mv agent/agents/<name>/agent.md.template agent/agents/<name>.md
```

Never edit `agent/agents/template/` itself — it must stay a pristine blank for the next agent.
Never write the files from scratch either: the template is the single source of the agent file
structure.

### 3. Fill the copy — minimally

Now fill placeholders in the copied files, and nothing more:

- `<name>.md` — replace every `<placeholder>` (name, domain, scope, dispatch rules), delete the
  `AGENT TEMPLATE` comment block.
- `STATUS.md` — replace `YYYY-MM-DD` with today's date. Keep "Empty until first task."
- `MEMORY.md` — replace `<name>` in the header. Stays empty; fills as lessons emerge.
- `PROJECT_MAP.md` — replace `<name>` and today's date. The stack section fills as the agent
  explores its area (the `REPLACE WITH YOUR STACK` marker shows where).
- `RULES.md` — replace `<name>` in the header. Keep the starter rules; add nothing speculative.

Do NOT pre-populate state with guesses. An empty file that fills from real work beats a
speculative one that has to be corrected later.

### 4. Register in `.claude/agents/` — with the memory links intact

The agent must exist in BOTH places:

- `agent/agents/<name>.md` + `agent/agents/<name>/` — the source of truth (definition + state)
- `.claude/agents/<name>.md` — a copy of the definition file, so Claude Code discovers it as a
  native dispatchable subagent

```bash
cp agent/agents/<name>.md .claude/agents/<name>.md
```

Before copying, verify the memory links inside the definition file: the `state-folder:` frontmatter,
the "State files" section, and the system prompt's PROJECT_MAP line must all reference the state
files by **full path from the project root** (`agent/agents/<name>/STATUS.md`, `MEMORY.md`,
`PROJECT_MAP.md`, `RULES.md`). Those links are what lets the `.claude/agents/` copy find its memory —
the state folder itself is NOT copied; it stays under `agent/agents/<name>/` as the single copy.

It's a copy, not a symlink: whenever the definition under `agent/agents/` changes later, re-copy it
to `.claude/agents/`. (For tools without native subagent discovery, skip this step — the definition
under `agent/agents/` is enough.)

### 5. Wire into routing

Add a row to the "Agent routing" table in the main schema (`AGENTS.md`).

### 6. Confirm to user

```
Created agent: <name>
Owns: [list]
Definition: agent/agents/<name>.md (+ copy in .claude/agents/<name>.md)
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

- Writing agent files by hand instead of copying `agent/agents/template/` — hand-written files drift from the canonical structure
- Editing `agent/agents/template/` while creating an agent — the template stays pristine
- Pre-filling state files with speculation "to be helpful" — they must reflect reality only
- Creating an agent before the domain has real recurring work — wait for the 3+ task signal
- Updating `STATUS.md` but forgetting `PROJECT_MAP.md` after structural changes — the map goes stale silently
- Writing requirements/wishes only in the conversation and not into state — next session starts blind
- Overlapping ownership with an existing agent — split or merge, never share a directory
- Copying the state folder into `.claude/agents/` — only the definition `.md` goes there; state lives once, under `agent/agents/<name>/`
- Editing the `.claude/agents/` copy directly — edit `agent/agents/<name>.md` and re-copy
