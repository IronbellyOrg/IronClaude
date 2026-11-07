76c8e162fa691dc0e348ea9c9dbfcd29d649431e
Review one task for spec compliance.

Task brief: ## Task 1: Append `merge_state` to the poll JSON line in `poll-ci-checks.sh`

Satisfies: R-001, R-009 (poll script rows).

Edit `src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh` (pr mode only; evidence mode is untouched).

- Add `mergeable,mergeStateStatus` to the `--json` field list of both `gh pr view "$PR" --repo "$REPO"` calls (`PR_JSON` at line 71 and `PR_AFTER` at line 108). Keep `--repo "$REPO"` on every `gh` line.
- The early-return payload (first `gh pr view` fails, line 73) becomes `{pr, head_sha:"", source:"ci", state:"polling", checks:[], merge_state:{mergeable:"", status:""}}`.
- The final `jq` output (lines 115 to 118) appends `merge_state:{mergeable:(.mergeable // ""), status:(.mergeStateStatus // "")}` after `checks`, read from the latest `PR_JSON` (the re-sampled one when it succeeded). The existing keys keep their names, values and order.
- Update the header comment block (the Output lines 8 to 9 only) to document the key; line 16 of the script (the comment line that quotes `gh pr checks --json`) is the key of an inventory row in `tests/skills/test_worker_contract.py` and stays byte-identical. The new comment must not contain the word "force" (any case) or the literal text `gh pr checks --repo`, and must not mention `gh pr` or `gh api`.
- In `tests/skills/test_worker_contract.py` replace the inventory rows keyed to the old `PR_JSON=...` (row near line 1806) and `PR_AFTER=...` (row near line 1838) lines of `poll-ci-checks.sh` with rows for the new lines, using the same `never-worker` classification and reason text as the neighbouring rows. Delete rows whose lines no longer exist.

Acceptance criteria (ids):
T1.AC1: With a stub where `gh pr view` returns `"mergeable":"CONFLICTING","mergeStateStatus":"DIRTY"`, `poll-ci-checks.sh --pr N --repo R` prints one JSON line whose keys are, in order, `pr`, `head_sha`, `source`, `state`, `checks`, `merge_state`, and `merge_state` is `{"mergeable":"CONFLICTING","status":"DIRTY"}`.
T1.AC2: When the first `gh pr view` fails the printed line has `merge_state` with two empty strings and the script exits 0.
T1.AC3: `uv run pytest tests/skills/test_worker_contract.py tests/pr_submit/test_static_grep.py tests/pr_submit/test_conflict_sync_protocol.py tests/pr_submit/test_conflict_scripts.py -q` passes, including `test_every_write_verb_hit_is_classified`, `test_classification_table_has_no_stale_entries`, `test_gh_command_lines_are_repo_scoped` and `test_poll_ci_evidence_mode_static_rules`.
Global constraints: 
- Edit canonical sources under `src/superclaude/` only, then run `make sync-dev`; the `.claude/` mirrors are generated and are never staged.
- Use `uv run ...` for every Python and pytest call; no bare `python` or `pip`.
- `src/superclaude/pr_submit/fsm.py`, `run_log.py`, `models.py` and `ci.py` are not edited, no new `EventType` is added and every existing push-safety rule stays as it is (R-003, R-004).
- `src/superclaude/pr_submit/conflicts.py` and `src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md` are in the core-pure file set of `tests/pr_submit/test_static_grep.py`: neither may contain the standalone words `gh` or `git` on any line, comments and docstrings included.
- Several tests pin exact lines of the files this plan edits: `tests/skills/test_worker_contract.py` (an inventory keyed by exact file line, with a stale-entry check), `tests/pr_submit/test_conflict_sync_protocol.py` (fragments E1 to E13, order pins) and `tests/pr_submit/test_static_grep.py`. Each task that changes a pinned line updates the pin in the same task. The router outcomes any prose describes are the table in R-005 of `./source.md`, which `_WAVE8A_ROWS` in `tests/pr_submit/test_conflicts_core.py` already pins, so no router row is added anywhere in this plan.
- Every new prose deliverable gets its own positive assertion scoped to that text (R-012 part d), so that removing only that text fails exactly that assertion.
- Non-goal: the go/no-go gate of the issue (one real run where the base moved, or a maintainer waiver) is a release sign-off item and stays open (R-014). Nothing in this plan runs against a real PR.
- Non-goal: `.dev/brainstorms/issue-305-pr-submit-conflict-resolution/merged-requirements.md` and `.dev/designs/issue-305-pr-submit-conflict-resolution/DESIGN.md` are historical records and are not edited.
- Owner authorization (2026-11-07, relayed by the coordinator): after the third advisory review left two word-level blocking findings (the "unconditional" end-of-wait re-read in R-010 and Task 7, and the over-general status bullet in R-005), the owner allowed word edits to `./source.md` and this plan, with the listed minor guardrails, and no fourth review. The corrections are in R-005, R-010, Task 7 and the guardrails of Tasks 1, 2, 6, 7, 9 and 10; the report is `.dev/reflect/pre-TASK-WF-p3Requirements-20261107-070713-20261107070932/REPORT.md`.
Start sha: 76c8e162fa691dc0e348ea9c9dbfcd29d649431e
Diff against the start snapshot: 
diff --git a/src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh b/src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh
index 340101ea..2706c88f 100755
--- a/src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh
+++ b/src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh
@@ -6,7 +6,10 @@
 # Usage   : poll-ci-checks.sh --pr <N> [--repo <owner/repo>]
 #           poll-ci-checks.sh --evidence-sha <40hex> [--repo <owner/repo>]
 # Output  : one line of JSON: {"pr":N,"head_sha":"...","source":"ci",
