#!/usr/bin/env bash
# Logs every change of the user-level spec-panel sha256 and of WORKER-CONTRACT.md presence.
L=/home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/phase4/install-watch.log
last=""
while [ ! -f /tmp/impl/exp/watch.stop ]; do
  s=$(sha256sum ~/.claude/commands/sc/spec-panel.md 2>/dev/null | cut -c1-12)
  w=$([ -e ~/.claude/WORKER-CONTRACT.md ] && echo present || echo absent)
  cur="$s wc=$w"
  if [ "$cur" != "$last" ]; then echo "$(date -u +%FT%TZ) spec-panel sha256[:12]=$s WORKER-CONTRACT.md=$w" >> "$L"; last="$cur"; fi
  read -t 20 -u 9 9<> <(:) || true
done
