#!/usr/bin/env bash
# Build the task folder of the I4 (BMAD first-use research) run exactly as it stood when quality gate N started.
# Copies only; never edits anything in place. Target must NOT exist yet and must be inside a COPY of the Coder
# worktree at commit f1ac0c93ad5a64b03f0ed49866d3adfe140c28b1 (see REPLAY.md), never inside the original worktree.
#
# usage: make_gate_entry.sh <1|2|3> <TARGET_TASK_DIR>
#   TARGET_TASK_DIR = <coder-copy>/.dev/tasks/to-do/TASK-RESEARCH-bmad-first-use-20261107-075901
#
# Gate 1 first step in the task file = line 218, Gate 2 = line 308, Gate 3 = line 371. Every unchecked box ("- [ ] ")
# before that line is ticked ("- [x] "), because the work behind those steps exists as files (research, synthesis,
# report). This tick rule is a RECONSTRUCTION: the original task-file ticks and Task Log entries at gate start were
# not recoverable per gate; see REPLAY.md "Reconstructed parts".
set -u -o pipefail
gate="${1:-}"; target="${2:-}"
here="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; in="$here/inputs"
[ -n "$gate" ] && [ -n "$target" ] || { echo "usage: $0 <1|2|3> <TARGET_TASK_DIR>" >&2; exit 2; }
case "$gate" in 1) first=218;; 2) first=308;; 3) first=371;; *) echo "gate must be 1, 2 or 3" >&2; exit 2;; esac
[ ! -e "$target" ] || { echo "refusing: $target already exists" >&2; exit 3; }
case "$target" in */.dev/tasks/to-do/TASK-RESEARCH-bmad-first-use-20261107-075901) ;; *) echo "refusing: unexpected target path" >&2; exit 3;; esac
case "$target" in /home/coder/workspaces/worktrees/Coder/bmad-ponytail-global/*) echo "refusing: that is the original worktree" >&2; exit 3;; esac

mkdir -p "$target"/{research,synthesis,qa,reviews}
tf="$in/task-file/TASK-RESEARCH-bmad-first-use-20261107-075901.md.v2-at-2026-11-07T15-38-37Z"
sed -E "1,$((first-1))s/^- \[ \] /- [x] /" "$tf" > "$target/TASK-RESEARCH-bmad-first-use-20261107-075901.md"
cp "$in/task-file/BUILD-REQUEST.md" "$target/"
if [ "$gate" = 1 ]; then
  cp "$in"/gate1-start/research/*.md "$target/research/"
else
  cp "$in"/common/research/*.md "$target/research/"
  cp "$in/common/gaps-and-questions.md" "$target/"
  cp "$in/gate${gate}-start/synthesis/"*.md "$target/synthesis/"
fi
[ "$gate" = 3 ] && cp "$in/gate3-start/RESEARCH-REPORT-bmad-first-use.md" "$target/"
echo "built gate $gate entry in $target"
(cd "$target" && find . -type f | sort | xargs sha256sum)
