#!/usr/bin/env bash
# install.sh — wire up agent-os into the current project.
#
# Detects which AI tool is in use (Claude Code, Codex, Cursor, Aider, Windsurf)
# and copies the matching adapter into place. Sets up git hooks for staleness
# checking. Does NOT overwrite existing files without confirmation.
#
# Run from the project root where you want to install agent-os:
#   bash /path/to/agent-os-starter/full/scripts/install.sh
#
# Or copy this entire repo and run from inside `full/`:
#   bash scripts/install.sh

set -e

# Resolve paths relative to this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"  # full/ directory
TARGET_ROOT="${PWD}"

if [ "$SOURCE_ROOT" = "$TARGET_ROOT" ]; then
  echo "Run install.sh from your project root, not from inside the starter."
  echo "Example: cd /path/to/your-project && bash $SCRIPT_DIR/install.sh"
  exit 1
fi

echo "Installing agent-os into: $TARGET_ROOT"
echo ""

# ── Detect tool ────────────────────────────────────────────────
detected_tools=()
[ -d "$TARGET_ROOT/.claude" ] && detected_tools+=("claude-code")
[ -d "$TARGET_ROOT/.cursor" ] && detected_tools+=("cursor")
[ -d "$TARGET_ROOT/.codex" ] && detected_tools+=("codex")
[ -f "$TARGET_ROOT/.aider.conf.yml" ] && detected_tools+=("aider")
[ -f "$TARGET_ROOT/.windsurfrules" ] && detected_tools+=("windsurf")

if [ ${#detected_tools[@]} -eq 0 ]; then
  echo "No AI tool config detected. Choose a tool to install for:"
  echo "  1) Claude Code      → CLAUDE.md + .claude/settings.json"
  echo "  2) Codex / OpenCode → AGENTS.md only"
  echo "  3) Cursor           → .cursor/rules/main.mdc"
  echo "  4) Aider            → CONVENTIONS.md"
  echo "  5) Windsurf         → .windsurfrules"
  read -r -p "Choose [1-5]: " choice
  case "$choice" in
    1) detected_tools=("claude-code") ;;
    2) detected_tools=("codex") ;;
    3) detected_tools=("cursor") ;;
    4) detected_tools=("aider") ;;
    5) detected_tools=("windsurf") ;;
    *) echo "Invalid choice. Exiting."; exit 1 ;;
  esac
fi

echo "Tool(s) to install for: ${detected_tools[*]}"
echo ""

# ── Copy core files (memory + agent-os) ────────────────────────
copy_with_confirm() {
  local src="$1"
  local dst="$2"
  if [ -e "$dst" ]; then
    read -r -p "  $dst exists. Overwrite? [y/N] " yn
    case "$yn" in [Yy]*) ;; *) echo "  Skipped: $dst"; return 0 ;; esac
  fi
  mkdir -p "$(dirname "$dst")"
  cp -R "$src" "$dst"
  echo "  Copied: $dst"
}

echo "Copying memory/ + agent-os/ + scripts/..."
[ ! -d "$TARGET_ROOT/memory" ] && cp -R "$SOURCE_ROOT/memory" "$TARGET_ROOT/" && echo "  Copied: memory/"
[ ! -d "$TARGET_ROOT/agent-os" ] && cp -R "$SOURCE_ROOT/agent-os" "$TARGET_ROOT/" && echo "  Copied: agent-os/"
mkdir -p "$TARGET_ROOT/scripts"
copy_with_confirm "$SOURCE_ROOT/scripts/context.sh" "$TARGET_ROOT/scripts/context.sh"
copy_with_confirm "$SOURCE_ROOT/scripts/git-hooks" "$TARGET_ROOT/scripts/git-hooks"
chmod +x "$TARGET_ROOT/scripts/context.sh" 2>/dev/null
chmod +x "$TARGET_ROOT/scripts/git-hooks/"*.py 2>/dev/null
chmod +x "$TARGET_ROOT/scripts/git-hooks/pre-commit" 2>/dev/null

echo ""

# ── Wire up adapter for each detected tool ─────────────────────
for tool in "${detected_tools[@]}"; do
  echo "Wiring adapter: $tool"
  case "$tool" in
    claude-code)
      copy_with_confirm "$SOURCE_ROOT/CLAUDE.md" "$TARGET_ROOT/CLAUDE.md"
      copy_with_confirm "$SOURCE_ROOT/AGENTS.md" "$TARGET_ROOT/AGENTS.md"
      ;;
    codex)
      copy_with_confirm "$SOURCE_ROOT/AGENTS.md" "$TARGET_ROOT/AGENTS.md"
      ;;
    cursor)
      copy_with_confirm "$SOURCE_ROOT/AGENTS.md" "$TARGET_ROOT/AGENTS.md"
      copy_with_confirm "$SOURCE_ROOT/adapters/cursor/.cursor/rules/main.mdc" "$TARGET_ROOT/.cursor/rules/main.mdc"
      ;;
    aider)
      copy_with_confirm "$SOURCE_ROOT/AGENTS.md" "$TARGET_ROOT/AGENTS.md"
      copy_with_confirm "$SOURCE_ROOT/adapters/aider/CONVENTIONS.md" "$TARGET_ROOT/CONVENTIONS.md"
      ;;
    windsurf)
      copy_with_confirm "$SOURCE_ROOT/AGENTS.md" "$TARGET_ROOT/AGENTS.md"
      copy_with_confirm "$SOURCE_ROOT/adapters/windsurf/.windsurfrules" "$TARGET_ROOT/.windsurfrules"
      ;;
  esac
done

echo ""

# ── Wire up git hooks ─────────────────────────────────────────
if [ -d "$TARGET_ROOT/.git" ]; then
  echo "Wiring up git hooks (staleness check + PII block)..."
  current_hooks_path=$(git -C "$TARGET_ROOT" config --get core.hooksPath 2>/dev/null || echo "")
  if [ "$current_hooks_path" = "scripts/git-hooks" ]; then
    echo "  core.hooksPath already set to scripts/git-hooks ✓"
  elif [ -n "$current_hooks_path" ]; then
    echo "  WARN: core.hooksPath is set to '$current_hooks_path'. Skipping to avoid conflict."
    echo "  To enable agent-os hooks: git config core.hooksPath scripts/git-hooks"
  else
    git -C "$TARGET_ROOT" config core.hooksPath scripts/git-hooks
    echo "  Set core.hooksPath = scripts/git-hooks ✓"
  fi
else
  echo "Not a git repo — skipping git hooks setup."
fi

echo ""
echo "Install complete. Next steps:"
echo "  1. Open the project in your AI tool — it should auto-load AGENTS.md/CLAUDE.md"
echo "  2. Replace the Acme Notes example content with your real project context"
echo "  3. Optional: rename memory/USER.md.template → memory/USER.md and fill in"
echo "  4. Optional: rename agent-os/rules/identity.md.template → identity.md to define your AI's persona"
