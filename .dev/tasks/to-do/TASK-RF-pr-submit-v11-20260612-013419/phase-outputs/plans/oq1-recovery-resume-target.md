# OQ-1 — recovery.py Branch-A resume target (PENDING human decision)

**DECISION: PENDING — requires human sign-off.** `recovery.py` source is LEFT UNCHANGED.

## Current Branch-A behavior (recovery.py:102-111)
When a crash is detected in the push window and the remote is reachable (`remote_reachable
is True`), `resolve_crash_window` synthesizes the missing `push_completed` event and returns
`(BRANCH_A_LANDED, MonitorState.S5_AWAITING_REREVIEW)` — i.e. it resumes directly into
"awaiting re-review".

## The V1.1 tension
Pre-V1.1, resuming a landed push to `S5_AWAITING_REREVIEW` was correct: a push was assumed
to trigger the re-review. Post-V1.1 (FR-8), a push does NOT auto-trigger a re-review — the
skill must first post an `auggie review` re-trigger comment (the new `S5A_RETRIGGER_REVIEW`
state) BEFORE awaiting the re-review. So a crash recovered as "landed" BETWEEN the push and
the re-trigger-comment post may semantically need to resume at `S5A_RETRIGGER_REVIEW` (the
re-trigger comment was not yet posted) rather than `S5_AWAITING_REREVIEW`.

## Candidate V1.1 behavior
Return `(BRANCH_A_LANDED, MonitorState.S5A_RETRIGGER_REVIEW)` when the recovered push has no
attributable re-trigger comment yet, so the resume re-enters the re-trigger step.

## Trade-off (why this is a human decision, not an auto-default)
- Resuming to `S5A_RETRIGGER_REVIEW` when a re-trigger comment WAS already posted (but the
  crash hid it) → **double-posts** the `auggie review` comment (mostly benign; INV-R1 bounds
  it to `<= max_rounds`, and the App is idempotent on duplicate triggers, but still noisy).
- Resuming to `S5_AWAITING_REREVIEW` when the re-trigger comment was NOT yet posted → the
  monitor waits forever for a re-review that will never come (the push didn't trigger it),
  burning the timeout budget → `TERMINAL_TIMEOUT` instead of advancing.
- The correct disambiguator is whether a re-trigger comment exists in the run-log/PR at
  recovery time — which needs a `rereview_requested` / re-trigger-comment watermark check
  that the addendum does NOT specify. The addendum is SILENT on `recovery.py`.

## Analysis note (still leaving the decision to the human)
The run-log already folds `rereview_request_count` (Phase 4, INV-R1). A future resolution
COULD make Branch-A inspect whether a `REREVIEW_REQUESTED` event exists for the current cycle
and choose `S5_AWAITING_REREVIEW` (re-trigger already posted) vs `S5A_RETRIGGER_REVIEW`
(not yet) accordingly. This is a viable design, but it is a NEW recovery contract the
addendum did not authorize, so it MUST be ratified by a human before shipping.

## Disposition
- `recovery.py` is NOT modified by this task. The V1.0 Branch-A behavior
  (`→ S5_AWAITING_REREVIEW`) ships unchanged.
- This OQ is logged under `### Follow-Up Items Identified` in the task file as a blocking
  human decision (Priority: High), and surfaced in the Task Summary.
