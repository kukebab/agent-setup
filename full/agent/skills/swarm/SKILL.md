---
name: swarm
description: Decompose a complex task into parallel subagents. Use when user says "create agents for this", "spin up a swarm", "parallel agents", "swarm this", "break this into subagents", "decompose".
---

# /swarm

Decompose a multi-domain task into parallel subagents and dispatch them concurrently.

## When to use

- Task has 3+ independent sub-tasks (no shared state, no order dependency)
- Total work is large enough that sequential execution would be slow
- Each sub-task is well-scoped enough to specify in 5-10 lines

User triggers: "swarm this", "parallel agents", "create agents for X", "decompose"

## When NOT to use

- Sub-tasks share files/state (would conflict)
- Sub-tasks have order dependencies (must be sequential)
- Whole task is small enough for one agent
- You'd be creating one-off agents that have no reuse value

## Procedure

### 1. Decompose

Break the task into sub-tasks. For each:

- Domain (which agent / which directory)
- Specific files to touch
- What changes, what stays
- Verification command

If you can't write each in <10 lines, the task isn't decomposed enough — keep splitting.

### 2. Identify dependencies

Map sub-tasks to dependencies. Anything that depends on another's output → NOT parallel.

Output a dispatch plan:

```
Parallel wave 1:
- agent-A: [task 1]
- agent-B: [task 2]
- agent-C: [task 3]

Sequential after wave 1:
- agent-D: [task that uses outputs from A/B/C]
```

### 3. Show the plan to the user

```
Plan:
Wave 1 (parallel, ~N min):
1. [agent] — [task]
2. [agent] — [task]
3. [agent] — [task]

Wave 2 (sequential, after wave 1):
4. [agent] — [task] (uses outputs from 1+2)

Proceed?
```

Wait for confirmation.

### 4. Dispatch wave 1 in parallel

Use multiple agent dispatches in a single message. Each agent gets:

- Specific scope (file paths, what to change, how to verify)
- Reference to its `PROJECT_MAP.md` for context
- Verification expectation

### 5. Collect results, verify

Per `agent/rules/agent-quality.md` IRON LAW:

- Each agent's "done" claim must be verified by the orchestrator
- Run the verification command yourself
- Read at least one modified file per agent

### 6. Dispatch later waves only after prior waves verified

Don't pipeline waves blindly. Wave N+1 starts only after wave N verified.

### 7. Final summary

```
Swarm complete:
- Wave 1: N agents, all verified
- Wave 2: N agents, all verified

Files modified: [list]
Tests passing: N/N
```

## Anti-patterns

- Dispatching agents for sub-tasks that share files — they'll conflict
- Skipping verification because "all agents reported success"
- Decomposition that isn't actually parallel (sequential dependencies disguised as parallel)
- Creating new ad-hoc agents for one-off swarm — use existing agents where possible
- Not confirming the plan with the user before dispatch
