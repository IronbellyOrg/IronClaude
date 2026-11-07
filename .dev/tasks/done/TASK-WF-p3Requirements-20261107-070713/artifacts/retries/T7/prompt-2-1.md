e4045437001da9cf42cb3deb70e8da4bf51041f4
Review one task for spec compliance.

Task brief: ## Task 7: Reconcile `refs/conflict-mechanical.md` with the late pass

Depends on: Task 5, Task 6

Run serially: Tasks 6 to 9 edit the same test files.

Satisfies: R-010 (`conflict-mechanical.md`), R-007, R-008, R-012 (part d).

Edit `src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md`.

- Section 8, bullet "End of the CI wait" (line 214): keep the final `mergeable` re-read, which runs when any hook this run read `conflicting` or the run was resumed, and its `late_conflict` halt as the backstop, add that a fired late trigger counts as a hook that read `conflicting`, and replace "late re-sync is #361" with a pointer to the Wave 8 late trigger. Do not call the re-read unconditional.
- Section 12, halt-reason table row `late_conflict` (line 289): replace "Late re-sync is #361." and list both causes: a Tier 2 conflict at the late pass with `--conflict-max-tier 2`, and the end-of-wait re-read that reads `CONFLICTING` (which needs no earlier conflict cycle, only an earlier `conflicting` read or a resume). Say that a Tier 1 conflict seen during the CI wait gets the one allowed cycle only under R-007 and R-008, and that a preserved review outcome is reported with its terminal status retained.
- Section 1 ("When this ref applies"): add one paragraph saying the late trigger re-enters hook `wave8a`, the cycle id is `conflict_cycle_id(plan.tier, len(conflict_cycles) + 1)` as in Step 3, and `--resume` restarts an open `wave8a` cycle at step 1. The paragraph must not contain any token of the order pins at `tests/pr_submit/test_conflict_sync_protocol.py` lines 116 to 133 (among them `sync_started`, `merge_preflight_ok`, the merge command, `merge_parent_ok(` and `--is-ancestor`), and any new line that names `conflict-intent.md` or `evidence-validator` must contain "Tier 2" (lines 412 to 427 of the same file).
- Add no new `gh` or `git` command line; the prohibited-operation scan (FR-21) must still pass.

