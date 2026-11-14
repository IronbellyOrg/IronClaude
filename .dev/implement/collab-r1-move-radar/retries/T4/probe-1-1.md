397b62f0e95b6dad3c9c888d7928c60899f86a87
## family h2-dropped-lines (from r1-1)
defect form: dropped_lines counts parser errors (including block-level notices and line-0 errors) instead of the block lines the merge parser will drop
command: grep -n -e 'DROPPED=' -e 'errors|length' -e 'dropped' .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/run-reviewer.sh .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/h2_normalize.py
before:
.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/run-reviewer.sh:85:DROPPED=0; REASK_S=null; REASK_TOK=0; REASK_MS=0
.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/run-reviewer.sh:110:      if [ "$(jq '.errors|length' "$OUT/$RID.h2-reask.json")" -le "$(jq '.errors|length' "$OUT/$RID.h
.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/run-reviewer.sh:115:  DROPPED=$(jq '.errors|length' "$OUT/$RID.h2.json")
.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/run-reviewer.sh:129:         dropped_lines:$dr, hang_kill:$hk, valid:$ok, role:$role, collab:$collab, argv:$argv}' "$LAST
coupled sites: h2_normalize.py (computes the count), run-reviewer.sh DROPPED and the re-ask keep-or-replace comparison (errors|length), tests/test_h2.py dropped_lines assertions
after:
.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/run-reviewer.sh:85:DROPPED=0; REASK_S=null; REASK_TOK=0; REASK_MS=0
.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/run-reviewer.sh:110:      # (more kept lines wins; on a tie, fewer dropped lines wins)
.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/run-reviewer.sh:112:           '[$a[0].kept_lines, -$a[0].dropped_lines] >= [$b[0].kept_lines, -$b[0].dropped_lines]' >/d
.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/run-reviewer.sh:117:  DROPPED=$(jq '.dropped_lines' "$OUT/$RID.h2.json")  # block lines the merge parser will not keep
.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/run-reviewer.sh:131:         dropped_lines:$dr, hang_kill:$hk, valid:$ok, role:$role, collab:$collab, argv:$argv}' "$LAST
.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/h2_normalize.py:5:"kept_lines", "dropped_lines"} (kept/dropped = block lines the merge parser keeps / loses).
.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/h2_normalize.py:44:def dropped_lines(text: str, parsed: dict) -> int:
.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/h2_normalize.py:49:    report is dropped. Block-level notices (several blocks, unclosed block) drop no line by themselves
.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/h2_normalize.py:65:                   "kept_lines": 0, "dropped_lines": 0}, open(errs, "w"))
.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/h2_normalize.py:72:               "dropped_lines": dropped_lines(new, parsed)}, open(errs, "w"))
