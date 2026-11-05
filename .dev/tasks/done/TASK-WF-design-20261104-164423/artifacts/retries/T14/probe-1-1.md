4d9051f27bf8e650277c80c36133a9bfe99311b6
family=finish-token-map
defect form: a FINISH_FAIL token mapped to one state when the script raises it at more than one step
command: grep -n -F -e 'tree_dirty' -- src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh
before:
src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md:92:- The precheck prints `{"precheck": "ok"}` (worktree changes only on unmerged paths; it takes no manifest, which is written only at step 9). `FINISH_FAIL tree_dirty`: abort, `merge_preflight_dirty`; any other token maps as in step 9.
src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md:118:| `tree_dirty` | `merge_preflight_dirty` | after the commit: the local merge commit is named; nothing pushed |
src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md:287:| `merge_preflight_dirty` | step 2; precheck `tree_dirty`; post-commit `tree_dirty` | The message above. After a commit, the local merge commit is named. |
src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh:25:#           unmerged | tree_dirty | markers | staged_unexpected | hook_rejected |
src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh:147:        || { cat -- "$TMP/err" >&2; fail tree_dirty "git diff of the work tree failed"; }
src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh:149:        || { cat -- "$TMP/err" >&2; fail tree_dirty "git diff of the unmerged paths failed"; }
src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh:155:            || fail tree_dirty "tracked file changed outside the conflict set: $path"
src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh:201:    1) fail tree_dirty "a tracked file has an unstaged change" ;;
src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh:202:    *) cat -- "$TMP/err" >&2; fail tree_dirty "git diff --quiet exited $DIFF_EXIT" ;;
src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh:272:    || { cat -- "$TMP/err" >&2; fail tree_dirty "git status failed after the commit"; }
src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh:273:[ ! -s "$TMP/status" ] || fail tree_dirty "tracked files differ from the new commit"
src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh:274:git diff --quiet HEAD 2>/dev/null || fail tree_dirty "the work tree differs from the new commit"
coupled sites: ref step 9 token table row (:118) and halt table merge_preflight_dirty row (:287); finish-merge.sh precheck (:15x), commit-mode step 3 (:201-202), step 8 (:271-274)
after: src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md:92:- The precheck prints `{"precheck": "ok"}` (worktree changes only on unmerged paths; it takes no manifest, which is written only at step 9). `FINISH_FAIL tree_dirty`: abort, `merge_preflight_dirty`; any other token maps as in step 9.
after: src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md:118:| `tree_dirty` (commit-mode step 3, before the commit) | `merge_preflight_dirty` | merge in progress, nothing committed |
after: src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md:119:| `tree_dirty` (commit-mode step 8, after the commit) | `merge_preflight_dirty` | the local merge commit is named; nothing pushed |
after: src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md:288:| `merge_preflight_dirty` | step 2; precheck `tree_dirty`; commit-mode `tree_dirty` (step 3 before the commit, step 8 after it) | The message above. Raised after the commit, the local merge commit is named; raised before it, the merge stays in progress with nothing committed. |
after: src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh:25:#           unmerged | tree_dirty | markers | staged_unexpected | hook_rejected |
after: src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh:147:        || { cat -- "$TMP/err" >&2; fail tree_dirty "git diff of the work tree failed"; }
after: src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh:149:        || { cat -- "$TMP/err" >&2; fail tree_dirty "git diff of the unmerged paths failed"; }
after: src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh:155:            || fail tree_dirty "tracked file changed outside the conflict set: $path"
after: src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh:201:    1) fail tree_dirty "a tracked file has an unstaged change" ;;
after: src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh:202:    *) cat -- "$TMP/err" >&2; fail tree_dirty "git diff --quiet exited $DIFF_EXIT" ;;
after: src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh:272:    || { cat -- "$TMP/err" >&2; fail tree_dirty "git status failed after the commit"; }
after: src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh:273:[ ! -s "$TMP/status" ] || fail tree_dirty "tracked files differ from the new commit"
after: src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh:274:git diff --quiet HEAD 2>/dev/null || fail tree_dirty "the work tree differs from the new commit"
