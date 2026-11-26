#!/usr/bin/env bash
# cleanup-sessions.sh <rundir>: queue this run's session files; delete queued files only when no run uses the sandbox (13.5, R-46).
set -u -o pipefail
source "$(dirname "$0")/../lib/common.sh"
RD=$1
RUN_ID=$(jq -r .run_id "$RD/run.json")
UUIDRX='/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\.jsonl$'
PROJ=$(realpath -m "$CLAUDE_PROJECTS")
OUT='[]'
for PD in "$RD"/TASK-WF-*/; do
  PD=${PD%/}; PKG=$(basename "$PD"); D=$SB/$PKG
  [ -d "$D" ] || continue
  r3_assert_writable "$D/pending-cleanup.txt" || continue
  MAN=$PD/reviews/sessions/manifest.txt
  ( flock 9
    [ -f "$MAN" ] && cat "$MAN" >> "$D/pending-cleanup.txt"
    rm -f "$D/active/$RUN_ID"
    deleted=0; status=active
    if [ -z "$(ls -A "$D/active" 2>/dev/null)" ]; then
      status=cleaned
      if [ -f "$D/pending-cleanup.txt" ]; then
        while IFS= read -r f; do
          [ -n "$f" ] || continue
          rf=$(realpath -m -- "$f")
          case "$rf" in "$PROJ"/*) ;; *) continue;; esac
          [[ "$rf" =~ $UUIDRX ]] || continue
          [ -f "$rf" ] && rm -f -- "$rf" && deleted=$((deleted+1))
        done < "$D/pending-cleanup.txt"
        : > "$D/pending-cleanup.txt"
      fi
      git -C "$D/repo" clean -fdX -q 2>/dev/null
      st=$(git -C "$D/repo" status --porcelain --ignored --untracked-files=all 2>&1)
      jq -n --arg p "$PKG" --arg s "$st" --argjson d $deleted '{pkg:$p,deleted:$d,status_after:$s,clean:($s=="")}' > "$PD/cleanup.json"
    else
      jq -n --arg p "$PKG" '{pkg:$p,deleted:0,deferred:true}' > "$PD/cleanup.json"
    fi
  ) 9>>"$D/cleanup.lock"
done
