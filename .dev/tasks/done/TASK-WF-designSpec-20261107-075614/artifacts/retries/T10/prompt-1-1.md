df030cd81562f472b4edb39a9e5d55b8f1db9e00
Review one task for spec compliance.

Task brief: ## Task 10: Wire the Wave 3, Wave 6 and Wave 8 bullets into `SKILL.md` and the overlay note into `refs/state-machine.md`

Depends on: Task 9

Edit `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` additively: one new bullet under each of Wave 3, Wave 6 and Wave 8 that loads `refs/merge-guard.md` only at L3 with `--merge-guard` `draft`, written as new sentences after, never inside, the pinned sentences. The Wave 3 bullet states that engage happens at the end of Wave 3 only when at least one verified finding of Medium severity or higher is routed to a fix, once per cycle id, and mints the cycle id; the Wave 6 bullet states that Pre-push runs at the pre-push head guard step before `push_decision` and that Release runs after `push_completed` and before reply, resolve and the S5a re-trigger; the Wave 8 bullet states that a CI-fix cycle engages with kind `ci` and releases after `push_completed` before the CI re-poll. The S5a re-trigger sentence and the Wave 6 pre-push sentence stay byte-identical. Edit `src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md` with a short overlay note that guard phases are folded values, not `MonitorState` members, without the words `gh` or `git` and outside the wait-only sentences pinned for that file. Avoid `gh pr` and `gh api` on new lines (refer to "the clear command from the ref"); add a `WRITE_VERB_CLASSIFICATION` entry as the last step for any new line that cannot avoid them. Extend `tests/pr_submit/test_merge_guard_protocol.py` with one test per bullet (each gated on L3 and `draft`) and one for the overlay note. Run `make sync-dev`.

