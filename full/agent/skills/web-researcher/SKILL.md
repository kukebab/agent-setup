---
name: web-researcher
description: Deep research on any topic using web search, multiple sources, and synthesis. Returns structured findings, ALWAYS saves to agent/memory/outputs/research/. Use when user asks to research, investigate, compare technologies, find best practices, or says "research", "find info", "compare", "deep dive", "investigate", "market research".
---

# /web-researcher

Run deep research on a topic. Multi-source web search, synthesis, structured output. **Always saves to disk.**

## When to use

- User asks to "research", "investigate", "compare", "deep dive", "find info on", "what are people saying about"
- User wants well-sourced analysis vs gut take
- Decision pending where outside intel matters

## When NOT to use

- Quick factual lookup ("what's the capital of X")
- Internal-only questions (use the wiki)
- The wiki already has the answer (grep wiki first)

## Procedure

### 1. Check the wiki first

Before any web search:

```bash
grep -r "<key terms>" agent/memory/wiki/
```

If wiki has the answer — cite it. Don't re-research what's already known.

### 2. Frame the research question

Identify:

- **Specific question** — what's being decided/learned?
- **Audience** — who'll use the answer? (informs depth)
- **Time horizon** — does recency matter? (filter by date)
- **Sources** — academic / industry / news / Reddit / GitHub?

### 3. Multi-source web search

- Start broad (3-5 search queries with different framings)
- Drill into top 5-10 sources per query
- Cross-check claims across at least 2 independent sources
- Flag where sources disagree

### 4. Synthesize

Don't just list sources. Synthesize:

- What's the rough consensus (if any)?
- What's contested?
- What's actually new vs marketing repackage?
- What does this mean for the specific decision pending?

### 5. Save to disk (MANDATORY)

File: `agent/memory/outputs/research/YYYY-MM-DD_<topic-slug>.md`

Template:

```markdown
# [Topic] — Research

**Date:** YYYY-MM-DD
**Question:** [the specific question being researched]
**Driver:** [why we needed this — link to relevant agent/memory/wiki/STATE.md]

## TL;DR

[2-4 sentence answer to the question, with the actionable recommendation]

## Findings

### [Category 1]

[claim with citations]

### [Category 2]

[claim with citations]

## What's contested

[where sources disagree, what to weight more]

## Recommendation

[given all of the above, here's what to do]

## Sources

- [Title](URL) — [date] — [why this source]
- ... (5-15 sources typically)
```

### 6. Update wiki if durable

If the research surfaced durable knowledge (not tied to a specific moment), create or update a `agent/memory/wiki/<topic>.md` page that summarizes the durable parts. Cite the research output as a source.

### 7. Confirm to user

```
Research saved: agent/memory/outputs/research/YYYY-MM-DD_<slug>.md

TL;DR: [2-line summary]

Sources: N
Wiki updated: [[topic]] [if applicable]
```

## Anti-patterns

- Single-source research (always cross-check)
- Skipping the save-to-disk step (the file IS the deliverable)
- Bullet-list of sources with no synthesis
- Making up sources or citations
- Treating wiki search as optional — always grep first
- Not citing dates on sources for time-sensitive claims
