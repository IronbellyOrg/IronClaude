#!/bin/sh
# SessionStart (matcher "startup") hook: give each checkout a codegraph index on its
# first session by starting ONE detached `codegraph init --yes <top>` when
# <top>/.codegraph/codegraph.db does not exist.
#
# POSIX sh. Always exits 0, prints nothing on stdout and never runs codegraph in the
# foreground. It never calls `status`, `index` or `sync`: each can destroy a
# concurrent init, while two racing inits are harmless and the MCP server heals an
# interrupted one. Opt out with SUPERCLAUDE_CODEGRAPH_AUTOINIT=0 (this hook only).

[ "${SUPERCLAUDE_CODEGRAPH_AUTOINIT:-}" = "0" ] && exit 0
[ -n "${HOME:-}" ] || exit 0

# The binary the installer registered (pointer file), else whatever is on PATH.
cg=$(cat "$HOME/.codegraph/.superclaude-bin" 2>/dev/null)
if [ ! -f "$cg" ] || [ ! -x "$cg" ]; then
    cg=$(command -v codegraph 2>/dev/null)
fi
{ [ -n "$cg" ] && [ -f "$cg" ] && [ -x "$cg" ]; } || exit 0

top=$(git -C "${CLAUDE_PROJECT_DIR:-$PWD}" rev-parse --show-toplevel 2>/dev/null) || exit 0
[ -n "$top" ] && [ "$top" != "$HOME" ] && [ "$top" != "/" ] || exit 0

# Any state of the database (complete, building, truncated, built by anyone) counts.
[ -e "$top/.codegraph/codegraph.db" ] && exit 0

log="${XDG_STATE_HOME:-$HOME/.local/state}/superclaude/codegraph-init.log"
mkdir -p "${log%/*}" 2>/dev/null || exit 0

# Every descriptor is redirected so Claude Code does not wait for the child.
nohup "$cg" init --yes "$top" </dev/null >>"$log" 2>&1 &
exit 0