Acceptance criteria:
- T10.AC1: The Wave 3 bullet test asserts the sentence names the Medium-or-higher routed-finding trigger and "once per cycle" and fails when either phrase is deleted (an unconditional "engage at the end of Wave 3" does not pass); the Wave 6 test asserts the Pre-push sentence and the Release-before-reply-resolve-re-trigger order; the Wave 8 test asserts the CI-fix sentence; each test fails when its sentence is removed.
- T10.AC2: The S5a re-trigger sentence and the Wave 6 pre-push sentence are asserted byte-identical by comparing the live text with string constants (the literal start text recorded in `./artifacts/pre-build-gate.md`, as the existing pins write them), not with `git show HEAD:`; `SKILL.md` has one python fence and no `src/superclaude` string; no new line contains `evidence-validator` or `conflict-intent.md`.
- T10.AC3: `uv run pytest tests/pr_submit -q` and `uv run pytest tests/skills/test_worker_contract.py -q` pass and `make verify-sync` exits 0.
Global constraints: - Edit canonical files under `src/superclaude/` only, then run `make sync-dev`; do not stage `.claude/` mirror files. Use UV for every Python command (`uv run pytest ...`, `uv run ruff ...`).
- The new pure module `src/superclaude/pr_submit/merge_guard.py` and every file already listed in `CORE_PURE_FILES` of `tests/pr_submit/test_static_grep.py` (including `refs/state-machine.md` and `refs/loop-guard.md`) must contain no whole word `gh` or `git` on any line, comments included. The module must not import `recovery` (an import cycle through `run_log`).
- Protocol and command text must not contain the string `src/superclaude`; `SKILL.md` must keep exactly one python code fence; edits to `SKILL.md` and `refs/state-machine.md` are additive sentences, bullets and rows placed after, never inside, the sentences pinned by `tests/pr_submit/test_static_grep.py` and `tests/pr_submit/test_conflict_sync_protocol.py`. A new `SKILL.md` line must not name `evidence-validator` or `conflict-intent.md` (a line-content test allows those words only on lines that also say "Tier 2") and must not use wording that the forbidden-force-push line test rejects; Task 1 lists the exact line-content rules before any edit.
- Every new line under `src/superclaude/skills/`, `src/superclaude/commands/` or `src/superclaude/agents/` that contains `gh pr`, `gh api` or a git write verb needs one entry in `WRITE_VERB_CLASSIFICATION` in `tests/skills/test_worker_contract.py` (key: repo-relative path, verb text, exact stripped line; category `never-worker` with the standard pr-submit reason text of the neighbouring entries). Add each entry last in the task that writes the file, because editing a classified line later makes the entry stale and fails `test_classification_table_has_no_stale_entries`; run `uv run pytest tests/skills/test_worker_contract.py -q` in that task.
- Cite tests and constants by symbol name (for example `_NEW_KEY_DEFAULTS`, `_RESOLUTION_SCRIPTS`, `CORE_PURE_FILES`, `WRITE_VERB_CLASSIFICATION`), never by line number, in plan text, task artifacts and the protocol prose this plan produces. Protocol prose carries no `file:NNN` pointers.
- No test or task may call GitHub. Script tests use a fake `gh` executable on `PATH`. The behaviour that needs a disposable fork PR (gates G1 live part, G2 live part, G4, G5 and G6 of ./source.md section 8) is recorded as OPEN and is a release gate, never claimed verified.
- Scope limits (non-goals of ./source.md): no labels, commit statuses or rulesets; ordinals 0 to 2 change only by one report line; conflict-merge cycles (Tier 1 and Tier 2) are never engaged; the guard is not held through re-review or CI; a second concurrent run on the same PR is unsupported.
- Owner decisions already accepted (listed in the ./source.md header and section 8) are fixed: draft not label; engage at the end of Wave 3; default on at `--monitor 3`; release on the confirmed push before replies and the re-trigger; unreadable timeline or unpublished exit keeps the PR draft; build now with no GitHub calls, release gate for G4 and G5.
- Run `make sync-dev` at the end of every task that edits a file under `src/superclaude/skills/` or `src/superclaude/commands/`, because the full test suite runs `make verify-sync` through `tests/cli/test_verify_sync_hooks.py`.
Start sha: df030cd81562f472b4edb39a9e5d55b8f1db9e00
Diff against the start snapshot: diff --git a/src/superclaude/skills/sc-pr-submit-protocol/SKILL.md b/src/superclaude/skills/sc-pr-submit-protocol/SKILL.md
index b238ff77..2056726e 100644
--- a/src/superclaude/skills/sc-pr-submit-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-pr-submit-protocol/SKILL.md
@@ -281,13 +281,16 @@ Wave 8a: (L1+) act on a conflict before the CI wait ← loads refs/conflict-mech
 - **Wave 1 (L1+):** load the contract via `superclaude.pr_submit.DetectionContract.for_arming()` — prefers an optional operator-local override (gitignored `.dev/pr-monitor/detection-contract.locked.md`) and falls back to the SHIPPED `refs/detection-contract.md` (baked `augmentcode[bot]` / `augmentcode` defaults). A missing or unlocked override is not a halt; the contract also carries the Codex identities (`codex_bot_login`, `codex_app_slug`) and `codex_retrigger_phrase`, and Codex is disabled only when both Codex identities are blank (it stays on while either remains). Initialize the output-dir + run-log + baseline, then enter the **attended poll loop** (above) with `scripts/poll-augment-review.sh` (interval ≥30s, timeout default 600s; the one snapshot serves both reviewers); each JSON line passes the snapshot gate before any FSM outcome; incomplete evidence keeps polling. Record `reviewer_absent{reviewer}` for a reviewer the merge settles as absent, and `reviewer_incomplete{reviewer, phase: "initial"}` for a present reviewer that did not complete by `--timeout` while the other's result was used. Every event that concerns one reviewer carries a `reviewer` field (`"augment"` or `"codex"`; a missing field means `augment`): `poll_result` (with the per-reviewer wait outcomes), `review_detected`, `findings_normalized`, `finding_verified`, `finding_unverified`, `route_decision`, `reply_posted`, `thread_resolved`, `rereview_requested`. On `--resume`, read `rebuild_state()["absent_reviewers"]` and keep those reviewers absent. Arm exactly once at L1+ (T-109); never at L0 (T-110). `--monitor 0` remains no-monitor. **C-initial (L3, Tier 2, only when Wave 0 planned it under `--conflict-max-tier 2`):** after arming and before the first review poll, load `refs/conflict-intent.md` and run the Tier 2 merge cycle of `refs/conflict-mechanical.md` through `transition(S2_CLASSIFY, "conflicting")`; its S5 wait is the run's first review wait.
 - **Wave 2:** load `refs/severity-routing.md`; use only the snapshot gate's `actionable_finding_comments` → `finding_from_comment` → `remap_severity(finding)` → `route(finding)` results from `superclaude.pr_submit` (Augment's and, for Codex, `codex_finding_comments` → the same three calls; a Codex P0/P1/P2/P3 badge is its severity hint, a missing or malformed badge is the Medium fail-safe), then map the remapped tier to its troubleshoot route (Medium → `--fix`; High/Critical → `--depth deep --fix`; Low/Nit → report-only). NEVER emit `--depth quick --fix`. Group the merged findings with `dedup_groups(findings)` (same path and line, `original_line` when the line is null): a **dedup group routes at its members' highest remapped tier**; every member keeps its own finding, verdict and thread.
 - **Wave 3:** load `refs/finding-verify.md`; spawn the `evidence-validator` agent (read-only) to confirm each finding's cited file:line exists and the defect reproduces (one verdict per finding, Augment and Codex in one batch). `unverified` → REPORT_ONLY, consuming NO round. A dedup group is dispatched only when at least one member is verified. Context only, once per cycle before verification: invoke `> Skill sc:impact-protocol` with `--diff origin/<baseRefName> --depth 1 --output-dir <output-dir>/impact/wave3 --caller sc-pr-submit-protocol` and read only `status`, `degraded`, `dependents[].caller`, `dependents[].file` and `unmapped_files` from its `return-contract.yaml`; the dependent names and files are background for the verifier, never a reason to verify, drop or re-tier a finding. Copy its `degraded` tokens into the run-log; `status: blocked|failed` counts as `graph:absent`.
