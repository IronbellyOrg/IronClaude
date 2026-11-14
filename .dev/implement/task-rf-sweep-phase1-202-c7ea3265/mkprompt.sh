#!/usr/bin/env bash
# Save the exact review prompt: usage mkprompt.sh T12 <k> <j> <brief-file> <diff-file> [delta-file] [prior-file] [recheck-file]
# Writes retries/<id>/prompt-<k>-<j>.md (line 1 = start sha) and prints the prompt body (lines 2..) for the Agent call.
set -u
R=/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode
D=$R/.dev/implement/task-rf-sweep-phase1-202-c7ea3265
id=$1; k=$2; j=$3; brief=$4; diff=$5; delta=${6:-/dev/null}; prior=${7:-/dev/null}; recheck=${8:-/dev/null}
start=$(grep -E "^$id: start sha=" "$D/progress.md" | tail -1 | sed 's/.*sha=//')
mkdir -p "$D/retries/$id"
out=$D/retries/$id/prompt-$k-$j.md
body=$(
  printf 'Review one task for spec compliance.\n\n'
  printf 'Task brief: %s\n' "$(cat "$brief")"
  printf 'Global constraints: the `### Key Constraints` section (lines 157-168) of the source file named in the task brief; read it from that file.\n'
  printf 'Start sha: %s\n' "$start"
  printf 'Diff against the start snapshot: %s\n' "$(cat "$diff")"
  printf 'Delta diff from the previous reviewed tree (empty on the first review): %s\n' "$(cat "$delta")"
  printf 'Earlier blocking findings of this start (empty on the first review): %s\n' "$(cat "$prior")"
  printf 'Saved-probe re-check hit locations (may be empty): %s\n\n' "$(cat "$recheck")"
  cat "$D/template-tail.txt"
)
{ printf '%s\n' "$start"; printf '%s\n' "$body"; } > "$out"
# delivery copy: same bytes as the saved prompt minus the start-sha header line; outside retries/ so the reviewer may read it
mkdir -p "$D/prompts"
printf '%s\n' "$body" > "$D/prompts/$id-$k-$j.txt"
echo "$D/prompts/$id-$k-$j.txt"
