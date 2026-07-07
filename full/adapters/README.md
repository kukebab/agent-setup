# Adapters

Tool-specific shims that point your AI agent (Cursor, Aider, Windsurf, etc.) at the canonical schema in `AGENTS.md` / `CLAUDE.md`.

## How adapters work

The schema (`AGENTS.md`) is universal — any agent that can read markdown can use it. But each tool has its OWN entrypoint file:

| Tool | Entry file | Mechanism |
|---|---|---|
| **Claude Code** | `CLAUDE.md` | auto-loaded at root |
| **Codex / OpenCode** | `AGENTS.md` | auto-loaded at root |
| **Cursor** | `.cursor/rules/*.mdc` | rule files with frontmatter |
| **Aider** | `CONVENTIONS.md` | auto-loaded if `--read CONVENTIONS.md` set |
| **Windsurf** | `.windsurfrules` | auto-loaded at root |
| **Cline** | `.clinerules` | auto-loaded at root |

Each adapter here is a thin shim that says "read AGENTS.md/CLAUDE.md for the schema". They don't duplicate content.

## Bundled adapters

- `cursor/.cursor/rules/main.mdc` — Cursor rule with `alwaysApply: true`
- `aider/CONVENTIONS.md` — Aider conventions doc
- `windsurf/.windsurfrules` — Windsurf rules

## Wiring up

Run `bash install.sh` (from the `full/` directory) — it detects your tool and copies the right adapter into place.

Or manually: copy the relevant adapter file into your project's expected location.

## Adding a new tool adapter

1. Find the tool's auto-load mechanism (their docs)
2. Create a file in `adapters/<tool>/` with the right path/format
3. Make it short — point at AGENTS.md, don't duplicate
4. Update this README's table

Pattern: maximum 30-40 lines per adapter. The whole point is "read the canonical schema."