+- **Wave 3 merge guard (L3 with `--merge-guard draft` only):** load `refs/merge-guard.md` (Engage). At the end of Wave 3, engage the guard only when at least one verified finding of Medium severity or higher is routed to a fix (the Medium-or-higher routed-finding trigger), once per cycle id. This is the single place that mints the cycle id, with `fix_cycle_id(kind, next_cycle_number(<run-log events>, kind))`: kind `fix` here, and kind `ci` for a CI-fix cycle (the Wave 8 guard bullet). The push triad and `rereview_requested` reuse that id.
 - **Wave 4:** load `refs/troubleshoot-dispatch.md`; for VERIFIED findings only, `> Skill sc:troubleshoot-protocol` for diagnosis, once per dedup group with every verified member's body in the seed and each body naming its reviewer; the group gets one diagnosis and one set of edits (no double fix), and `fix_applied` is recorded for **every** member's `fix_key`. **At L1 (G-edit `ordinal < 2`): PROPOSE "fix these? y/n" and apply NO edits.** At L2+ the skill applies the diagnosed edits ITSELF in the working tree (troubleshoot does NOT auto-apply — `sc:pr-submit` owns edit application in `S3_FIXING`). Before the cycle's first edit, record the operator's pending files (`git status --porcelain=v1 -z --untracked-files=all`: every modified, staged and untracked file, both sides of a rename) as `OPERATOR_PENDING`; the Wave 6 fix commit refuses any of them. Before the cycle's first edit, also run the impact warning of `refs/troubleshoot-dispatch.md` ("Impact warning before a fix").
 - **Wave 5:** run the VAL validator (below). **At L2 the ceiling stops here:** after applying the edits in `S3_FIXING` and validating in `S7_VALIDATING`, the FSM HALTs at `S4'_HALT_BEFORE_PUSH` — changes are left in the working tree with NO commit, NO push, NO reply (`S3_FIXING → S7_VALIDATING → S4'_HALT_BEFORE_PUSH`, matching `state-machine.md` §5.2a). Only L3 proceeds to Wave 6.
 - **Wave 6 (L3 only):** load `refs/thread-reply.md`. **Fix commit:** when the cycle applied edits (`applied_edits > 0`) and VAL is green, commit all of them as exactly one commit (one per cycle, never one per finding; VAL has already passed, so a validation retry never adds a second commit), staging only the files those edits changed (`git add -- <paths>`, never `git add -A` or `git add .`, which would sweep in run artifacts and other untracked files) and committing with `git commit --only -- <paths>` so nothing else already in the index is committed, and set `target_sha := git rev-parse HEAD`; every thread replied to in this cycle cites that one SHA. Before staging anything (before the `git add` above), if a path to commit is in `OPERATOR_PENDING`, append `terminal_halted` (reason `fix_commit_failed`), HALT with nothing committed or pushed, and tell the operator: "The fix touched files that had your own uncommitted changes: <paths>. Nothing was committed or pushed. Those files now hold both your changes and the fix: separate them by hand (do not discard the files), then re-run with `--pr <N>`." Otherwise, if the commit fails (for example a pre-commit hook rejects it) or HEAD did not advance, append `terminal_halted` (reason `fix_commit_failed`), HALT with nothing pushed, and tell the operator: "The fix commit failed (<error>). Nothing was pushed; the edits, and any changes a hook made, are in your working tree. Fix the cause, then either commit and push the fix yourself or discard it, and re-run with `--pr <N>`." A halted cycle replies to and resolves no thread. A crash re-drive (Branch B) skips this step and pushes the record's `target_sha`. **Pre-push head guard, before `push_decision`:** re-read `gh pr view <N> --repo "$REPO" --json headRefName,headRefOid,isCrossRepository` and require `pr_head_ok(<local branch>, pre_push_sha, headRefName, headRefOid, isCrossRepository)` and `headRefName == HEAD_BRANCH`. Compare the stored `pre_push_sha`, never local HEAD (local HEAD is the new fix commit). False → append `terminal_halted` (reason `pr_head_mismatch`), HALT with nothing pushed, write no push record, and tell the operator: "PR #<N>'s head moved from <pre_push_sha> to <headRefOid> (or its branch is no longer `<HEAD_BRANCH>`) during the run. Nothing was pushed. Review the new PR commits, make your checkout equal the new PR head, then re-run with `--pr <N>`." When this cycle made a fix commit, the message adds: "This cycle's fixes are in local commit <target_sha>: drop it, or rebase it onto the new head and push it yourself." Next, when the cycle applied edits (a zero-edit cycle has no fix commit; INV-016 predicate 5 blocks its push and still records `push_decision`), read the parents of the commit to push (`git rev-list --parents -n 1 <target_sha>`, dropping the first id) and require `superclaude.pr_submit.fsm.push_parent_ok(<parents>, pre_push_sha)`: a fast-forward push publishes every commit between the PR head and `target_sha`, so the push may carry only this cycle's fix commit. False → append `terminal_halted` (reason `push_range_mismatch`), HALT with nothing pushed and no push record, and tell the operator: "Nothing was pushed. The fix commit <target_sha> sits on top of local commits that are not on PR #<N>: <`git log --oneline <pre_push_sha>..<target_sha>^`>. Publish those commits yourself if you want them on the PR, otherwise drop them; make your checkout equal the PR head, then re-run with `--pr <N>` (the open review threads are fixed again)." Then set `target_branch := HEAD_BRANCH`. The deterministic core DECIDES (evaluates the INV-016 conjunction, records the write-ahead push triad `push_decision` → `push_initiated` (fsynced BEFORE the push) → `push_completed`, keyed on the PRE-push idempotency key `push:<run_id>:<cycle_id>:<pre_push_sha>:<target_branch>`); the SKILL performs the actual `git push origin <target_sha>:<target_branch>` (never an upstream parent remote, never the repo's default/protected branch, never a force push) ONLY when the conjunction holds, then set `pre_push_sha := target_sha`, then reply (citing `applied_edits` status — `applied_edits==0` says "no code change applied", never "resolved") and resolve via `scripts/reply-resolve-thread.sh` (reply FIRST, then resolve; the script finds the thread by its root comment id, so an Augment or a Codex root works the same). In a dedup group, **every verified member's thread** is replied to and resolved, all citing the cycle's one fix SHA; an unverified or Low/Nit member gets no reply and no resolve, and the report lists the group once with "flagged by: augment, codex". **S5a re-trigger (FR-8):** load `refs/review-retrigger.md`; a push does NOT auto-trigger a re-review by either bot — AFTER resolve, and ONLY when this cycle applied edits (`applied_edits > 0`) or is a Tier 2 merge cycle (push kind `merge`; `superclaude.pr_submit.fsm.should_retrigger`), post **one re-trigger comment per present reviewer** BEFORE re-entering the S5 poll: for each reviewer in `pending_retriggers(<run-log events>, cycle_id, <present reviewers>)` (the present reviewers that have no `rereview_requested` for this `cycle_id` yet), run `scripts/retrigger-review.sh --pr <N> --repo "$REPO" --body "<retrigger_phrase(contract, reviewer)>"` (`auggie review` for Augment, `@codex review` for Codex). The core decides whether/when to re-trigger (`do_retrigger` seam, INV-R1: at most once per push cycle, `rereview_request_count <= max_rounds`, counted per cycle, not per comment); the script does the `gh api` issue-comment POST (NFR-6). Right after each reviewer's successful POST, take that reviewer's UTC watermark and append a **`rereview_requested{cycle_id, reviewer, timestamp}`** run-log event with that time (the INV-R1 producer — folded into `rereview_request_count` by distinct `cycle_id` in `rebuild_state`, and consumed by crash recovery's OQ-1 resume decision: a landed-push crash with NO `rereview_requested` for its cycle resumes at `S5a_RETRIGGER_REVIEW` to re-post; one WITH it resumes at `S5_AWAITING_REREVIEW`). **Resume of a re-triggered cycle:** reuse the `cycle_id` of the dangling push record (never a new one); on every resume at `S5a_RETRIGGER_REVIEW` or `S5_AWAITING_REREVIEW`, first call `pending_retriggers` and post the reviewers still missing (a crash between the Augment and the Codex post neither skips Codex nor re-posts Augment), then take each reviewer's watermark from the `timestamp` of its latest `rereview_requested` for the cycle before the S5 poll. The `round_counter` ticks only when the subsequent poll attributes the re-review to our pushed SHA (the relocated INV-001 increment) — a timed-out re-trigger does NOT advance the counter.
