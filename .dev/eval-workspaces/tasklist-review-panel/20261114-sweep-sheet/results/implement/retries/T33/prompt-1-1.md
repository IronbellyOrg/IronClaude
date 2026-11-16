5ea476189333a9b92f4342bbe045abb722824433
Review one task for spec compliance.

Task brief: ## Task 33: Create the freeze, order, sandbox-ground-truth and open-checks scripts, then run the build checkpoint

Depends on: Task 32, Task 31, Task 30

Create `bin/freeze.sh` (hashes of cards, extractors, words, formats, rank table and briefs into `config/freeze.json`; prints the `git tag` command with `echo` or `printf` only; never runs it), `bin/check-order.sh` (`freeze` and `prereg` modes comparing commit times of the freeze tag, the ground-truth commit, `prereg.json` and the first `run.json`, reading the tag with `git rev-parse` or `git log`, never `git tag`), `bin/check-sandbox-gt.sh` (a `grep -r` for ground-truth file names and field names over every `SB/<doc>/repo` and every `RUN/prepass/sheets`) and `bin/open-manual-checks.sh` (lists the M records of TESTING section 3 still open: the `swap_test` records, `fixtures/recall/AUTHORS.md`, attestations, the README second-reader record). Create `tests/test_freeze.py` (K5: `test_freeze_prints_but_never_tags`) and `tests/test_order.py` (REQ-33, REQ-36, REQ-44: `test_freeze_tag_before_gt_commit`, `test_gt_before_tag_fails`, `test_freeze_json_hashes_match_files`, `test_gt_hash_matches_prereg`, `test_every_planted_plan_has_twin`, `test_prereg_commit_before_first_run`). Then run the build checkpoint of IMPLEMENTATION section 2 (after step 13) and save its output.

