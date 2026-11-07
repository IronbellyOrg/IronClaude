a19cded4aa916fc7a49de082e19c5e0b36223905
Review one task for spec compliance.

Task brief: ## Task 6: Document the payload and the trigger in `refs/ci-poll.md`

Depends on: Task 1, Task 5

Satisfies: R-010 (`ci-poll.md`), R-009 (ci-poll rows), R-012 (part d).

Edit `src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md`.

- In "Poll surfaces" add `mergeable,mergeStateStatus` to the documented `gh pr view` field list and document the `merge_state` object (shape, empty strings when unavailable, appended after `checks`).
- Update the "Division of labour" bullet that says the script returns "a coarse `state` plus the raw `checks` array" so it names `merge_state`.
- Add a section "Late conflict trigger (P3)" after "Wave 8 entry": the trigger is `late_conflict_trigger(payload, wait_sha=...)` on every poll; it fires for a payload that carries a conflicting state, including a wait stuck at `polling` with no checks; it never changes `classify_checks`; `UNKNOWN`, missing values and a payload for another head never fire it. Reconcile the `pr_conflicting` skip sentence with the new section.
- The wait-only sentence pinned in `tests/pr_submit/test_static_grep.py` (lines 791 to 808) stays byte-identical, and the table row on line 28 of the ref that holds it stays on one line.
- In `tests/skills/test_worker_contract.py` replace or delete every inventory row whose keyed `refs/ci-poll.md` text changed (the `gh pr view <N> --repo <owner/repo> --json number,url,headRefOid` line row near 1654, and the line-21 paragraph row near 1223 to 1230 if that paragraph is reworded) and add a never-worker row for every new line of the ref that the scanner reports.

Acceptance criteria (ids):
T6.AC1: Four new assertions in `tests/pr_submit/test_static_grep.py`, each run on `_prose(path)` of the ref (the helper takes the file `Path`), pin separately: the documented `merge_state` shape, the updated "Division of labour" bullet, the reconciled `pr_conflicting` skip sentence, and the "Late conflict trigger (P3)" section heading together with its trigger sentence; removing only one of the four texts fails only its assertion.
T6.AC2: `uv run pytest tests/pr_submit/test_static_grep.py tests/skills/test_worker_contract.py tests/pr_submit/test_conflict_sync_protocol.py -q` passes, including the stale-entry check.
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
Start sha: a19cded4aa916fc7a49de082e19c5e0b36223905
Diff against the start snapshot: 
diff --git a/src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md b/src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md
index 795acf95..22136223 100644
--- a/src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md
+++ b/src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md
@@ -12,7 +12,7 @@ split keeps `gh` out of the deterministic core (NFR-6).
 ## Poll surfaces (FR-CI-2 / FR-CI-10 / FR-CI-11)
 
 ```bash
-gh pr view <N> --repo <owner/repo> --json number,url,headRefOid
+gh pr view <N> --repo <owner/repo> --json number,url,headRefOid,mergeable,mergeStateStatus
 gh pr checks <N> --repo <owner/repo> --required --json name,state,bucket,link,workflow
 # if that list is empty, fall back to:
 gh pr checks <N> --repo <owner/repo> --json name,state,bucket,link,workflow
@@ -20,6 +20,8 @@ gh pr checks <N> --repo <owner/repo> --json name,state,bucket,link,workflow
 
 No `conclusion` field — `gh pr checks --json` does not emit it. Empty, malformed, or multiple-document stdout is **not** a parsed empty array. A valid nonempty required list takes precedence; otherwise a valid all-checks list is used. If the chosen list is empty and either query failed to parse, emit `state:polling`, `checks:[]`; only two parsed empty arrays, with `expect_checks` false, justify `clean`; with `expect_checks` true an empty chosen list is `polling` (see Expected checks after a push). Pending exit 8 may still contain valid JSON — keep it.
 
+The poll line also carries `merge_state`, an object `{"mergeable": <string>, "status": <string>}` that holds GitHub's `mergeable` and `mergeStateStatus` values and is appended after `checks`; both strings are empty when the read failed, the early-return payload included. It is data only: `classify_checks` never reads it.
+
 ## Wave 8 entry (SKILL-owned, not an FSM edge)
 
 | Augment outcome | CI wait | CI fix |
@@ -29,7 +31,7 @@ No `conclusion` field — `gh pr checks --json` does not emit it. Empty, malform
 | `TERMINAL_AUGMENT_NO_RESPONSE` | Arm, wait-only; retain Augment status; report CI alongside. Never `transition(clean)` | No (the one Tier 1 sync push excepted) |
 | `HALT_HUMAN` / `VALIDATION_FAIL` / `TERMINAL_TIMEOUT` / `TERMINAL_FAILED` / L0 | Do not arm | No |
 
-When the PR is still conflicting and no merge commit was pushed, the SKILL skips the CI wait with reason `pr_conflicting`: GitHub runs no `pull_request` checks on a conflicting PR, so the lists would read empty.
+When the PR is still conflicting and no merge commit was pushed, the SKILL skips the CI wait with reason `pr_conflicting`: GitHub runs no `pull_request` checks on a conflicting PR, so the lists would read empty. A PR that turns conflicting while the wait runs is noticed through `merge_state` instead (see Late conflict trigger (P3) below), because its check lists may read empty or stay pending.
 
 The wait consumes no remediation round. A `polling` result (including a failed check query) continues at the configured interval until completion or `--timeout`. A non-zero script exit (e.g. `gh` without `pr checks --json`) is not `polling`: stop and report the missing prerequisite. The observed CI matrix has run longer than the 600s default, so a CI wait needs a `--timeout` sized to the full check run; never promise an indefinite wait. When `--required` returns a nonempty parsed list it is the chosen set; otherwise use the parsed all-checks list. Optional checks outside the chosen set do not block completion.
 
@@ -40,6 +42,10 @@ The wait consumes no remediation round. A `polling` result (including a failed c
 
 `bucket` values: `pass` | `fail` | `pending` | `skipping` | `cancel`.
 
+## Late conflict trigger (P3)
+
+On every poll the SKILL evaluates `superclaude.pr_submit.conflicts.late_conflict_trigger(payload, wait_sha=...)` before it acts on the classification. The trigger fires for a payload whose `merge_state` reads conflicting, including a wait stuck at `polling` with no checks, and it never changes `classify_checks`; `UNKNOWN`, missing values and a payload for another head never fire it. A fired trigger runs Wave 8a once more under the router, as `SKILL.md` Wave 8 describes.
+
 ## Log fetch (SKILL, only after non-human findings)
 
 ```bash
