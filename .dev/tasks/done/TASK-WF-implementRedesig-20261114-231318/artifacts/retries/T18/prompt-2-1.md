dcbafbbbb2b98561998d2d5745447d43b70d1275
Review one task for spec compliance.

Task brief: ## Task 18: Write the freeze, order, sandbox-check, parity and open-checks scripts

Depends on: Task 17

Follow `RL/IMPLEMENTATION.md` step 7 (last five scripts), `RL/DESIGN.md` sections 11.1, 3.5 and K5, and `RL/TESTING.md` REQ-33, REQ-34, REQ-36, REQ-44 and section 4. Create `RL/bin/freeze.sh` (hashes `recipes/recipes.json`, `recipes/rl-block.txt`, `recipes/search-form.txt`, `config/lenses.json`, the cards, the briefs and `rl/*.py` into `config/freeze.json`, prints the `git tag` command and never runs it; K5), `RL/bin/check-order.sh` (`freeze`: tag commit time earlier than the first commit of a ground-truth file, and the hash check; `prereg`: `prereg.json` commit earlier than the first `run.json`), `RL/bin/check-sandbox-gt.sh` (`grep -r` for ground-truth file names and field names over every sandbox under `/tmp/evalsb-recipe` and every `RUN/briefs`, prints nothing when clean, exits non-zero on a hit, never prints file content), `RL/bin/check-z0-parity.sh <doc>` (renders the Z0 brief with the copied code and prints its sha256), `RL/bin/open-manual-checks.sh` (lists the manual records still open, plus `ran-audit` printing 20 spike rows with their transcripts). Write `RL/tests/test_freeze.py::test_freeze_prints_but_never_tags`, `RL/tests/test_order.py` (`test_freeze_tag_before_gt_commit`, `test_gt_before_tag_fails`, `test_freeze_json_hashes_match_files`, `test_gt_hash_matches_prereg`, `test_every_planted_plan_has_twin`, `test_prereg_commit_before_first_run`, using a temporary git repository and synthetic files only) and `RL/tests/test_check_scripts.py` (`test_sandbox_gt_check_finds_a_planted_trap_and_is_silent_when_clean`, `test_z0_parity_prints_a_stable_hash`, `test_open_manual_checks_lists_open_records`).


Acceptance criteria (ids added by the orchestrator, in source order):
T18.AC1: `$T $RL/tests/test_freeze.py $RL/tests/test_order.py $RL/tests/test_check_scripts.py -q` exits 0.
T18.AC2: `git tag -l` is unchanged after running `bin/freeze.sh`.
T18.AC3: `bin/check-order.sh freeze` exits 0 only when the tag commit is earlier than the first ground-truth commit in the temporary repository.
T18.AC4: `bin/open-manual-checks.sh` lists the open M records (REQ-08 recipe reviews, REQ-28 ran audit, REQ-31 report read, REQ-32 timing spike, REQ-33, REQ-36, REQ-40, REQ-41 bands, REQ-44, REQ-45, REQ-38 content review, REQ-35 model-stage ablation).

Global constraints: ## Constraints

Path names used by every task (all repo-relative to the checkout root `REPO`, which is `git rev-parse --show-toplevel`):

- `RL` is `.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger`. It holds `DESIGN.md`, `TESTING.md`, `IMPLEMENTATION.md` and `SHARED-MANIFEST-DESIGN-TIME.tsv`, which are the specification and are never edited by the build.
- `SW` is `.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet`, the sibling build (Redesign 1). It is read only: no task writes, edits, moves or deletes anything under it, and no task runs a script or a test from inside it.
- `MR` is `.dev/brainstorms/20261113-223124-panel-process-redesign/merged-requirements.md` (sections 3.0, 3.2, 5 and 6 are the requirements source; the design documents already map them). `EVAL` is `.dev/eval-workspaces/tasklist-review-panel/20261111-a1` (read only).
- Design ids: `K1` to `K9` (constraints), `DR-1` to `DR-16` (decisions) and `REQ-nn` (requirements) are those of `RL/DESIGN.md` sections 1.2 and 1.3 and of `RL/TESTING.md` section 3.

