# Manual Install

For users who prefer not to use the AI-paste flow ([`INSTALL_PROMPT.md`](INSTALL_PROMPT.md)).

## Prerequisites

- A project (any tech stack — language, framework, scale all irrelevant to the pattern)
- An AI tool (Claude Code, Codex, Cursor, Aider, Windsurf — anything that reads markdown)
- Optional: git (Advanced Mode pre-commit hooks need it)

## Choose mode

**Simple Mode** — minimum viable. 18 files. Pure Karpathy wiki + minimal live state (single `learnings.md`). 5-minute setup.

**Advanced Mode** — complete framework. ~60 files. Adds rules, agents, skills, hooks, governance, a lifecycle-split `learnings/` directory, and the `/mine-learnings` trace→learnings loop. 15-minute setup.

If unsure → start Simple. Graduate later by copying `full/agent/` over your existing setup.

## Simple Mode install

```bash
git clone https://github.com/kukebab/agent-setup
cp -R agent-setup/starter/. /path/to/your-project/
```

Then edit:

1. `your-project/memory/STATE.md` — replace Acme Notes priorities with yours; bump `Last updated:` to today
2. `your-project/memory/learnings.md` — keep the format spec, clear the example MISTAKES/WINS/PATTERNS
3. `your-project/memory/wiki/` — replace Acme example pages with your topics, OR delete them and start with empty `INDEX.md` (populate via `/ingest` later)
4. `your-project/memory/daily/` — delete the example day, your AI will create today's entry on first session
5. Open the project in your AI agent — it auto-loads `AGENTS.md` (or `CLAUDE.md`)

That's it. 12 files, ~5 minutes.

## Advanced Mode install

```bash
git clone https://github.com/kukebab/agent-setup
cd /path/to/your-project/
bash /path/to/agent-setup/full/install.sh
```

The installer:

- Detects your AI tool
- Asks before overwriting any existing files (default = skip)
- Copies the whole `agent/` bundle (`memory/`, `rules/`, `skills/`, `hooks/`, `agents/`, `scripts/`) plus `adapters/`
- Drops thin `AGENTS.md`/`CLAUDE.md` stubs at your project root pointing at `agent/AGENTS.md`
- Wires git hooks for the staleness check
- Stamps `agent/VERSION.md` with the installed schema version
- Prints next-step verification

After install:

1. **Verify:** `bash agent/scripts/context.sh` — should print STATE + INDEX without errors
2. **Replace example data** with your project's reality:
   - `agent/memory/STATE.md` — your priorities
   - `agent/memory/learnings/` — empty the Acme example entries from `mistakes.md` / `patterns.md` / `decisions.md` / `constraints.md` / `archive.md` (keep the format/intro blocks). Leave `inbox/learnings-candidates.md` as the empty queue
   - `agent/memory/projects/` — delete Bluefin/Tessera, add yours (or leave empty)
   - `agent/memory/wiki/` — delete sync-engine/billing-flows/etc., add yours (or empty `INDEX.md`)
   - `agent/memory/outputs/specs/` and `outputs/research/` — delete the Acme samples
   - `agent/memory/daily/` — delete the Acme example day
   - `agent/agents/backend-dev/PROJECT_MAP.md` — replace with your stack/dirs
3. **Try the trace→learnings loop:** `python agent/scripts/mine_learnings.py --no-llm` mines your latest session transcript for candidate learnings (zero setup; review via `/mine-learnings`)
4. **Optional persona:** rename `agent/rules/identity.md.template` → `identity.md`, customize
5. **Optional personal context:** rename `agent/memory/USER.md.template` → `USER.md`, fill in
6. **Open in your AI agent** — verify `AGENTS.md` is auto-loaded

## Customizing for your stack

The schema is stack-agnostic. Stack only appears in:

- `agent/agents/backend-dev/PROJECT_MAP.md` — has explicit `<!-- REPLACE WITH YOUR STACK -->` marker
- Optionally any rules you write yourself

Replace those with your stack. Everything else (rules, skills, hooks, schema) is universal.

## Tool-specific notes

| Tool | Auto-loaded | Extra files |
|---|---|---|
| Claude Code | `CLAUDE.md` (stub, points at `agent/AGENTS.md`) | optional: `.claude/settings.json` for hooks (template in `agent/hooks/README.md`) |
| Codex / OpenCode | `AGENTS.md` (stub, points at `agent/AGENTS.md`) | none |
| Cursor | `.cursor/rules/main.mdc` (manual or via `install.sh`) | references `agent/AGENTS.md` |
| Aider | `CONVENTIONS.md` (manual or via `install.sh`) | also `aider --read AGENTS.md` |
| Windsurf | `.windsurfrules` (manual or via `install.sh`) | references `agent/AGENTS.md` |

We ship both `AGENTS.md` and `CLAUDE.md` (identical thin stubs) at root because different tools auto-load different files. No conflict — the real content lives once, in `agent/AGENTS.md`.

## Troubleshooting

**My AI doesn't see `AGENTS.md`**
Different tools auto-load different files. We ship both `AGENTS.md` and `CLAUDE.md` at root — most tools pick one. If your tool needs a tool-specific entry (`.cursor/rules/`, `CONVENTIONS.md`, `.windsurfrules`), see `full/adapters/` or run `install.sh`.

**`bash agent/scripts/context.sh` fails**
Likely `agent/memory/STATE.md` doesn't exist yet. Make sure you copied the full `agent/` directory, or that you renamed the file correctly.

**Pre-commit hook blocks my commit**
The staleness check fired. Two paths:
- (a) bump the `Last updated:` date in the file you edited (the right move 95% of the time)
- (b) `STALENESS_SKIP=1 git commit ...` if you're intentionally preserving an old date

**Multiple AI tools open in the same project**
Fine. They all read markdown; the schema is identical. Each tool picks its own auto-load file.

**Existing `agent/` directory at install time**
The installer asks: skip / merge (only new files) / backup-and-replace. Default is skip. Your existing notes are sacred.

**I have an older install and want the newer schema**
Don't re-run `install.sh` blindly — it won't overwrite your customized files, but it also won't
merge structural changes. Use [`UPDATE_PROMPT.md`](UPDATE_PROMPT.md) instead: paste it into your
AI agent, it reads `agent/VERSION.md`, diffs against `CHANGELOG.md`, and walks you through what
changed.

## Uninstall

```bash
rm -rf agent/ AGENTS.md CLAUDE.md
# Plus tool-specific adapter files if you wired them
git config --unset core.hooksPath  # if you set it
```

The pattern is filesystem-only — no daemons, no installed binaries, no system integration to clean up.

## License

MIT.
