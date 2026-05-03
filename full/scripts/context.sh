#!/usr/bin/env bash
# context.sh — generate session-start context summary.
#
# Collects STATE + INDEX + learnings MISTAKES + latest daily + recent commits
# into a single text block. Used by hooks/session-start.sh to inject into
# session at start, but works standalone too:
#
#   bash scripts/context.sh                    # all defaults
#   bash scripts/context.sh bluefin-coffee     # include client file (clients/bluefin-coffee.md)
#
# Output is plain text, not markdown — designed to be embedded in hook output.

set -e

REPO_ROOT="${REPO_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
cd "$REPO_ROOT" 2>/dev/null

CLIENT_NAMESPACE="$1"

echo "# Session Context"
echo "Generated: $(date '+%Y-%m-%d %H:%M')"
echo ""

# STATE
if [ -f memory/STATE.md ]; then
  echo "## STATE"
  head -200 memory/STATE.md
  echo ""
fi

# Top-level INDEX
if [ -f memory/INDEX.md ]; then
  echo "## INDEX"
  head -100 memory/INDEX.md
  echo ""
fi

# Wiki INDEX
if [ -f memory/wiki/INDEX.md ]; then
  echo "## WIKI INDEX"
  head -50 memory/wiki/INDEX.md
  echo ""
fi

# learnings MISTAKES (recent only)
if [ -f memory/learnings.md ]; then
  echo "## RECENT MISTAKES (don't repeat)"
  awk '/^## MISTAKES/,/^## WINS/' memory/learnings.md | head -100
  echo ""
fi

# Client file (if namespace given)
if [ -n "$CLIENT_NAMESPACE" ] && [ -f "memory/clients/$CLIENT_NAMESPACE.md" ]; then
  echo "## CLIENT: $CLIENT_NAMESPACE"
  head -100 "memory/clients/$CLIENT_NAMESPACE.md"
  echo ""
fi

# Latest daily entry
LATEST_DAILY=$(ls -t memory/daily/*.md 2>/dev/null | head -1)
if [ -n "$LATEST_DAILY" ]; then
  echo "## LATEST DAILY: $(basename "$LATEST_DAILY")"
  head -80 "$LATEST_DAILY"
  echo ""
fi

# Recent git activity
if git rev-parse --git-dir >/dev/null 2>&1; then
  echo "## RECENT COMMITS"
  git log --oneline --no-decorate -5 2>/dev/null
  echo ""
fi

echo "---"