-#           "state":"polling|clean|findings","checks":[...]}
+#           "state":"polling|clean|findings","checks":[...],
+#           "merge_state":{"mergeable":"...","status":"..."}} where the two
+#           strings are GitHub's mergeable and mergeStateStatus values ("" when
+#           the read failed); the late-conflict trigger reads them (issue #361).
 #           Evidence mode (no --pr needed) reads the commit's check runs and
 #           commit statuses: {"evidence_sha":"<sha>","evidence_checks":N,"source":"ci"}
 #           with N = check runs + statuses, or -1 when either read fails or does
@@ -68,9 +71,9 @@ case "$CHECKS_HELP" in
     *) die "installed gh lacks 'gh pr checks --json' (see 'gh --version'); upgrade gh and confirm via 'gh pr checks --help' before CI wait" 2 ;;
 esac
 
-PR_JSON="$(gh pr view "$PR" --repo "$REPO" --json number,url,headRefOid 2>/dev/null || true)"
+PR_JSON="$(gh pr view "$PR" --repo "$REPO" --json number,url,headRefOid,mergeable,mergeStateStatus 2>/dev/null || true)"
 if [ -z "$PR_JSON" ]; then
-    jq -nc --argjson pr "$PR" '{pr:$pr, head_sha:"", source:"ci", state:"polling", checks:[]}'
+    jq -nc --argjson pr "$PR" '{pr:$pr, head_sha:"", source:"ci", state:"polling", checks:[], merge_state:{mergeable:"", status:""}}'
     exit 0
 fi
 
@@ -105,7 +108,7 @@ fi
 
 # Re-sample head after checks so a mid-poll push cannot pair new checks with an old SHA.
 HEAD1="$(printf '%s' "$PR_JSON" | jq -r '.headRefOid // empty')"
-PR_AFTER="$(gh pr view "$PR" --repo "$REPO" --json number,url,headRefOid 2>/dev/null || true)"
+PR_AFTER="$(gh pr view "$PR" --repo "$REPO" --json number,url,headRefOid,mergeable,mergeStateStatus 2>/dev/null || true)"
 [ -n "$PR_AFTER" ] && PR_JSON="$PR_AFTER"
 HEAD2="$(printf '%s' "$PR_JSON" | jq -r '.headRefOid // empty')"
 if [ -n "$HEAD1" ] && [ -n "$HEAD2" ] && [ "$HEAD1" != "$HEAD2" ]; then
@@ -115,6 +118,7 @@ fi
 printf '%s' "$PR_JSON" | jq -c \
     --arg state "$STATE" \
     --argjson checks "$CHECKS_JSON" \
-    '{pr:.number, head_sha:.headRefOid, source:"ci", state:$state, checks:$checks}'
+    '{pr:.number, head_sha:.headRefOid, source:"ci", state:$state, checks:$checks,
+      merge_state:{mergeable:(.mergeable // ""), status:(.mergeStateStatus // "")}}'
 
 exit 0
diff --git a/tests/skills/test_worker_contract.py b/tests/skills/test_worker_contract.py
index bb01c70c..4ec2e722 100644
--- a/tests/skills/test_worker_contract.py
+++ b/tests/skills/test_worker_contract.py
@@ -1805,7 +1805,7 @@ WRITE_VERB_CLASSIFICATION = {
     (
         "src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh",
         "gh pr",
-        'PR_JSON="$(gh pr view "$PR" --repo "$REPO" --json number,url,headRefOid 2>/dev/null || true)"',
+        'PR_JSON="$(gh pr view "$PR" --repo "$REPO" --json number,url,headRefOid,mergeable,mergeStateStatus 2>/dev/null || true)"',
     ): (
         "never-worker",
         "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
@@ -1837,7 +1837,7 @@ WRITE_VERB_CLASSIFICATION = {
     (
         "src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh",
         "gh pr",
-        'PR_AFTER="$(gh pr view "$PR" --repo "$REPO" --json number,url,headRefOid 2>/dev/null || true)"',
+        'PR_AFTER="$(gh pr view "$PR" --repo "$REPO" --json number,url,headRefOid,mergeable,mergeStateStatus 2>/dev/null || true)"',
     ): (
         "never-worker",
         "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",

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
