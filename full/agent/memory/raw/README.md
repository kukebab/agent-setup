# raw/

Immutable source dumps. Articles, transcripts, scrapes, pasted text, downloaded PDFs. Whatever feeds your wiki.

## Rules

- **Never edit a file in `raw/`.** It's a frozen snapshot of input.
- **Never rename or delete.** Wiki pages cite raw sources by filename.
- **Date every file:** `YYYY-MM-DD_short-slug.md`
- **Binary files** (PDFs, images): keep a `.md` companion with metadata + key excerpts.

## Why immutable

When wiki pages claim "according to [source]", that claim must remain verifiable. If the source can shift, the wiki loses trust. Treat `raw/` as a read-only archive.

## How to ingest

When you share a URL/file/text with your AI:

1. Save verbatim to `raw/YYYY-MM-DD_slug.md`
2. Update relevant `wiki/` pages
3. Append to today's `daily/`

This is the **Ingest** operation — see `agent/skills/ingest/SKILL.md` for the canonical flow.

## Tip

The [Obsidian Web Clipper](https://obsidian.md/clipper) browser extension converts web articles to markdown in one click. Drop them straight into `raw/` and tell your agent to ingest.