Acceptance criteria (ids):
T7.AC1: `rg -n "#361" src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md` finds nothing and `rg -n "sync_cycles" src` finds nothing.
T7.AC2: Three new assertions in `tests/pr_submit/test_conflict_sync_protocol.py` pin separately the section 8 bullet clause (the words "fired late trigger"), the two causes in the `late_conflict` row, and the section 1 paragraph (the words "len(conflict_cycles) + 1" and "wave8a"); removing only one text fails only its assertion.
T7.AC3: `uv run pytest tests/pr_submit/test_conflict_sync_protocol.py tests/pr_submit/test_static_grep.py tests/skills/test_worker_contract.py -q` passes, including `MECHANICAL_PINS` and the order pins.
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
Start sha: e4045437001da9cf42cb3deb70e8da4bf51041f4
Diff against the start snapshot: 
diff --git a/src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md b/src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md
index 5ac66a21..164373a8 100644
--- a/src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md
+++ b/src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md
@@ -10,6 +10,7 @@ This ref sequences merge-conflict detection and the merge cycle (issue #305). Th
 - Terms: "ours" is the PR head in this checkout (stage 2); "theirs" is the recorded base tip `base_sha` (stage 3); stage 1 is the merge base (S-09).
 - The core decides the class of each path, the plan tier, the route (`conflict_action`), the gates, the cycle ids, the commit message and the resume plans. Nothing in this ref overrides a core answer.
 - Tier 2 steps also need `refs/conflict-intent.md` (Tier 2 only: L3, `--conflict-max-tier 2`, loaded at `C-initial`).
+- The Wave 8 late trigger (`SKILL.md`) re-enters hook `wave8a`; it adds no hook label, and its cycle id is `conflict_cycle_id(plan.tier, len(conflict_cycles) + 1)`, as in Step 3 of section 5. An open `wave8a` cycle that `--resume` restarts begins again at step 1 (section 10).
 
 ## 2. Detection
 
@@ -211,7 +212,7 @@ Step 13.
 - **Tier 2:** append `sync_concluded{pushed, merge_sha}`; `transition(S4_PUSHING, "pushed")`, then S6 and RESOLVING with zero threads; `should_retrigger(0, "merge")` is true, so S5a re-triggers the configured reviewers (see `refs/conflict-intent.md`, Tier 2), and the S5 wait is the run's first review wait.
 - **Skip rule:** a PR still conflicting with nothing pushed skips the CI wait with reason `pr_conflicting` (GitHub runs no `pull_request` checks on a conflicting PR, so the lists would read empty).
 - With `expect_checks` true an empty check list is `polling`; expiry is the existing Wave 8 CI timeout with reason `ci_not_started`, never `clean`, and the report never says tests passed.
-- **End of the CI wait:** when any hook this run read `conflicting` (or the run was resumed), read `mergeable` once more before sending `transition(clean)`. `CONFLICTING` means no `transition(clean)`: `terminal_halted`, reason `late_conflict` (late re-sync is #361).
+- **End of the CI wait:** when any hook this run read `conflicting` (or the run was resumed), read `mergeable` once more before sending `transition(clean)`; a fired late trigger counts as a hook that read `conflicting`, so this re-read stays the backstop behind the late pass. `CONFLICTING` means no `transition(clean)`: `terminal_halted`, reason `late_conflict` (the Wave 8 late trigger in `SKILL.md` runs before this backstop).
 
 ```bash
 gh pr view <N> --repo "$REPO" --json mergeable
@@ -286,7 +287,7 @@ The `merge_preflight_dirty` message: "Your checkout has uncommitted changes to t
 |---|---|---|
 | `foreign_op_in_progress` | Wave 0 operation check; resume row 3 | A merge, rebase, cherry-pick, revert or sequencer operation is in progress (named). Nothing was created or pushed. Finish or abort it yourself, then re-run. For a merge left by an earlier L2 run: commit and push it yourself, or abort it, then re-run. |
 | `conflict_tier3` | Wave 0 (L3); `C-initial`; Wave 8a from `clean` / `REPORT_ONLY` | The Tier 3 template of section 4. |
-| `late_conflict` | Wave 8a Tier 2; end of the CI wait when `mergeable` reads `CONFLICTING` again | PR #N conflicts with `origin/<base>`; a text conflict is resolved only before the first review (`--conflict-max-tier 2`, L3). Nothing was pushed for it. Late re-sync is #361. |
+| `late_conflict` | Wave 8a Tier 2 with `--conflict-max-tier 2`; the end-of-wait `mergeable` re-read when it reads `CONFLICTING` (it needs no earlier conflict cycle, only an earlier `conflicting` read or a resume) | PR #N conflicts with `origin/<base>`; a text conflict is resolved only before the first review (`--conflict-max-tier 2`, L3). Nothing was pushed for it. A Tier 1 conflict first seen during the CI wait gets the one allowed cycle only when no conflict cycle started earlier and `--conflict-max-tier` is at least 1: at L3 it merges and pushes, at L2 it resolves locally and halts before the push, and at L1 it only proposes; after a preserved review outcome (`HALT_MAX_ROUNDS`, `TERMINAL_AUGMENT_NO_RESPONSE`) the outcome is only reported and that terminal status is kept. |
 | `tier_above_cap` | Wave 8a | The conflict is Tier t, above `--conflict-max-tier c`. Nothing was pushed. Re-run with a higher cap or resolve it yourself. |
 | `github_disagrees` | Wave 8a | GitHub reads conflicting, a local merge of `origin/<base>`@<base_sha> is clean; CI was not waited for. Re-run in a few minutes. |
 | `probe_failed`, `merge_tree_unsupported` | Wave 8a (tier unclassified) | Conflict detection could not run (reason); the PR reads conflicting, so CI was not waited for. |
diff --git a/tests/pr_submit/test_conflict_sync_protocol.py b/tests/pr_submit/test_conflict_sync_protocol.py
index 9a7ea99e..ea64d9f4 100644
--- a/tests/pr_submit/test_conflict_sync_protocol.py
+++ b/tests/pr_submit/test_conflict_sync_protocol.py
@@ -133,6 +133,62 @@ def test_conflict_mechanical_order_pins():
     )
 
 
+# --- Issue #361 (P3): the late trigger in the mechanical ref, one pin per text ------
+
+
+def test_mechanical_ref_end_of_wait_bullet_counts_a_fired_late_trigger():
+    text = _prose(MECHANICAL_REF)
+    assert (
+        "a fired late trigger counts as a hook that read `conflicting`, so this "
+        "re-read stays the backstop behind the late pass."
+    ) in text
+    assert "#361" not in text
+    assert "unconditional" not in text
+
+
+def test_mechanical_ref_late_conflict_row_lists_both_causes():
+    assert (
+        "| `late_conflict` | Wave 8a Tier 2 with `--conflict-max-tier 2`; the "
+        "end-of-wait `mergeable` re-read when it reads `CONFLICTING` (it needs no "
+        "earlier conflict cycle, only an earlier `conflicting` read or a resume) |"
+    ) in _prose(MECHANICAL_REF)
+
+
+def test_mechanical_ref_late_conflict_row_states_the_tier1_late_cycle_and_preserved_rule():
+    text = _prose(MECHANICAL_REF)
+    assert (
+        "A Tier 1 conflict first seen during the CI wait gets the one allowed cycle "
+        "only when no conflict cycle started earlier and `--conflict-max-tier` is at "
+        "least 1: at L3 it merges and pushes, at L2 it resolves locally and halts "
+        "before the push, and at L1 it only proposes;"
+    ) in text
+    assert (
+        "after a preserved review outcome (`HALT_MAX_ROUNDS`, "
+        "`TERMINAL_AUGMENT_NO_RESPONSE`) the outcome is only reported and that "
+        "terminal status is kept."
+    ) in text
+
+
+def test_mechanical_ref_end_of_wait_bullet_points_at_the_wave_8_late_trigger():
+    assert (
+        "`late_conflict` (the Wave 8 late trigger in `SKILL.md` runs before this "
+        "backstop)."
+    ) in _prose(MECHANICAL_REF)
+
+
+def test_mechanical_ref_section_1_says_the_late_trigger_reenters_wave8a():
+    text = _prose(MECHANICAL_REF)
+    assert (
+        "The Wave 8 late trigger (`SKILL.md`) re-enters hook `wave8a`; it adds no hook "
+        "label, and its cycle id is `conflict_cycle_id(plan.tier, "
+        "len(conflict_cycles) + 1)`, as in Step 3 of section 5."
+    ) in text
+    assert (
+        "An open `wave8a` cycle that `--resume` restarts begins again at step 1 "
+        "(section 10)."
+    ) in text
+
+
 def _section(text: str, start: str, end: str) -> str:
     assert start in text and end in text, (start, end)
     return text[text.index(start) : text.index(end, text.index(start))]

Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): F1.1 the late_conflict row (conflict-mechanical.md:290) said the Tier 1 late cycle runs only at L3; it also starts at L2 (resolve_local, halt_before_push) and L1 only proposes. Fixed in the diff above. F1.2 the Tier 1/preserved-outcome sentences in that row and the pointer clause at :215 had no scoped assertion. Two assertions were added in the diff above. Check that both are fixed and nothing new broke.
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
