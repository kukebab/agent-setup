# Acme Notes — AI Agent Schema

> This is the schema document for the Acme Notes team wiki. It tells your AI agent how the wiki is structured, what conventions we use, and how to maintain it. Based on [Karpathy's LLM wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

## If you are an AI agent installing this into a project or knowledge workspace

1. Copy this schema and the `memory/` layout into the target repo.
2. Preserve existing project files — never overwrite or delete without asking the user first.
3. Replace the Acme Notes example content with the user's real project context (priorities, learnings, wiki topics).
4. If the user already has any `memory/` files, ask before merging or replacing them.

## What this is

`memory/` is a persistent, LLM-maintained wiki for this project. Your AI agent reads from it for context and writes to it as work happens. Knowledge compounds across sessions instead of being re-derived every time.

## Memory layout

- `memory/STATE.md` — current priorities, blockers, status. Read first every session.
- `memory/learnings.md` — mistakes, wins, patterns. Append after every correction.
- `memory/daily/YYYY-MM-DD.md` — append-only event log per day.
- `memory/wiki/` — topic pages, one `.md` per concept. Cross-link via `[[topic-name]]`.
- `memory/raw/` — immutable source dumps. Never edit, never rename.
- `memory/outputs/` — generated deliverables (specs, reports, drafts).

## Skills (memory loop workflows)

4 skills live in `agent-os/skills/`. Each is a `SKILL.md` file describing a workflow you can invoke:

- **`/morning`** — load context (STATE + learnings + INDEX + latest daily), propose plan
- **`/endday`** — save session events to daily, update STATE if priorities shifted, log user corrections to learnings
- **`/ingest`** — Karpathy ingest. URL/file/text → raw/ + update wiki/ + log daily/. The single most important skill — without it the wiki never grows
- **`/lint`** — Karpathy lint. Mechanical wiki health check + semantic pass

How they're invoked depends on the tool (Claude Code: `/morning`; Codex/Cursor: read `SKILL.md` when context matches description trigger phrases).

## Operations (Karpathy)

### Ingest

When the user shares a URL, file, transcript, or pasted text:

1. Save the source verbatim to `memory/raw/YYYY-MM-DD_<slug>.md`. Never edit later.
2. Read it. Extract key facts.
3. Update relevant `memory/wiki/*.md` pages — strengthen claims, add cross-references, flag contradictions with existing content.
4. Append to today's `memory/daily/YYYY-MM-DD.md`: what was ingested, what changed.

### Query

When the user asks a question:

1. Read `memory/wiki/INDEX.md` first to find relevant pages.
2. Drill into those pages. Read raw sources only if pages are insufficient.
3. Answer with citations to wiki pages.
4. If the answer is non-trivial and reusable, file it back as a new wiki page or `memory/outputs/` deliverable.

### Lint

Periodic health check (run when asked, or after big ingest days):

1. Find orphan pages (no inbound links from other pages or INDEX).
2. Find broken `[[cross-links]]` (pointing to non-existent pages).
3. Find stale claims (contradicted by newer sources).
4. Suggest missing topics (concepts mentioned in passing that deserve their own page).

## Conventions

- Wiki pages start with a one-paragraph blockquote summary.
- Cross-link via `[[topic-name]]` (no `.md` extension).
- Every `memory/raw/` file is dated: `YYYY-MM-DD_short-slug.md`.
- `daily/` entries are append-only. New session = new section in same day's file.
- `learnings.md` MISTAKES section: append after every user correction, using the format in that file.

## Session start

Read in order:

1. `memory/STATE.md`
2. `memory/learnings.md` (MISTAKES section)
3. `memory/wiki/INDEX.md`
4. Latest `memory/daily/*.md`

That's enough context to act. Don't re-read the wiki end-to-end every session.

## When you outgrow Simple Mode

This setup works for a small team with one or two AI agents. When you need:

- Multi-domain agent state (separate context per role)
- Behavioral rules (auto-loaded policies)
- Skills (reusable workflows like `/ingest`, `/lint`)
- Hooks (runtime enforcement, pre-commit governance)

→ See [agent-setup Advanced Mode](https://github.com/kukebab/agent-setup/tree/main/full).

## References

- [Karpathy's LLM wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — the foundational pattern.
- [agent-setup](https://github.com/kukebab/agent-setup) — this repo.
