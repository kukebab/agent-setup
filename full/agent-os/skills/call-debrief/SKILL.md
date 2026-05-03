---
name: call-debrief
description: Extract decisions, action items, participants, and build implementation plan from call transcript OR audio recording. Auto-detects project context. Saves structured markdown debrief to memory/outputs/call-debriefs/. Updates memory/clients/ and memory/daily/. Use when user pastes a transcript, drops audio, or says "call debrief", "call notes", "what was decided", "transcript".
---

# /call-debrief

Extract structured decisions and action items from a call. Save them where they belong.

## When to use

- User pastes a call transcript
- User drops an audio file path (.mp3, .wav, .m4a, .ogg)
- User says: "call debrief", "call notes", "what was decided", "transcript", "разбери звонок"

## Procedure

### 1. Identify the call

Determine:

- **Participants** — who was on the call (names + roles if known)
- **Date** — date of the call (use today if not stated)
- **Topic** — what was discussed at high level
- **Client/project context** — does this match an existing `memory/clients/<name>.md`?

If audio file: transcribe first (whisper or equivalent), then proceed.

### 2. Extract structure

Read the transcript. Identify:

- **Decisions** — what was decided, by whom, with rationale
- **Action items** — who's doing what by when
- **Open questions** — things deferred or unresolved
- **Risks/blockers** — anything flagged
- **Customer asks (if client call)** — feature requests, complaints, expansion signals

### 3. Save the debrief

File: `memory/outputs/call-debriefs/YYYY-MM-DD_<topic-slug>.md`

Template:

```markdown
# Call Debrief — [Topic]

**Date:** YYYY-MM-DD
**Participants:** [list]
**Duration:** [if known]
**Context:** [client / internal / vendor / etc.]

## Executive Summary

[2-3 sentence summary of what happened]

## Decisions

1. **[Decision]** — [rationale]
   Owner: [who]
2. **[Decision]** — [rationale]
   Owner: [who]

## Action Items

- [ ] **[who]** — [what] (by [when])
- [ ] **[who]** — [what] (by [when])

## Open Questions

- [question, who needs to resolve, when]

## Risks / Blockers

- [risk + mitigation if discussed]

## Customer asks (if client call)

- [feature/issue + priority + commitment level]

## Raw transcript

[Optional: full transcript here, or link to raw/ if very long]
```

### 4. Update related state files

- **If client call** — update `memory/clients/<name>.md`:
  - "Recent events" section: add dated entry
  - "Open asks" section: add new requests
  - "Current state as of" date: bump to today
- **Always** — update `memory/daily/YYYY-MM-DD.md`:
  - Add 1-2 bullet summary of the call under "Actions"
  - Add any decisions to "Decisions" section
  - Add insights to "Insights" if applicable

### 5. Confirm to user

```
Debrief saved: memory/outputs/call-debriefs/YYYY-MM-DD_<slug>.md

Decisions: N
Action items: N (X assigned to you, Y to others)
Open questions: N

Updated:
- memory/clients/<name>.md (if client call)
- memory/daily/YYYY-MM-DD.md
```

## Anti-patterns

- Just dumping the transcript without extraction — the value is in structure
- Skipping client file update — the debrief disappears in outputs/ otherwise
- Making up names/decisions — only extract what's explicitly in the transcript
- Long verbose summaries — tight bullets, the structure does the work
