#!/usr/bin/env python3
"""
Wiki health check — mechanical lint for the Karpathy LLM wiki pattern.

Reports findings, makes no changes. The /lint skill reads this output
and applies safe auto-fixes plus a semantic pass.

Usage:
  python3 .claude/agent/skills/lint/agent/scripts/lint-wiki.py

Optional env:
  WIKI_DIR — override wiki directory (default: ./agent/memory/wiki)
"""
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

WIKI_DIR = Path(os.environ.get("WIKI_DIR") or Path.cwd() / "memory" / "wiki")
INDEX = WIKI_DIR / "INDEX.md"

if not WIKI_DIR.is_dir():
    print(f"ERROR: wiki dir not found: {WIKI_DIR}", file=sys.stderr)
    sys.exit(1)

LINK_RE = re.compile(r"\[\[([a-z0-9][a-z0-9-]*)\]\]")
UPDATED_RE = re.compile(r"^updated:\s*([^\s#]+)", re.MULTILINE)
TOPIC_RE = re.compile(r"^topic:\s*([^\s#]+)", re.MULTILINE)
TAGS_RE = re.compile(r"^tags:", re.MULTILINE)


def read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8")
    except Exception:
        return ""


def strip_fm(content: str) -> str:
    if content.startswith("---"):
        parts = content.split("---", 2)
        return parts[2] if len(parts) >= 3 else content
    return content


_INLINE_CODE_RE = re.compile(r"`[^`]*`")


def iter_prose_lines(content: str):
    """Yield (lineno, stripped_line) for lines NOT inside fenced code blocks.
    Inline `code` spans are also blanked so link-matches inside them are ignored."""
    in_fence = False
    for i, raw in enumerate(content.splitlines(), 1):
        stripped = raw.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        # Remove inline code spans
        cleaned = _INLINE_CODE_RE.sub("", raw)
        yield i, cleaned


def extract_links_from_prose(content: str) -> list[tuple[int, str]]:
    """Return list of (lineno, target) for [[links]] that appear in prose (not code)."""
    out = []
    for lineno, line in iter_prose_lines(content):
        for ref in LINK_RE.findall(line):
            out.append((lineno, ref))
    return out


def all_links_from_prose(content: str) -> set[str]:
    return {ref for _, ref in extract_links_from_prose(content)}


pages = sorted(p for p in WIKI_DIR.glob("*.md") if p.name != "INDEX.md")
page_names = {p.stem for p in pages}

index_content = read(INDEX)
index_links = all_links_from_prose(index_content)

# Build inbound link map: name -> set of pages linking to it (prose only)
inbound: dict[str, set[str]] = {n: set() for n in page_names}
for p in pages:
    for target in all_links_from_prose(read(p)):
        if target in inbound and target != p.stem:
            inbound[target].add(p.stem)

today = datetime.now().strftime("%Y-%m-%d")

print(f"# Wiki Lint Report — {today}")
print()
print(f"Wiki dir: `{WIKI_DIR}`")
print(f"Total pages: **{len(pages)}**")
print()

# --- 1. Orphans
print("## 🔴 Orphans (not in INDEX and no inbound links)")
orphans = []
for p in pages:
    name = p.stem
    if name not in index_links and not inbound[name]:
        m = UPDATED_RE.search(read(p))
        orphans.append((name, m.group(1) if m else "unknown"))
if not orphans:
    print("_None_")
else:
    for name, updated in orphans:
        print(f"- `agent/memory/wiki/{name}.md` (updated: {updated})")
print()

# --- 2. Broken cross-links (skip code fences and inline code)
print("## 🔴 Broken [[cross-links]]")
broken: list[tuple[str, int, str]] = []
for p in list(pages) + [INDEX]:
    content = read(p)
    for lineno, ref in extract_links_from_prose(content):
        if ref not in page_names:
            broken.append((p.name, lineno, ref))
if not broken:
    print("_None_")
else:
    for filename, lineno, ref in broken:
        print(f"- `agent/memory/wiki/{filename}` line {lineno} → `[[{ref}]]`")
print()

