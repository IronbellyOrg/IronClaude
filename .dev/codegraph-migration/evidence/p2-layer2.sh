#!/usr/bin/env bash
set -euo pipefail
R=$(git rev-parse --show-toplevel)
EV="$R/.dev/codegraph-migration/evidence/P2-layer2.md"
REAL_HOME="$HOME"; REAL_SUM=$(jq -S '.mcpServers' "$REAL_HOME/.claude.json" | sha256sum | cut -d' ' -f1)   # only MCP servers: live sessions rewrite the rest of the file
S=$(mktemp -d /tmp/p2-codegraph-it.XXXXXXXX); chmod 700 "$S"
trap 'cd /; pkill -f "$S/home/.codegraph" || true; rm -rf "$S"' EXIT
mkdir -p "$S/bin"
for t in claude uv git jq node sha256sum; do p=$(command -v "$t") && ln -s "$p" "$S/bin/$t"; done
export UV_CACHE_DIR="$(uv cache dir)"                                     # keep uv's real cache; only HOME moves
export HOME="$S/home" CLAUDE_CONFIG_DIR="$S/home" CODEGRAPH_TELEMETRY=0 DO_NOT_TRACK=1 CODEGRAPH_NO_UPDATE_CHECK=1
export PATH="$S/bin:$HOME/.local/bin:/usr/bin:/bin"
mkdir -p "$HOME"; echo '{"mcpServers":{}}' > "$HOME/.claude.json"
if command -v codegraph >/dev/null; then echo "codegraph visible on PATH; download path would not run" >&2; exit 1; fi
PHASE='from superclaude.cli.install_mcp import install_codegraph_mcp as f; ok,msg=f(); print(msg); raise SystemExit(0 if ok else 1)'
{ echo "# P2 layer 2 evidence $(date -u +%FT%TZ)"; echo '```text'; } > "$EV"

