#!/usr/bin/env bash
# Task 12 acceptance checks over INSTALL.md
cd /home/coder/workspaces/worktrees/IronClaude/bs346-ledger
P=.dev/tasks/to-do/TASK-WF-spec-20261108-181649
I=.dev/brainstorms/346-ledger/INSTALL.md
for s in '~/.claude/commands/sc/spec-panel-ledger.md' '~/.claude/skills/sc-review-ledger/SKILL.md' '~/.claude/skills/sc-review-ledger/scripts/review_ledger.py' \
  '/sc:spec-panel-ledger --ledger .dev/orca-command-refactor/specs/orca-worker-contract-spec.review-ledger --revert-unclaimed' \
  'no `## Unattended mode` section' 'c8d80346a96c' 'heartbeat' 'ledger-steps' 'headline_raw'; do
  printf '%s: %s\n' "$s" "$(grep -cF -- "$s" "$I")"; done
missing=0
for f in $( { git status --porcelain --untracked-files=all | grep '^??' | cut -c4-; } | grep -vxF -f <(cut -c4- $P/artifacts/untracked-before.txt) | grep -v -e '^\.dev/tasks/' -e '^\.claude/'; echo tests/recommend/test_routing_refresh.py); do
  grep -qF "| \`$f\`" "$I" || { echo "MISSING $f"; missing=$((missing+1)); }; done
echo "files checked, missing=$missing"