+- **Wave 6 merge guard (L3 with `--merge-guard draft` only):** load `refs/merge-guard.md` (Pre-push and Release). Pre-push runs at the pre-push head guard step before `push_decision`: the guard's read must show the PR `OPEN`, otherwise append `terminal_halted` with reason `pr_not_open`, push nothing and report the local commit. Release runs after `push_completed` (or the zero-edit proof) and before any reply, resolve or S5a re-trigger, with the cycle id the Wave 3 guard bullet minted; when the PR stays a draft, print the clear command from the ref.
 - **Wave 6b (L2+ decline fallback, FR-9/FR-10):** load `refs/auggie-fallback.md`. When the classifier returns `declined` (an Augment "abnormally large" decline observed at the initial S2 poll OR the S5 re-trigger poll), append a **`decline_detected`** run-log event, then engage the single-shot fallback: gate **strict-once** on the durable `auggie_review_invoked` idempotency record (comment-independent, survives resume — INV-R2; on engage, append an **`auggie_fallback_invoked{pr_number}`** event, the producer folded into that set), clamp the effective budget `effective_max_rounds := min(effective_max_rounds, 1)` (the `clamp_max_rounds` helper, recorded once via the **`max_rounds_clamped{effective_max_rounds}`** event — INV-R3 monotone-min fold), then invoke `> Skill sc:auggie-review-protocol --depth quick --remediation-offer` and re-enter Waves 2-6 ONCE under the clamp, with the fallback's findings plus any merged Codex `findings` of the same round (verify-before-remediate still applies — fallback findings are NOT trusted verbatim, FR-9.4). At L2 this can apply and validate local fixes but still halts before push/reply per Wave 5; only L3 performs push, reply, resolve, and re-trigger side effects. NO second invoke, NO second re-trigger (for either reviewer), NO loop-back; `push_count <= max_rounds + 1` for the whole run. This is `sc:pr-submit` invoking its OWN review — do **NOT** "take the App's bait" by treating the App's `augment review` decline comment as our operator re-trigger. (`--depth quick` here targets `/sc:auggie-review` — a review, no `--fix` — so it does NOT conflict with the severity-routing STOP on `--depth quick --fix`.)
 - **Wave 7:** load `refs/loop-guard.md`; the round counter ticks only at `S5_AWAITING_REREVIEW → S2_CLASSIFY`; HALT at `round_counter >= max_rounds`. Fallback outcomes REUSE the existing `terminal_clean` / `terminal_max_rounds` status values (OQ-2 reuse recommendation).
 - **Wave 8 (L1+, after Augment `clean` / `REPORT_ONLY` / `HALT_MAX_ROUNDS` / `TERMINAL_AUGMENT_NO_RESPONSE`):** load `refs/ci-poll.md`, then run Wave 8a (below) before the CI poll loop. These are the merged review outcomes: `clean` is the merged clean of the reviewers used, and `TERMINAL_AUGMENT_NO_RESPONSE` is reached only when no configured reviewer responded (a silent Augment with Codex present continues with Codex and never arms from here). Arm via `superclaude.pr_submit.ci.should_arm_ci_wait`. Do **not** `transition(clean)` yet. Set SKILL-owned `source=ci`, reset wait elapsed, switch the attended poll loop to `scripts/poll-ci-checks.sh --pr <N> --repo "$REPO"`. Classify via `superclaude.pr_submit.ci.classify_checks(payload, wait_sha=<sha at flip or last push>, expect_checks=<the value recorded for that push, else false>)`. Human-gate (`is_human_gate`) → `HALT_HUMAN` when Augment has not halted; after Augment `HALT_MAX_ROUNDS` or `TERMINAL_AUGMENT_NO_RESPONSE`, keep its terminal status and report the CI human-gate alongside it. No Finding or auto-fix on those wait-only paths (`ci_wait_autofix` is false). If `round_counter >= max_rounds`, CI polling is wait-only: non-human `findings` → `REPORT_ONLY` without fetching logs, editing, or pushing a fix; the single Tier 1 sync push of Wave 8a (`SYNC_CAP = 1`) is the only push a wait-only path allows, and it is not a fix. Otherwise non-human `findings` → `gh run view <id> --repo "$REPO" --log-failed` once → `findings_from_logs`; empty → `REPORT_ONLY`; else Waves 3–5 under the same ordinals and `round_counter`. An L3 CI push runs the Wave 6 pre-push head guard and push triad with `target_branch := HEAD_BRANCH`, then sets `pre_push_sha := target_sha`. It also makes the Wave 6 single fix commit and runs the guard's parent check (`push_parent_ok`), so this push too carries only the cycle's one fix commit; its triad passes `push_kind="ci"`, `review_terminal` and `expect_checks=True`. After an L3 CI push: do **not** call `retrigger-review.sh`, reply, or resolve; re-poll CI on the new `headRefOid`. When CI is `clean` after an ordinary Augment `clean` / `REPORT_ONLY`, send `transition(clean)` → `TERMINAL_CLEAN`. After `HALT_MAX_ROUNDS` or `TERMINAL_AUGMENT_NO_RESPONSE`, leave that terminal FSM status unchanged and report CI clean alongside it (no `transition(clean)` from a terminal state — never claim `TERMINAL_CLEAN` for a silent Augment review). L0 never reaches Wave 8. Do not arm on `HALT_HUMAN` / `VALIDATION_FAIL` / `TERMINAL_TIMEOUT` / `TERMINAL_FAILED`. CI `polling` continues at the configured interval until completion or timeout; when the chosen list is empty, a failed check query is `polling`, not no-Actions `clean`. Only parsed empty required **and** all-checks lists, with `expect_checks` false, prove there are no Actions; with `expect_checks` true an empty list is `polling`, and expiry is the CI timeout with reason `ci_not_started`, never clean. A nonempty required list is the chosen set; optional pending checks outside it do not block completion.
 - **Wave 8a (L1+, conflict act before the CI wait; same entry outcomes as Wave 8):** read `gh pr view <N> --repo "$REPO" --json baseRefName,mergeable,mergeStateStatus,headRefName,headRefOid,isCrossRepository` (same `UNKNOWN` re-reads). Only `conflicting` or a persistent `unknown` loads `refs/conflict-mechanical.md`, re-probes and acts on `conflict_action(hook="wave8a", entering=<review outcome>)`: at L3 a Tier 1 conflict becomes one sync merge commit pushed fast-forward (no round, no re-trigger, no reply, no resolve; the one push a wait-only path allows), then the CI wait runs on the new head with `expect_checks`; L2 leaves it resolved and validated but uncommitted (`halt_before_push`, only after `clean` / `REPORT_ONLY`); L1 proposes (also only after `clean` / `REPORT_ONLY`). A PR still conflicting with nothing pushed skips the CI wait with reason `pr_conflicting` (GitHub runs no `pull_request` checks on it) and ends with the status `conflict_action` returns. When any hook this run read `conflicting`, re-read `mergeable` before sending `transition(clean)`; `CONFLICTING` → `terminal_halted`, reason `late_conflict` (late re-sync: #361).
+- **Wave 8 merge guard (L3 with `--merge-guard draft` only):** load `refs/merge-guard.md` (Engage and Release). A CI-fix cycle that routes a verified finding of Medium severity or higher to a fix engages the guard with kind `ci` (cycle id `ci-<n>`), and releases after `push_completed` before the CI re-poll.
 
 ## VAL — the §10 validation gate list (owned by the SKILL, not the core)
 

diff --git a/src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md b/src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md
index 97583485..52d2e3aa 100644
--- a/src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md
+++ b/src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md
@@ -180,6 +180,10 @@ a non-halted CI-clean path sends `clean` to `transition()`. L0 never enters this
   `conflict_tier3`); a Tier 3 found by a later hook takes the human-gate route to `HALT_HUMAN`, or is
   reported alongside a preserved terminal.
 