@@ -70,8 +76,9 @@ never `clean` and the report never says tests passed.
 
 ## Division of labour
 
-- The **poll script** does one poll and returns a coarse `state` plus the raw
-  `checks` array. It performs no arithmetic and holds no state.
+- The **poll script** does one poll and returns a coarse `state`, the raw
+  `checks` array and GitHub's `merge_state`. It performs no arithmetic and holds
+  no state.
 - **`classify_checks`** maps buckets to `polling` / `clean` / `findings`.
 - The **SKILL** owns `source=ci`, the wait-clock reset, human-gate →
   `HALT_HUMAN` only before Augment halts (otherwise report alongside the
diff --git a/tests/pr_submit/test_static_grep.py b/tests/pr_submit/test_static_grep.py
index 2317bde1..0094550b 100644
--- a/tests/pr_submit/test_static_grep.py
+++ b/tests/pr_submit/test_static_grep.py
@@ -808,6 +808,40 @@ def test_wait_only_sentences_name_the_one_sync_exception():
     ) in ci_poll
 
 
+# --- Issue #361 (P3): refs/ci-poll.md documents merge_state and the late trigger --
+
+_CI_POLL_REF = SKILL_DIR / "refs" / "ci-poll.md"
+
+
+def test_ci_poll_documents_the_merge_state_object():
+    assert (
+        "The poll line also carries `merge_state`, an object "
+        '`{"mergeable": <string>, "status": <string>}` that holds GitHub\'s '
+        "`mergeable` and `mergeStateStatus` values and is appended after `checks`"
+    ) in _prose(_CI_POLL_REF)
+
+
+def test_ci_poll_division_of_labour_names_merge_state():
+    assert (
+        "returns a coarse `state`, the raw `checks` array and GitHub's `merge_state`"
+    ) in _prose(_CI_POLL_REF)
+
+
+def test_ci_poll_pr_conflicting_sentence_points_at_the_late_trigger():
+    assert (
+        "A PR that turns conflicting while the wait runs is noticed through "
+        "`merge_state` instead (see Late conflict trigger (P3) below)"
+    ) in _prose(_CI_POLL_REF)
+
+
+def test_ci_poll_has_the_late_conflict_trigger_section():
+    assert (
+        "## Late conflict trigger (P3) On every poll the SKILL evaluates "
+        "`superclaude.pr_submit.conflicts.late_conflict_trigger(payload, "
+        "wait_sha=...)` before it acts on the classification."
+    ) in _prose(_CI_POLL_REF)
+
+
 def test_s5a_retrigger_widened_for_merge_cycles_only():
     """P2 / QA-3a: the Wave 6 S5a re-trigger is widened only for a Tier 2 merge cycle;
     the zero-edit fix-commit sentence and the state-machine parent-check sentence are
diff --git a/tests/skills/test_worker_contract.py b/tests/skills/test_worker_contract.py
index ca18e306..4165bd45 100644
--- a/tests/skills/test_worker_contract.py
+++ b/tests/skills/test_worker_contract.py
@@ -1653,7 +1653,7 @@ WRITE_VERB_CLASSIFICATION = {
     (
         "src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md",
         "gh pr",
-        "gh pr view <N> --repo <owner/repo> --json number,url,headRefOid",
+        "gh pr view <N> --repo <owner/repo> --json number,url,headRefOid,mergeable,mergeStateStatus",
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