# --- 3. Missing/incomplete frontmatter
print("## 🟡 Missing or incomplete frontmatter")
fm_issues: list[tuple[str, str]] = []
for p in pages:
    content = read(p)
    if not content.startswith("---"):
        fm_issues.append((p.stem, "no frontmatter block"))
        continue
    head = content[:600]
    missing = []
    if not TOPIC_RE.search(head):
        missing.append("topic")
    if not UPDATED_RE.search(head):
        missing.append("updated")
    if not TAGS_RE.search(head):
        missing.append("tags")
    if missing:
        fm_issues.append((p.stem, "missing: " + ", ".join(missing)))
if not fm_issues:
    print("_None_")
else:
    for name, issue in fm_issues:
        print(f"- `agent/memory/wiki/{name}.md` — {issue}")
print()

# --- 4. Missing blockquote summary
print("## 🟡 Missing blockquote summary")
no_summary: list[tuple[str, str]] = []
for p in pages:
    body = strip_fm(read(p)).strip()
    for line in body.splitlines():
        if line.strip():
            if not line.strip().startswith(">"):
                no_summary.append((p.stem, line.strip()[:60]))
            break
if not no_summary:
    print("_None_")
else:
    for name, first in no_summary:
        print(f"- `agent/memory/wiki/{name}.md` — starts with: `{first}...`")
print()

# --- 5. Missing ## Sources
print("## 🟡 Missing `## Sources` section")
no_sources: list[str] = []
for p in pages:
    content = read(p).lower()
    if "## sources" not in content:
        no_sources.append(p.stem)
if not no_sources:
    print("_None_")
else:
    for name in no_sources:
        print(f"- `agent/memory/wiki/{name}.md`")
print()

# --- 6. Not referenced in INDEX
print("## 🟡 Not referenced in INDEX.md")
missing_index = sorted(p.stem for p in pages if p.stem not in index_links)
if not missing_index:
    print("_None_")
else:
    for name in missing_index:
        print(f"- `agent/memory/wiki/{name}.md`")
print()

# --- 7. Tiny pages
print("## 🟡 Tiny pages (< 500 bytes)")
tiny = [(p.stem, p.stat().st_size) for p in pages if p.stat().st_size < 500]
if not tiny:
    print("_None_")
else:
    for name, size in tiny:
        print(f"- `agent/memory/wiki/{name}.md` ({size} bytes)")
print()

# --- 8. Stale
cutoff_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
print(f"## 🟡 Stale (updated before {cutoff_date})")
stale: list[tuple[str, str]] = []
for p in pages:
    m = UPDATED_RE.search(read(p))
    if m:
        val = m.group(1).strip().strip('"').strip("'")
        if len(val) >= 10 and val[:10] < cutoff_date:
            stale.append((p.stem, val))
if not stale:
    print("_None_")
else:
    for name, updated in stale:
        print(f"- `agent/memory/wiki/{name}.md` (updated: {updated})")
print()

# --- 9. Duplicate topic fields
print("## 🟡 Duplicate `topic:` fields")
topics: dict[str, list[str]] = {}
for p in pages:
    m = TOPIC_RE.search(read(p))
    if m:
        topics.setdefault(m.group(1).strip(), []).append(p.stem)
dupes = [(t, f) for t, f in topics.items() if len(f) > 1]
if not dupes:
    print("_None_")
else:
    for topic, files in dupes:
        print(f"- topic `{topic}` used by: {', '.join(files)}")
print()

# --- Stats
total_links = sum(len(extract_links_from_prose(read(p))) for p in pages)
print("## 🟢 Stats")
print(f"- Total pages: {len(pages)}")
print(f"- Total outbound `[[links]]`: {total_links}")
if pages:
    print(f"- Avg links per page: {total_links / len(pages):.1f}")
print(f"- Pages in INDEX: {len(index_links & page_names)} / {len(pages)}")
print(f"- Orphans: {len(orphans)}")
print(f"- Broken links: {len(broken)}")
print(f"- Frontmatter issues: {len(fm_issues)}")
print(f"- Missing summary: {len(no_summary)}")
print(f"- Missing sources: {len(no_sources)}")
print(f"- Not in INDEX: {len(missing_index)}")
print(f"- Tiny pages: {len(tiny)}")
print(f"- Stale pages: {len(stale)}")
print(f"- Duplicate topics: {len(dupes)}")
print()
print("---")
print("Lint complete.")
