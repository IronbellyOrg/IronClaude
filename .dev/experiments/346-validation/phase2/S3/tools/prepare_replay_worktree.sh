#!/usr/bin/env bash
# Prepare a FRESH experiment worktree (based on master at or after 95f2c6e4) for the S3 replay:
# remove everything that would leak the finished answer and restore the repo files the original
# reviewers fact-checked. All changes are local and uncommitted. Never run this in the main
# checkout or in a worktree that holds real work.
# Usage: prepare_replay_worktree.sh <replay worktree> [--apply]   (default is a dry run)
set -eu -o pipefail
WT=$1; APPLY=${2:-}
BASE=8b4858f7   # original base commit (Orca reflog: branch created from origin/master 2026-11-05T17:01:24Z)
git -C "$WT" merge-base --is-ancestor 95f2c6e4 HEAD || { echo "HEAD must contain 95f2c6e4 (PR 427)" >&2; exit 2; }
[ -z "$(git -C "$WT" status --porcelain --untracked-files=no)" ] || { echo "worktree has tracked changes; use a fresh one" >&2; exit 2; }
run() { if [ "$APPLY" = "--apply" ]; then "$@"; else echo "DRY: $*"; fi; }
PURGE=(
  .dev/brainstorms/20261105-170229-launch-level-hook      # the finished plan, reviews, merged spec
  docs/designs/sc-issue-launch-level-hook.md              # the finished design
  tests/hooks/fixtures/launch_level
  tests/hooks/test_launch_job_identity.py
  src/superclaude/hooks/scripts/launch-job-identity.sh
  plugins/superclaude/hooks/scripts/launch-job-identity.sh
  .dev/codegraph-migration/evidence/P2-hook-session.md
  .dev/brainstorms/20261105-024132-issue-claim-orca-worktree-flag/hook-session-result.md   # the original run's own result
  .dev/tasks/done/TASK-WF-p1LivePlanBrief-20261105-164506          # follow-on runs that name the launch-level design
  .dev/tasks/done/TASK-WF-authorizedNarrow-20261106-214325
  .dev/tasks/to-do/TASK-WF-implementDocsDes-20261106-210206
  .dev/experiments                                        # phase-1 and phase-2 reports describe this incident
)
for p in "${PURGE[@]}"; do [ -e "$WT/$p" ] && run rm -rf "$WT/$p"; done
# repo files the reviewers read, as at the original base commit
for p in src/superclaude/hooks/hooks.json plugins/superclaude/hooks/hooks.json src/superclaude/cli/install_hooks.py tests/cli/test_install_hooks.py src/superclaude/core/WORKER-CONTRACT.md; do
  run git -C "$WT" checkout "$BASE" -- "$p"
done
# directories the reviewers grepped in the repo (they changed between 8b4858f7 and 95f2c6e4 for reasons unrelated to PR 427):
# delete first so files added later disappear, then restore the base tree. None of these is a file PR 427 touched.
for d in src/superclaude/skills/sc-pr-submit-protocol src/superclaude/skills/sc-implement-protocol; do
  [ -e "$WT/$d" ] && run rm -rf "$WT/$d"
  run git -C "$WT" checkout "$BASE" -- "$d"
done
# leakage check (meaningful after --apply): nothing may still mention the launch-level design
LEFT=$(git -C "$WT" grep -lIi -e 'launch-level' -e 'launch_level' -e 'launch level' -- . 2>/dev/null || true)
echo "remaining mentions of the launch-level design: ${LEFT:-none}"
[ "$APPLY" = "--apply" ] && [ -n "$LEFT" ] && echo "REVIEW THE LIST ABOVE: remove or justify each file before the run" || true
