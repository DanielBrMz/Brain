#!/usr/bin/env bash
# Brain + Claude Code setup for a new machine
# Usage: ./setup.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CLAUDE_DIR="$HOME/.claude"
CONFIG_SRC="$SCRIPT_DIR/claude-config"

echo "=== Brain + Claude Code Setup ==="
echo "Source: $CONFIG_SRC"
echo "Target: $CLAUDE_DIR"
echo ""

# 1. Create ~/.claude if needed
mkdir -p "$CLAUDE_DIR/agents" "$CLAUDE_DIR/rules" "$CLAUDE_DIR/hooks"

# 2. Copy agents
echo "[1/5] Installing 28 agents..."
cp "$CONFIG_SRC"/agents/*.md "$CLAUDE_DIR/agents/"

# 3. Copy rules (preserve directory structure)
echo "[2/5] Installing rules..."
cp -r "$CONFIG_SRC"/rules/* "$CLAUDE_DIR/rules/"

# 4. Copy hooks
echo "[3/5] Installing hooks..."
cp "$CONFIG_SRC"/hooks/hooks.json "$CLAUDE_DIR/hooks/hooks.json"

# 5. Copy AGENTS.md
echo "[4/5] Installing AGENTS.md..."
cp "$CONFIG_SRC/AGENTS.md" "$CLAUDE_DIR/AGENTS.md"

# 6. Settings
if [ -f "$CLAUDE_DIR/settings.json" ]; then
  echo "[5/5] settings.json already exists — skipping (see claude-config/settings.json.example)"
else
  echo "[5/5] Creating settings.json from template..."
  cp "$CONFIG_SRC/settings.json.example" "$CLAUDE_DIR/settings.json"
fi

echo ""
echo "=== Done ==="
echo ""
echo "Next steps:"
echo "  1. Open Obsidian and point it at: $SCRIPT_DIR"
echo "  2. Install Claude Code plugins:"
echo "     claude plugin install everything-claude-code@everything-claude-code"
echo "     claude plugin install obsidian@obsidian-skills"
echo "  3. Create .mcp.json locally (not tracked) with your MCP server config"
echo "  4. Create .claude/settings.local.json locally for project-specific permissions"
echo "  5. Place project repos under ~/Documents/Projects/ as referenced in CLAUDE.md"
echo ""
echo "Sensitive files to create manually (NOT in git):"
echo "  - .mcp.json (Jira/Atlassian tokens)"
echo "  - .claude/settings.local.json (SSH permissions)"
echo "  - ~/.claude/projects/*/memory/ (auto-created by Claude Code)"