# 1. install through IronClaude's phase (download + verify + register)
uv run --no-sync --project "$R" python -c "$PHASE" | tee -a "$EV"
test "$("$HOME/.local/bin/codegraph" --version)" = 1.6.2
CG=$(readlink -f "$HOME/.local/bin/codegraph"); echo "launcher realpath: $CG" | tee -a "$EV"
jq -e --arg c "$CG" '.mcpServers.codegraph | .command == $c and .args == ["serve","--mcp"]' "$HOME/.claude.json" | tee -a "$EV"
MT=$(uv run --no-sync --project "$R" python -c 'from superclaude.cli.install_codegraph import MCP_TOOLS; print(MCP_TOOLS)')
jq -e --arg t "$MT" '.mcpServers.codegraph.env.CODEGRAPH_MCP_TOOLS == $t' "$HOME/.claude.json" | tee -a "$EV"   # X-1: tool list registered
jq '.mcpServers.codegraph' "$HOME/.claude.json" | tee -a "$EV"
diff <(jq -S 'del(.command)' "$R/.dev/codegraph-migration/evidence/P2-add-json-shape.json") <(jq -S '.mcpServers.codegraph | del(.command)' "$HOME/.claude.json")   # same stored shape as the T2 probe
# 2. idempotency: a second run with a dead proxy makes no download and no registry change
cp "$HOME/.claude.json" "$S/before.json"; ls "$HOME/.codegraph/versions" > "$S/versions.before"
https_proxy=http://127.0.0.1:9 HTTPS_PROXY=http://127.0.0.1:9 uv run --no-sync --project "$R" python -c "$PHASE" | tee -a "$EV"
cmp "$S/before.json" "$HOME/.claude.json"
ls "$HOME/.codegraph/versions" | cmp - "$S/versions.before"
# 3. offline reuse (the Coder path): a baked-style copy on PATH, no ~/.local/bin link, dead proxy
mkdir -p "$S/baked"; ln -s "$CG" "$S/baked/codegraph"; rm "$HOME/.local/bin/codegraph"
PATH="$S/baked:$PATH" https_proxy=http://127.0.0.1:9 HTTPS_PROXY=http://127.0.0.1:9 uv run --no-sync --project "$R" python -c "$PHASE" | tee -a "$EV"
jq -e --arg c "$CG" '.mcpServers.codegraph.command == $c' "$HOME/.claude.json"
ls "$HOME/.codegraph/versions" | cmp - "$S/versions.before"
ln -s "$CG" "$HOME/.local/bin/codegraph"
# 4. real index + query on an isolated copy of this worktree (never index the real worktree from the sandbox)
git clone -q --no-hardlinks "$R" "$S/project"; cd "$S/project"
codegraph init --yes | tail -3 | tee -a "$EV"
codegraph status > "$S/status.txt"; cat "$S/status.txt" >> "$EV"
grep 'Index is up to date' "$S/status.txt" >/dev/null
if grep 'never finished' "$S/status.txt" >/dev/null; then echo "index truncated" >&2; exit 1; fi
codegraph query install_codegraph_mcp > "$S/q.txt"; cat "$S/q.txt" >> "$EV"; grep 'src/superclaude/cli/install_mcp.py' "$S/q.txt" >/dev/null
codegraph callers install_codegraph_mcp > "$S/c.txt"; cat "$S/c.txt" >> "$EV"; grep 'src/superclaude/cli/main.py' "$S/c.txt" >/dev/null
# 5. the registered MCP entry starts and answers
claude mcp get codegraph > "$S/get.txt"; cat "$S/get.txt" >> "$EV"; grep -i 'connected' "$S/get.txt" >/dev/null
if grep -iE 'disconnected|not connected|failed' "$S/get.txt" >/dev/null; then echo "MCP server not connected" >&2; exit 1; fi
# 5b. the registered tool list: exactly the MCP_TOOLS tools are listed, explore is absent and a call to it fails (X-1, X-25)
CODEGRAPH_MCP_TOOLS="$MT" node "$R/.dev/codegraph-migration/evidence/p2-mcp-tools.mjs" "$CG" "$S/project" "$S/tools.json"
jq '{names: (.tools | map(.name)), tools_bytes, instructions_bytes, explore_call_error}' "$S/tools.json" | tee -a "$EV"
jq -e --arg t "$MT" '((.tools | map(.name) | sort) == ($t | split(",") | map("codegraph_" + .) | sort)) and .explore_call_error == true' "$S/tools.json"
cd "$R"
# 6. retire after codegraph is ready: seed the current-pin Serena entry and a kind-B codebase-memory entry, run the full install in the sandbox
SER='{"type":"stdio","command":"uvx","args":["--from","serena-agent==1.7.0","serena","start-mcp-server","--context","claude-code","--project-from-cwd","--enable-web-dashboard","false","--enable-gui-log-window","false"],"env":{}}'   # exact live shape, incl. "env":{}
CBM="{\"type\":\"stdio\",\"command\":\"$HOME/.local/bin/codebase-memory-mcp\",\"args\":[]}"
printf '#!/bin/sh\necho "codebase-memory-mcp 0.12.1"\n' > "$HOME/.local/bin/codebase-memory-mcp"; chmod 755 "$HOME/.local/bin/codebase-memory-mcp"   # kind-B binary present
jq --argjson s "$SER" --argjson c "$CBM" '.mcpServers.serena=$s | .mcpServers["codebase-memory-mcp"]=$c' "$HOME/.claude.json" > "$S/seed.json"
cp "$S/seed.json" "$HOME/.claude.json"
jq -e '.mcpServers | has("serena") and has("codebase-memory-mcp")' "$HOME/.claude.json"   # seeding really happened
if ! uv run --no-sync --project "$R" superclaude install > "$S/install.txt" 2>&1; then cat "$S/install.txt" >> "$EV"; echo "install failed" >&2; exit 1; fi
cat "$S/install.txt" >> "$EV"
jq -e '(.mcpServers | has("serena") or has("codebase-memory-mcp")) | not' "$HOME/.claude.json"
jq -e '.mcpServers | has("codegraph")' "$HOME/.claude.json"
test -x "$HOME/.local/bin/codebase-memory-mcp"                             # kind-B binary itself is left in place
grep 'uninstall -y' "$S/install.txt" >/dev/null                             # and its upstream uninstall command is printed
grep -F 'serena-agent==1.7.0' "$S/install.txt" >/dev/null                     # the removed Serena argv is printed (§2.12)
# 6b. the real installed hook, real binary, on a fresh clone (outside Claude Code)
git clone -q --no-hardlinks "$R" "$S/project2"
out=$(CLAUDE_PROJECT_DIR="$S/project2" sh "$HOME/.claude/hooks/codegraph-session-start.sh"); test -z "$out"
n=0; until pgrep -f "codegraph\.js init --yes $S/project2" >/dev/null; do n=$((n+1)); test $n -le 20; sleep 0.1; done   # started within 2 s
n=0; while pgrep -f "codegraph\.js init --yes $S/project2" >/dev/null; do n=$((n+1)); test $n -le 300; sleep 1; done   # finished within 300 s
(cd "$S/project2" && codegraph status) > "$S/status2.txt"; grep 'Index is up to date' "$S/status2.txt" >/dev/null
if grep 'never finished' "$S/status2.txt" >/dev/null; then echo "hook init truncated" >&2; exit 1; fi
# 7. same seeds with codegraph unavailable: install exits 1 at the codegraph stage, Serena and the kind-B entry are kept
H2="$S/home2"; mkdir -p "$H2/.local/bin"; cp "$HOME/.local/bin/codebase-memory-mcp" "$H2/.local/bin/"
CBM2="{\"type\":\"stdio\",\"command\":\"$H2/.local/bin/codebase-memory-mcp\",\"args\":[]}"
jq -n --argjson s "$SER" --argjson c "$CBM2" '{mcpServers:{serena:$s, "codebase-memory-mcp":$c}}' > "$H2/.claude.json"
if HOME="$H2" CLAUDE_CONFIG_DIR="$H2" PATH="$S/bin:/usr/bin:/bin" https_proxy=http://127.0.0.1:9 HTTPS_PROXY=http://127.0.0.1:9 uv run --no-sync --project "$R" superclaude install > "$S/install2.txt" 2>&1; then echo "install passed without codegraph" >&2; exit 1; fi
cat "$S/install2.txt" >> "$EV"
grep -i 'codegraph' "$S/install2.txt" | grep -i 'download' >/dev/null        # it failed at the codegraph download stage
jq -e '.mcpServers | has("serena") and has("codebase-memory-mcp")' "$H2/.claude.json"
echo '```' >> "$EV"
# 8. the real HOME was not touched
test "$(jq -S '.mcpServers' "$REAL_HOME/.claude.json" | sha256sum | cut -d' ' -f1)" = "$REAL_SUM"
echo "LAYER2_OK" | tee -a "$EV"
