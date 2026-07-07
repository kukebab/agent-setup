#!/usr/bin/env bash
# commit-memory-reminder.sh — nudges memory updates after git commit (Claude Code).
#
# Fires as a PostToolUse hook after a Bash tool call. If the command was
# `git commit` AND succeeded, prints a reminder for the AI to:
#   1. Append a concise entry to agent/memory/daily/YYYY-MM-DD.md
#   2. If a non-obvious lesson emerged, append to agent/memory/learnings/mistakes.md
#
# Why: catches the "I committed but forgot to log it" gap. Daily logs and
# learnings drift if not nudged.
#
# Wire up in .claude/settings.json:
#   "hooks": {
#     "PostToolUse": [{
#       "matcher": "Bash",
#       "hooks": [{ "type": "command", "command": "bash agent/hooks/commit-memory-reminder.sh" }]
#     }]
#   }
#
# Exit 2 + stderr = non-blocking feedback to the AI.

set -e

input=$(cat)

# Extract command + result from the hook payload
result=$(printf '%s' "$input" | python3 -c "
import sys, json, re
try:
    d = json.load(sys.stdin)
    ti = d.get('tool_input', {}) or {}
    tr = d.get('tool_response', {}) or {}
    cmd = (ti.get('command') or '').strip()
    stdout = (tr.get('stdout') or '')
    interrupted = tr.get('interrupted', False)
    # Heuristic: git commit succeeded if stdout has a commit hash like '[main abc1234]'
    m = re.search(r'\[\w+\s+([0-9a-f]{7,40})\]', stdout)
    ok = bool(m) and not interrupted
    print(json.dumps({'cmd': cmd[:200], 'ok': ok, 'hash': m.group(1) if m else ''}))
except Exception:
    print(json.dumps({'cmd': '', 'ok': False, 'hash': ''}))
" 2>/dev/null)

# Parse result and emit reminder only if a git commit succeeded
parsed=$(printf '%s' "$result" | python3 -c "
import sys, json, re
d = json.load(sys.stdin)
cmd = d.get('cmd', '')
ok = d.get('ok', False)
hsh = d.get('hash', '')
# Match 'git commit' but not other git commands
is_commit = bool(re.match(r'^\s*git\s+commit\b', cmd)) and not '--amend' in cmd
print('1' if (is_commit and ok) else '0')
print(hsh)
" 2>/dev/null)

should_fire=$(echo "$parsed" | sed -n '1p')
commit_hash=$(echo "$parsed" | sed -n '2p')

if [ "$should_fire" = "1" ]; then
  TODAY=$(date +%Y-%m-%d)
  cat >&2 <<EOF
Memory-loop reminder (commit ${commit_hash}):

Per agent/rules/agent-quality.md memory-loop scaling, this commit needs:
- Append entry to agent/memory/daily/${TODAY}.md describing what changed (1-2 bullets minimum)
- If a non-obvious lesson emerged → append to agent/memory/learnings/mistakes.md MISTAKES section
- For structural commits (new file/module) → also update relevant agent's PROJECT_MAP.md

Shortcut to skip: if this is a trivial fix (<30 lines, single file, no surprises),
just one bullet in agent/memory/daily/ is enough. Skip the rest.
EOF
  exit 2
fi

exit 0
