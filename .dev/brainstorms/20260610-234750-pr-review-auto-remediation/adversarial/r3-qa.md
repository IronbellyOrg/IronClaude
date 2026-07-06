---
artifact: adversarial-round-3-resolution
role: qa
round: 3
topic: "PR Review Auto-Remediation Monitor (V1.0)"
created: 2026-06-11
owns: [INV-015]
verifies: [INV-001, INV-007, INV-009, INV-015, INV-016]
---

# Round 3 -- QA Normative Resolution (verifying tests + sufficiency adjudication)

I accept the architect's INV-001 counter definition (single increment edge on `S5_AWAITING_REREVIEW --[review_observed AND sha_attributed_to_our_push]--> S2_CLASSIFY`) and INV-016 5-predicate conjunction. I accept the backend's INV-007 write-ahead push sequence and INV-009 fix-dedup/reply-key separation. Below are the canonical tests that move each HIGH invariant from UNADDRESSED to a stated disposition, followed by my honest INV-015 adjudication.

---

## INV-001 -- Counter monotonicity + fence-post

### T-626-OFF-BY-ONE (canonical fence-post)

**Fixture:** `MockRemediationHarness(arm_findings=3, max_rounds=2)`. Simulate the FSM from arm through two full cycles:
1. Arm with 3 Medium+ findings, `round_counter=0`, `pushed_commit_shas={}`.
2. Trigger fix+push cycle #1: `pre_push_sha="sha1"`; `push_initiated{target_sha="sha1"}`; `push_completed`; write `pushed_commit_shas={"sha1"}`.
3. Simulate attributed re-review: `review_observed=True`, `review_sha="sha1"`. This fires the `S5-->S2` increment edge.
4. Trigger fix+push cycle #2: `pre_push_sha="sha2"`; push sequence; `pushed_commit_shas={"sha1","sha2"}`.
5. Simulate attributed re-review: `review_sha="sha2"` fires the increment edge.

**Assertion:** After step 3, `round_counter==1`, gate `1>=2` is False, FSM proceeds to cycle #2. After step 5, `round_counter==2`, gate `2>=2` is True, FSM routes to `HALT_MAX_ROUNDS`. Total pushes: exactly 2. No increment occurs at arm, at push emission, or at validation.

**Expected:** `assert round_counter == 2; assert push_count == 2; assert state == HALT_MAX_ROUNDS`

### T-VANISHED-MONO (vanished-review monotonicity)

**Fixture:** Same as T-626 through step 5 (counter reaches 2, HALT). Then:
6. Poll the review endpoint: the re-review with `sha="sha2"` has been dismissed (returns 404 / empty). This simulates Augment force-push-dismissing the review after we already incremented.

**Assertion:** `round_counter` remains exactly 2 (irrevocable, never decrements). FSM stays in `HALT_MAX_ROUNDS`. No re-entry to `S3_DIAGNOSE`.

**Expected:** `assert round_counter == 2; assert state == HALT_MAX_ROUNDS; assert troubleshoot_mock.call_count == 2`

**STATUS: ADDRESSED** -- Both tests are derivable from the architect's single-normative sentence. T-626 proves the gate predicate under `>=`; T-VANISHED-MONO proves the irrevocability clause (INV-001 normative para 1, final sentence). Fence-post is provable; monotonicity is a one-way counter by design.

---

## INV-007 -- Crash between git push and push_completed

### T-CRASH-WINDOW-NO-DOUBLE-PUSH

**Fixture:** `MockCrashResumeHarness(arm_findings=2, max_rounds=2)`. Simulate:
1. Normal fix cycle #1 completes: counter=1.
2. Fix cycle #2: `push_decision` written, `push_initiated{target_sha="sha2"}` written and fsynced.
3. **Kill session** (raise `SystemExit`) between `git push` returning success and `push_completed` being appended.
4. `--resume`: load JSONL, find idempotency key with `push_initiated` but no `push_completed`.
5. Mock remote query: `target_sha="sha2"` IS reachable from remote branch tip.

