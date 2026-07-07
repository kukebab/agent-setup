# Git Hooks

Pre-commit governance for agent-os projects. Enforces source-of-truth discipline at commit time, regardless of which AI tool you use.

## What's here

- **`pre-commit`** — runs on every `git commit`. Two phases:
  1. PII pattern check (configurable per-project, empty by default)
  2. Staleness check (hard-block on 3 patterns)
- **`check-staleness.py`** — implements the staleness gate, called by pre-commit

## Activation

Wire up once per checkout:

```bash
git config core.hooksPath agent/scripts/git-hooks
```

The `install.sh` script does this automatically.

## What gets hard-blocked

A commit is rejected when ANY of these is true:

| Trigger | Why |
|---|---|
| `agent/memory/STATE.md` body changed AND `Last updated:` is < today | Top-level state header drifted from body |
| `agent/memory/projects/*.md` current-state region changed AND `## Current State as of YYYY-MM-DD` is < today | Client snapshot date drifted from body |
| `agent/agents/*/PROJECT_MAP.md` body changed AND `Last updated:` is < today | Agent code map drifted |

## What gets warned (no block)

- `agent/agents/*/STATUS.md` body changed AND `Last updated:` < today (event log; historical sections OK)
- Missing headers on any of the above files

## Bypass

Two escape hatches:

```bash
STALENESS_SKIP=1 git commit ...   # only skips staleness; PII still enforced
git commit --no-verify             # skips ALL hooks (nuclear)
```

Use `STALENESS_SKIP=1` if you're intentionally preserving an old date (e.g. backfilling historical entries). Don't make it a habit.

## PII pattern (customize per project)

Open `pre-commit` and edit the `pii_pattern=''` line. Examples:

```bash
pii_pattern='^secrets/|^projects/.+/raw/.+\.pdf$|\.env\.'
```

Default is empty (no PII enforcement) — set it before relying on it.

## Why this matters

The single-source-of-truth map in `AGENTS.md` says: "when you touch one source, scan its mirrors for stale markers and bring them along in the same commit." This hook enforces that mechanically. Without it, the rule is instructional and gets violated under deadline pressure.

## Past incident reference

When a daily log says "shipped X" but `STATE.md` still shows old priorities, there's a discrepancy that future sessions trip over. The hook catches the most common drift pattern (date marker stale).