Acceptance criteria:
- T33.AC1: `$T $SW/tests/test_freeze.py $SW/tests/test_order.py -q` exits 0, and `git tag -l` is unchanged after `bin/freeze.sh` runs in the temporary repository of the test.
- T33.AC2: `$T $SW/tests -q -m "not slow and not freeze"` exits 0 and its summary line is saved to `SW/results/tests-final.log`; `$T $SW/tests -q -m slow` exits 0.
- T33.AC3: `uv run --frozen --project $REPO ruff check $SW` and `uv run --frozen --project $REPO ruff format --check $SW` exit 0; `$T $REPO/tests/review -q` exits 0.
- T33.AC4: `git status --porcelain -- src tests .claude` prints nothing, and under `.dev/tasks/` the only entries are this plan's own package folder (plan, source snapshot, contract, grounding note and the executor's ledger); no other `.dev/tasks/` folder changed.
- T33.AC5: `bash $SW/bin/open-manual-checks.sh` prints the open manual records, and `SW/results/open-manual-checks.txt` holds that output; the freeze (step 14) has not been done.
- T33.AC6: `bash $SW/bin/check-sandbox-gt.sh` exits 0 with no output over the sandboxes the tests built.
- T33.AC7: `gitcheck $SW/bin` (Constraints) prints nothing over every script of the finished `bin/`, and `grep -rn "claude-opus-5-5" $SW/bin $SW/sweep $SW/scaffold` hits only `bin/judge-one.sh`; this re-runs the checks that Task 27 first runs.
Global constraints: - Names used by every task. `SW` is the folder `.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet` (repo-relative). Its three specification files are `SW/DESIGN.md`, `SW/IMPLEMENTATION.md` (section 2 holds the steps) and `SW/TESTING.md` (section 2 fixtures, section 3 requirement map, section 4 constraint tests). Section and row names in a task refer to those files. Test names written `file::function` live under `SW/tests/`. `MR` is `.dev/brainstorms/20261113-223124-panel-process-redesign/merged-requirements.md`, `RR` is `.dev/eval-workspaces/tasklist-review-panel/20261111-a1/tools/run-reviewer.sh`, `JJ` is `.dev/eval-workspaces/tasklist-review-panel/20261111-a1/tools/tmp-scripts/judge-one.sh`, `FND` is `src/superclaude/cli/review/findings.py`, `MRG` is `src/superclaude/cli/review/merge_cmd.py`, `LED` is `src/superclaude/cli/review/ledger.py`.
- Shell variables for every command, run from the repository root: `REPO="$(git rev-parse --show-toplevel)"`, `SW="$REPO/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet"`, `T="uv run --frozen --project $REPO pytest -p no:cacheprovider"`, `PYRUN="uv run --frozen --project $REPO python"`, and `export PYTHONDONTWRITEBYTECODE=1`. Python only through `uv run`; never `python -m`, `pip install` or bare `python script.py`.
- Git-write check. `gitcheck() { grep -rnE '\bgit\b[^|;&]*\b(add|commit|tag|push)\b' "$1" | grep -vE 'git -C "\$\{?SB[A-Za-z_]*\}?' | grep -vE ':[0-9]+:[[:space:]]*(#|echo|printf)'; }` prints nothing for a directory when no script in it runs `git add`, `commit`, `tag` or `push` except as `git -C "$SB..."` (a sandbox directory variable), in printed text or in a comment. A script that must read a tag uses `git rev-parse`, `git log` or `git for-each-ref`, never `git tag`. Tasks 8, 27 and 33 run it; Task 27 also shows it prints the probe line for a temporary file that holds `git add -A`, so the check is not vacuous.
- Write scope (DESIGN K1). Every file the build creates lives under `SW`. Scratch goes only to pytest `tmp_path` or `/tmp`; the sandbox root is `/tmp/evalsb-sweep`. `src/`, `tests/`, `.claude/` and every existing folder under `.dev/tasks/` are not touched. Evidence a task produces is written under `SW/results/`, not into this plan's package.
- Git scope. The build stages, commits and pushes nothing, and creates no tag (DESIGN K5). Staging of this plan's package stays with the session that runs `/sc:implement`. The sandbox builder's own `git init`, `git add` and snapshot commit run inside a throwaway sandbox under `/tmp` and are not repository writes; they are spelled `git -C "$SB..."`, which is how the git-write check (`gitcheck`, above) tells them from a write to the real repository.
- No model. No reviewer, judge or spike session is started. Every test that needs `claude` uses the fake `SW/tests/fakes/claude` (TESTING F-FAKE). Scripts that start models in real use (`bin/run-spike.sh`, `bin/run-schedule.sh`, `bin/judge-batch.sh`) are built and tested only against the fake.
- Never open any `ground-truth*.json` or score file. Tests marked `freeze` (the real-ground-truth lint, the recall tests) are written but not run by the build; the build runs `-m "not slow and not freeze"` plus `-m slow` where a task says so.
- Read-only imports. `FND`, `MRG` and `LED` are imported or called, never edited. `FND._check_finding` and `FND._blocks_after` are private; they are reached only through `SW/scaffold/fnd.py` (DESIGN section 2.3).
- Folder names. No folder is named `lib/` (`.gitignore` line 13 ignores it; DESIGN K7). Code folders are `scaffold/`, `sweep/` and `analysis/`.
- Decisions DD-1 to DD-15 of DESIGN section 1.3 hold as written; a conflict between this plan and DESIGN.md is settled by DESIGN.md. Step 0 is done (`SW/results/step0.md`); its sub-steps 0.4, 0.5 and 0.6 were not run, so the task that needs each one runs or reads it first (0.4 in Task 24, 0.5 in Task 26, 0.6 in Tasks 6 and 28). Step 0.3 measured a scope taken from IMPLEMENTATION.md, not the DD-5 scope; Task 23 measures the DD-5 scope.
- Out of scope: steps 14 to 16, Redesign 2, the optional verifier of `MR` 3.0.9, any change under `src/`, and any file under `fixtures/recall/` or `holdout-gt/`.
- Line counts in the design are planning values (unmeasured).
Start sha: 5ea476189333a9b92f4342bbe045abb722824433
Diff against the start snapshot: diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/bin/check-order.sh b/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/bin/check-order.sh
new file mode 100755
index 000000000..44d8fd03c
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/bin/check-order.sh
@@ -0,0 +1,139 @@
+#!/usr/bin/env bash
+# check-order.sh {freeze|prereg|twins} [options]   (DESIGN AO-5, REQ-33, REQ-36, REQ-44; read-only)
+# Checks the order of the things that the experiment must do in a fixed order, by commit times, and the hashes that tie them.
+# It only reads: git log, git rev-parse (a tag is read with those, never made), sha256sum, jq. Exit 0 the order holds, 1 it does
+# not (the reason is printed), 2 a bad argument or a missing input.
+#   freeze  --repo DIR --freeze FILE --gt PATH [--gt PATH ...]
+#           The freeze tag named by `freeze_tag` in FILE (default <SW>/config/freeze.json) exists and its commit time is earlier
+#           than the first commit that added any file under a --gt path (default <SW>/holdout-gt); the ground truth must also
+#           be committed (an uncommitted ground truth proves nothing). And every file in FILE's `files` still has the recorded
+#           sha256 (an extractor changed after the freeze fails here). The tree of the files is the folder above FILE's folder.
+#   prereg  --repo DIR --prereg FILE --runs DIR [--gt-dir DIR]
+#           FILE (default <SW>/config/prereg.json) is committed, and its first commit is earlier than the first run.json under
+#           DIR (default <SW>/runs): the first commit that added one, or, for runs that are not committed, the oldest file time.
+#           With no run.json yet the order holds. If FILE has `ground_truth_sha256` {document: sha256}, each ground-truth file
+#           (DIR/<doc>.json or DIR/<doc>/ground-truth.json under --gt-dir, default <SW>/holdout-gt) must have that sha256.
+#   twins   --manifest FILE
+#           Every entry of `planted` in the manifest names a `twin` file (relative to the manifest's folder) that exists.
+# --repo defaults to the repository that holds this script. Times are commit times (%ct, whole seconds): equal times fail,
+# because the order cannot be shown.
+set -u -o pipefail
+source "$(dirname "$0")/common.sh"
+
+usage() {
+  sed -n '2,2p' "$0" | sed 's/^# \{0,1\}//' >&2
+  exit 2
+}
+MODE=${1:-}
+case "$MODE" in freeze | prereg | twins) shift ;; *) usage ;; esac
+REPOD=$REPO FREEZE=$SW/config/freeze.json PREREG=$SW/config/prereg.json RUNS=$SW/runs GTDIR=$SW/holdout-gt MANIFEST=
+GTS=()
+while [ $# -gt 0 ]; do
+  [ $# -ge 2 ] || usage
+  case "$1" in
+    --repo) REPOD=$2 ;;
+    --freeze) FREEZE=$2 ;;
+    --gt) GTS+=("$2") ;;
+    --prereg) PREREG=$2 ;;
+    --runs) RUNS=$2 ;;
+    --gt-dir) GTDIR=$2 ;;
+    --manifest) MANIFEST=$2 ;;
+    *) usage ;;
+  esac
+  shift 2
+done
+
+fail() { echo "ORDER_FAIL: $*" >&2; exit 1; }
+rel() { # rel PATH: PATH relative to the repository top, for git log
+  local top p
+  top=$(git -C "$REPOD" rev-parse --show-toplevel) || exit 2
+  p=$(realpath -m -- "$1")
+  echo "${p#"$(realpath -m -- "$top")"/}"
+}
+first_add_time() { # first_add_time PATHSPEC...: the earliest commit time of a commit that added a file under the pathspecs
+  local p t out=""
+  for p in "$@"; do
+    # the smallest commit time among the commits that added a file (history order is not time order after a rebase)
+    t=$(git -C "$REPOD" log --diff-filter=A --format=%ct -- "$p" 2>/dev/null | sort -n | head -n 1)
+    if [ -n "$t" ] && { [ -z "$out" ] || [ "$t" -lt "$out" ]; }; then
+      out=$t
+    fi
+  done
+  echo "$out"
+}
+rel_all() { # rel_all PATH...: each path relative to the repository top
+  local p
+  for p in "$@"; do rel "$p"; done
+}
+
+case "$MODE" in
+  freeze)
+    [ -f "$FREEZE" ] || { echo "E_ARG: no freeze record $FREEZE" >&2; exit 2; }
+    [ ${#GTS[@]} -gt 0 ] || GTS=("$GTDIR")
+    NAME=$(jq -r '.freeze_tag // empty' "$FREEZE")
+    [ -n "$NAME" ] || fail "$FREEZE records no freeze_tag"
+    REF=refs/tags/$NAME
+    git -C "$REPOD" rev-parse -q --verify "$REF" >/dev/null || fail "the freeze tag $NAME does not exist in $REPOD (a person makes it; bin/freeze.sh prints the command)"
+    T_FREEZE=$(git -C "$REPOD" log -1 --format=%ct "$REF") || exit 2
+    mapfile -t GT_SPECS < <(rel_all "${GTS[@]}")
+    T_GT=$(first_add_time "${GT_SPECS[@]}")
+    [ -n "$T_GT" ] || fail "the ground truth under ${GTS[*]} is not committed, so its order cannot be shown"
+    [ "$T_FREEZE" -lt "$T_GT" ] || fail "the freeze tag $NAME ($T_FREEZE) is not earlier than the first ground-truth commit ($T_GT)"
+    TREE=$(dirname "$(dirname "$(realpath -m -- "$FREEZE")")")
+    BAD=0
+    while IFS=$'\t' read -r f h; do
+      [ -n "$f" ] || continue
+      now=$(sha256sum -- "$TREE/$f" 2>/dev/null | cut -d' ' -f1)
+      if [ "$now" != "$h" ]; then
+        echo "ORDER_FAIL: $f changed after the freeze (recorded ${h:0:12}, now ${now:0:12})" >&2
+        BAD=1
+      fi
+    done < <(jq -r '.files | to_entries[] | [.key, .value] | @tsv' "$FREEZE")
+    [ "$BAD" = 0 ] || exit 1
+    echo "ORDER_OK freeze: tag $NAME ($T_FREEZE) is earlier than the first ground-truth commit ($T_GT); every frozen file is unchanged"
+    ;;
+  prereg)
+    [ -f "$PREREG" ] || fail "$PREREG does not exist: write it with analysis/analyze.py prereg --write"
+    T_PRE=$(first_add_time "$(rel "$PREREG")")
+    [ -n "$T_PRE" ] || fail "$PREREG is not committed, so its order cannot be shown"
+    T_RUN=$(first_add_time ":(glob)$(rel "$RUNS")/**/run.json")
+    if [ -z "$T_RUN" ] && [ -d "$RUNS" ]; then
+      T_RUN=$(find "$RUNS" -name run.json -printf '%T@\n' 2>/dev/null | sort -n | head -n 1)
+      T_RUN=${T_RUN%.*}
+    fi
+    if [ -n "$T_RUN" ]; then
+      [ "$T_PRE" -lt "$T_RUN" ] || fail "$PREREG ($T_PRE) is not earlier than the first run.json ($T_RUN)"
+    fi
+    BAD=0
+    while IFS=$'\t' read -r doc want; do
+      [ -n "$doc" ] || continue
+      gt=
+      for c in "$GTDIR/$doc.json" "$GTDIR/$doc/ground-truth.json"; do [ -f "$c" ] && gt=$c && break; done
+      [ -n "$gt" ] || { echo "ORDER_FAIL: no ground-truth file for $doc under $GTDIR" >&2; BAD=1; continue; }
+      have=$(sha256sum -- "$gt" | cut -d' ' -f1)
+      [ "$have" = "$want" ] || { echo "ORDER_FAIL: the ground truth of $doc has sha256 ${have:0:12}, prereg.json records ${want:0:12}" >&2; BAD=1; }
+    done < <(jq -r '(.ground_truth_sha256 // {}) | to_entries[] | [.key, .value] | @tsv' "$PREREG")
+    [ "$BAD" = 0 ] || exit 1
+    WHEN="any run (none has started)"
+    [ -z "$T_RUN" ] || WHEN="the first run.json ($T_RUN)"
+    echo "ORDER_OK prereg: ${PREREG##*/} ($T_PRE) is earlier than $WHEN; the ground-truth hashes match"
+    ;;
+  twins)
+    [ -f "$MANIFEST" ] || { echo "E_ARG: --manifest FILE is required" >&2; exit 2; }
+    DIR=$(dirname "$MANIFEST")
+    BAD=0
+    N=0
+    while IFS=$'\t' read -r plan twin; do
+      N=$((N + 1))
+      if [ -z "$twin" ]; then
+        echo "ORDER_FAIL: planted plan $plan has no clean twin" >&2
+        BAD=1
+      elif [ ! -f "$DIR/$twin" ]; then
+        echo "ORDER_FAIL: the twin $twin of $plan does not exist" >&2
+        BAD=1
+      fi
+    done < <(jq -r '.planted[] | [(.plan // .id // "?"), (.twin // "")] | @tsv' "$MANIFEST")
+    [ "$BAD" = 0 ] || exit 1
+    echo "ORDER_OK twins: all $N planted plans have an existing twin"
+    ;;
+esac
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/bin/check-sandbox-gt.sh b/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/bin/check-sandbox-gt.sh
new file mode 100755
index 000000000..701f341e2
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/bin/check-sandbox-gt.sh
@@ -0,0 +1,52 @@
+#!/usr/bin/env bash
+# check-sandbox-gt.sh [--sb DIR] [--runs DIR]   (REQ-34, DESIGN AO-6; read-only)
+# A recursive grep for ground truth over every sandbox repository (DIR/<doc>/repo and DIR/<doc>/repo-raw) and every sheet of
+# every run (RUNS/*/*/prepass/sheets): a file whose name starts with `ground-truth`, and any text that holds a field name of
+# a ground-truth item or of a judge score (plan_quote, blocking_in_implement, gt_covered_any, gt_covered_blocking).
+# It prints one line per hit and nothing when the places are clean. Run it before the first arm and after the last.
+#   --sb DIR     the sandbox root (default SW_SB_ROOT or /tmp/evalsb-sweep)
+#   --runs DIR   the run folders (default <SW>/runs); the sheets are RUNS/<stage>/<run>/prepass/sheets and, for a folder of runs
+#                directly under RUNS, RUNS/<run>/prepass/sheets
+# Exit: 0 clean (and no output); 1 a hit (printed); 2 no sandbox under the root, so nothing could be checked (a clean result
+# over nothing would prove nothing).
+set -u -o pipefail
+source "$(dirname "$0")/common.sh"
+
+usage() {
+  sed -n '2,2p' "$0" | sed 's/^# \{0,1\}//' >&2
+  exit 2
+}
+SBROOT=$SB RUNS=$SW/runs
+while [ $# -gt 0 ]; do
+  [ $# -ge 2 ] || usage
+  case "$1" in
+    --sb) SBROOT=$2 ;;
+    --runs) RUNS=$2 ;;
+    *) usage ;;
+  esac
+  shift 2
+done
+
+PLACES=()
+for d in "$SBROOT"/*/repo "$SBROOT"/*/repo-raw; do
+  [ -d "$d" ] && PLACES+=("$d")
+done
+[ ${#PLACES[@]} -gt 0 ] || { echo "E_NO_SANDBOX: no <doc>/repo under $SBROOT; build it with bin/build-sandbox.sh" >&2; exit 2; }
+for d in "$RUNS"/*/*/prepass/sheets "$RUNS"/*/prepass/sheets; do
+  [ -d "$d" ] && PLACES+=("$d")
+done
+
+HITS=0
+FIELDS='plan_quote|blocking_in_implement|gt_covered_any|gt_covered_blocking'
+for place in "${PLACES[@]}"; do
+  while IFS= read -r f; do
+    echo "$f: a file named like ground truth"
+    HITS=1
+  done < <(find "$place" -path '*/.git' -prune -o \( -iname 'ground-truth*' -o -iname 'ground_truth*' \) -print 2>/dev/null)
+  while IFS= read -r line; do
+    echo "$line"
+    HITS=1
+  done < <(grep -rEIn --exclude-dir=.git -e "$FIELDS" -- "$place" 2>/dev/null | cut -c1-200)
+done
+[ "$HITS" = 0 ] || exit 1
+exit 0
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/bin/freeze.sh b/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/bin/freeze.sh
new file mode 100755
index 000000000..45e3777a3
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/bin/freeze.sh
@@ -0,0 +1,69 @@
+#!/usr/bin/env bash
+# freeze.sh [--sw DIR] [--out FILE] [--tag NAME]   (DESIGN AO-5, K5, REQ-33)
+# Records the sha256 of every file that the freeze covers (the cards, the extractors, the word lists, the format dictionaries,
+# the rank table and the briefs) in config/freeze.json, and PRINTS the git commands that a person then runs. It never runs
+# git tag, git add or git commit (K5): the tag is made by a person.
+#   --sw DIR    the sweep-sheet tree to hash (default: this one); another tree only under /tmp (a test hook)
+#   --out FILE  where the record goes (default <sw>/config/freeze.json); under SW or /tmp
+#   --tag NAME  the tag name that is recorded as `freeze_tag` (default sweep-sheet-freeze-<UTC date>)
+# Frozen files: cards/*.json, sweep/extractors.py, sweep/words.py, sweep/formats.py, sweep/rank.py (the rank table is one dict
+# in that file, so its hash covers the table), briefs/*.txt.
+# The record has `freeze_tag` (the name bin/run-panel.sh copies into every run.json), `files` {path relative to the tree:
+# sha256} and the date. A frozen file that is not committed, or that differs from the last commit, stops the script (exit 3):
+# the tag would name a commit that does not hold what was hashed.
+# Exit: 0 recorded and printed; 2 bad argument or missing frozen file; 3 a frozen file is not committed as it is.
+set -u -o pipefail
+source "$(dirname "$0")/common.sh"
+
+usage() {
+  sed -n '2,2p' "$0" | sed 's/^# \{0,1\}//' >&2
+  exit 2
+}
+TREE=$SW OUT= TAGNAME=
+while [ $# -gt 0 ]; do
+  [ $# -ge 2 ] || usage
+  case "$1" in
+    --sw) TREE=$2 ;;
+    --out) OUT=$2 ;;
+    --tag) TAGNAME=$2 ;;
+    *) usage ;;
+  esac
+  shift 2
+done
+if [ "$(realpath -m -- "$TREE")" != "$(realpath -m -- "$SW")" ]; then
+  case "$(realpath -m -- "$TREE")/" in /tmp/?*) ;; *) echo "E_OVERRIDE: --sw $TREE is outside /tmp/" >&2; exit 2 ;; esac
+fi
+[ -d "$TREE" ] || { echo "E_ARG: no tree $TREE" >&2; exit 2; }
+OUT=${OUT:-$TREE/config/freeze.json}
+sw_assert_writable "$OUT" || exit 2
+TAGNAME=${TAGNAME:-sweep-sheet-freeze-$(date -u +%Y%m%d)}
+[[ $TAGNAME =~ ^[A-Za-z0-9][A-Za-z0-9._/-]*$ ]] || { echo "E_ARG: bad tag name $TAGNAME" >&2; exit 2; }
+
+FILES=()
+for f in "$TREE"/cards/*.json "$TREE"/briefs/*.txt "$TREE"/sweep/extractors.py "$TREE"/sweep/words.py "$TREE"/sweep/formats.py "$TREE"/sweep/rank.py; do
+  [ -f "$f" ] || { echo "E_MISSING: frozen file $f does not exist" >&2; exit 2; }
+  FILES+=("${f#"$TREE"/}")
+done
+
+# Every frozen file must be committed as it is: git status is read-only.
+TOP=$(git -C "$TREE" rev-parse --show-toplevel 2>/dev/null) || { echo "E_GIT: $TREE is not in a git repository" >&2; exit 3; }
+DIRTY=$(cd "$TREE" && git status --porcelain -- "${FILES[@]}")
+if [ -n "$DIRTY" ]; then
+  echo "E_UNCOMMITTED: these frozen files are not committed as they are; commit them first:" >&2
+  printf '%s\n' "$DIRTY" >&2
+  exit 3
+fi
+
+HASHES=$(cd "$TREE" && for f in "${FILES[@]}"; do printf '%s\t%s\n' "$f" "$(sha256sum -- "$f" | cut -d' ' -f1)"; done)
+JSON=$(jq -n --arg tag "$TAGNAME" --arg date "$(date -u +%Y-%m-%dT%H:%M:%SZ)" --arg h "$HASHES" \
+  '{schema: "sweep-freeze/1", freeze_tag: $tag, created: $date,
+    files: ($h | split("\n") | map(split("\t") | {key: .[0], value: .[1]}) | from_entries)}')
+mkdir -p "$(dirname "$OUT")" || exit 2
+printf '%s\n' "$JSON" >"$OUT"
+
+N=${#FILES[@]}
+printf 'freeze.sh: %s frozen files hashed into %s\n' "$N" "$OUT"
+printf 'Nothing was staged, committed or tagged. A person now runs, in %s:\n' "$TOP"
+printf '  git add %s && git commit -m "freeze: sweep sheet cards, extractors, words, formats, rank table, briefs"\n' "$OUT"
+printf '  git tag -a %s -m "Sweep Sheet freeze"\n' "$TAGNAME"
+printf 'The tag must exist before the hold-out ground truth is committed (bin/check-order.sh freeze).\n'
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/bin/open-manual-checks.sh b/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/bin/open-manual-checks.sh
new file mode 100755
index 000000000..a663afcec
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/bin/open-manual-checks.sh
@@ -0,0 +1,51 @@
+#!/usr/bin/env bash
+# open-manual-checks.sh [--sw DIR]   (TESTING section 3 rows of kind M, section 6 item 4; read-only)
+# Prints the manual (M) records that are still open, one line each: `OPEN <id>: <what is missing>`, then `open: <n>`.
+# A record is closed by the file or the entry that its row names; this script only looks for them and decides nothing.
+#   swap:C1 .. swap:C8       cards/C<n>.json `swap_test` has a reviewer and a date (REQ-08)
+#   recall-authors           fixtures/recall/AUTHORS.md exists and is not empty (REQ-21)
+#   readme-second-reader     cards/README.md has no line "Second reader ... Status: OPEN" (REQ-38)
+#   owner-values             config/prereg.json exists and says owner_confirmed true (REQ-41)
+#   spike                    config/values.json: spike.runs is 5 or more (REQ-32)
+#   gt-attestation           config/attestation.md exists (REQ-36)
+#   attest:<id>              results/attestations.md has a line `ATTEST <id>: <person>, <date>, <statement>` for each of:
+#                            freeze-order (REQ-33), prereg-order (REQ-44), report-measured-values (REQ-31),
+#                            report-headline (REQ-40), report-claims (REQ-45)
+#   model-stage-ablation     not run (DD-13): an owner decision, listed so that it is not forgotten
+# Exit: always 0 (it reports; it does not gate). --sw DIR reads another tree (a test hook, under /tmp only).
+set -u -o pipefail
+source "$(dirname "$0")/common.sh"
+
+TREE=$SW
+if [ $# -ge 1 ]; then
+  [ "$1" = --sw ] && [ $# -eq 2 ] || { sed -n '2,2p' "$0" | sed 's/^# \{0,1\}//' >&2; exit 2; }
+  case "$(realpath -m -- "$2")/" in /tmp/?*) TREE=$2 ;; *) echo "E_OVERRIDE: --sw $2 is outside /tmp/" >&2; exit 2 ;; esac
+fi
+OPEN=0
+open() { echo "OPEN $1: $2"; OPEN=$((OPEN + 1)); }
+
+for n in 1 2 3 4 5 6 7 8; do
+  f=$TREE/cards/C$n.json
+  if [ ! -f "$f" ]; then
+    open "swap:C$n" "cards/C$n.json does not exist"
+  elif [ -z "$(jq -r '.swap_test.reviewer // ""' "$f")" ] || [ -z "$(jq -r '.swap_test.date // ""' "$f")" ]; then
+    open "swap:C$n" "swap_test has no reviewer or no date: a second author must replace the domain nouns by placeholders and sign"
+  fi
+done
+
+[ -s "$TREE/fixtures/recall/AUTHORS.md" ] || open recall-authors "fixtures/recall/AUTHORS.md is missing: who seeded the recall plans, and that they had not read the extractors"
+if [ ! -f "$TREE/cards/README.md" ] || grep -Eq 'Second reader.*Status: OPEN' "$TREE/cards/README.md"; then
+  open readme-second-reader "cards/README.md still says the second reader's record is OPEN"
+fi
+if [ "$(jq -r '.owner_confirmed // false' "$TREE/config/prereg.json" 2>/dev/null)" != true ]; then
+  open owner-values "config/prereg.json is missing or not confirmed by the owner (analysis/analyze.py prereg --write --owner-values FILE)"
+fi
+runs=$(jq -r '.spike.runs // 0' "$TREE/config/values.json" 2>/dev/null || echo 0)
+[ "${runs:-0}" -ge 5 ] 2>/dev/null || open spike "config/values.json has no spike record of 5 runs (bin/run-spike.sh timing; needs the owner's go-ahead)"
+[ -f "$TREE/config/attestation.md" ] || open gt-attestation "config/attestation.md is missing: the ground-truth author, the date, 'has not seen the recipes, cards or extractors', the hashes"
+for id in freeze-order prereg-order report-measured-values report-headline report-claims; do
+  grep -Eq "^ATTEST $id: .+, .+, .+" "$TREE/results/attestations.md" 2>/dev/null || open "attest:$id" "results/attestations.md has no ATTEST $id line"
+done
+open model-stage-ablation "not run: 8 extra arms and 96 panel runs outside the run budget; an owner decision (DD-13)"
+echo "open: $OPEN"
+exit 0
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/results/open-manual-checks.txt b/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/results/open-manual-checks.txt
new file mode 100644
index 000000000..8073ea6f2
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/results/open-manual-checks.txt
@@ -0,0 +1,20 @@
+OPEN swap:C1: swap_test has no reviewer or no date: a second author must replace the domain nouns by placeholders and sign
+OPEN swap:C2: swap_test has no reviewer or no date: a second author must replace the domain nouns by placeholders and sign
+OPEN swap:C3: swap_test has no reviewer or no date: a second author must replace the domain nouns by placeholders and sign
+OPEN swap:C4: swap_test has no reviewer or no date: a second author must replace the domain nouns by placeholders and sign
+OPEN swap:C5: swap_test has no reviewer or no date: a second author must replace the domain nouns by placeholders and sign
+OPEN swap:C6: swap_test has no reviewer or no date: a second author must replace the domain nouns by placeholders and sign
+OPEN swap:C7: swap_test has no reviewer or no date: a second author must replace the domain nouns by placeholders and sign
+OPEN swap:C8: swap_test has no reviewer or no date: a second author must replace the domain nouns by placeholders and sign
+OPEN recall-authors: fixtures/recall/AUTHORS.md is missing: who seeded the recall plans, and that they had not read the extractors
+OPEN readme-second-reader: cards/README.md still says the second reader's record is OPEN
+OPEN owner-values: config/prereg.json is missing or not confirmed by the owner (analysis/analyze.py prereg --write --owner-values FILE)
+OPEN spike: config/values.json has no spike record of 5 runs (bin/run-spike.sh timing; needs the owner's go-ahead)
+OPEN gt-attestation: config/attestation.md is missing: the ground-truth author, the date, 'has not seen the recipes, cards or extractors', the hashes
+OPEN attest:freeze-order: results/attestations.md has no ATTEST freeze-order line
+OPEN attest:prereg-order: results/attestations.md has no ATTEST prereg-order line
+OPEN attest:report-measured-values: results/attestations.md has no ATTEST report-measured-values line
+OPEN attest:report-headline: results/attestations.md has no ATTEST report-headline line
+OPEN attest:report-claims: results/attestations.md has no ATTEST report-claims line
+OPEN model-stage-ablation: not run: 8 extra arms and 96 panel runs outside the run budget; an owner decision (DD-13)
+open: 19
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/results/tests-final.log b/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/results/tests-final.log
new file mode 100644
index 000000000..a9867bb88
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/results/tests-final.log
@@ -0,0 +1 @@
+747 passed, 6 deselected in 196.31s (0:03:16)
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/tests/order_support.py b/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/tests/order_support.py
new file mode 100644
index 000000000..c6258ce10
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/tests/order_support.py
@@ -0,0 +1,96 @@
+"""Temporary git repositories with dated commits for the freeze and order tests (TESTING REQ-33, REQ-36, REQ-44, K5).
+
+Git runs only inside the repository that a test creates under tmp_path; the tests write there and nowhere else.
+"""
+
+import os
+import re
+import subprocess
+from pathlib import Path
+
+CLEAN_ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
+IDENT = [
+    "-c",
+    "user.name=t",
+    "-c",
+    "user.email=t@example.invalid",
+    "-c",
+    "commit.gpgsign=false",
+    "-c",
+    "tag.gpgsign=false",
+]
+FROZEN = {
+    "cards/C1.json": '{"id": "C1"}\n',
+    "cards/C2.json": '{"id": "C2"}\n',
+    "briefs/base.txt": "a brief part\n",
+    "sweep/extractors.py": "EXTRACTORS = {}\n",
+    "sweep/words.py": "WORDS = ()\n",
+    "sweep/formats.py": "FORMATS = {}\n",
+    "sweep/rank.py": "TABLE = {}\n",
+}
+
+
+def git(repo, *args, when=None, check=True):
+    env = dict(CLEAN_ENV)
+    if when is not None:
+        # "@<epoch seconds>": git does not read a bare small number as a date
+        env["GIT_AUTHOR_DATE"] = env["GIT_COMMITTER_DATE"] = f"@{when} +0000"
+    r = subprocess.run(
+        ["git", "-C", str(repo), *IDENT, *args], capture_output=True, text=True, env=env
+    )
+    if check:
+        assert r.returncode == 0, (args, r.stderr)
+    return r
+
+
+def make_repo(root):
+    repo = Path(root) / "repo"
+    repo.mkdir()
+    git(repo, "init", "-q", "-b", "main")
+    return repo
+
+
+def write(repo, files):
+    for rel, text in files.items():
+        p = repo / rel
+        p.parent.mkdir(parents=True, exist_ok=True)
+        p.write_text(text)
+
+
+def save(repo, files, when, msg="m"):
+    """Write the files, record them in one commit dated `when` (epoch seconds), return the commit id."""
+    write(repo, files)
+    git(repo, "add", "-A")
+    git(repo, "commit", "-q", "-m", msg, when=when)
+    return git(repo, "rev-parse", "HEAD").stdout.strip()
+
+
+def mark(repo, name, when):
+    """An annotated tag on HEAD dated `when`."""
+    git(repo, "tag", "-a", name, "-m", "freeze", when=when)
+
+
+def tags(repo):
+    return git(repo, "tag", "-l").stdout.split()
+
+
+# the check of the plan's Constraints (`gitcheck`), written out in Python so that a test can run it over any folder
+GIT_WRITE = re.compile(r"\bgit\b[^|;&]*\b(add|commit|tag|push)\b")
+SANDBOX_VAR = re.compile(r'git -C "\$\{?SB[A-Za-z_]*\}?')
+SAID = re.compile(r"^\s*(#|echo|printf)")
+
+
+def gitcheck(folder):
+    """Lines of the files under folder that run git add, commit, tag or push, except `git -C "$SB..."` and printed or commented text."""
+    hits = []
+    for p in sorted(Path(folder).rglob("*")):
+        if not p.is_file() or "__pycache__" in p.parts:
+            continue
+        for n, line in enumerate(p.read_text(errors="replace").splitlines(), 1):
+            if (
+                GIT_WRITE.search(line)
+                and not SANDBOX_VAR.search(line)
+                and not SAID.match(line)
+            ):
+                hits.append(f"{p}:{n}:{line}")
+    return hits
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/tests/test_freeze.py b/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/tests/test_freeze.py
new file mode 100644
index 000000000..6f5c44638
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/tests/test_freeze.py
@@ -0,0 +1,116 @@
+"""K5, AO-5: bin/freeze.sh hashes the frozen files and prints the tag command; it never tags, stages or commits."""
+
+import hashlib
+import json
+import subprocess
+
+from helpers import SW
+from order_support import FROZEN, git, gitcheck, make_repo, save, tags
+
+FREEZE = SW / "bin" / "freeze.sh"
+
+
+def run_freeze(roots, repo, *extra):
+    tree = repo / "sw"
+    cmd = [
+        "bash",
+        str(FREEZE),
+        "--sw",
+        str(tree),
+        "--out",
+        str(tree / "config" / "freeze.json"),
+        *extra,
+    ]
+    return subprocess.run(cmd, capture_output=True, text=True, env=roots.with_env())
+
+
+def committed_tree(tmp_roots):
+    repo = make_repo(tmp_roots.root)
+    save(repo, {f"sw/{k}": v for k, v in FROZEN.items()}, 1000)
+    return repo
+
+
+def test_freeze_prints_but_never_tags(tmp_roots):
+    repo = committed_tree(tmp_roots)
+    before_tags, before_log = tags(repo), git(repo, "log", "--format=%H").stdout
+    r = run_freeze(tmp_roots, repo, "--tag", "sweep-freeze-test")
+    assert r.returncode == 0, r.stderr
+    # K5: git tag -l is unchanged, nothing was staged or committed, and the command is printed for a person
+    assert tags(repo) == before_tags == []
+    assert git(repo, "log", "--format=%H").stdout == before_log
+    assert git(repo, "status", "--porcelain").stdout.split() == [
+        "??",
+        "sw/config/",
+    ]  # the record only, untracked
+    assert (
+        '  git tag -a sweep-freeze-test -m "Sweep Sheet freeze"'
+        in r.stdout.splitlines()
+    )
+    assert "Nothing was staged, committed or tagged" in r.stdout
+    # the record: the tag name the launcher copies into run.json, and the sha256 of every frozen file
+    rec = json.loads((repo / "sw" / "config" / "freeze.json").read_text())
+    assert (
+        rec["schema"] == "sweep-freeze/1" and rec["freeze_tag"] == "sweep-freeze-test"
+    )
+    assert rec["files"] == {
+        k: hashlib.sha256(v.encode()).hexdigest() for k, v in sorted(FROZEN.items())
+    }
+
+
+def test_freeze_refuses_files_that_are_not_committed_as_they_are(tmp_roots):
+    repo = committed_tree(tmp_roots)
+    (repo / "sw" / "sweep" / "words.py").write_text(
+        "WORDS = ('changed',)\n"
+    )  # a change after the commit
+    r = run_freeze(tmp_roots, repo)
+    assert r.returncode == 3 and "E_UNCOMMITTED" in r.stderr and "words.py" in r.stderr
+    assert not (repo / "sw" / "config" / "freeze.json").exists() and tags(repo) == []
+    git(repo, "checkout", "--", "sw/sweep/words.py")
+    (repo / "sw" / "briefs" / "extra.txt").write_text(
+        "not committed\n"
+    )  # a new frozen file that was never committed
+    r = run_freeze(tmp_roots, repo)
+    assert r.returncode == 3 and "extra.txt" in r.stderr
+
+
+def test_freeze_needs_every_frozen_file_and_a_sane_path(tmp_roots, tmp_path):
+    repo = committed_tree(tmp_roots)
+    (repo / "sw" / "sweep" / "rank.py").unlink()
+    r = run_freeze(tmp_roots, repo)
+    assert r.returncode == 2 and "E_MISSING" in r.stderr
+    r = subprocess.run(
+        ["bash", str(FREEZE), "--sw", "/etc"],
+        capture_output=True,
+        text=True,
+        env=tmp_roots.with_env(),
+    )
+    assert r.returncode == 2 and "E_OVERRIDE" in r.stderr
+    r = subprocess.run(
+        [
+            "bash",
+            str(FREEZE),
+            "--sw",
+            str(repo / "sw"),
+            "--out",
+            "/var/tmp/sw-freeze-refused.json",
+        ],
+        capture_output=True,
+        text=True,
+        env=tmp_roots.with_env(),
+    )
+    assert r.returncode == 2 and "E_NOT_WRITABLE" in r.stderr
+
+
+def test_gitcheck_probe_and_the_bin_folder_is_clean(tmp_path):
+    # the check is not vacuous: a file with a git add line is reported
+    probe = tmp_path / "probe.sh"
+    probe.write_text("#!/bin/bash\ngit add -A\n")
+    assert gitcheck(tmp_path) == [f"{probe}:2:git add -A"]
+    # a sandbox directory variable, a printed line and a comment are allowed
+    probe.write_text(
+        'git -C "$SBT" add -A -f\nprintf "  git tag -a x"\n# git push\n  echo "git commit"\n'
+    )
+    assert gitcheck(tmp_path) == []
+    assert (
+        gitcheck(SW / "bin") == []
+    )  # no script of the harness stages, commits, tags or pushes except in a sandbox
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/tests/test_open_checks.py b/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/tests/test_open_checks.py
new file mode 100644
index 000000000..09f157e7d
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/tests/test_open_checks.py
@@ -0,0 +1,153 @@
+"""bin/open-manual-checks.sh (TESTING section 6 item 4) and bin/check-sandbox-gt.sh (REQ-34, the real-run check)."""
+
+import json
+import re
+import subprocess
+
+from helpers import SW
+from panel_support import make_world
+
+OPEN = SW / "bin" / "open-manual-checks.sh"
+SANDBOX_GT = SW / "bin" / "check-sandbox-gt.sh"
+
+
+def open_checks(roots, *extra):
+    r = subprocess.run(
+        ["bash", str(OPEN), *map(str, extra)],
+        capture_output=True,
+        text=True,
+        env=roots.with_env(),
+    )
+    assert r.returncode == 0, r.stderr  # it reports; it never gates
+    return r.stdout.splitlines()
+
+
+def test_open_records_are_listed_for_this_tree(tmp_roots):
+    lines = open_checks(tmp_roots)
+    open_ids = [
+        m.group(1) for m in (re.match(r"OPEN (\S+?): ", ln) for ln in lines) if m
+    ]
+    assert lines[-1] == f"open: {len(open_ids)}"
+    # nothing of the manual side has been done in this build: the eight swap tests, the authors file, the second reader,
+    # the owner values, the spike, the attestations
+    for n in range(1, 9):
+        assert f"swap:C{n}" in open_ids
+    for want in (
+        "recall-authors",
+        "readme-second-reader",
+        "owner-values",
+        "spike",
+        "gt-attestation",
+        "attest:freeze-order",
+        "attest:prereg-order",
+        "attest:report-claims",
+        "model-stage-ablation",
+    ):
+        assert want in open_ids, want
+
+
+def test_closing_records_removes_them_from_the_list(tmp_roots, tmp_path):
+    tree = tmp_path / "tree"
+    for n in range(1, 9):
+        (tree / "cards").mkdir(parents=True, exist_ok=True)
+        (tree / "cards" / f"C{n}.json").write_text(
+            json.dumps({"swap_test": {"reviewer": "A. Second", "date": "2026-11-20"}})
+        )
+    (tree / "cards" / "README.md").write_text(
+        "- Second reader of this table: reader: B, date: 2026-11-21. Status: DONE.\n"
+    )
+    (tree / "fixtures" / "recall").mkdir(parents=True)
+    (tree / "fixtures" / "recall" / "AUTHORS.md").write_text(
+        "Seeded by A. Second, who had not read the extractors.\n"
+    )
+    (tree / "config").mkdir()
+    (tree / "config" / "prereg.json").write_text(json.dumps({"owner_confirmed": True}))
+    (tree / "config" / "values.json").write_text(
+        json.dumps({"spike": {"runs": 5, "c_luna": 2.0}})
+    )
+    (tree / "config" / "attestation.md").write_text("signed\n")
+    (tree / "results").mkdir()
+    ids = (
+        "freeze-order",
+        "prereg-order",
+        "report-measured-values",
+        "report-headline",
+        "report-claims",
+    )
+    (tree / "results" / "attestations.md").write_text(
+        "\n".join(f"ATTEST {i}: C. Reader, 2026-11-22, confirmed" for i in ids) + "\n"
+    )
+    lines = open_checks(tmp_roots, "--sw", tree)
+    assert lines == [
+        "OPEN model-stage-ablation: not run: 8 extra arms and 96 panel runs outside the run budget; an owner decision (DD-13)",
+        "open: 1",
+    ]
+    # one record reopened: the attestation line for the claims is missing again, and a card loses its signature
+    (tree / "results" / "attestations.md").write_text(
+        "\n".join(f"ATTEST {i}: C. Reader, 2026-11-22, confirmed" for i in ids[:-1])
+        + "\n"
+    )
+    (tree / "cards" / "C3.json").write_text(
+        json.dumps({"swap_test": {"reviewer": "", "date": ""}})
+    )
+    lines = open_checks(tmp_roots, "--sw", tree)
+    assert [ln.split(":")[0] for ln in lines[:-1]] == [
+        "OPEN swap",
+        "OPEN attest",
+        "OPEN model-stage-ablation",
+    ] and lines[-1] == "open: 3"
+    assert (
+        subprocess.run(
+            ["bash", str(OPEN), "--sw", "/etc"],
+            capture_output=True,
+            text=True,
+            env=tmp_roots.with_env(),
+        ).returncode
+        == 2
+    )
+
+
+def test_sandbox_ground_truth_check_is_clean_over_built_sandboxes(tmp_roots):
+    w = make_world(
+        tmp_roots
+    )  # F-REPO with its trap file named ground-truth.json, built into a sandbox by build-sandbox.sh
+    r = w.run("SS", "ss")  # a run that has prepass/sheets
+    assert r.returncode == 0, r.stderr
+    assert (r.dir / "prepass" / "sheets").is_dir()
+    cmd = [
+        "bash",
+        str(SANDBOX_GT),
+        "--sb",
+        str(tmp_roots.sb),
+        "--runs",
+        str(tmp_roots.runs),
+    ]
+    out = subprocess.run(cmd, capture_output=True, text=True, env=tmp_roots.with_env())
+    assert (out.returncode, out.stdout, out.stderr) == (
+        0,
+        "",
+        "",
+    )  # exits 0 with no output
+    # a ground-truth file in the sandbox, and a field name in a sheet, are found
+    (w.sandbox / "ground-truth.json").write_text("{}\n")
+    out = subprocess.run(cmd, capture_output=True, text=True, env=tmp_roots.with_env())
+    assert (
+        out.returncode == 1
+        and f"{w.sandbox}/ground-truth.json: a file named like ground truth"
+        in out.stdout
+    )
+    (w.sandbox / "ground-truth.json").unlink()
+    sheet = next((r.dir / "prepass" / "sheets").glob("*.md"))
+    sheet.write_text(sheet.read_text() + "\nplan_quote: x\n")
+    out = subprocess.run(cmd, capture_output=True, text=True, env=tmp_roots.with_env())
+    assert (
+        out.returncode == 1 and f"{sheet}:" in out.stdout and "plan_quote" in out.stdout
+    )
+    # no sandbox at all: nothing could be checked, which is not a pass
+    none = subprocess.run(
+        ["bash", str(SANDBOX_GT), "--sb", str(tmp_roots.root / "empty")],
+        capture_output=True,
+        text=True,
+        env=tmp_roots.with_env(),
+    )
+    assert none.returncode == 2 and "E_NO_SANDBOX" in none.stderr
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/tests/test_order.py b/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/tests/test_order.py
new file mode 100644
index 000000000..b371609d8
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet/tests/test_order.py
@@ -0,0 +1,243 @@
+"""REQ-33, REQ-36, REQ-44: bin/check-order.sh compares commit times and hashes in a temporary repository.
+Commit times are set by the tests (the times below are epoch seconds), so the order is exact."""
+
+import hashlib
+import json
+import os
+import subprocess
+from types import SimpleNamespace
+
+from helpers import SW
+from order_support import FROZEN, make_repo, mark, save, write
+
+CHECK = SW / "bin" / "check-order.sh"
+FREEZE = SW / "bin" / "freeze.sh"
+GT_FILE = '{"items": []}\n'
+GT_PATH = "sw/holdout-gt/HO-1/ground-truth.json"
+
+
+def sub(roots, name):
+    """Another root under the test's folder, so that one test can hold several repositories."""
+    p = roots.root / name
+    p.mkdir()
+    return SimpleNamespace(root=p, with_env=roots.with_env)
+
+
+def check(roots, mode, **kw):
+    cmd = ["bash", str(CHECK), mode]
+    for k, v in kw.items():
+        cmd += [f"--{k.replace('_', '-')}", str(v)]
+    return subprocess.run(cmd, capture_output=True, text=True, env=roots.with_env())
+
+
+def run_freeze(roots, tree, tag):
+    out = tree / "config" / "freeze.json"
+    r = subprocess.run(
+        ["bash", str(FREEZE), "--sw", str(tree), "--out", str(out), "--tag", tag],
+        capture_output=True,
+        text=True,
+        env=roots.with_env(),
+    )
+    assert r.returncode == 0, r.stderr
+    return out
+
+
+def frozen_repo(roots, tag_time=1100, tag="sweep-freeze-test", tagged=True):
+    """A repository with the frozen files committed at 1000, freeze.json (made by bin/freeze.sh) committed and, unless
+    `tagged` is False, tagged at `tag_time`. Returns (repo, freeze.json path)."""
+    repo = make_repo(roots.root)
+    save(repo, {f"sw/{k}": v for k, v in FROZEN.items()}, 1000)
+    out = run_freeze(roots, repo / "sw", tag)
+    save(repo, {}, tag_time, "freeze record")
+    if tagged:
+        mark(repo, tag, tag_time)
+    return repo, out
+
+
+def freeze_args(repo, freeze):
+    return {"repo": repo, "freeze": freeze, "gt": repo / "sw" / "holdout-gt"}
+
+
+def test_freeze_tag_before_gt_commit(tmp_roots):
+    repo, freeze = frozen_repo(tmp_roots)
+    save(repo, {GT_PATH: GT_FILE}, 2000)  # the hold-out author writes it after the tag
+    r = check(tmp_roots, "freeze", **freeze_args(repo, freeze))
+    assert r.returncode == 0, r.stderr
+    assert (
+        "ORDER_OK freeze: tag sweep-freeze-test (1100) is earlier than the first ground-truth commit (2000)"
+        in r.stdout
+    )
+
+
+def test_gt_before_tag_fails(tmp_roots):
+    repo = make_repo(tmp_roots.root)
+    save(repo, {GT_PATH: GT_FILE}, 500)  # the ground truth first: the wrong order
+    save(repo, {f"sw/{k}": v for k, v in FROZEN.items()}, 1000)
+    freeze = run_freeze(tmp_roots, repo / "sw", "late")
+    save(repo, {}, 1100)
+    mark(repo, "late", 1100)
+    r = check(tmp_roots, "freeze", **freeze_args(repo, freeze))
+    assert (
+        r.returncode == 1
+        and "(1100) is not earlier than the first ground-truth commit (500)" in r.stderr
+    )
+    # the same time is not earlier either: the order cannot be shown
+    same_root = sub(tmp_roots, "same")
+    repo2, freeze2 = frozen_repo(same_root, tag_time=1100)
+    save(repo2, {GT_PATH: GT_FILE}, 1100)
+    r = check(tmp_roots, "freeze", **freeze_args(repo2, freeze2))
+    assert (
+        r.returncode == 1
+        and "(1100) is not earlier than the first ground-truth commit (1100)"
+        in r.stderr
+    )
+
+
+def test_freeze_needs_the_tag_and_a_committed_ground_truth(tmp_roots):
+    repo, freeze = frozen_repo(tmp_roots, tagged=False)
+    write(repo, {GT_PATH: GT_FILE})  # written, not committed
+    args = freeze_args(repo, freeze)
+    r = check(tmp_roots, "freeze", **args)
+    assert (
+        r.returncode == 1 and "freeze tag sweep-freeze-test does not exist" in r.stderr
+    )
+    mark(repo, "sweep-freeze-test", 1100)
+    r = check(tmp_roots, "freeze", **args)
+    assert (
+        r.returncode == 1 and "is not committed" in r.stderr
+    )  # an uncommitted ground truth shows no order
+    r = check(tmp_roots, "freeze", **{**args, "freeze": repo / "nope.json"})
+    assert r.returncode == 2 and "no freeze record" in r.stderr
+    assert check(tmp_roots, "nonsense").returncode == 2
+
+
+def test_freeze_json_hashes_match_files(tmp_roots):
+    repo, freeze = frozen_repo(tmp_roots)
+    save(repo, {GT_PATH: GT_FILE}, 2000)
+    args = freeze_args(repo, freeze)
+    assert check(tmp_roots, "freeze", **args).returncode == 0
+    # an extractor changed after the freeze, committed or not: the hash check fails
+    write(repo, {"sw/sweep/extractors.py": "EXTRACTORS = {'E1': 1}\n"})
+    r = check(tmp_roots, "freeze", **args)
+    assert (
+        r.returncode == 1 and "sweep/extractors.py changed after the freeze" in r.stderr
+    )
+    assert "cards/C1.json" not in r.stderr  # only the changed file is named
+    save(repo, {}, 2100, "extractor edit")
+    assert check(tmp_roots, "freeze", **args).returncode == 1
+    write(
+        repo, {"sw/sweep/extractors.py": FROZEN["sweep/extractors.py"]}
+    )  # restored: the recorded hash holds again
+    assert check(tmp_roots, "freeze", **args).returncode == 0
+    rec = json.loads(freeze.read_text())
+    assert (
+        rec["files"]["sweep/extractors.py"]
+        == hashlib.sha256(FROZEN["sweep/extractors.py"].encode()).hexdigest()
+    )
+
+
+def prereg_repo(roots, gt_hash=None, prereg_time=100):
+    repo = make_repo(roots.root)
+    prereg = {
+        "schema": "sweep-prereg/1",
+        "ground_truth_sha256": {} if gt_hash is None else {"HO-1": gt_hash},
+    }
+    save(
+        repo,
+        {GT_PATH: GT_FILE, "sw/config/prereg.json": json.dumps(prereg)},
+        prereg_time,
+    )
+    return repo
+
+
+def prereg_args(repo):
+    return {
+        "repo": repo,
+        "prereg": repo / "sw" / "config" / "prereg.json",
+        "runs": repo / "sw" / "runs",
+        "gt_dir": repo / "sw" / "holdout-gt",
+    }
+
+
+def test_gt_hash_matches_prereg(tmp_roots):
+    good = hashlib.sha256(GT_FILE.encode()).hexdigest()
+    repo = prereg_repo(tmp_roots, gt_hash=good)
+    r = check(tmp_roots, "prereg", **prereg_args(repo))
+    assert r.returncode == 0, r.stderr
+    assert (
+        "the ground-truth hashes match" in r.stdout and "none has started" in r.stdout
+    )
+    # the ground truth is edited after it was hashed: the record no longer matches
+    write(repo, {GT_PATH: '{"items": [1]}\n'})
+    r = check(tmp_roots, "prereg", **prereg_args(repo))
+    assert r.returncode == 1 and "the ground truth of HO-1 has sha256" in r.stderr
+    # a hash that the record names for a document with no ground-truth file
+    (repo / GT_PATH).unlink()
+    r = check(tmp_roots, "prereg", **prereg_args(repo))
+    assert r.returncode == 1 and "no ground-truth file for HO-1" in r.stderr
+    # prereg.json that was never committed shows no order
+    other = make_repo(sub(tmp_roots, "uncommitted").root)
+    write(other, {"sw/config/prereg.json": "{}\n"})
+    r = check(tmp_roots, "prereg", **prereg_args(other))
+    assert r.returncode == 1 and "is not committed" in r.stderr
+
+
+def test_prereg_commit_before_first_run(tmp_roots):
+    repo = prereg_repo(tmp_roots, prereg_time=100)
+    save(repo, {"sw/runs/stage1/r1/run.json": "{}\n"}, 200)
+    r = check(tmp_roots, "prereg", **prereg_args(repo))
+    assert (
+        r.returncode == 0 and "is earlier than the first run.json (200)" in r.stdout
+    ), r.stderr
+    # the first commit of any run.json counts: a second run committed at 150 is the first
+    save(repo, {"sw/runs/stage1/r0/run.json": "{}\n"}, 150)
+    r = check(tmp_roots, "prereg", **prereg_args(repo))
+    assert r.returncode == 0 and "(150)" in r.stdout
+    # the other order, and equal times (the order cannot be shown)
+    late = prereg_repo(sub(tmp_roots, "late"), prereg_time=300)
+    save(late, {"sw/runs/stage1/r1/run.json": "{}\n"}, 300)
+    r = check(tmp_roots, "prereg", **prereg_args(late))
+    assert (
+        r.returncode == 1 and "is not earlier than the first run.json (300)" in r.stderr
+    )
+    early = prereg_repo(sub(tmp_roots, "early"), prereg_time=300)
+    save(
+        early, {"sw/runs/stage1/r1/run.json": "{}\n"}, 50
+    )  # a run committed before prereg.json
+    r = check(tmp_roots, "prereg", **prereg_args(early))
+    assert r.returncode == 1 and "(50)" in r.stderr
+    # runs that are not committed are timed by their file times
+    plain = prereg_repo(sub(tmp_roots, "plain"), prereg_time=1000)
+    run = plain / "sw" / "runs" / "stage1" / "r1" / "run.json"
+    write(plain, {"sw/runs/stage1/r1/run.json": "{}\n"})
+    os.utime(run, (500, 500))  # the run file is older than prereg.json
+    r = check(tmp_roots, "prereg", **prereg_args(plain))
+    assert r.returncode == 1 and "(500)" in r.stderr
+    os.utime(run, (5000, 5000))
+    assert check(tmp_roots, "prereg", **prereg_args(plain)).returncode == 0
+
+
+def test_every_planted_plan_has_twin(tmp_path, tmp_roots):
+    d = tmp_path / "planted"
+    d.mkdir()
+    for name in ("p1.md", "p1-clean.md", "p2.md", "p2-clean.md"):
+        (d / name).write_text("text\n")
+    manifest = d / "manifest.json"
+    entries = [
+        {"plan": "p1.md", "twin": "p1-clean.md"},
+        {"plan": "p2.md", "twin": "p2-clean.md"},
+    ]
+    manifest.write_text(json.dumps({"planted": entries}))
+    r = check(tmp_roots, "twins", manifest=manifest)
+    assert r.returncode == 0 and "all 2 planted plans have an existing twin" in r.stdout
+    (d / "p2-clean.md").unlink()  # a twin that is named but missing
+    r = check(tmp_roots, "twins", manifest=manifest)
+    assert (
+        r.returncode == 1 and "the twin p2-clean.md of p2.md does not exist" in r.stderr
+    )
+    manifest.write_text(
+        json.dumps({"planted": [{"plan": "p3.md"}]})
+    )  # a planted plan with no twin at all
+    r = check(tmp_roots, "twins", manifest=manifest)
+    assert r.returncode == 1 and "planted plan p3.md has no clean twin" in r.stderr
+    assert check(tmp_roots, "twins").returncode == 2

Codegraph context: index_state: fresh; checked_at: 2026-11-14T20:52:06Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel; projectPath: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel. Call codegraph only when index_state: fresh, never to widen scope. Q2b: the files this task changed are new files that the graph does not index (shell, new Python, Markdown) plus small additions to existing test files; the dependents of the changed symbols were searched with Grep and no dependent outside the diff was found.
Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): 

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