**Assertion:** Resume appends `push_completed{recovered:true}` using the original `push_initiated` fields. FSM enters `S5_AWAITING_REREVIEW` (NOT back to `S3_DIAGNOSE`). No second `git push` is issued. The mocked push executor records exactly one push for cycle #2.

**Expected:** `assert push_executor.push_count == 2; assert resume_state == S5_AWAITING_REREVIEW; assert push_completed.recovered == True`

**STATUS: ADDRESSED** -- The backend's 3-case resume rule (remote has SHA / remote lacks SHA / ambiguous) + pre-push `push_initiated` write-ahead with the pre-push-based idempotency key closes the probe's hole. The test proves no double-push occurs when the crash lands in the push-->log window.

---

## INV-009 -- Fresh comment_id on re-review

### T-FRESH-COMMENT-NO-DOUBLE-FIX

**Fixture:** `MockDedupHarness(arm_findings=2, max_rounds=2)`. Simulate:
1. Fix cycle #1 runs on finding `F1` at `src/app.py:42` with body `"null pointer in handler"`. `fix_key = sha256("src/app.py\n42\nnull pointer in handler")`. Fix applied, `applied_edits=1`.
2. Re-review arrives: same finding `F1` at same `src/app.py:42` with the SAME body, but under a NEW `comment_id="aug-999"` (fresh Augment comment).
3. The monitor processes the re-review: fix-dedup lookup by `fix_key` finds the prior applied record.

**Assertion:** No second fix is computed or applied for `F1` (`fix_suppressed=True`). A reply IS posted on the fresh thread `aug-999` because `reply_key` is thread-scoped and this thread has no prior reply. The reply text cites `applied_edits=1` (e.g., "Edit was applied and validated in the previous cycle") and does NOT say "resolved" unless the status permits. Old thread `aug-001` remains resolved only by its own resolve key.

**Expected:** `assert troubleshoot_mock.call_count == 1; assert reply_posted_on_new_thread == True; assert reply_text_contains("applied") == True; assert reply_text_contains("resolved") == False`

**STATUS: ADDRESSED** -- The fix-dedup key (`body + file:line`, comment_id-independent) and the reply-key (thread-scoped with fix_key + status citation) together close the probe's "reply-without-fix" hole. The test proves suppression of redundant fix computation and truthful reply wording.

---

## INV-016 -- G-push 5-predicate conjunction, zero-edit block

### T-ZERO-EDIT-NO-PUSH

**Fixture:** `MockGPushHarness(arm_findings=2, max_rounds=2, monitor_ordinal=3)`. Simulate:
1. Fix cycle: troubleshoot runs but produces zero grounded edits (`applied_edits=0`, all findings ungroundable/dropped).
2. Validation: targeted tests pass trivially (nothing changed, so tests remain green).
3. Evaluate the 5-predicate G-push conjunction: predicate (1) `ordinal>=3` True, (2) `validation=="validated"` True, (3) `needs_human_decision==False` True, (4) `round_counter < max_rounds` True, **(5) `applied_edits > 0` False**.

**Assertion:** The conjunction evaluates to False. FSM routes to `TERMINAL_CLEAN` (report-only). NO `git push` is executed. NO "resolved" announcement is posted. A `push_decision{authorized:false, predicate_5_false:true, applied_edits:0}` audit record is written.

**Expected:** `assert push_executor.push_count == 0; assert "resolved" not in announcements; assert push_decision.authorized == False; assert push_decision.predicate_5_applied_edits == 0`

**STATUS: ADDRESSED** -- Predicate (5) (`applied_edits > 0`) is the new guard that closes the "push/announce-resolved with nothing changed" hole. The test proves the conjunction blocks on this single predicate even when all others pass. The mandatory `push_decision` audit record provides post-hoc verifiability.

---

## INV-015 -- Sufficiency challenge (QA adjudication)

### The honest question

