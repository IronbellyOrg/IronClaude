#!/usr/bin/env bash
# Task 18 sandbox checks. Never touches the real HOME: every call sets HOME and CLAUDE_CONFIG_DIR to a temp dir.
set -u
cd /home/coder/workspaces/worktrees/IronClaude/feat-codememory-codegraph-init
PKG=$(pwd)/.dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100
F=$PKG/artifacts/final
OUT=$F/sandbox.txt
: > "$OUT"
say() { printf '%s\n' "$*" | tee -a "$OUT"; }

FILTER=(-e '/\.claude/skills/ccsession-tag/install\.sh:' -e '/\.claude/commands/sc/load\.md:[0-9]+:.*\.serena/memories' -e '/\.claude/skills/sc-cleanup-audit-protocol/SKILL\.md:[0-9]+:.*\.serena/' -e '/\.claude/settings\.json\.bak\.[0-9]{8}T[0-9]{6}Z:')
# PATH without any Orca directory (the real orca CLI would talk to the live Orca app)
SAFEPATH=$(printf '%s' "$PATH" | tr ':' '\n' | grep -v -i orca | paste -sd:)
UVC=$(uv cache dir)

T=$(mktemp -d /tmp/p1-sbx.XXXXXX)
mkdir -p "$T/bin" "$T/fresh" "$T/old" "$T/ci"
cat > "$T/bin/claude" <<'EOF'
#!/usr/bin/env bash
echo "$*" >> "$HOME/claude-calls.log"
case "$1" in
  --version) echo "2.0.0 (stub)"; exit 0 ;;
  plugin) exit 0 ;;
esac
if [ "${1:-} ${2:-}" = "mcp remove" ] && [ "${4:-}" = "--scope" ] && [ "${5:-}" = "user" ]; then
  f="${CLAUDE_CONFIG_DIR:-$HOME}/.claude.json"
  tmp=$(mktemp)
  jq --arg n "$3" 'del(.mcpServers[$n])' "$f" > "$tmp" && mv "$tmp" "$f"
  exit 0
fi
exit 1
EOF
chmod +x "$T/bin/claude"
say "sandbox root: $T"

# ---------------- fresh ----------------
say "== FRESH: superclaude install in an empty HOME =="
env HOME="$T/fresh" UV_CACHE_DIR="$UVC" PATH="$T/bin:$SAFEPATH" CLAUDE_CONFIG_DIR="$T/fresh" uv run --no-sync superclaude install > "$F/sandbox-fresh-install.txt" 2>&1
say "fresh install rc=$?"
tail -4 "$F/sandbox-fresh-install.txt" | tee -a "$OUT"
hits=$(rg -n -i --hidden --no-ignore -g '!claude-calls.log' 'serena|codebase-memory|codebase_memory' "$T/fresh" | rg -v "${FILTER[@]}")
if [ -z "$hits" ]; then say "fresh residual search: EMPTY (pass)"; else say "fresh residual search: HITS"; printf '%s\n' "$hits" | cut -c1-200 | head -20 | tee -a "$OUT"; fi
if grep -q 'mcp add' "$T/fresh/claude-calls.log" 2>/dev/null; then say "fresh claude call log: HAS mcp add (FAIL)"; else say "fresh claude call log: no mcp add (pass)"; fi
say "fresh claude calls: $(wc -l < "$T/fresh/claude-calls.log" 2>/dev/null || echo 0)"

# ---------------- existing ----------------
say "== EXISTING: seeded HOME, then ./update.sh =="
mkdir -p "$T/old/.claude/commands/sc" "$T/old/.local/bin"
python3 - "$T/old" <<'EOF'
import json, sys
home = sys.argv[1]
row_a = ["--from", "git+https://github.com/oraios/serena", "serena", "start-mcp-server", "--context", "ide-assistant", "--enable-web-dashboard", "false", "--enable-gui-log-window", "false"]
cfg = {
    "mcpServers": {
        "codebase-memory-mcp": {"type": "stdio", "command": "/usr/local/bin/codebase-memory-mcp", "args": []},
        "serena": {"type": "stdio", "command": "uvx", "args": row_a, "env": {}},
        "tavily": {"type": "stdio", "command": "npx", "args": ["-y", "tavily-mcp@0.2.22"], "env": {}},
    },
    "projects": {"/x": {"mcpServers": {"serena": {"type": "stdio", "command": "uvx", "args": row_a, "env": {}}}}},
}
json.dump(cfg, open(f"{home}/.claude.json", "w"), indent=2)
settings = {"hooks": {"PreToolUse": [{
    "matcher": "Edit|Write|mcp__serena__replace_content|mcp__serena__replace_symbol_body|mcp__serena__insert_after_symbol|mcp__serena__insert_before_symbol",
    "hooks": [{"type": "command", "command": "~/.claude/hooks/freshness-pre-edit.sh", "timeout": 5}]}]}}
