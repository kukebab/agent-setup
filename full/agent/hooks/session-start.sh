#!/usr/bin/env bash
# session-start.sh — auto-load project context at session start (Claude Code).
#
# Wraps agent/scripts/context.sh into a SessionStart hook output. Injects directly
# into session context so the AI doesn't have to manually read STATE.md /
# agent/memory/learnings/mistakes.md / latest daily on every session.
#
# Wire up in .claude/settings.json:
#   "hooks": {
#     "SessionStart": [{ "hooks": [
#       { "type": "command", "command": "bash agent/hooks/session-start.sh" }
#     ]}]
#   }
#
# Falls back gracefully if context.sh doesn't exist yet.

cd "$CLAUDE_PROJECT_DIR" 2>/dev/null || exit 0

CONTEXT_SCRIPT="$CLAUDE_PROJECT_DIR/agent/scripts/context.sh"

if [ ! -x "$CONTEXT_SCRIPT" ]; then
  # No context script wired up yet — silent exit is fine
  exit 0
fi

BACKUP_PATH="$CLAUDE_PROJECT_DIR/.claude/.last-session-context.txt"
mkdir -p "$(dirname "$BACKUP_PATH")" 2>/dev/null

FULL_CONTEXT="$(bash "$CONTEXT_SCRIPT" 2>/dev/null)"
echo "$FULL_CONTEXT" > "$BACKUP_PATH" 2>/dev/null

PREAMBLE="# SESSION CONTEXT (auto-loaded — DO NOT skip)
This is the live project state, recent activity, and known mistakes-to-avoid. Treat it as already-read context for the rest of the session — don't Read STATE.md / agent/memory/learnings/mistakes.md again unless something looks stale.

If this content appears truncated (cut off mid-section, no '---' footer at the end), the FULL version is at: $BACKUP_PATH — Read it immediately.
---
"

printf '%s\n%s' "$PREAMBLE" "$FULL_CONTEXT" | python3 -c "
import sys, json
print(json.dumps({
    'hookSpecificOutput': {
        'hookEventName': 'SessionStart',
        'additionalContext': sys.stdin.read()
    }
}))
"
