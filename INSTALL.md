# Manual Install

For users who prefer not to use the AI-paste flow ([`INSTALL_PROMPT.md`](INSTALL_PROMPT.md)).

## Prerequisites

- A project (any tech stack — language, framework, scale all irrelevant to the pattern)
- An AI tool (Claude Code, Codex, Cursor, Aider, Windsurf — anything that reads markdown)
- Optional: git (Advanced Mode pre-commit hooks need it)

## Choose mode

**Simple Mode** — minimum viable. 12 files. Pure Karpathy wiki + minimal live state. 5-minute setup.

**Advanced Mode** — complete framework. ~50 files. Adds rules, agents, skills, hooks, governance. 15-minute setup.

If unsure → start Simple. Graduate later by copying `full/agent-os/` over your existing setup.

## Simple Mode install

```bash
git clone https://github.com/bruceorchestrator/agent-os-starter
cp -R agent-os-starter/starter/. /path/to/your-project/
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
git clone https://github.com/bruceorchestrator/agent-os-starter
cd /path/to/your-project/
bash /path/to/agent-os-starter/full/scripts/install.sh
```

The installer:

- Detects your AI tool
- Asks before overwriting any existing files (default = skip)
- Copies `memory/`, `agent-os/`, `adapters/`, `scripts/`
- Wires git hooks for the staleness check
- Prints next-step verification

After install:

1. **Verify:** `bash scripts/context.sh` — should print STATE + INDEX without errors
2. **Replace example data** with your project's reality:
   - `memory/STATE.md` — your priorities
   - `memory/clients/` — delete Bluefin/Tessera, add yours (or leave empty)
   - `memory/wiki/` — delete sync-engine/billing-flows/etc., add yours (or empty `INDEX.md`)
   - `memory/outputs/specs/` and `outputs/research/` — delete the Acme samples
   - `memory/daily/` — delete the Acme example day
   - `agent-os/agents/backend-dev/PROJECT_MAP.md` — replace with your stack/dirs
3. **Optional persona:** rename `agent-os/rules/identity.md.template` → `identity.md`, customize
4. **Optional personal context:** rename `memory/USER.md.template` → `USER.md`, fill in
5. **Open in your AI agent** — verify `AGENTS.md` is auto-loaded

## Customizing for your stack

The schema is stack-agnostic. Stack only appears in:

- `agent-os/agents/backend-dev/PROJECT_MAP.md` — has explicit `<!-- REPLACE WITH YOUR STACK -->` marker
- Optionally any rules you write yourself

Replace those with your stack. Everything else (rules, skills, hooks, schema) is universal.

## Tool-specific notes

| Tool | Auto-loaded | Extra files |
|---|---|---|
| Claude Code | `CLAUDE.md` | optional: `.claude/settings.json` for hooks (template in `agent-os/hooks/README.md`) |
| Codex / OpenCode | `AGENTS.md` | none |
| Cursor | `.cursor/rules/main.mdc` (manual or via `install.sh`) | references `AGENTS.md` |
| Aider | `CONVENTIONS.md` (manual or via `install.sh`) | also `aider --read AGENTS.md` |
| Windsurf | `.windsurfrules` (manual or via `install.sh`) | references `AGENTS.md` |

We ship both `AGENTS.md` and `CLAUDE.md` (identical content) at root because different tools auto-load different files. No conflict.

## Troubleshooting

**My AI doesn't see `AGENTS.md`**
Different tools auto-load different files. We ship both `AGENTS.md` and `CLAUDE.md` at root — most tools pick one. If your tool needs a tool-specific entry (`.cursor/rules/`, `CONVENTIONS.md`, `.windsurfrules`), see `full/adapters/` or run `install.sh`.

**`bash scripts/context.sh` fails**
Likely `memory/STATE.md` doesn't exist yet. Make sure you copied the full `memory/` directory, or that you renamed the file correctly.

**Pre-commit hook blocks my commit**
The staleness check fired. Two paths:
- (a) bump the `Last updated:` date in the file you edited (the right move 95% of the time)
- (b) `STALENESS_SKIP=1 git commit ...` if you're intentionally preserving an old date

**Multiple AI tools open in the same project**
Fine. They all read markdown; the schema is identical. Each tool picks its own auto-load file.

**Existing `memory/` directory at install time**
The installer asks: skip / merge (only new files) / backup-and-replace. Default is skip. Your existing notes are sacred.

## Uninstall

```bash
rm -rf memory/ agent-os/ AGENTS.md CLAUDE.md
# Plus tool-specific adapter files if you wired them
git config --unset core.hooksPath  # if you set it
```

The pattern is filesystem-only — no daemons, no installed binaries, no system integration to clean up.

## License

MIT.