json.dump(settings, open(f"{home}/.claude/settings.json", "w"), indent=2)
open(f"{home}/.claude/CLAUDE.md", "w").write("# stale core file\n| serena | Symbol navigation, project memory | --serena |\n")
open(f"{home}/.claude/commands/sc/reflect.md", "w").write("# stale reflect\nUses mcp__serena__find_symbol for symbols.\n")
EOF
say "seeded: $(jq -c '.mcpServers|keys' "$T/old/.claude.json")"
env HOME="$T/old" CLAUDE_CONFIG_DIR="$T/old" PIPX_HOME="$T/pipx" PIPX_BIN_DIR="$T/pbin" UV_CACHE_DIR="$UVC" PATH="$T/pbin:$T/bin:$SAFEPATH" ./update.sh > "$F/sandbox-update.txt" 2>&1
UPD_RC=$?
say "update.sh rc=$UPD_RC"
tail -8 "$F/sandbox-update.txt" | cut -c1-200 | tee -a "$OUT"
echo "UPD_RC=$UPD_RC" > "$T/upd.rc"
say "keys after: $(jq -c '.mcpServers|keys' "$T/old/.claude.json")  (expect [\"tavily\"])"
say "project-scope serena kept: $(jq '.projects["/x"].mcpServers|has("serena")' "$T/old/.claude.json")  (expect true)"
if rg -n 'mcp__serena' "$T/old/.claude/settings.json" > /dev/null; then say "settings.json still has mcp__serena (FAIL)"; else say "settings.json: no mcp__serena (pass)"; fi
hits=$(rg -n -i --hidden --no-ignore 'serena|codebase-memory' "$T/old/.claude" | rg -v "${FILTER[@]}")
if [ -z "$hits" ]; then say "existing residual search over ~/.claude: EMPTY (pass)"; else say "existing residual search: HITS"; printf '%s\n' "$hits" | cut -c1-200 | head -20 | tee -a "$OUT"; fi
ls "$T/old/.claude"/settings.json.bak.* > /dev/null 2>&1 && say "settings.json.bak.* backup exists (pass): $(ls "$T/old/.claude"/settings.json.bak.* | wc -l)" || say "NO settings.json.bak.* backup (FAIL)"
say "existing claude calls: $(cat "$T/old/claude-calls.log" 2>/dev/null | grep -c 'mcp remove') mcp remove; adds: $(grep -c 'mcp add' "$T/old/claude-calls.log" 2>/dev/null || echo 0)"

# ---------------- current pin kept ----------------
say "== PIN: current-pin serena entry is kept =="
jq '.mcpServers.serena = {"type":"stdio","command":"uvx","args":["--from","serena-agent==1.7.0","serena","start-mcp-server","--context","claude-code","--project-from-cwd","--enable-web-dashboard","false","--enable-gui-log-window","false"],"env":{}}' "$T/old/.claude.json" > "$T/old/tmp.json" && mv "$T/old/tmp.json" "$T/old/.claude.json"
env HOME="$T/old" CLAUDE_CONFIG_DIR="$T/old" UV_CACHE_DIR="$UVC" PATH="$T/bin:$SAFEPATH" uv run --no-sync superclaude install --force > "$F/sandbox-pin-install.txt" 2>&1
say "pin install rc=$?"
say "serena entry kept: $(jq '.mcpServers|has("serena")' "$T/old/.claude.json")  (expect true)"
grep -q 'Legacy Serena registration kept until codegraph is ready' "$F/sandbox-pin-install.txt" && say "output contains the Tier K line (pass)" || say "Tier K line MISSING (FAIL)"

# ---------------- no claude CLI ----------------
say "== ROBUSTNESS: no claude CLI on PATH =="
if env PATH=/usr/bin:/bin sh -c 'command -v claude' > /dev/null; then say "claude still on the restricted PATH (setup problem)"; fi
env HOME="$T/ci" CLAUDE_CONFIG_DIR="$T/ci" PATH=/usr/bin:/bin "$(pwd)/.venv/bin/superclaude" install > "$F/sandbox-noclaude-install.txt" 2>&1
RC1=$?
env HOME="$T/ci" CLAUDE_CONFIG_DIR="$T/ci" PATH=/usr/bin:/bin "$(pwd)/.venv/bin/superclaude" doctor --verbose > "$F/sandbox-noclaude-doctor.txt" 2>&1
RC2=$?
say "no-claude install rc=$RC1, doctor rc=$RC2 (expect 0 and 0)"

say "== cleanup =="
echo "$T" > /tmp/p1-sbx.root
git status --short -- . ':!.dev'
