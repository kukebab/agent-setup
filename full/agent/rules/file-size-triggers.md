# File Size Triggers — Architectural Hygiene

Per-change quality rules catch ugly diffs but miss long-term file growth. This rule fires on the **size of the target file BEFORE the edit**, regardless of how clean the individual change is. Goal: prevent god-files (the kind reviewers flag months later).

## Hard Triggers — File-Size Pre-Check

**Before adding ANY code to an existing file, run `wc -l <file>` and apply this gate:**

| Size of target file | Allowed action |
|---|---|
| < 500 lines | Edit freely |
| 500–1000 lines | If the new code introduces a new concern (entry point / I/O / domain rule / external integration / AI orchestration / validation), say to the user: "`foo.py` is already N lines, growing into <new concern>. Split now or after this fix?" Wait for answer. |
| 1000–2000 lines | NO new feature additions without explicit user approval. Bug fixes + small extensions to existing concerns OK. |
| > 2000 lines | Stop. Split first, feature second. Refuse incremental additions until decomposition is agreed. |

The check is **mechanical**: file size is observable, no judgment needed for the gate itself. Judgment only kicks in for the discussion of HOW to split.

## Single-Responsibility Audit (when triggered)

A file is a "god-file" if it owns **3+** of these concerns:

- HTTP / cron entry points (route handlers, webhooks, scheduled jobs)
- Business / domain logic (rules, scoring, matching, state machines)
- Storage / DB operations (raw SQL, ORM calls, migrations)
- External I/O (HTTP clients, queue consumers, scraping)
- AI / LLM orchestration (prompts, model routing, retries)
- Validation / sanitization / data cleanup
- UI rendering (a component with > 1 dialog inside)

When you detect 3+ in one file: tell the user what concerns you see and propose a file-by-concern split. Don't implement until they agree.

## Soft Triggers — Passive Flags

Even when not adding code (just reading), if a relevant file is > 800 lines AND the user is about to make a non-trivial decision tied to it (architecture, integration, refactor), mention it once:

> "By the way, `foo.py` is already 1200 lines and holds <X> + <Y>. Want to split before this change, or continue as is?"

One mention per session per file. Don't nag.

## What This Rule Does NOT Cover

- One-off scripts (audits, backfills, batch jobs) — long is fine if single-job
- Type definitions (schema files, `types/index.ts`) — naturally accumulate
- Config files, fixtures, generated code — exempt
- Frontend page-level files where the framework puts everything in one place — case-by-case

## Counter-Rule: Don't Refactor for the Sake of It

If the file is large but **cohesive** (single domain, single owner, no concern-mixing), do NOT propose a split just because of line count. Cohesion > size. The triggers above use line count as a **prompt to check cohesion**, not a verdict.

Examples of large-but-fine files:
- An extractors module (1200 lines, all PDF/DOCX/XLSX text extraction) — single domain
- A validators module (1300 lines, all field validation) — single domain
- A type registry — expected to grow

When a new project starts, the rule is: **the first time a file crosses 800 lines, even if clean, ask "is this still one concern?"** That's the hygiene discipline this rule enforces.