+### 5.2e Merge guard overlay (issue #375)
+
+The merge guard's phases (`ENGAGE_PENDING`, `HELD`, `RELEASE_PENDING`, `RELEASED` and `DISABLED`) are folded values of the run log's `draft_guard` state, read by `fold_draft_guard`. They are not `MonitorState` members: the guard adds no state and no transition, and a guard decision never changes the FSM state. The procedure is `refs/merge-guard.md`.
+
 ## 5.3 G-push — the 5-predicate runtime conjunction (INV-016, verbatim)
 
 > **INV-016.** A push is authorized at the `S4_PUSHING` transition if and only if ALL of the

diff --git a/tests/pr_submit/test_merge_guard_protocol.py b/tests/pr_submit/test_merge_guard_protocol.py
index 918e02b8..f4d4c553 100644
--- a/tests/pr_submit/test_merge_guard_protocol.py
+++ b/tests/pr_submit/test_merge_guard_protocol.py
@@ -532,3 +532,152 @@ def test_the_new_skill_lines_name_no_gh_write_no_python_and_no_second_ref_rule()
         )
     assert text.count("```python") == 1
     assert "src/superclaude" not in text
+
+
+# --- the Wave 3, Wave 6 and Wave 8 guard bullets and the state-machine overlay ----
+
+STATE_MACHINE = SKILL_DIR / "refs" / "state-machine.md"
+GATE = "(L3 with `--merge-guard draft` only)"
+# Literal starts of the two sentences this plan must leave byte-identical (the "Pinned
+# literal starts" of the pre-build record); compared as constants, not with git history.
+S5A_START = (
+    "**S5a re-trigger (FR-8):** load `refs/review-retrigger.md`; a push does NOT "
+    "auto-trigger a re-review by either bot — AFTER resolve, and ONLY when this cycle "
+    "applied edits (`applied_edits > 0`) or is a Tier 2 merge cycle (push kind `merge`; "
+    "`superclaude.pr_submit.fsm.should_retrigger`), post **one re-trigger comment per "
+    "present reviewer** BEFORE re-entering the S5 poll:"
+)
+PREPUSH_SENTENCE = (
+    "**Pre-push head guard, before `push_decision`:** re-read "
+    '`gh pr view <N> --repo "$REPO" --json headRefName,headRefOid,isCrossRepository` '
+    "and require `pr_head_ok(<local branch>, pre_push_sha, headRefName, headRefOid, "
+    "isCrossRepository)` and `headRefName == HEAD_BRANCH`."
+)
+WAVE6_LINE_START = "- **Wave 6 (L3 only):**"
+
+
+def _guard_bullet(text: str, wave: int) -> str | None:
+    prefix = f"- **Wave {wave} merge guard "
+    found = [line for line in text.splitlines() if line.startswith(prefix)]
+    return found[0] if len(found) == 1 else None
+
+
+def _bullet_problems(text: str, wave: int, required: tuple[str, ...]) -> list[str]:
+    bullet = _guard_bullet(text, wave)
+    if bullet is None:
+        return [f"the Wave {wave} guard bullet is missing or repeated"]
+    problems = []
+    for need in (GATE, "load `refs/merge-guard.md`", *required):
+        if need not in bullet:
+            problems.append(f"the Wave {wave} bullet lacks {need!r}")
+    return problems
+
+
+WAVE3_NEEDS = (
+    "At the end of Wave 3, engage the guard only when at least one verified finding "
+    "of Medium severity or higher is routed to a fix",
+    "the Medium-or-higher routed-finding trigger",
+    "once per cycle id",
+    "the single place that mints the cycle id",
+    "kind `ci` for a CI-fix cycle",
+)
+WAVE6_NEEDS = (
+    "Pre-push runs at the pre-push head guard step before `push_decision`",
+    "`pr_not_open`",
+    "Release runs after `push_completed`",
+    "before any reply, resolve or S5a re-trigger",
+    "print the clear command from the ref",
+)
+WAVE8_NEEDS = (
+    "engages the guard with kind `ci` (cycle id `ci-<n>`)",
+    "releases after `push_completed` before the CI re-poll",
+)
+
+
+def _case_insensitive_start(text: str, phrase: str) -> str:
+    """The text with `phrase` removed once, tolerating a capital letter at its start."""
+    for variant in (phrase, phrase[0].upper() + phrase[1:]):
+        if variant in text:
+            return text.replace(variant, "", 1)
+    raise AssertionError(phrase)
+
+
+@pytest.mark.parametrize(
+    ("wave", "needs"), [(3, WAVE3_NEEDS), (6, WAVE6_NEEDS), (8, WAVE8_NEEDS)]
+)
+def test_each_guard_bullet_is_gated_and_states_its_sentences(wave, needs):
+    text = _skill()
+    assert _bullet_problems(text, wave, needs) == []
+    bullet = _guard_bullet(text, wave)
+    # The bullet is a new physical line after the pinned wave line, never inside it.
+    assert bullet and bullet.startswith(f"- **Wave {wave} merge guard {GATE}:**")
+
+
+@pytest.mark.parametrize(
+    ("wave", "needs"), [(3, WAVE3_NEEDS), (6, WAVE6_NEEDS), (8, WAVE8_NEEDS)]
+)
+def test_each_guard_bullet_test_fails_when_a_phrase_or_the_bullet_is_removed(
+    wave, needs
+):
+    text = _skill()
+    bullet = _guard_bullet(text, wave)
+    assert bullet
+    for need in (GATE, "load `refs/merge-guard.md`", *needs):
+        mutated = text.replace(bullet, _case_insensitive_start(bullet, need), 1)
+        assert mutated != text, need
+        assert _bullet_problems(mutated, wave, needs), need
+    assert _bullet_problems(text.replace(bullet, ""), wave, needs)
+
+
+def test_the_wave3_bullet_is_not_an_unconditional_engage():
+    """An unconditional "engage at the end of Wave 3" must not pass the test."""
+    text = _skill()
+    bullet = _guard_bullet(text, 3)
+    assert bullet
+    unconditional = bullet.replace(
+        "only when at least one verified finding of Medium severity or higher is routed to a fix",
+        "",
+    )
+    assert unconditional != bullet
+    assert _bullet_problems(text.replace(bullet, unconditional), 3, WAVE3_NEEDS)
+
+
+def test_the_wave6_bullet_puts_pre_push_before_release_and_release_before_the_rest():
+    bullet = _guard_bullet(_skill(), 6)
+    assert bullet
+    assert bullet.index("Pre-push runs") < bullet.index("Release runs")
+    assert bullet.index("Release runs after `push_completed`") < bullet.index(
+        "before any reply, resolve or S5a re-trigger"
+    )
+
+
+def test_the_wave8_text_names_the_ci_kind_and_the_ci_cycle_id():
+    bullet = _guard_bullet(_skill(), 8)
+    assert bullet and "kind `ci`" in bullet and "`ci-<n>`" in bullet
+
+
+def test_the_s5a_and_pre_push_sentences_are_byte_identical_to_the_recorded_text():
+    text = _skill()
+    wave6 = [line for line in text.splitlines() if line.startswith(WAVE6_LINE_START)]
+    assert len(wave6) == 1
+    for sentence in (S5A_START, PREPUSH_SENTENCE):
+        assert text.count(sentence) == 1, sentence[:40]
+        assert sentence in wave6[0], sentence[:40]
+    # The new bullet is its own line: it never sits inside the pinned Wave 6 line.
+    assert "merge guard" not in wave6[0]
+
+
+def test_the_state_machine_overlay_says_guard_phases_are_folded_values():
+    from superclaude.pr_submit.fsm import MonitorState
+
+    text = STATE_MACHINE.read_text(encoding="utf-8")
+    start = text.index("### 5.2e Merge guard overlay")
+    note = text[start : text.index("## 5.3 G-push")]
+    prose = " ".join(note.split())
+    assert "are not `MonitorState` members" in prose
+    assert "folded values" in prose and "`refs/merge-guard.md`" in prose
+    assert "never changes the FSM state" in prose
+    for phase in mg.Phase:
+        assert f"`{phase.name}`" in prose, phase
+        assert phase.name not in MonitorState.__members__
+    assert re.search(r"\bgh\b|\bgit\b", note) is None

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
