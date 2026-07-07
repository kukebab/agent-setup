---
name: morning
description: Start of day — load context, show plan. Use when user says "morning", "good morning", "start day", "what's on", or invokes `/morning`.
---

# /morning

Start-of-day ritual. Load fresh context and propose a plan for the day.

## When to use

- User starts a new session at the beginning of their workday
- Trigger phrases: "morning", "good morning", "start day", "begin", "/morning"
- After several hours of inactivity (signals fresh session)

## Procedure

### 1. Load context

Read in this order:

- `agent/memory/STATE.md` — current priorities and blockers
- `agent/memory/learnings/mistakes.md` MISTAKES section — recent corrections
- `agent/memory/wiki/INDEX.md` — what topics exist
- Latest 1-3 entries in `agent/memory/daily/*.md` — recent events
- `agent/memory/projects/*.md` if any client work is active

### 1.5 Size check (one-line nudge if agent/memory/learnings/mistakes.md is bloated)

Run `wc -l agent/memory/learnings/mistakes.md`. If > 500 lines, append to the briefing:

```
🟡 agent/memory/learnings/mistakes.md is N lines. Curated memory should stay ~300-500. Run /review-learnings to consolidate.
```

One line, non-blocking. User decides.

### 2. Compose summary

Output a short briefing (≤ 200 words):

- **Top priorities (P0/P1):** from STATE.md
- **Recent activity:** key events from latest daily logs
- **Active blockers:** anything stalling progress
- **Watchpoints:** open client asks, deadlines this week

Keep it tight. The user is starting their day, not reading a novel.

### 3. Propose a plan for today

Based on what you read, propose 2-4 things to focus on today. Lead with the most important.

Format:

```
Today's plan:
1. [most important thing] — why
2. [second priority] — why
3. [third priority, optional] — why

Start with #1?
```

### 4. Wait

Don't start working until the user confirms or redirects.

## Anti-patterns

- Reading the entire wiki — only read what's needed for the briefing
- Long summaries — the user already knows their project; surface only what's fresh
- Proposing 8 things — pick 2-4
- Starting work before the user agrees to the plan
