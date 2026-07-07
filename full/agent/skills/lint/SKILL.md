---
name: lint
description: Wiki health check — orphans, broken [[cross-links]], missing frontmatter/blockquote/sources, INDEX drift, tiny/stale pages, duplicate topics. Runs mechanical script then semantic pass via LLM. Auto-fixes safe issues, flags the rest. Use when user says "lint", "lint wiki", "audit memory", "check wiki", "wiki audit", or as monthly maintenance.
allowed-tools: Read Write Edit Bash Grep Glob
---

# /lint — Karpathy LLM Wiki health check

The **Lint** operation from Karpathy's pattern. Two phases: mechanical (script) then semantic (LLM). Reports findings, auto-fixes what's safe, flags the rest.

## When to use

- User asks: "lint", "lint wiki", "audit memory", "check wiki", "health check"
- After a big ingest day (5+ new wiki pages)
- Monthly maintenance trigger
- Before an important query where wiki trustworthiness matters

## Two phases

### Phase 1 — Mechanical (script)

Run the checker:

```bash
python3 agent/skills/lint/agent/scripts/lint-wiki.py
```

Output is a markdown report with:

1. **Stats** — total pages, links, orphans count
2. **🔴 Orphans** — pages not linked from INDEX or any other page
3. **🔴 Broken cross-links** — `[[topic]]` refs to non-existent pages
4. **🟡 Missing/incomplete frontmatter**
5. **🟡 Missing blockquote summary** — first content line isn't `> ...`
6. **🟡 Missing `## Sources`** section
7. **🟡 Not referenced in INDEX.md**
8. **🟡 Tiny pages** — <500 bytes
9. **🟡 Stale pages** — `updated` >90 days ago
10. **🟡 Duplicate topic fields**

Plus a separate check on `agent/memory/learnings/mistakes.md`:

11. **🟡 agent/memory/learnings/mistakes.md size** — if > 500 lines, surface "consider running `/review-learnings` to curate". This is the lifecycle separating active operational memory from `agent/memory/learnings/archive.md`.

Read the report. Don't truncate it.

### Phase 2 — Semantic (LLM pass)

For each page flagged "stale" + a random sample of 5 non-flagged pages:

1. `Read` the page
2. Look for:
   - **Time-sensitive claims** — "currently", "as of X", recent dates. Still likely true?
   - **Missing cross-links** — topic names mentioned as plain text that should be `[[linked]]`
   - **INDEX description mismatch** — does the page summary match what INDEX.md says?
   - **Broad contradictions** — does the page disagree with another page materially?

3. Add a `## ⚠️ Semantic issues` section with findings.

## Output format

```markdown
# Wiki Lint Report — YYYY-MM-DD

## Summary
- Total pages: N
- Orphans: N | Broken links: N | Stale: N
- Auto-fixed: N issues
- Needs review: N issues

## 🔴 Critical issues
<orphans, broken links>

## 🟡 Hygiene issues
<frontmatter, summary, sources, INDEX drift, tiny pages>

## ⚠️ Semantic issues (LLM pass)
<stale claims, missing links, contradictions>

## ✅ Auto-fixed
- [list]

## 🧑 Requires user review
1. [specific decision needed]
2. [specific decision needed]
```

## Auto-fix policy

**Safe to fix without asking:**

- Add missing `updated:` frontmatter using `git log -1 --format=%as -- <path>` for value
- Add missing `topic:` field — derive from filename
- Add missing `tags:` field with empty list `[]`
- Add missing INDEX entry for orphaned page (use first line of blockquote as description)
- Fix obvious typo in `[[link]]` where fuzzy match confidence ≥ 90% to existing page

**Do NOT auto-fix (flag only):**

- Delete orphan pages — may be intentional archives
- Rewrite stale claims — needs human judgment
- Resolve contradictions — needs human judgment
- Merge duplicate topics — needs canonical-form judgment
- Add missing blockquote summaries — writing them well requires understanding intent
- Add missing `## Sources` — we don't know what sources retroactively were

## Procedure

1. Run `python3 agent/skills/lint/agent/scripts/lint-wiki.py` — capture full output
2. Parse the report. Count issues per category.
3. Apply auto-fixes from "Safe" list. Use `Edit` for each. Track changes.
4. Phase 2 semantic pass on stale + 5 random sample
5. Compose final report with all sections
6. Return to user. Don't truncate.

## Anti-patterns

- Skipping Phase 2 — semantic issues are the hard-to-find ones
- Auto-fixing things outside the safe list
- Treating every stale page as a problem — some pages describe stable things
- Summarizing the report — user needs full findings
- Running lint and then forgetting to actually fix or log
