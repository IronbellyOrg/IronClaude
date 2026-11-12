---
needs_human_decision: true
status: RESOLVED
---

# Cursor template decision (OQ-17)

## Question

The step 1.0a capture (item 7.16) read the `worker-list` page object and found a cursor field. In plain words: when a Run has more workers than one page holds (100), `orca-ide orchestration worker-list` can hand back a cursor to fetch the next page. Today the sweep's list of allowed Orca commands has exactly 10 templates and none of them passes a cursor. Do you want one more template added so the sweep can read the next page, or do you want the allowlist to stay at 10?

Quoted from the design and the capture:

> DESIGN line 559 (`docs/designs/orchestrator-mode.md`): "The `worker-list` cursor template is not in the set; it is added only after step 1.0a captures the cursor field, as one extra template (SPEC line 320)."

> DESIGN line 995, open item 5: "`worker-list` page size and cursor field", closed by "Step 1.0a item 3"; behaviour until closed: "A full page of `WORKER_LIST_PAGE` rows sets truncated and the total is a lower bound; no cursor template".

> Capture, `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/readonly-probe.md` section 3 (line 461): page object `{"limit": 100, "total": 5, "hasMore": false, "nextCursor": null}`. The cursor field is `result.page.nextCursor` (with `result.page.hasMore`). It was null because the named Run has 5 workers. The flag that passes a cursor to the next call was not observed: the allowlist forbids any other command, and no Run in the capture had a second page.

## Options

Options as the item text states them:

- "An approval resumes into the step 2 follow-up": you approve one extra allowlist template for reading the next `worker-list` page. Then, before the code step: a DESIGN edit item for sections 7.3, 11, 12 and 15.1 with its own review gate; the 8.10 and 10.3 template count changes from the literal 10 to the approved count recorded in the 1.0a facts file; the item 7.16 forbidden list and its grep are updated to allow the approved command line, and that command line is captured again; and the R5 review gate (items 6.5 to 6.22) runs again over the new edit. The approved command line (its cursor flag name) has to be named by you or found in a further capture, because the first capture did not observe it.
- "A refusal resumes with the allowlist unchanged": the allowlist stays at exactly 10 templates. Item 7.17 records "cursor field present, no cursor template; the DESIGN 973 full-page lower bound applies". Then item 8.10 does not page by the captured cursor field and treats a full page of 100 worker rows as truncated, with the total shown as a lower bound.

## Recommendation

Refuse for Phase 1 and keep the allowlist at 10. Reason: the capture never saw the flag that passes a cursor, so a template written now would be a guess; the design already says what the report does without it (a full page sets truncated and the total is a lower bound); and approval adds a design edit plus a full re-run of the review gate. A Run with more than 100 workers would then show "at least 100", which is honest but not complete. This recommendation does NOT authorize adoption.

## Blocked work

Blocks: item 7.17 (it halts while this record is PENDING or `Chosen:` is empty), and with it step 1.2 and every later item (Phase 8 onward, including the 8.10 and 10.3 template count).

## Operator decision

OPERATOR DECISION: Keep the 10 commands; add no cursor command.
Chosen: Refuse the extra cursor command. The allowlist stays at exactly 10 templates. A full page of 100 worker rows is shown as truncated with a lower-bound total (DESIGN line 995, open item 5, behaviour until closed).
Decided by: Ryan Wiancko, owner, 2026-11-11.
Decision source: In this session's OQ-17 question the owner first asked for the pros and cons of each option (not a decision), then selected "Keep the 10 commands (Recommended)". The selected option's text reads: "PROS: no design change, no new review round, nothing to guess; the design already defines the behaviour (a full page of 100 is shown as truncated and the total as 'at least N', and unmatched sessions stay 'could not determine', so it errs on the safe side). Can still be added in a later phase with no rework. CONS: a Run with more than 100 workers is only partly seen. One of your listed Runs (run_58af03dbfa92) has 100 or more, so this can really happen." This resolves OQ-17 only; no other decision is inferred.
