# Hooks

Runtime enforcement scripts. Hooks fire automatically at specific events — they're how the AI agent harness (Claude Code, Codex, etc.) injects discipline beyond what static files can do.

## Why hooks matter

Static rules tell the AI what to do. Hooks make sure it actually happens. Examples:

- **`session-start.sh`** — automatically loads `STATE.md`, `learnings.md`, latest `daily/` into the session at start. The AI doesn't have to remember to read them; the harness injects them.
- **`commit-memory-reminder.sh`** — fires after `git commit`, nudges the AI to update `daily/` and `learnings.md`. Catches the "I committed but forgot to log" gap.

These complement rules in `agent-os/rules/` — rules are policy, hooks are enforcement.

## Tool support

Hook mechanism varies by tool:

| Tool | Hook system |
|---|---|
| **Claude Code** | `.claude/settings.json` `hooks` config — full support |
| **Codex** | Limited — pre/post task only |
| **Cursor / Aider** | No native hooks; equivalent via prompt prefixes |

For non-Claude-Code tools, hook content can often be inlined into the schema as instructions ("at session start, read X / Y / Z").

## What's bundled

- **`session-start.sh`** — loads project context at session start
- **`commit-memory-reminder.sh`** — nudges memory updates after `git commit`

## Wiring up (Claude Code)

In your project's `.claude/settings.json`:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          { "type": "command", "command": "bash agent-os/hooks/session-start.sh" }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "bash agent-os/hooks/commit-memory-reminder.sh" }
        ]
      }
    ]
  }
}
```

## Pre-commit (separate)

The pre-commit hook (`scripts/git-hooks/pre-commit` + `check-staleness.py`) is a **git hook**, not a Claude Code hook. It enforces staleness discipline at commit time regardless of which AI tool you use. Wire it once per checkout:

```bash
git config core.hooksPath scripts/git-hooks
```

See `scripts/git-hooks/README.md` for details.

## Adding your own hooks

When you find yourself repeating the same nudge to the AI every session — "remember to update daily/", "check the staleness" — that's a hook candidate.

Test:

- Is it deterministic (same trigger → same action)? → hook
- Is it judgment-based (depends on context)? → rule, not hook
