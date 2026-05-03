---
name: ingest
description: Reflexive Karpathy LLM-wiki Ingest. Save external source (URL, gist, YouTube, repo, article, PDF, file path, or pasted text) to memory/raw/, extract topics, update memory/wiki/, and log in memory/daily/. Use when user shares a URL/video/article/repo/gist/transcript, drops a file path, pastes a large block of text, or says "ingest this", "save this", "remember this article", "add to memory", "ingest <url>". Do NOT use for one-off lookups where the user doesn't want to keep the content.
---

# /ingest — Karpathy LLM Wiki Ingest

The **Ingest** operation from Karpathy's pattern. New source → `raw/` → update `wiki/` → log `daily/`.

## When to use

Trigger reflexively when the user:

- Shares a URL or link
- Drops a file path
- Pastes a large block of text (>200 words)
- Sends a YouTube/video link
- Sends a tweet, gist, or repo URL
- Says: "ingest", "save this", "remember this", "add to memory", "проанализируй и сохрани"

Do NOT trigger for:

- Simple lookups ("what does this say?") where the user doesn't want to keep it
- Casual references in conversation
- Things already in memory (search first; if found, cite instead)

## Procedure

### 1. Save raw source (immutable)

```
File: memory/raw/YYYY-MM-DD_<slug>.md
```

Slug = short kebab-case description (e.g. `karpathy-llm-wiki-gist`, `notion-team-spaces-launch`).

Content:

- For URLs: fetch content, save full text + metadata (URL, title, author, date)
- For pasted text: save verbatim
- For YouTube: fetch transcript, save with video URL + title
- For repos: save README + key file excerpts (don't dump entire repo)
- For PDFs/files: save companion `.md` with key excerpts

**Never edit `raw/` files later.** Frozen snapshot.

### 2. Read and extract

Read the raw source. Identify:

- Key facts / claims
- New topics not yet in wiki
- Topics that update existing wiki pages
- Contradictions with existing wiki content

### 3. Update `memory/wiki/`

For each topic touched:

- **New topic** → create `wiki/<topic>.md` with:
  - One-paragraph blockquote summary
  - Key sections
  - `## Sources` section linking back to raw file
  - Cross-links via `[[topic-name]]`
- **Existing topic** → update relevant section. If the new source contradicts existing claims, add a `> [!note]` callout noting both views with dates.

Update `wiki/INDEX.md` with new entries.

### 4. Append to `daily/YYYY-MM-DD.md`

```markdown
## Ingest

- **[Source title]** ([type: article/video/repo/etc.])
  - Saved to `raw/YYYY-MM-DD_slug.md`
  - Updated wiki: [[topic1]], [[topic2]]
  - Created wiki: [[new-topic]] [if applicable]
  - Key takeaways: [1-3 bullet points]
```

### 5. Confirm to user

Brief output:

```
Ingested: [title]
- raw: raw/YYYY-MM-DD_slug.md
- wiki updates: [list]
- daily logged

Key takeaways:
- [point 1]
- [point 2]
```

## Anti-patterns

- Saving only to raw/ without updating wiki — half-job, wiki doesn't compound
- Editing raw/ later — destroys verifiability
- Creating shallow wiki pages — if a topic only has 2 sentences, fold it into an existing page
- Re-ingesting a source already in raw/ (check first)
- Long verbose summaries to user — keep confirmation tight
