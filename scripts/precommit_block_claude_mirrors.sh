#!/usr/bin/env bash
set -euo pipefail

mapfile -t generated_paths < <(
  git diff --cached --name-only --diff-filter=ACMR -- \
    '.claude/skills' \
    '.claude/agents' \
    '.claude/commands' \
    '.claude/hooks' \
    '.claude/templates'
)

if [ "${#generated_paths[@]}" -eq 0 ]; then
  exit 0
fi

printf '❌ Generated .claude mirrors must not be committed.\n'
printf '   Edit src/superclaude/ first, run make sync-dev for local mirrors, and stage only src/.\n\n'
printf 'Staged generated mirror paths:\n'
printf '  - %s\n' "${generated_paths[@]}"
printf '\nAllowed exception: .claude/settings.json only.\n'
exit 1