The probe proved that max_rounds + validation + HALT is **necessary-only**, not sufficient, for bounding R4 blast radius. A validated fix that greens targeted tests but breaks an untested behavior gets pushed and announced resolved within budget. This is not a bug the test can eliminate -- it is an inherent property of proxy validation.

### T-VALIDATED-NOT-VERIFIED (audit fixture)

**Fixture:** `MockBehavioralDriftHarness(arm_findings=1, max_rounds=2)`. Simulate:
1. Fix cycle: troubleshoot fixes `F1` at `src/auth.py:55`. `applied_edits=1`.
2. Targeted tests (`tests/test_auth.py::test_login_flow`) pass. Lint and format pass.
3. The fix silently changes behavior: `token_expiry_seconds` from 3600 to 0 (a bug in an untested code path).
4. A non-targeted behavioral test exists: `tests/test_auth.py::test_token_expiry_default` -- it FAILS because expiry is now 0.
5. The monitor runs only the targeted test set (as designed); the behavioral test is NOT in the targeted set.
6. Push proceeds (all 5 G-push predicates True). Announcement says "resolved."
7. The run-log records: `push{validation_status:"validated_not_verified", behavioral_test_failures:["test_token_expiry_default"], applied_edits:1}`.

**Assertion:** The push DID occur (inherent, not preventable by the monitor). The run-log records `validated_not_verified` with the list of behavioral test failures detected post-hoc. `round_counter` increments normally. The system HALTs at `max_rounds` if the cycle repeats.

**Expected:** `assert push_executor.push_count == 1; assert run_log_entry.validation_status == "validated_not_verified"; assert len(run_log_entry.behavioral_test_failures) == 1`

### Adjudication verdict

**INV-015 is ADDRESSED-via-accepted-risk**, and this is the honest disposition. The test above does NOT prevent the bad push -- it cannot, because the monitor's validation scope is necessarily bounded by the targeted test set. What the test proves is:

1. **Detection:** The `validated_not_verified` audit record captures exactly this pattern -- a fix that passed targeted validation but drifted an untested behavior.
2. **Auditability:** The run-log records which behavioral tests failed, enabling post-hoc review.
3. **Bounded blast radius:** `max_rounds` still caps the number of such pushes (<=2 by default), and INV-016's 5-predicate conjunction ensures each push at least made a real edit and passed all gates the monitor can check.

The merged spec MUST surface this as a **known limitation**:

> "Validation authorizes a push within this gated envelope; it is NOT a correctness guarantee. A fix that passes targeted tests may break untested behaviors. Such pushes are recorded as `validated_not_verified` in the run-log. Operators should maintain a comprehensive behavioral test suite to minimize this residual risk."

This is irreducible residual risk. No test can make it fully ADDRESSED because the gap is between "what we test" and "what exists." The honest posture is audited acceptance with bounded count, not false sufficiency.

**STATUS: ADDRESSED-via-accepted-risk** -- The merged spec must carry the known-limitation clause above.

---

## Final disposition summary

| Invariant | Test(s) | STATUS |
|-----------|---------|--------|
| INV-001 (counter definition + monotonicity) | T-626-OFF-BY-ONE, T-VANISHED-MONO | **ADDRESSED** |
| INV-007 (push idempotency / crash window) | T-CRASH-WINDOW-NO-DOUBLE-PUSH | **ADDRESSED** |
| INV-009 (dedup vs fresh comment_id) | T-FRESH-COMMENT-NO-DOUBLE-FIX | **ADDRESSED** |
| INV-016 (G-push 5-predicate + zero-edit block) | T-ZERO-EDIT-NO-PUSH | **ADDRESSED** |
| INV-015 (sufficiency / validated-not-verified) | T-VALIDATED-NOT-VERIFIED | **ADDRESSED-via-accepted-risk** |

**All 5 HIGH invariants are cleared.** Four are ADDRESSED (tests prove the invariant holds under the normative resolution). INV-015 is ADDRESSED-via-accepted-risk -- the audit fixture detects and records the pattern, but the residual risk is irreducible and must be surfaced as a known limitation in the merged spec. Convergence is achieved.
