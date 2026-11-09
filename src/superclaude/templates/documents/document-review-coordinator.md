# Document-review coordinator record

Copy for an authorized document-review loop. This is a prose record, not a parser, runner or permission to invoke a workflow. Follow the spec-panel Review Loop contract; other protocols retain their own policies. Never use this template to reset an existing loop.

## Identity and authority

- Loop id and owner:
- Authorized review scope and dependent step:
- Edit authorization (none unless explicitly given):
- Candidate frozen identity (path plus revision/hash), baseline identity, prior report identities:
- Actual reviewer model and source (or unknown):
- Checked scope and dependencies; exclusions:
- Applicable required assurance predicates and evidence:

## Durable budget (fill before dispatch, including resume)

- Reviews consumed: __ / 3; fixes consumed: __ / 2.
- Last completed phase; current phase and outcome; candidate frozen after F2:
- Predeclared failed-delivery recovery allowance: __ (default zero); used: __.
- Check known exhaustion before initial-review defaults. Maximum R1→F1→R2→F2→R3, with early stop. Missing headers or files do not reset spent budget. Named missing, empty, unreadable or ambiguous inputs mean INCOMPLETE and stop the dependent step.
- A completed INCOMPLETE review or empty-diff review consumes a review slot. Failed delivery recovery is not a new substantive review. Clarification grants no restart or edits. At exhaustion return results and unresolved decisions once; attended: ask one scoped decision; unattended: record and stop the dependent step. No automatic fourth review or hidden F3.
- If phase outcome or mutation ownership is uncertain, preserve the last known identity and budget, record uncertainty and stop the dependent step until reconciled. Do not overwrite, rerun a fix or assume zero consumed slots.

## Finding ledger (retain prior rows)

| Id / source report | Original label / consequence-based grade | Evidence and wrong outcome | Origin / dependency | State: resolved/open/regressed | Disposition: active/deferred/disputed/withdrawn | Resolution evidence |
|---|---|---|---|---|---|---|
| | | | | | | |

Record duplicate/unknown identities explicitly. Never drop prior resolved rows, deferred or disputed findings. Missing required rows mean INCOMPLETE, not zero. Separate new labels, unresolved prior, carries, deferred/withdrawn and audit unions; a union is not a count of unique new findings.

## Gate and repair handoff

- Confirmed High/Critical blocker ids and substantiated high-consequence outcomes:
- Genuine Medium/Low/Nit warnings (never mandatory repairs or restarts):
- Unknown required predicates / credible severe concerns, missing evidence and relevance:
- Verdict: PASS / FAIL / INCOMPLETE. PASS requires adequate checked-scope evidence, every applicable required assurance predicate established and no confirmed High/Critical blockers. Adequately evidenced zero is valid; scope-limited PASS is not whole-document clearance. Binary output: FAIL with reason evidence-incomplete, not invented defects or automatic repair.
- Reviser brief only with consent, adequate evidence and a remaining fix slot: named blockers or separately authorized edits, affected text and necessary dependencies. Permit safe deletion/narrowing without removing required safety behavior. No unrelated mechanisms. No arbitrary growth cap.
- Per-finding gross added/deleted and net bytes, candidate byte size before/after, shared/uncertain attribution counted once:
- Post-F2 necessity audit: report-only. Later repairs need separate bounded approval.

## Optional follow-ups and stop

- Nonblocking follow-up candidates and unresolved decisions:
- Attended top-level session's single batched optional issue question: asked / not asked; response:
- Unattended: record without waiting, filing or acting. ISSUE-BACKLOG.md is a copied template after approval, not a writable queue.
- Final available results, scope limit, dependent step stopped (if any), and next explicitly authorized decision:
