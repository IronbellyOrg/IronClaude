50c5db155fa557067ccaa5f7b7c19296c9c38fc3
Review one task for spec compliance.

Task brief: ## Task 12: Update SKILL.md for two reviewers

Depends on: Task 9

Edit src/superclaude/skills/sc-pr-submit-protocol/SKILL.md per design sections 4-13: the description, Purpose and attended poll loop name Augment and Codex; the snapshot gate code block adds the Codex gate and `merge_wait` exactly as in design section 14; Wave 1 records `reviewer_absent` / `reviewer_incomplete`; Waves 2-4 use `dedup_groups` and name the reviewer in run-log events; Wave 6 re-triggers each present reviewer via `pending_retriggers` and `retrigger_phrase` with a per-reviewer watermark; the Output Contract adds `reviewers`; `terminal_augment_no_response` is described as no configured reviewer responding. Then run make sync-dev and make verify-sync.

Acceptance criteria:
- SKILL.md references only installed-safe names (the `superclaude.pr_submit` package, `scripts/...`, `refs/...`); `grep -n 'src/superclaude' src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` finds no new hit.
- make verify-sync passes and tests/pr_submit/test_skill_parse.py passes.
Global constraints: 
- The design file .dev/pr-submit-codex/design/pr-submit-codex-design.md is the specification; do not add behaviour it does not describe.
- Keep the deterministic core src/superclaude/pr_submit/ free of gh and git command tokens (NFR-6, checked by tests/pr_submit/test_static_grep.py).
- Augment-only behaviour must stay identical apart from the added reviewer_absent event and reviewer fields (design sections 5 and 6); existing tests in tests/pr_submit/ keep passing.
- Never hardcode src/superclaude/ paths inside installed primitives (command, skill, refs, scripts); keep script file names unchanged.
- plugins/superclaude/ has no pr-submit twin (design section 3), so no mirror edit is needed; do not create one.
- Edit src/superclaude/ only, then run make sync-dev; never edit or stage .claude/ copies.
- Run pytest only on named files or tests/pr_submit, never the full suite or tests/cli/eval/ as a directory; use uv run.
- .dev/tasks/ is always staged (git add .dev/tasks), including this package and its artifacts/.
Start sha: 50c5db155fa557067ccaa5f7b7c19296c9c38fc3
Diff against the start snapshot: diff --git a/src/superclaude/skills/sc-pr-submit-protocol/SKILL.md b/src/superclaude/skills/sc-pr-submit-protocol/SKILL.md
index 38db1da1..6a62d59c 100644
--- a/src/superclaude/skills/sc-pr-submit-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-pr-submit-protocol/SKILL.md
@@ -1,6 +1,6 @@
 ---
 name: sc:pr-submit-protocol
-description: "PR-review auto-remediation monitor — opens a PR on the fork, runs an attended in-session poll loop for the Augment Code review, re-grades + verifies each finding, dispatches verified findings to /sc:troubleshoot, then (at higher ordinals) fixes, validates, pushes, replies, and resolves under a capped monotonic round counter. The --monitor {0,1,2,3} ordinal is a capability ceiling on ONE finite state machine, not four code paths."
+description: "PR-review auto-remediation monitor — opens a PR on the fork, runs an attended in-session poll loop for the Augment Code and Codex reviews (each reviewer optional and detected on the PR), re-grades + verifies each finding, dispatches verified findings to /sc:troubleshoot, then (at higher ordinals) fixes, validates, pushes, replies, and resolves under a capped monotonic round counter. The --monitor {0,1,2,3} ordinal is a capability ceiling on ONE finite state machine, not four code paths."
 allowed-tools: Read, Grep, Glob, Write, Edit, Bash(gh *), Bash(git *), Bash(uv *), Bash(make *), Bash(jq *), Task, Skill
 ---
 