Scope rules that hold for every task:

- Create or edit files only under `RL`, plus scratch under `/tmp` (sandboxes under `/tmp/evalsb-recipe`, scratch under `/tmp/rl-*`). Nothing under `src/`, `tests/`, `.claude/`, any existing folder under `.dev/tasks/`, `SW`, `EVAL`, `.dev/eval-workspaces/tasklist-review-panel/20261113-collab` or any other folder is changed.
- No task runs `git commit` or `git push`, and no task runs `git add` for a path under `RL`. The freeze tag (K5) is only printed, never created.
- No task opens, reads, greps the content of or copies any `ground-truth*.json`, score file or judge output of a study package, and no recipe, card, brief, fixture, regex or example uses a study answer. Fixtures are invented. Tests that need ground truth use the synthetic `RL/fixtures/gt/` files only. The tests marked `freeze` (they read the real ground truth or need a second author's records) are never run by this build.
- Python runs only through uv. No `python -m`, no bare `pip`. No code folder is named `lib/` (K7).
- No reviewer or judge session is started and no network call is made. Tests use the fake `claude` at `RL/tests/fakes/claude`. If a task ever needed a model it would use `claude-sonnet-5-5` or `claude-haiku-5-5`; Opus is only the blind judge script's model; never Qwen or glm.
- Files under `RL/scaffold/`, `RL/cards/`, `RL/briefs/`, `RL/bin/common.sh`, `RL/bin/build-sandbox.sh` and the copied tests are copies of sibling files and are never edited after the copy (DESIGN 3.1). A copied test that fails is reported, not edited.
- Shell variables used in task commands:

```
REPO=$(git rev-parse --show-toplevel)
RL=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger
SW=$REPO/.dev/eval-workspaces/tasklist-review-panel/20261114-sweep-sheet
MR=$REPO/.dev/brainstorms/20261113-223124-panel-process-redesign/merged-requirements.md
T="uv run --frozen --project $REPO pytest -p no:cacheprovider"
PYRUN="uv run --frozen --project $REPO python"
export PYTHONDONTWRITEBYTECODE=1 NOFALLBACK=1 SUPERCLAUDE_CODEGRAPH_AUTOINIT=0
```


Start sha: dcbafbbbb2b98561998d2d5745447d43b70d1275
Diff against the start snapshot: (the diff is 1129 lines; it is saved as a file: read /tmp/rl-impl/T18/diff2.patch with the Read tool, in parts. The files it touches exist on disk under the repo; read them as needed.)

Codegraph context: index_state: fresh; checked_at: 2026-11-15T03:24:25Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel; projectPath: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel
call codegraph only when index_state: fresh, never to widen scope
Q2b: this task changes no existing symbol; the files it creates are new, so there are no dependents outside the diff.

Delta diff from the previous reviewed tree (empty on the first review): diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/bin/check-sandbox-gt.sh b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/bin/check-sandbox-gt.sh
index 192f643e1..58af65602 100755
--- a/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/bin/check-sandbox-gt.sh
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/bin/check-sandbox-gt.sh
@@ -2,7 +2,8 @@
 # usage: check-sandbox-gt.sh [DIR ...]                                               (REQ-34, DESIGN 11.1 AO-6)
 # Reviewers never receive ground truth. This looks for it: a `grep -r` over every sandbox under the sandbox root
 # ($SW_SB_ROOT, default /tmp/evalsb-recipe) and over every RUN/briefs folder under the runs root ($RL_RUNS_ROOT, default
-# RL/runs), or over the folders named on the command line instead. It looks for
+# RL/runs; at any depth, so the spike runs runs/spike-timing/<run>/briefs and runs/spike-compliance/<run>/briefs count),
+# or over the folders named on the command line instead. It looks for
 #   * a file whose name starts with ground-truth, ground_truth or groundtruth, and
 #   * a file that holds a ground-truth file name (ground-truth*.json) or one of the ground-truth field names
 #     plan_quote and blocking_in_implement.
@@ -28,9 +29,12 @@ if [ $# -gt 0 ]; then
 else
   RUNS=${RL_RUNS_ROOT:-$SW/runs}
   [ ! -d "$SB" ] || DIRS+=("$SB")
-  for b in "$RUNS"/*/briefs; do
-    [ -d "$b" ] && DIRS+=("$b")
-  done
+  # every briefs folder at any depth: runs/<id>/briefs and the spike runs of bin/run-spike.sh, runs/spike-*/<run>/briefs
+  if [ -d "$RUNS" ]; then
+    while IFS= read -r b; do
+      DIRS+=("$b")
+    done < <(find "$RUNS" -name .git -prune -o -type d -name briefs -print | sort)
+  fi
 fi
 [ ${#DIRS[@]} -gt 0 ] || exit 0
 
diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/tests/test_check_scripts.py b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/tests/test_check_scripts.py
index 702ca81c5..14e882ce3 100644
--- a/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/tests/test_check_scripts.py
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/tests/test_check_scripts.py
@@ -97,6 +97,23 @@ def test_sandbox_gt_check_finds_a_planted_trap_and_is_silent_when_clean(tmp_path
     assert r.returncode == 0 and r.stdout == ""
 
 
+def test_sandbox_gt_check_searches_spike_run_briefs(tmp_path):
+    # bin/run-spike.sh writes runs/spike-timing/<run>/ and runs/spike-compliance/<run>/, one level deeper than runs/<id>/
+    clean_tree(tmp_path)
+    for spike, run_id in (
+        ("spike-timing", "timing-rl-1"),
+        ("spike-compliance", "compliance-1"),
+    ):
+        brief = tmp_path / "runs" / spike / run_id / "briefs" / "t2b-1.txt"
+        put(brief, "review the plan\n")
+        assert sh(SANDBOX_GT, tmp_path).stdout == ""
+        brief.write_text("check plan_quote here\n", encoding="utf-8")
+        r = sh(SANDBOX_GT, tmp_path)
+        assert r.returncode == 1 and r.stdout.strip() == str(brief)
+        brief.unlink()
+    assert sh(SANDBOX_GT, tmp_path).returncode == 0
+
+
 def test_sandbox_gt_check_is_silent_with_no_sandbox_at_all(tmp_path):
     r = sh(SANDBOX_GT, tmp_path)
     assert r.returncode == 0 and r.stdout == ""

Earlier blocking findings of this start (empty on the first review): F1.1 sev=blocking trigger=B4 ac=scope at=.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/bin/check-sandbox-gt.sh:31 anchor="every `RUN/briefs`" chk=n,n,n,y family=sandbox-gt-run-depth fix=find every `briefs` folder under the runs root (any depth) instead of only runs/<id>/briefs, and add a test that plants a trap in runs/spike-compliance/<run>/briefs/ covers="`RL/bin/check-sandbox-gt.sh` (`grep -r` for ground-truth file names and field names over every sandbox under `/tmp/evalsb-recipe` and every `RUN/briefs`" first=A1 origin=new: the loop `for b in "$RUNS"/*/briefs` finds only runs/<id>/briefs; bin/run-spike.sh writes spike runs to runs/spike-timing/<run>/briefs and runs/spike-compliance/<run>/briefs, which the script never searches; a planted `plan_quote` there printed nothing and exited 0; the test only plants at depth one (tests/test_check_scripts.py:67)
Saved-probe re-check hit locations (may be empty): bin/check-sandbox-gt.sh:4; bin/check-sandbox-gt.sh:36

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
