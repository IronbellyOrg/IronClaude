#!/usr/bin/env bash
# MIG-001 / T08.04 — verify bare-review mirror matches src on staged changes.
#
# Pre-commit hook entry: `verify-bare-review-mirror-matches-src`. Fires when
# any path under src/superclaude/skills/sc-bare-review/ is staged. Diffs the
# source tree against the generated mirror at .claude/skills/sc-bare-review/
# and exits non-zero on drift, prompting `make sync-dev`.
#
# Scope rationale: the project-wide `make verify-sync` is the authoritative
# CI gate. This focused pre-commit assertion narrows the check to the
# migrating skill so contributors see the drift fast — without paying the
# full verify-sync sweep cost on every commit.
set -euo pipefail

SRC="src/superclaude/skills/sc-bare-review"
MIRROR=".claude/skills/sc-bare-review"

if [ ! -d "$SRC" ]; then
  exit 0
fi

if [ ! -d "$MIRROR" ]; then
  printf '❌ bare-review mirror missing: %s\n' "$MIRROR"
  printf '   Source path: %s\n' "$SRC"
  printf '   Run: make sync-dev\n'
  exit 1
fi

drift=$(diff -rq \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  --exclude='__init__.py' \
  "$SRC" "$MIRROR" 2>&1 || true)

if [ -n "$drift" ]; then
  printf '❌ bare-review src ↔ mirror drift detected.\n\n'
  printf '%s\n\n' "$drift"
  printf '   Source:  %s\n' "$SRC"
  printf '   Mirror:  %s\n' "$MIRROR"
  printf '   Run: make sync-dev && make verify-sync\n'
  printf '   Stage only %s/ paths — never the .claude/ mirror.\n' "$SRC"
  exit 1
fi

exit 0