@@ -16,13 +16,23 @@ personas: [analyzer, architect, security, qa, devops]
 ## Purpose
 
 `sc:pr-submit` opens a PR on the resolved origin repo (origin's `owner/repo` — never an upstream parent), runs an
-**attended, in-session** poll loop for the Augment Code review, re-grades each finding's severity
+**attended, in-session** poll loop for the review findings of two reviewers, the Augment Code App
+and the Codex connector (`chatgpt-codex-connector`), re-grades each finding's severity
 through the reused auggie-review rubric, **verifies each finding grounds in real code before
 remediating** (verify-before-remediate — no round and no push is ever spent on a hallucinated or
 stale finding), dispatches only verified findings to `/sc:troubleshoot` for diagnosis, then — at
 higher autonomy ordinals — applies the fix itself, validates, pushes, replies on the finding
 thread, and resolves it. It terminates deterministically under a capped, monotonic round counter.
 
+**Two reviewers, one path.** One poll snapshot serves both reviewers. Each has a small adapter in
+`superclaude.pr_submit` (identities, completion proof, severity, re-trigger phrase); everything
+after the normalized `Finding` list is shared. A reviewer is **present** when the snapshot holds
+activity by its identities (`reviewer_activity`); a reviewer that never shows activity is recorded
+**absent** (`reviewer_absent{reviewer}`, sticky, rebuilt on `--resume` from
+`rebuild_state()["absent_reviewers"]`) and ignored for the rest of the run, so an Augment-only or a
+Codex-only PR works unchanged. The two results are merged by `merge_wait` **before** the FSM sees
+an outcome: no new FSM state or edge.
+
 **The `--monitor {0,1,2,3}` ordinal is a capability ceiling on a SINGLE finite state machine**
 (`refs/state-machine.md`), compared at exactly three gates plus one override — NOT four divergent
 code paths. The deterministic decisions (classification, severity remap, the FSM gate table, the
@@ -46,9 +56,10 @@ wall-clock start when entering a wait (Wave 1, the S5 re-review wait, or the Wav
 1. Run the wave's poll script **once** in the foreground (`scripts/poll-augment-review.sh` or
    `scripts/poll-ci-checks.sh`, always `--repo "$REPO"`). A non-zero exit is a prerequisite or
    usage failure: stop and report it, never retry it as `polling`.
-2. Classify the one JSON line with the existing core: use the **Augment snapshot gate** below,
+2. Classify the one JSON line with the existing core: use the **review snapshot gate** below
+   (Augment and Codex on the same snapshot, then `merge_wait`),
    or `superclaude.pr_submit.ci.classify_checks` for CI; append the run-log event only after the gate.
-3. Validated non-polling result → leave the wait and continue the wave. For Augment `polling`, do **not**
+3. Validated non-polling merged result → leave the wait and continue the wave. For Augment `polling`, do **not**
    call raw `timed_out`. Compute `silent = poll_succeeded(payload) and not has_augment_activity(payload, contract)`, then
    `st = rebuild_state()`, `already = pr in st["silence_rerequest_invoked"]`,
    `clock = st["silence_rerequested_at"]`, and
@@ -58,8 +69,13 @@ wall-clock start when entering a wait (Wave 1, the S5 re-review wait, or the Wav
    If True, append `{event_type: silence_rerequested, pr_number, elapsed}` then
    `scripts/retrigger-review.sh --body "augment review" --pr <N> --repo "$REPO"`. That write-ahead pair
    does not tick `round_counter` or `rereview_request_count`. Then sleep ≥ `--poll-interval` and continue.
-   `TERMINAL_AUGMENT_NO_RESPONSE` → report App trigger mode, Allowlist, quota; comment `augment review` by hand; Wave 8 wait-only (`should_arm_ci_wait` True, `ci_wait_autofix` False); never `transition(clean)`.
-   `TERMINAL_TIMEOUT` → partial activity, no Wave 8. CI `polling` still uses `timed_out` for the Wave 8 timeout. Else wait **at least** `--poll-interval` seconds (or `fsm.next_backoff` after
+   The silence poke is Augment-only; Codex is never poked. `nxt` is **Augment's** wait outcome, not
+   the run's: pass it to `merge_wait` (gate section below; `nxt = None` when Augment is not `polling`).
+   When `nxt` is `TERMINAL_AUGMENT_NO_RESPONSE` while Codex is present, append
+   `reviewer_absent{reviewer: "augment"}` and continue the wait with Codex alone; do not stop.
+   Only the merged outcomes end the wait:
+   merged `no_response` (no configured reviewer, Augment or Codex, responded) → `TERMINAL_AUGMENT_NO_RESPONSE` → report App trigger mode, Allowlist, quota; comment `augment review` by hand; Wave 8 wait-only (`should_arm_ci_wait` True, `ci_wait_autofix` False); never `transition(clean)`.
+   merged `timeout` → `TERMINAL_TIMEOUT` → partial activity, no Wave 8. CI `polling` still uses `timed_out` for the Wave 8 timeout. Else wait **at least** `--poll-interval` seconds (or `fsm.next_backoff` after
    403/429; the wait counts toward `--timeout`) with a bounded blocking wait the host permits, then
    repeat from 1.
 
@@ -69,16 +85,19 @@ detached loop, or subagent, and never claim the wait survives session exit. The
 (L0/L1/L2/L3), `round_counter` / `max_rounds`, and `HALT_MAX_ROUNDS` preservation are unchanged by
 the loop.
 
-### Augment snapshot gate (normative; before any FSM outcome)
+### Review snapshot gate (normative; before any FSM outcome)
 
-For the initial wait set `pushed_sha = None`, `watermark = None`. In S5 retain the exact pushed full
-SHA and a trustworthy UTC re-trigger watermark (see `refs/review-retrigger.md`). On each poll execute
-this gate using the same immutable snapshot; the public explicit head argument is an **override**,
-not a comparison against the actual snapshot head:
+For the initial wait set `pushed_sha = None`, `watermark = None`, `codex_watermark = None`. In S5
+retain the exact pushed full SHA and one trustworthy UTC re-trigger watermark **per reviewer**
+(`watermark` for Augment, `codex_watermark` for Codex; see `refs/review-retrigger.md`). On each
+poll execute this gate using the same immutable snapshot; the public explicit head argument is an
+**override**, not a comparison against the actual snapshot head. The Augment part is unchanged; the
+Codex part applies the same rules to the same snapshot and `expected_head`:
 
 ```python
 from superclaude.pr_submit import (
-    actionable_finding_comments, classify, finding_from_comment, remap_severity, route,
+    actionable_finding_comments, classify, classify_codex, codex_finding_comments,
+    finding_from_comment, remap_severity, reviewer_activity, route,
 )
 
 expected_head = payload.get("head_sha") if pushed_sha is None else pushed_sha
@@ -106,8 +125,57 @@ else:
         else:
             findings = [remap_severity(finding) for finding in findings]
             routes = [route(finding) for finding in findings]
+
+codex_findings = []
+codex_routes = []
+if pushed_sha is not None and (
+    payload.get("head_sha") != pushed_sha or codex_watermark is None
+):
+    codex_state = "polling"
+else:
+    codex_state = classify_codex(
+        payload, contract, watermark=codex_watermark, current_head_sha=expected_head,
+    )
+    if codex_state == "findings":
+        selected = codex_finding_comments(
+            payload, contract, watermark=codex_watermark, current_head_sha=expected_head,
+        )
+        try:
+            if not selected:
+                raise ValueError("Codex findings signal without actionable root details")
+            codex_findings = [finding_from_comment(raw) for raw in selected]
+        except ValueError:
+            codex_state = "polling"
+            codex_findings = []
+        else:
+            codex_findings = [remap_severity(finding) for finding in codex_findings]
+            codex_routes = [route(finding) for finding in codex_findings]
+activity = reviewer_activity(payload, contract)
+```
+
+Then merge the two per-reviewer results (`augment_wait_outcome`, `codex_wait_outcome`,
+`merge_wait`, `reviewer_identities` from `superclaude.pr_submit`), after step 3 has computed `nxt`
+for an Augment `polling` state (`nxt = None` otherwise):
+
+```text
+absent = set(rebuild_state()["absent_reviewers"])   # plus, in S5, every reviewer not re-triggered this cycle
+aug_wait = augment_wait_outcome(review_state, nxt,
+    absent="augment" in absent or not reviewer_identities(contract, "augment"))
+cx_wait = codex_wait_outcome(codex_state, active=activity["codex"], elapsed=elapsed,
+    timeout=timeout, silence_timeout=silence_timeout, other_settled=aug_wait != "pending",
+    absent="codex" in absent or not reviewer_identities(contract, "codex"))
+decision = merge_wait((aug_wait, review_state), (cx_wait, codex_state))
 ```
 
+`decision["outcome"]` is the round outcome: `polling` keeps waiting; `clean` / `findings` /
+`declined` go to the FSM like today's Augment result, with the findings of the reviewers in
+`decision["used"]` (Augment's `findings` plus `codex_findings`); `no_response` and `timeout` are the
+step 3 terminal handling. For each reviewer in `decision["absent"]` that is not yet recorded (and,
+in S5, was re-triggered), append `reviewer_absent{reviewer}`; for each reviewer in
+`decision["incomplete"]` when the outcome is `clean` / `findings` / `declined`, append
+`reviewer_incomplete{reviewer, phase: "initial"|"rereview"}` and report it. Codex has no silence
+poke and no decline; a Codex `findings` result joins Augment's `declined` S5b re-entry.
+
 An empty selection is possible with legacy `has_findings` / `findings_count` signals; invalid roots
 raise `ValueError`. Both are **incomplete**, not clean: resume step 3's bounded polling without
 resetting elapsed time. Never pass `review_state="findings"` with an empty `findings` list to
@@ -122,6 +190,15 @@ optimistic legacy default; `polling` keeps waiting, expiry supplies `"timeout"`,
 uses the existing fallback without a round tick. No clean, round increment or remediation on a head
 mismatch, incomplete snapshot or normalization failure. CI retains its independent Wave 8 gate.
 
+**S5 with two reviewers.** The S5 wait covers **only the reviewers re-triggered in this cycle**
+(those with a `rereview_requested` for the `cycle_id`); every other reviewer is passed to the merge
+as absent and is not recorded absent. Each reviewer's result is attributed against its own
+watermark. The re-review is **attributed** (the INV-001 edge, one tick per cycle) when at least one
+re-triggered reviewer reaches `done` (`clean` or `findings`) on the pushed SHA; a re-triggered
+reviewer still `incomplete` at S5 expiry gets `reviewer_incomplete{reviewer, phase: "rereview"}` and
+the other reviewer's attributed result is used; `"timeout"` when none reaches `done`; `declined` when
+Augment declines (existing).
+
 The normalized findings then pass Waves 2–3: Low/Nit report-only, other tiers still require the
 read-only evidence-validator before diagnosis or edits. `verification_status` starts `"unverified"`;
 remote verification claims are ignored. An outdated unresolved root remains visible even when
@@ -163,13 +240,14 @@ monitor that could only ever report `polling`. `--monitor 0` skips this prefligh
 | `reply_count` | int | Threads replied to. |
 | `summary_posted` | bool | Whether the single clean-re-review summary thread was posted. |
 | `applied_edits` | int | Grounded edits applied this run (INV-016 predicate 5). |
-| `rereview_request_count` | int | S5a `auggie review` re-trigger comments posted (INV-R1; monotone, `<= max_rounds`). |
+| `rereview_request_count` | int | S5a re-triggered push cycles (INV-R1; one per cycle however many reviewers were re-triggered, folded by distinct `cycle_id`; monotone, `<= max_rounds`). |
+| `reviewers` | object | `{"augment": "present"\|"absent"\|"incomplete", "codex": "present"\|"absent"\|"incomplete"}`: each reviewer's standing at the end of the run. |
 | `fallback_engaged` | bool | Whether the oversized-PR `/sc:auggie-review` fallback was engaged (a `declined` was observed). |
 | `auggie_review_invoked` | bool | Whether `/sc:auggie-review` was actually invoked (INV-R2 strict-once; at most once per PR). |
 | `fallback_round_counter` | int | The SEPARATE single-shot fallback counter (cap 1, independent of `round_counter`). |
 | `run_log_path` | string | The authoritative `monitor-run-<PR>.jsonl`. |
 
-When CI wait follows Augment `HALT_MAX_ROUNDS` or `TERMINAL_AUGMENT_NO_RESPONSE`, preserve that Augment status and report CI's observed outcome (including timeout or human-gate) alongside it in the summary. CI clean is not an Augment clean re-review.
+The `status` enum is unchanged: `terminal_augment_no_response` means no configured reviewer (Augment, Codex) responded. When CI wait follows Augment `HALT_MAX_ROUNDS` or `TERMINAL_AUGMENT_NO_RESPONSE`, preserve that Augment status and report CI's observed outcome (including timeout or human-gate) alongside it in the summary. CI clean is not an Augment clean re-review.
 
 ## Wave / Phase Structure (refs are LAZY-loaded per wave, never pre-loaded)
 
@@ -188,15 +266,15 @@ Wave 8: CI wait (after Augment clean / REPORT_ONLY / HALT_MAX_ROUNDS / TERMINAL_
 
 - **Wave 0 (all ordinals):** resolve the target repo once from the origin remote (`REPO="$(git remote get-url origin | sed -E 's#^ssh://[^/]+/##; s#^git@[^:]+:##; s#^https?://[^/]+/##; s#\.git$##')"`; only if origin has no URL, fall back to `gh repo view --json nameWithOwner -q .nameWithOwner` — never prefer it, because gh picks an `upstream` remote over `origin`) and the base branch (`gh repo view "$REPO" --json defaultBranchRef -q .defaultBranchRef.name`, overridable via `--base`). BEFORE creating anything: confirm `git remote -v` shows origin = `$REPO` and rebase if behind `origin/<base>` (with `--pr <N>`, at any level, do not rebase: the PR head is already published, so report how many commits it is behind instead). Then open the PR with `gh pr create --repo "$REPO" --base <base> --head <head> --title "..." --body "..."` and verify the returned URL's `owner/repo` equals `$REPO` (a misroute → HALT). With `--pr <N>`, skip `gh pr create` and attach to that PR instead, checking the URL from `gh pr view <N> --repo "$REPO" --json url`. Pass `--repo "$REPO"` to every poll/reply/retrigger script too. At **L0 (`--monitor 0`)** the FSM never leaves `S0_IDLE` — open the PR and return, byte-for-byte identical to today (AC-1).
 - **Wave 0 head binding (L1+ only; L0 skips it):** after `gh pr create`, or on `--pr <N>` attach, read the PR head with `gh pr view <N> --repo "$REPO" --json headRefName,headRefOid,isCrossRepository` (a failed or unparsable read → HALT) and the checkout with `git branch --show-current` and `git rev-parse HEAD`. Require `superclaude.pr_submit.fsm.pr_head_ok(local_branch, local_sha, headRefName, headRefOid, isCrossRepository, allow_cross_repo=(ordinal < 3))`; a head on a fork is allowed only below L3, where nothing is pushed. False → HALT before Wave 1 with status `terminal_halted`, reason `pr_head_mismatch` (appended to the run-log when one exists), and tell the operator: "PR #<N>'s head `<headRefName>`@<headRefOid> does not match your checkout `<local_branch>`@<local_sha>. Do not close the PR. Check out `<headRefName>` and make it equal the PR head (push if you are ahead; a branch Wave 0 rebased needs a force-push, which this skill never does for you; `git pull --ff-only` if you are behind), then re-run with `--pr <N>`." True → bind `HEAD_BRANCH := headRefName` and `pre_push_sha := headRefOid` for the whole run; every push targets `HEAD_BRANCH`, never the checkout's branch name. `--resume` repeats this binding against the live PR: when crash recovery finds a dangling `push_initiated`, check only the branch (`pr_branch_ok(local_branch, headRefName, isCrossRepository, allow_cross_repo=(ordinal < 3))` and `pr_branch_ok(<the record's target_branch>, headRefName, False)`), leave the SHA to `resolve_crash_window` (local HEAD may already be the fix commit), and set `pre_push_sha` from that record: its `target_sha` when the push landed (Branch A), its `pre_push_sha` when the push is re-driven (Branch B: skip the Wave 6 fix commit, set `target_sha` from the record, and the re-driven push first runs the Wave 6 pre-push head guard with the record's `pre_push_sha`; after Branch A, the guard's parent check stops the next push if local commits were made since the landed push); otherwise require the full `pr_head_ok` and set `pre_push_sha := headRefOid`.
-- **Wave 1 (L1+):** load the contract via `superclaude.pr_submit.DetectionContract.for_arming()` — prefers an optional operator-local override (gitignored `.dev/pr-monitor/detection-contract.locked.md`) and falls back to the SHIPPED `refs/detection-contract.md` (baked `augmentcode[bot]` / `augmentcode` defaults). A missing or unlocked override is not a halt. Initialize the output-dir + run-log + baseline, then enter the **attended poll loop** (above) with `scripts/poll-augment-review.sh` (interval ≥30s, timeout default 600s); each JSON line passes the snapshot gate before any FSM outcome; incomplete evidence keeps polling. Arm exactly once at L1+ (T-109); never at L0 (T-110). `--monitor 0` remains no-monitor.
-- **Wave 2:** load `refs/severity-routing.md`; use only the snapshot gate's `actionable_finding_comments` → `finding_from_comment` → `remap_severity(finding)` → `route(finding)` results from `superclaude.pr_submit`, then map the remapped tier to its troubleshoot route (Medium → `--fix`; High/Critical → `--depth deep --fix`; Low/Nit → report-only). NEVER emit `--depth quick --fix`.
-- **Wave 3:** load `refs/finding-verify.md`; spawn the `evidence-validator` agent (read-only) to confirm each finding's cited file:line exists and the defect reproduces. `unverified` → REPORT_ONLY, consuming NO round.
-- **Wave 4:** load `refs/troubleshoot-dispatch.md`; for VERIFIED findings only, `> Skill sc:troubleshoot-protocol` for diagnosis. **At L1 (G-edit `ordinal < 2`): PROPOSE "fix these? y/n" and apply NO edits.** At L2+ the skill applies the diagnosed edits ITSELF in the working tree (troubleshoot does NOT auto-apply — `sc:pr-submit` owns edit application in `S3_FIXING`). Before the cycle's first edit, record the operator's pending files (`git status --porcelain=v1 -z --untracked-files=all`: every modified, staged and untracked file, both sides of a rename) as `OPERATOR_PENDING`; the Wave 6 fix commit refuses any of them.
+- **Wave 1 (L1+):** load the contract via `superclaude.pr_submit.DetectionContract.for_arming()` — prefers an optional operator-local override (gitignored `.dev/pr-monitor/detection-contract.locked.md`) and falls back to the SHIPPED `refs/detection-contract.md` (baked `augmentcode[bot]` / `augmentcode` defaults). A missing or unlocked override is not a halt; the contract also carries the Codex identities (`codex_bot_login`, `codex_app_slug`) and `codex_retrigger_phrase`, and an empty Codex identity disables Codex. Initialize the output-dir + run-log + baseline, then enter the **attended poll loop** (above) with `scripts/poll-augment-review.sh` (interval ≥30s, timeout default 600s; the one snapshot serves both reviewers); each JSON line passes the snapshot gate before any FSM outcome; incomplete evidence keeps polling. Record `reviewer_absent{reviewer}` for a reviewer the merge settles as absent, and `reviewer_incomplete{reviewer, phase: "initial"}` for a present reviewer that did not complete by `--timeout` while the other's result was used. Every event that concerns one reviewer carries a `reviewer` field (`"augment"` or `"codex"`; a missing field means `augment`): `poll_result` (with the per-reviewer wait outcomes), `review_detected`, `findings_normalized`, `finding_verified`, `finding_unverified`, `route_decision`, `reply_posted`, `thread_resolved`, `rereview_requested`. On `--resume`, read `rebuild_state()["absent_reviewers"]` and keep those reviewers absent. Arm exactly once at L1+ (T-109); never at L0 (T-110). `--monitor 0` remains no-monitor.
+- **Wave 2:** load `refs/severity-routing.md`; use only the snapshot gate's `actionable_finding_comments` → `finding_from_comment` → `remap_severity(finding)` → `route(finding)` results from `superclaude.pr_submit` (Augment's and, for Codex, `codex_finding_comments` → the same three calls; a Codex P0/P1/P2/P3 badge is its severity hint, a missing or malformed badge is the Medium fail-safe), then map the remapped tier to its troubleshoot route (Medium → `--fix`; High/Critical → `--depth deep --fix`; Low/Nit → report-only). NEVER emit `--depth quick --fix`. Group the merged findings with `dedup_groups(findings)` (same path and line, `original_line` when the line is null): a **dedup group routes at its members' highest remapped tier**; every member keeps its own finding, verdict and thread.
+- **Wave 3:** load `refs/finding-verify.md`; spawn the `evidence-validator` agent (read-only) to confirm each finding's cited file:line exists and the defect reproduces (one verdict per finding, Augment and Codex in one batch). `unverified` → REPORT_ONLY, consuming NO round. A dedup group is dispatched only when at least one member is verified.
+- **Wave 4:** load `refs/troubleshoot-dispatch.md`; for VERIFIED findings only, `> Skill sc:troubleshoot-protocol` for diagnosis, once per dedup group with every verified member's body in the seed and each body naming its reviewer; the group gets one diagnosis and one set of edits (no double fix), and `fix_applied` is recorded for **every** member's `fix_key`. **At L1 (G-edit `ordinal < 2`): PROPOSE "fix these? y/n" and apply NO edits.** At L2+ the skill applies the diagnosed edits ITSELF in the working tree (troubleshoot does NOT auto-apply — `sc:pr-submit` owns edit application in `S3_FIXING`). Before the cycle's first edit, record the operator's pending files (`git status --porcelain=v1 -z --untracked-files=all`: every modified, staged and untracked file, both sides of a rename) as `OPERATOR_PENDING`; the Wave 6 fix commit refuses any of them.
 - **Wave 5:** run the VAL validator (below). **At L2 the ceiling stops here:** after applying the edits in `S3_FIXING` and validating in `S7_VALIDATING`, the FSM HALTs at `S4'_HALT_BEFORE_PUSH` — changes are left in the working tree with NO commit, NO push, NO reply (`S3_FIXING → S7_VALIDATING → S4'_HALT_BEFORE_PUSH`, matching `state-machine.md` §5.2a). Only L3 proceeds to Wave 6.
-- **Wave 6 (L3 only):** load `refs/thread-reply.md`. **Fix commit:** when the cycle applied edits (`applied_edits > 0`) and VAL is green, commit all of them as exactly one commit (one per cycle, never one per finding; VAL has already passed, so a validation retry never adds a second commit), staging only the files those edits changed (`git add -- <paths>`, never `git add -A` or `git add .`, which would sweep in run artifacts and other untracked files) and committing with `git commit --only -- <paths>` so nothing else already in the index is committed, and set `target_sha := git rev-parse HEAD`; every thread replied to in this cycle cites that one SHA. Before staging anything (before the `git add` above), if a path to commit is in `OPERATOR_PENDING`, append `terminal_halted` (reason `fix_commit_failed`), HALT with nothing committed or pushed, and tell the operator: "The fix touched files that had your own uncommitted changes: <paths>. Nothing was committed or pushed. Those files now hold both your changes and the fix: separate them by hand (do not discard the files), then re-run with `--pr <N>`." Otherwise, if the commit fails (for example a pre-commit hook rejects it) or HEAD did not advance, append `terminal_halted` (reason `fix_commit_failed`), HALT with nothing pushed, and tell the operator: "The fix commit failed (<error>). Nothing was pushed; the edits, and any changes a hook made, are in your working tree. Fix the cause, then either commit and push the fix yourself or discard it, and re-run with `--pr <N>`." A halted cycle replies to and resolves no thread. A crash re-drive (Branch B) skips this step and pushes the record's `target_sha`. **Pre-push head guard, before `push_decision`:** re-read `gh pr view <N> --repo "$REPO" --json headRefName,headRefOid,isCrossRepository` and require `pr_head_ok(<local branch>, pre_push_sha, headRefName, headRefOid, isCrossRepository)` and `headRefName == HEAD_BRANCH`. Compare the stored `pre_push_sha`, never local HEAD (local HEAD is the new fix commit). False → append `terminal_halted` (reason `pr_head_mismatch`), HALT with nothing pushed, write no push record, and tell the operator: "PR #<N>'s head moved from <pre_push_sha> to <headRefOid> (or its branch is no longer `<HEAD_BRANCH>`) during the run. Nothing was pushed. Review the new PR commits, make your checkout equal the new PR head, then re-run with `--pr <N>`." When this cycle made a fix commit, the message adds: "This cycle's fixes are in local commit <target_sha>: drop it, or rebase it onto the new head and push it yourself." Next, when the cycle applied edits (a zero-edit cycle has no fix commit; INV-016 predicate 5 blocks its push and still records `push_decision`), read the parents of the commit to push (`git rev-list --parents -n 1 <target_sha>`, dropping the first id) and require `superclaude.pr_submit.fsm.push_parent_ok(<parents>, pre_push_sha)`: a fast-forward push publishes every commit between the PR head and `target_sha`, so the push may carry only this cycle's fix commit. False → append `terminal_halted` (reason `push_range_mismatch`), HALT with nothing pushed and no push record, and tell the operator: "Nothing was pushed. The fix commit <target_sha> sits on top of local commits that are not on PR #<N>: <`git log --oneline <pre_push_sha>..<target_sha>^`>. Publish those commits yourself if you want them on the PR, otherwise drop them; make your checkout equal the PR head, then re-run with `--pr <N>` (the open review threads are fixed again)." Then set `target_branch := HEAD_BRANCH`. The deterministic core DECIDES (evaluates the INV-016 conjunction, records the write-ahead push triad `push_decision` → `push_initiated` (fsynced BEFORE the push) → `push_completed`, keyed on the PRE-push idempotency key `push:<run_id>:<cycle_id>:<pre_push_sha>:<target_branch>`); the SKILL performs the actual `git push origin <target_sha>:<target_branch>` (never an upstream parent remote, never the repo's default/protected branch, never a force push) ONLY when the conjunction holds, then set `pre_push_sha := target_sha`, then reply (citing `applied_edits` status — `applied_edits==0` says "no code change applied", never "resolved") and resolve via `scripts/reply-resolve-thread.sh` (reply FIRST, then resolve). **S5a re-trigger (FR-8):** load `refs/review-retrigger.md`; a push does NOT auto-trigger an Augment re-review — AFTER resolve, and ONLY when this cycle applied edits (`applied_edits > 0`), post the re-trigger comment via `scripts/retrigger-review.sh --pr <N>` BEFORE re-entering the S5 poll. The core decides whether/when to re-trigger (`do_retrigger` seam, INV-R1: at most once per push cycle, `rereview_request_count <= max_rounds`); the script does the `gh api` issue-comment POST (NFR-6). On posting the re-trigger, append a **`rereview_requested{cycle_id}`** run-log event (the INV-R1 producer — folded into `rereview_request_count` by `rebuild_state`, and consumed by crash recovery's OQ-1 resume decision: a landed-push crash with NO `rereview_requested` for its cycle resumes at `S5a_RETRIGGER_REVIEW` to re-post; one WITH it resumes at `S5_AWAITING_REREVIEW`). The `round_counter` ticks only when the subsequent poll attributes the re-review to our pushed SHA (the relocated INV-001 increment) — a timed-out re-trigger does NOT advance the counter.
-- **Wave 6b (L2+ decline fallback, FR-9/FR-10):** load `refs/auggie-fallback.md`. When the classifier returns `declined` (an Augment "abnormally large" decline observed at the initial S2 poll OR the S5 re-trigger poll), append a **`decline_detected`** run-log event, then engage the single-shot fallback: gate **strict-once** on the durable `auggie_review_invoked` idempotency record (comment-independent, survives resume — INV-R2; on engage, append an **`auggie_fallback_invoked{pr_number}`** event, the producer folded into that set), clamp the effective budget `effective_max_rounds := min(effective_max_rounds, 1)` (the `clamp_max_rounds` helper, recorded once via the **`max_rounds_clamped{effective_max_rounds}`** event — INV-R3 monotone-min fold), then invoke `> Skill sc:auggie-review-protocol --depth quick --remediation-offer` and re-enter Waves 2-6 ONCE under the clamp (verify-before-remediate still applies — fallback findings are NOT trusted verbatim, FR-9.4). At L2 this can apply and validate local fixes but still halts before push/reply per Wave 5; only L3 performs push, reply, resolve, and re-trigger side effects. NO second invoke, NO second re-trigger, NO loop-back; `push_count <= max_rounds + 1` for the whole run. This is `sc:pr-submit` invoking its OWN review — do **NOT** "take the App's bait" by treating the App's `augment review` decline comment as our operator re-trigger. (`--depth quick` here targets `/sc:auggie-review` — a review, no `--fix` — so it does NOT conflict with the severity-routing STOP on `--depth quick --fix`.)
+- **Wave 6 (L3 only):** load `refs/thread-reply.md`. **Fix commit:** when the cycle applied edits (`applied_edits > 0`) and VAL is green, commit all of them as exactly one commit (one per cycle, never one per finding; VAL has already passed, so a validation retry never adds a second commit), staging only the files those edits changed (`git add -- <paths>`, never `git add -A` or `git add .`, which would sweep in run artifacts and other untracked files) and committing with `git commit --only -- <paths>` so nothing else already in the index is committed, and set `target_sha := git rev-parse HEAD`; every thread replied to in this cycle cites that one SHA. Before staging anything (before the `git add` above), if a path to commit is in `OPERATOR_PENDING`, append `terminal_halted` (reason `fix_commit_failed`), HALT with nothing committed or pushed, and tell the operator: "The fix touched files that had your own uncommitted changes: <paths>. Nothing was committed or pushed. Those files now hold both your changes and the fix: separate them by hand (do not discard the files), then re-run with `--pr <N>`." Otherwise, if the commit fails (for example a pre-commit hook rejects it) or HEAD did not advance, append `terminal_halted` (reason `fix_commit_failed`), HALT with nothing pushed, and tell the operator: "The fix commit failed (<error>). Nothing was pushed; the edits, and any changes a hook made, are in your working tree. Fix the cause, then either commit and push the fix yourself or discard it, and re-run with `--pr <N>`." A halted cycle replies to and resolves no thread. A crash re-drive (Branch B) skips this step and pushes the record's `target_sha`. **Pre-push head guard, before `push_decision`:** re-read `gh pr view <N> --repo "$REPO" --json headRefName,headRefOid,isCrossRepository` and require `pr_head_ok(<local branch>, pre_push_sha, headRefName, headRefOid, isCrossRepository)` and `headRefName == HEAD_BRANCH`. Compare the stored `pre_push_sha`, never local HEAD (local HEAD is the new fix commit). False → append `terminal_halted` (reason `pr_head_mismatch`), HALT with nothing pushed, write no push record, and tell the operator: "PR #<N>'s head moved from <pre_push_sha> to <headRefOid> (or its branch is no longer `<HEAD_BRANCH>`) during the run. Nothing was pushed. Review the new PR commits, make your checkout equal the new PR head, then re-run with `--pr <N>`." When this cycle made a fix commit, the message adds: "This cycle's fixes are in local commit <target_sha>: drop it, or rebase it onto the new head and push it yourself." Next, when the cycle applied edits (a zero-edit cycle has no fix commit; INV-016 predicate 5 blocks its push and still records `push_decision`), read the parents of the commit to push (`git rev-list --parents -n 1 <target_sha>`, dropping the first id) and require `superclaude.pr_submit.fsm.push_parent_ok(<parents>, pre_push_sha)`: a fast-forward push publishes every commit between the PR head and `target_sha`, so the push may carry only this cycle's fix commit. False → append `terminal_halted` (reason `push_range_mismatch`), HALT with nothing pushed and no push record, and tell the operator: "Nothing was pushed. The fix commit <target_sha> sits on top of local commits that are not on PR #<N>: <`git log --oneline <pre_push_sha>..<target_sha>^`>. Publish those commits yourself if you want them on the PR, otherwise drop them; make your checkout equal the PR head, then re-run with `--pr <N>` (the open review threads are fixed again)." Then set `target_branch := HEAD_BRANCH`. The deterministic core DECIDES (evaluates the INV-016 conjunction, records the write-ahead push triad `push_decision` → `push_initiated` (fsynced BEFORE the push) → `push_completed`, keyed on the PRE-push idempotency key `push:<run_id>:<cycle_id>:<pre_push_sha>:<target_branch>`); the SKILL performs the actual `git push origin <target_sha>:<target_branch>` (never an upstream parent remote, never the repo's default/protected branch, never a force push) ONLY when the conjunction holds, then set `pre_push_sha := target_sha`, then reply (citing `applied_edits` status — `applied_edits==0` says "no code change applied", never "resolved") and resolve via `scripts/reply-resolve-thread.sh` (reply FIRST, then resolve; the script finds the thread by its root comment id, so an Augment or a Codex root works the same). In a dedup group, **every verified member's thread** is replied to and resolved, all citing the cycle's one fix SHA; an unverified or Low/Nit member gets no reply and no resolve, and the report lists the group once with "flagged by: augment, codex". **S5a re-trigger (FR-8):** load `refs/review-retrigger.md`; a push does NOT auto-trigger a re-review by either bot — AFTER resolve, and ONLY when this cycle applied edits (`applied_edits > 0`), post **one re-trigger comment per present reviewer** BEFORE re-entering the S5 poll: for each reviewer in `pending_retriggers(<run-log events>, cycle_id, <present reviewers>)` (the present reviewers that have no `rereview_requested` for this `cycle_id` yet), run `scripts/retrigger-review.sh --pr <N> --repo "$REPO" --body "<retrigger_phrase(contract, reviewer)>"` (`auggie review` for Augment, `@codex review` for Codex). The core decides whether/when to re-trigger (`do_retrigger` seam, INV-R1: at most once per push cycle, `rereview_request_count <= max_rounds`, counted per cycle, not per comment); the script does the `gh api` issue-comment POST (NFR-6). Right after each reviewer's successful POST, take that reviewer's UTC watermark and append a **`rereview_requested{cycle_id, reviewer, timestamp}`** run-log event with that time (the INV-R1 producer — folded into `rereview_request_count` by distinct `cycle_id` in `rebuild_state`, and consumed by crash recovery's OQ-1 resume decision: a landed-push crash with NO `rereview_requested` for its cycle resumes at `S5a_RETRIGGER_REVIEW` to re-post; one WITH it resumes at `S5_AWAITING_REREVIEW`). **Resume of a re-triggered cycle:** reuse the `cycle_id` of the dangling push record (never a new one); on every resume at `S5a_RETRIGGER_REVIEW` or `S5_AWAITING_REREVIEW`, first call `pending_retriggers` and post the reviewers still missing (a crash between the Augment and the Codex post neither skips Codex nor re-posts Augment), then take each reviewer's watermark from the `timestamp` of its latest `rereview_requested` for the cycle before the S5 poll. The `round_counter` ticks only when the subsequent poll attributes the re-review to our pushed SHA (the relocated INV-001 increment) — a timed-out re-trigger does NOT advance the counter.
+- **Wave 6b (L2+ decline fallback, FR-9/FR-10):** load `refs/auggie-fallback.md`. When the classifier returns `declined` (an Augment "abnormally large" decline observed at the initial S2 poll OR the S5 re-trigger poll), append a **`decline_detected`** run-log event, then engage the single-shot fallback: gate **strict-once** on the durable `auggie_review_invoked` idempotency record (comment-independent, survives resume — INV-R2; on engage, append an **`auggie_fallback_invoked{pr_number}`** event, the producer folded into that set), clamp the effective budget `effective_max_rounds := min(effective_max_rounds, 1)` (the `clamp_max_rounds` helper, recorded once via the **`max_rounds_clamped{effective_max_rounds}`** event — INV-R3 monotone-min fold), then invoke `> Skill sc:auggie-review-protocol --depth quick --remediation-offer` and re-enter Waves 2-6 ONCE under the clamp, with the fallback's findings plus any merged Codex `findings` of the same round (verify-before-remediate still applies — fallback findings are NOT trusted verbatim, FR-9.4). At L2 this can apply and validate local fixes but still halts before push/reply per Wave 5; only L3 performs push, reply, resolve, and re-trigger side effects. NO second invoke, NO second re-trigger (for either reviewer), NO loop-back; `push_count <= max_rounds + 1` for the whole run. This is `sc:pr-submit` invoking its OWN review — do **NOT** "take the App's bait" by treating the App's `augment review` decline comment as our operator re-trigger. (`--depth quick` here targets `/sc:auggie-review` — a review, no `--fix` — so it does NOT conflict with the severity-routing STOP on `--depth quick --fix`.)
 - **Wave 7:** load `refs/loop-guard.md`; the round counter ticks only at `S5_AWAITING_REREVIEW → S2_CLASSIFY`; HALT at `round_counter >= max_rounds`. Fallback outcomes REUSE the existing `terminal_clean` / `terminal_max_rounds` status values (OQ-2 reuse recommendation).
-- **Wave 8 (L1+, after Augment `clean` / `REPORT_ONLY` / `HALT_MAX_ROUNDS` / `TERMINAL_AUGMENT_NO_RESPONSE`):** load `refs/ci-poll.md`. Arm via `superclaude.pr_submit.ci.should_arm_ci_wait`. Do **not** `transition(clean)` yet. Set SKILL-owned `source=ci`, reset wait elapsed, switch the attended poll loop to `scripts/poll-ci-checks.sh --pr <N> --repo "$REPO"`. Classify via `superclaude.pr_submit.ci.classify_checks(payload, wait_sha=<sha at flip or last push>)`. Human-gate (`is_human_gate`) → `HALT_HUMAN` when Augment has not halted; after Augment `HALT_MAX_ROUNDS` or `TERMINAL_AUGMENT_NO_RESPONSE`, keep its terminal status and report the CI human-gate alongside it. No Finding or auto-fix on those wait-only paths (`ci_wait_autofix` is false). If `round_counter >= max_rounds`, CI polling is wait-only: non-human `findings` → `REPORT_ONLY` without fetching logs, editing, or pushing. Otherwise non-human `findings` → `gh run view <id> --repo "$REPO" --log-failed` once → `findings_from_logs`; empty → `REPORT_ONLY`; else Waves 3–5 under the same ordinals and `round_counter`. An L3 CI push runs the Wave 6 pre-push head guard and push triad with `target_branch := HEAD_BRANCH`, then sets `pre_push_sha := target_sha`. It also makes the Wave 6 single fix commit and runs the guard's parent check (`push_parent_ok`), so this push too carries only the cycle's one fix commit. After an L3 CI push: do **not** call `retrigger-review.sh`, reply, or resolve; re-poll CI on the new `headRefOid`. When CI is `clean` after an ordinary Augment `clean` / `REPORT_ONLY`, send `transition(clean)` → `TERMINAL_CLEAN`. After `HALT_MAX_ROUNDS` or `TERMINAL_AUGMENT_NO_RESPONSE`, leave that terminal FSM status unchanged and report CI clean alongside it (no `transition(clean)` from a terminal state — never claim `TERMINAL_CLEAN` for a silent Augment review). L0 never reaches Wave 8. Do not arm on `HALT_HUMAN` / `VALIDATION_FAIL` / `TERMINAL_TIMEOUT` / `TERMINAL_FAILED`. CI `polling` continues at the configured interval until completion or timeout; when the chosen list is empty, a failed check query is `polling`, not no-Actions `clean`. Only parsed empty required **and** all-checks lists prove there are no Actions. A nonempty required list is the chosen set; optional pending checks outside it do not block completion.
+- **Wave 8 (L1+, after Augment `clean` / `REPORT_ONLY` / `HALT_MAX_ROUNDS` / `TERMINAL_AUGMENT_NO_RESPONSE`):** load `refs/ci-poll.md`. These are the merged review outcomes: `clean` is the merged clean of the reviewers used, and `TERMINAL_AUGMENT_NO_RESPONSE` is reached only when no configured reviewer responded (a silent Augment with Codex present continues with Codex and never arms from here). Arm via `superclaude.pr_submit.ci.should_arm_ci_wait`. Do **not** `transition(clean)` yet. Set SKILL-owned `source=ci`, reset wait elapsed, switch the attended poll loop to `scripts/poll-ci-checks.sh --pr <N> --repo "$REPO"`. Classify via `superclaude.pr_submit.ci.classify_checks(payload, wait_sha=<sha at flip or last push>)`. Human-gate (`is_human_gate`) → `HALT_HUMAN` when Augment has not halted; after Augment `HALT_MAX_ROUNDS` or `TERMINAL_AUGMENT_NO_RESPONSE`, keep its terminal status and report the CI human-gate alongside it. No Finding or auto-fix on those wait-only paths (`ci_wait_autofix` is false). If `round_counter >= max_rounds`, CI polling is wait-only: non-human `findings` → `REPORT_ONLY` without fetching logs, editing, or pushing. Otherwise non-human `findings` → `gh run view <id> --repo "$REPO" --log-failed` once → `findings_from_logs`; empty → `REPORT_ONLY`; else Waves 3–5 under the same ordinals and `round_counter`. An L3 CI push runs the Wave 6 pre-push head guard and push triad with `target_branch := HEAD_BRANCH`, then sets `pre_push_sha := target_sha`. It also makes the Wave 6 single fix commit and runs the guard's parent check (`push_parent_ok`), so this push too carries only the cycle's one fix commit. After an L3 CI push: do **not** call `retrigger-review.sh`, reply, or resolve; re-poll CI on the new `headRefOid`. When CI is `clean` after an ordinary Augment `clean` / `REPORT_ONLY`, send `transition(clean)` → `TERMINAL_CLEAN`. After `HALT_MAX_ROUNDS` or `TERMINAL_AUGMENT_NO_RESPONSE`, leave that terminal FSM status unchanged and report CI clean alongside it (no `transition(clean)` from a terminal state — never claim `TERMINAL_CLEAN` for a silent Augment review). L0 never reaches Wave 8. Do not arm on `HALT_HUMAN` / `VALIDATION_FAIL` / `TERMINAL_TIMEOUT` / `TERMINAL_FAILED`. CI `polling` continues at the configured interval until completion or timeout; when the chosen list is empty, a failed check query is `polling`, not no-Actions `clean`. Only parsed empty required **and** all-checks lists prove there are no Actions. A nonempty required list is the chosen set; optional pending checks outside it do not block completion.
 
 ## VAL — the §10 validation gate list (owned by the SKILL, not the core)
 
@@ -238,8 +316,11 @@ A validation retry does NOT increment `round_counter`.
 | Checkout is not the PR head (Wave 0 head binding) or the PR head moved before a push (pre-push head guard) | `terminal_halted`, reason `pr_head_mismatch`; nothing pushed; do NOT close the PR; give the recovery steps from the HALT message. |
 | The commit to push is not exactly one commit on top of the PR head (the pre-push head guard's parent check) | `terminal_halted`, reason `push_range_mismatch`; nothing pushed; do NOT close the PR; list the other local commits and tell the operator to make the checkout equal the PR head, then re-run with `--pr <N>`. |
 | The fix touched a file with the operator's own pending changes, the fix commit fails, or HEAD does not advance (Wave 6 fix commit) | `terminal_halted`, reason `fix_commit_failed`; nothing pushed; do NOT close the PR; edits (and any hook changes) left in the working tree; never tell the operator to discard a file that holds their own changes; give the recovery steps from the HALT message. |
-| Augment silent (no attributed review/comment) | `terminal_augment_no_response`; Wave 8 wait-only; check App trigger mode, Allowlist, quota; comment `augment review` by hand. |
-| Review starts but never completes | `terminal_timeout`; no Wave 8; no edits/push. |
+| Augment silent while Codex is present | `reviewer_absent{reviewer: "augment"}`; the run continues with Codex alone. |
+| Codex shows no activity by the time Augment settles (or by `--silence-timeout`) | `reviewer_absent{reviewer: "codex"}`; Codex is ignored for the run (no wait, no re-trigger, no poke). |
+| No configured reviewer responded (Augment and Codex both absent) | `terminal_augment_no_response`; Wave 8 wait-only; check App trigger mode, Allowlist, quota; comment `augment review` by hand. |
+| One reviewer completes, the other is active but never completes | the completed reviewer's result is used; `reviewer_incomplete{reviewer, phase}` is recorded and reported. |
+| Review starts but never completes (no reviewer completes) | `terminal_timeout`; no Wave 8; no edits/push. |
 | 403 / 429 / secondary-limit | exponential backoff 30→…→cap 300s, counts toward timeout. |
 | `needs_human_decision` finding | `terminal_halted`; no auto-mutation (override, FR-4.4). |
 | Validation failure | no push/reply/resolve; L2 halt; L3 one retry within budget. |
--- a/tests/pr_submit/test_codex_reviews.py
+++ b/tests/pr_submit/test_codex_reviews.py
@@ -12,6 +12,7 @@
 import copy
 import json
 import os
+import re
 import subprocess
 from pathlib import Path
 
@@ -649,3 +650,78 @@
             "body=@codex review",
         ]
     ]
+
+
+# --- 10. the SKILL snapshot gate and the A5 wording (design sections 14 and 18) -----
+
+SKILL_MD = SCRIPTS.parent / "SKILL.md"
+
+
+def _skill_gate(payload, *, pushed_sha=None, watermark=None, codex_watermark=None):
+    text = SKILL_MD.read_text(encoding="utf-8")
+    blocks = re.findall(r"```python\n(.*?)\n```", text, re.DOTALL)
+    assert len(blocks) == 1, "keep one executable snapshot gate"
+    namespace = {
+        "payload": payload,
+        "contract": CONTRACT,
+        "pushed_sha": pushed_sha,
+        "watermark": watermark,
+        "codex_watermark": codex_watermark,
+    }
+    exec(compile(blocks[0], str(SKILL_MD), "exec"), namespace)
+    return namespace
+
+
+def test_skill_gate_adds_the_codex_part_on_the_same_snapshot(findings336):
+    gated = _skill_gate(findings336)
+    assert gated["codex_state"] == "findings"
+    assert [f.reviewer for f in gated["codex_findings"]] == ["codex"] * 3
+    assert gated["codex_routes"] == ["--fix"] * 3
+    assert gated["activity"] == {"augment": True, "codex": True}
+    assert gated["review_state"] == classify(findings336, CONTRACT)
+
+
+def test_skill_gate_codex_part_keeps_the_pushed_head_and_watermark_rules(findings336):
+    head = findings336["head_sha"]
+    assert _skill_gate(findings336, pushed_sha="b" * 40)["codex_state"] == "polling"
+    assert _skill_gate(findings336, pushed_sha=head)["codex_state"] == "polling"
+    late = "2099-01-01T00:00:00Z"
+    gated = _skill_gate(findings336, pushed_sha=head, codex_watermark=late)
+    assert gated["codex_state"] == "polling" and gated["codex_findings"] == []
+
+
+def test_skill_states_the_a5_rules():
+    """A5: the SKILL text states the dedup, S5, fallback, event and resume rules."""
+    text = SKILL_MD.read_text(encoding="utf-8")
+    for fragment in (
+        "dedup_groups(findings)",
+        "routes at its members' highest remapped tier",
+        "`fix_applied` is recorded for **every** member's `fix_key`",
+        "**every verified member's thread** is replied to and resolved",
+        '"flagged by: augment, codex"',
+        "covers **only the reviewers re-triggered in this cycle**",
+        "at least one\nre-triggered reviewer reaches `done`",
+        'reviewer_incomplete{reviewer, phase: "rereview"}',
+        "plus any merged Codex `findings`",
+        'rebuild_state()["absent_reviewers"]',
+        "pending_retriggers(",
+        "rereview_requested{cycle_id, reviewer, timestamp}",
+        "reuse the `cycle_id` of the dangling push record",
+    ):
+        assert fragment in text, fragment
+    events = text[text.index("Every event that concerns one reviewer") :]
+    events = events[: events.index("On `--resume`")]
+    for name in (
+        "poll_result",
+        "review_detected",
+        "findings_normalized",
+        "finding_verified",
+        "finding_unverified",
+        "route_decision",
+        "reply_posted",
+        "thread_resolved",
+        "rereview_requested",
+    ):
+        assert f"`{name}`" in events, name
+    resume = text[text.index("**Resume of a re-triggered cycle:**") :]
+    assert resume.index("pending_retriggers") < resume.index("before the S5 poll")
diff --git a/tests/pr_submit/test_cosmos_protocol.py b/tests/pr_submit/test_cosmos_protocol.py
index 3d8d7a18..c8efa068 100644
--- a/tests/pr_submit/test_cosmos_protocol.py
+++ b/tests/pr_submit/test_cosmos_protocol.py
@@ -39,6 +39,7 @@ def attended_gate(payload, *, pushed_sha=None, watermark=WATERMARK):
         "contract": core.DetectionContract.load(SKILL / "refs/detection-contract.md"),
         "pushed_sha": pushed_sha,
         "watermark": watermark,
+        "codex_watermark": None,
     }
     exec(compile(blocks[0], str(SKILL / "SKILL.md"), "exec"), namespace)
     return namespace
diff --git a/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t12-grep.log b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t12-grep.log
new file mode 100644
index 00000000..d8eb5ce4
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t12-grep.log
@@ -0,0 +1,4 @@
+start sha: d1b69dd3df21a9feeb693d5f515e4611b521f6a6 tree=50c5db15
+$ grep -n src/superclaude on start-tree SKILL.md
+$ grep -n src/superclaude on live SKILL.md
+rc=1
diff --git a/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t12-sync.log b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t12-sync.log
new file mode 100644
index 00000000..52c90cec
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t12-sync.log
@@ -0,0 +1,217 @@
+🔄 Syncing src/superclaude/ → .claude/ for local development...
+✅ Sync complete.
+   Skills:    36 directories
+   Agents:    45 files
+   Commands:  43 files
+   Hooks:     12 files
+   Templates: 52 files
+sync-dev rc=0
+🔍 Verifying src/superclaude/ ↔ .claude/ sync...
+
+=== Skills ===
+  ✅ ccsession-tag
+  ✅ confidence-check
+  ✅ operational-guide
+  ✅ prd
+  ✅ readme
+  ✅ roadmap
+  ✅ sc-adversarial-protocol
+  ✅ sc-auggie-review-protocol
+  ✅ sc-bare-review
+  ✅ sc-brainstorm-protocol
+  ✅ sc-cleanup-audit-protocol
+  ✅ sc-cli-eval-protocol
+  ✅ sc-cli-portify-protocol
+  ✅ sc-crash-recovery
+  ✅ sc-implement-protocol
+  ✅ sc-init-lite-protocol
+  ✅ sc-pm-protocol
+  ✅ sc-post-release-protocol
+  ✅ sc-pr-submit-protocol
+  ✅ sc-recommend
+  ✅ sc-reflect-protocol
+  ✅ sc-release-split-protocol
+  ✅ sc-review-translation-protocol
+  ✅ sc-roadmap-protocol
+  ✅ sc-swarm-wizard-protocol
+  ✅ sc-task-protocol
+  ✅ sc-tasklist-protocol
+  ✅ sc-troubleshoot-protocol
+  ✅ sc-validate-roadmap-protocol
+  ✅ sc-validate-tests-protocol
+  ✅ sc-workflow-protocol
+  ✅ task-builder
+  ✅ task
+  ✅ tdd
+  ✅ tech-reference
+  ✅ tech-research
+
+=== Agents ===
+  ✅ audit-analyzer.md
+  ✅ audit-comparator.md
+  ✅ audit-consolidator.md
+  ✅ audit-scanner.md
+  ✅ audit-validator.md
+  ✅ auggie-reviewer.md
+  ✅ backend-architect.md
+  ✅ business-panel-experts.md
+  ✅ confidence-calibrator.md
+  ✅ debate-orchestrator.md
+  ✅ deep-research-agent.md
+  ✅ deep-research.md
+  ✅ devops-architect.md
+  ✅ eval-docs-loader.md
+  ✅ eval-run-reporter.md
+  ✅ eval-suite-author.md
+  ✅ evidence-validator.md
+  ✅ frontend-architect.md
+  ✅ implement-retry-adviser.md
+  ✅ learning-guide.md
+  ✅ merge-executor.md
+  ✅ performance-engineer.md
+  ✅ pm-agent.md
+  ✅ python-expert.md
+  ✅ quality-engineer.md
+  ✅ refactoring-expert.md
+  ✅ reflect-reviewer.md
+  ✅ repo-index.md
+  ✅ requirements-analyst.md
+  ✅ reuse-auditor.md
+  ✅ rf-analyst.md
+  ✅ rf-assembler.md
+  ✅ rf-qa-qualitative.md
+  ✅ rf-qa.md
+  ✅ rf-task-builder.md
+  ✅ rf-task-executor.md
+  ✅ rf-task-researcher.md
+  ✅ rf-team-lead.md
+  ✅ root-cause-analyst.md
+  ✅ security-engineer.md
+  ✅ self-review.md
+  ✅ socratic-mentor.md
+  ✅ system-architect.md
+  ✅ technical-writer.md
+  ✅ troubleshoot-analyst.md
+
+=== Commands ===
+  ✅ adversarial.md
+  ✅ agent.md
+  ✅ analyze.md
+  ✅ auggie-review.md
+  ✅ brainstorm.md
+  ✅ build.md
+  ✅ business-panel.md
+  ✅ cleanup-audit.md
+  ✅ cleanup.md
+  ✅ cli-eval.md
+  ✅ cli-portify.md
+  ✅ design.md
+  ✅ document.md
+  ✅ explain.md
+  ✅ git.md
+  ✅ help.md
+  ✅ implement.md
+  ✅ improve.md
+  ✅ index-repo.md
+  ✅ index.md
+  ✅ init-lite.md
+  ✅ load.md
+  ✅ pm.md
+  ✅ post-release.md
+  ✅ pr-submit.md
+  ✅ recommend.md
+  ✅ reflect.md
+  ✅ release-split.md
+  ✅ research.md
+  ✅ review-translation.md
+  ✅ roadmap.md
+  ✅ save.md
+  ✅ spawn.md
+  ✅ spec-panel.md
+  ✅ swarm-wizard.md
+  ✅ task.md
+  ✅ tasklist.md
+  ✅ tdd.md
+  ✅ test.md
+  ✅ troubleshoot.md
+  ✅ validate-roadmap.md
+  ✅ validate-tests.md
+  ✅ workflow.md
+
+=== Hooks ===
+  ✅ auggie-flag-clear.sh
+  ✅ codegraph-session-start.sh
+  ✅ freshness-file-changed.sh
+  ✅ freshness-post-read.sh
+  ✅ freshness-pre-edit.sh
+  ✅ freshness-session-start.sh
+  ✅ freshness-subagent-start.sh
+  ✅ freshness-subagent-stop.sh
+  ✅ freshness-user-prompt.sh
+  ✅ reject-workspace-writes.sh
+  ✅ sc-recommend-phase0.sh
+  ✅ pragmatic-subagent.js
+
+=== Templates ===
+  ✅ workflow/05_prd_template.md
+  ✅ workflow/03_project_plan_template.md
+  ✅ workflow/03_component_authoring_template.md
+  ✅ workflow/00_mdtm_template_simple_task.md
+  ✅ workflow/01_mdtm_template_generic_task__gfdoc.md
+  ✅ workflow/06_architecture_proposal_template.md
+  ✅ workflow/02_mdtm_template_complex_task.md
+  ✅ workflow/04_feature_brief_template.md
+  ✅ workflow/changelog_template.md
+  ✅ workflow/01_mdtm_template_generic_task.md
+  ✅ workflow/99_mdtm_template_generic_task_old.md
+  ✅ documents/prd_template.md
+  ✅ documents/operational_guide_template.md
+  ✅ documents/GFxAI_Master_Documentation_Template.md
+  ✅ documents/tdd_template.md
+  ✅ documents/agent_template_analysis.md
+  ✅ documents/supplemental-doc-creation-checklist.md
+  ✅ documents/agent_template_qa.md
+  ✅ documents/skill_template.md
+  ✅ documents/roadmap_template.md
+  ✅ documents/agent_template_worker.md
+  ✅ documents/release-spec-template.md
+  ✅ documents/supplemental_doc_template.md
+  ✅ documents/technical_reference_template.md
+  ✅ documents/readme_template.md
+  ✅ modularization-template-review/qa-fix-summary_template.md
+  ✅ modularization-template-review/qa-task-research-alignment_report_template.md
+  ✅ modularization-template-review/analyst-synthesis-review_report_template.md
+  ✅ modularization-template-review/research-notes_template.md
+  ✅ modularization-template-review/synthetic-dnsp-finding.contract
+  ✅ modularization-template-review/INDEX.md
+  ✅ modularization-template-review/qa-task-validation-structure_report_template.md
+  ✅ modularization-template-review/qa-cross-source-contradictions_template.md
+  ✅ modularization-template-review/track-scope-map_template.md
+  ✅ modularization-template-review/claim-evidence-matrix_template.md
+  ✅ modularization-template-review/qa-inventory_report_template.md
+  ✅ modularization-template-review/analyst-coverage-matrix_template.md
+  ✅ modularization-template-review/codebase-research_template.md
+  ✅ modularization-template-review/analyst-completeness_report_template.md
+  ✅ modularization-template-review/analyst-gap-analysis_template.md
+  ✅ modularization-template-review/qa-lens_report_template.md
+  ✅ modularization-template-review/qa-consolidated-findings_template.md
+  ✅ modularization-template-review/qa-task-validation-b2_report_template.md
+  ✅ modularization-template-review/qa-research-gap_report_template.md
+  ✅ modularization-template-review/qa-research-evidence_report_template.md
+  ✅ modularization-template-review/qa-qualitative-operational_report_template.md
+  ✅ modularization-template-review/qa-qualitative-sufficiency_report_template.md
+  ✅ modularization-template-review/analyst-cross-validation_report_template.md
+  ✅ modularization-template-review/qa-acceptance-methodology-audit_template.md
+  ✅ modularization-template-review/pipeline-complete_report_template.md
+  ✅ modularization-template-review/qa-source-fidelity_template.md
+  ✅ modularization-template-review/qa-research-depth_report_template.md
+  ✅ modularization-template-review/web-research_template.md
+
+=== Installer Registration ===
+  ✅ _FRESHNESS_SCRIPTS matches src/superclaude/hooks/scripts/*.sh and *.js
+
+=== Hooks Cross-Consistency ===
+  ✅ hooks.json matcher and auggie-flag-clear.sh case body agree on auggie prefixes
+
+✅ All components in sync.
+verify-sync rc=0
diff --git a/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t12-test.log b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t12-test.log
new file mode 100644
index 00000000..842df16a
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t12-test.log
@@ -0,0 +1,56 @@
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
+SuperClaude: 4.3.5
+benchmark: 5.3.0 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
+rootdir: /home/coder/workspaces/IronClaude/.dev/worktrees/pr-submit-codex
+configfile: pyproject.toml
+plugins: superclaude-4.3.5, benchmark-5.3.0, anyio-4.15.1, cov-7.1.0
+collected 705 items
+
+tests/pr_submit/test_auggie_fallback.py ............                     [  1%]
+tests/pr_submit/test_augment_review_remediation.py .......               [  2%]
+tests/pr_submit/test_autonomy_gates.py .......                           [  3%]
+tests/pr_submit/test_ci_classify.py ....................                 [  6%]
+tests/pr_submit/test_codex_reviews.py .................................. [ 11%]
+........................                                                 [ 14%]
+tests/pr_submit/test_contract_setup_diagnosis.py ..............          [ 16%]
+tests/pr_submit/test_contract_setup_evidence.py .....................    [ 19%]
+tests/pr_submit/test_contract_setup_pr_submit_integration.py ......      [ 20%]
+tests/pr_submit/test_contract_setup_questions.py .........               [ 21%]
+tests/pr_submit/test_contract_setup_validation.py .............          [ 23%]
+tests/pr_submit/test_contract_setup_writer.py ................           [ 25%]
+tests/pr_submit/test_cosmos_poll.py .................................... [ 31%]
+...............................................................          [ 40%]
+tests/pr_submit/test_cosmos_protocol.py ...............                  [ 42%]
+tests/pr_submit/test_cosmos_review.py .................................. [ 46%]
+........................................................................ [ 57%]
+                                                                         [ 57%]
+tests/pr_submit/test_crash_recovery.py ................                  [ 59%]
+tests/pr_submit/test_detection_contract.py ............................. [ 63%]
+.....                                                                    [ 64%]
+tests/pr_submit/test_edge_cases.py ...................                   [ 66%]
+tests/pr_submit/test_finding_verify.py ...                               [ 67%]
+tests/pr_submit/test_gate_helper_coverage.py ...........                 [ 68%]
+tests/pr_submit/test_gate_helper_differentials.py ...................... [ 72%]
+                                                                         [ 72%]
+tests/pr_submit/test_idempotency.py ......                               [ 72%]
+tests/pr_submit/test_loop_guard.py .............                         [ 74%]
+tests/pr_submit/test_monitor_arm.py ...                                  [ 75%]
+tests/pr_submit/test_pre_pr_checks.py .................................. [ 80%]
+.....                                                                    [ 80%]
+tests/pr_submit/test_rate_limit.py ....                                  [ 81%]
+tests/pr_submit/test_reply_resolve.py ..........                         [ 82%]
+tests/pr_submit/test_review_retrigger.py .......                         [ 83%]
+tests/pr_submit/test_run_log.py ............                             [ 85%]
+tests/pr_submit/test_setup_questions_resolution.py ....                  [ 85%]
+tests/pr_submit/test_severity_router.py ............................     [ 89%]
+tests/pr_submit/test_silence.py .................                        [ 92%]
+tests/pr_submit/test_skill_parse.py ..............                       [ 94%]
+tests/pr_submit/test_static_grep.py ...................                  [ 97%]
+tests/pr_submit/test_timeout.py .....                                    [ 97%]
+tests/pr_submit/test_troubleshoot_seed.py ....                           [ 98%]
+tests/pr_submit/test_validated_not_verified.py ...                       [ 98%]
+tests/pr_submit/test_validation_gate.py .........                        [100%]
+
+============================= 705 passed in 14.52s =============================
+rc=0
diff --git a/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t12-skill-parse.log b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t12-skill-parse.log
new file mode 100644
index 00000000..2e390c6e
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t12-skill-parse.log
@@ -0,0 +1,13 @@
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
+SuperClaude: 4.3.5
+benchmark: 5.3.0 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
+rootdir: /home/coder/workspaces/IronClaude/.dev/worktrees/pr-submit-codex
+configfile: pyproject.toml
+plugins: superclaude-4.3.5, benchmark-5.3.0, anyio-4.15.1, cov-7.1.0
+collected 14 items
+
+tests/pr_submit/test_skill_parse.py ..............                       [100%]
+
+============================== 14 passed in 0.07s ==============================
+rc=0
diff --git a/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t12-lint.log b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t12-lint.log
new file mode 100644
index 00000000..bbea970e
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t12-lint.log
@@ -0,0 +1,2 @@
+All checks passed!
+39 files already formatted
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
