---
name: create-spec
description: Generate a structured specification before complex work (new module, major feature, integration). AI-readable format with numbered requirements, acceptance criteria (Given-When-Then), data contracts, and edge cases. Use when user says "spec", "specification", "create spec", "write spec", "PRD", or before any 2+ hour task.
---

# /create-spec

Generate a structured spec doc before non-trivial work. Saves to `memory/outputs/specs/`.

## When to use

- User asks for "spec", "specification", "PRD"
- Before any task estimated >2 hours
- Before any task with >3 distinct stages
- When multiple people / agents will collaborate on the work

## When NOT to use

- One-line bug fixes
- Trivial config changes
- Pure research/investigation tasks (use `/web-researcher` instead)

## Procedure

### 1. Gather context

Ask up to 3 clarifying questions if scope is unclear. Examples:

- What's the minimum thing that solves the user's problem?
- What's explicitly out of scope?
- Who's the customer for this?

Don't ask 8 questions. Pick the 3 that matter most for scope clarity.

### 2. Compose the spec

File: `memory/outputs/specs/YYYY-MM-DD_<feature-slug>.md`

Template:

```markdown
# [Feature Name] — Spec

**Date:** YYYY-MM-DD
**Owner:** [who's building]
**Driver:** [who asked / customer for this]
**Customer (if applicable):** [[clients/<name>]]
**ETA:** [target date]

## Problem

[1-2 paragraphs on what's broken / missing / needed. Concrete user pain.]

## Goal

[The smallest thing that solves the problem. One sentence ideally.]

## Out of scope (v1)

- [explicit list of things NOT in this spec — equally important as in-scope]

## Acceptance criteria

Given [precondition], when [action], then [observable outcome]:

- [criterion 1]
- [criterion 2]
- [criterion 3]

## Technical approach

[1-2 paragraphs on HOW. Library choices, integration points, key constraints.]

## Risks

- [risk] — [mitigation]

## Rollout

- [phased plan: alpha / beta / GA]
- [success metrics]

## Cross-links

- Related: [[wiki/<topic>]]
- Customer context: [[clients/<name>]]
```

### 3. Save and confirm

```
Spec saved: memory/outputs/specs/YYYY-MM-DD_<slug>.md

Key points:
- [3-bullet summary]

Ready to start, or refine spec first?
```

## Anti-patterns

- Writing a 5-page spec for a 2-hour feature — proportion to scope
- Skipping "out of scope" — that's where bugs hide
- Vague acceptance criteria ("user can export") — must be observable/testable
- Not linking to customer context if there's a real customer driving the work
- Burying the spec in chat — the file IS the artifact, must be saved
