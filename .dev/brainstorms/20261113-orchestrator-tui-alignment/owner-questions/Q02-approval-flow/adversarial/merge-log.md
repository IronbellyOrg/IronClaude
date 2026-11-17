# Merge log: Q2 approval flow

## Metadata

- Date: 2026-11-14
- Executor: merge-executor (adversarial pipeline step 5)
- Base: `adversarial/variant-2-original.md` (proposal B)
- Plan: `adversarial/refactor-plan.md` (12 planned changes, 5 rejected, auto-approved)
- Sources read: `adversarial/variant-3-original.md` (C), `adversarial/variant-1-original.md` (A), `adversarial/round1-advocate-V2.md`, `adversarial/round1-advocate-V3.md`, `00-state-machine-and-failure-modes.md`
- Output: `merged-proposal.md` (in the Q02-approval-flow folder)
- Code facts used (verified by the orchestrator, not re-read by the executor): `predicates.py` lines 253 to 255 (`unchanged_since` skips own-login comments); `approval_of` orders against a trigger label event and the store creation time; `record.py` exclusive non-blocking `fcntl.flock` (line 403) and `_fsync_dir` (lines 310 to 313); `WORKER-CONTRACT.md` line 136 input veto; `launch-prompt.md` "A human approves by replying `approved` in this session or by running the printed implement command."; no code reads who moved a Project Status.
- Rejected changes (C-001, X-001, C-004, C-006 and X-002, C-005 as a watcher actuator): none included. C-005 appears only as an owner decision, per change 12.

## Changes Applied

| # | Title | Status | Provenance tag | Where applied | Before / after |
|---|---|---|---|---|---|
| 1 | Read-only stage-status verb | applied | V3 Design item 4, U-008 | Design item 4 ("Checks run as code"); build table new row; GitHub flow step 3 | Before: base named no mechanism for the checks. After: the coordinator runs a read-only verb so checks run as code |
| 2 | New stage predicates, not plain reuse | applied | V2 concession 4, V3 concession 3 | Design item 4; GitHub flow step 3; build table verb row; Who may approve | Before: "reusing the watcher's `approval_of` and `unchanged_since` rules". After: reuse of GitHub reads and actor checks plus new predicates, with the two reasons (own-login skip, trigger-label ordering) |
| 3 | Label removal is the revocation signal | applied | V3 F5 row, C-008 | F5 row; Design item 4 ("Revocation") | Before: F5 triggered by "moved backwards". After: label removal revokes; a Status move back is shown and reported, never acted on alone |
| 4 | Label event id as evidence; key unchanged; "approved, starting" marker; marker-without-row rule | applied | V3 U-004, V3 concessions 4 and 5 | Design item 2 ("Key and evidence", "Lost ledger"); Design item 4 ("Public marker"); F1, F2 rows | Before: marker comment only after an Orca approval, after the instruction. After: marker after the row and before the instruction for both channels, non-blocking, retried at each wake; start-up treats a marker without a row as an existing row |
| 5 | Helper built on `record.py` lock and fsync | applied | V1 Design item 1, V1 strength 1 | Design item 2 ("Built on the watcher's store code"); build table helper row | Before: "a small CLI helper that takes a per-issue lock". After: same helper, reusing `record.py` file lock (line 403) and `_fsync_dir` (lines 310 to 313); no new locking code |
| 6 | Correct the coordinator-down claim | applied | V2 concession 2 | F2 row; new "While the coordinator is down" paragraph in How an approval flows | Before: "Orca approvals wait in the Run mailbox (replayed until acknowledged)". After: an approval typed in the coordinator session cannot be made while it is down; only GitHub approvals and a future TUI message wait; Run mailbox delivery UNVERIFIED |
| 7 | Delivery: resolve the person-prompt veto | applied | V2 concession 3, A-002 | Design item 3 ("Delivery to the agent"); build table delivery row | Before: "type one line into its waiting prompt (WC A3 rules)". After: names the "never answer a person prompt" veto (line 136) and two routes: a written narrow exception for one line per row (first release), SW-13 supervised worker (durable) |
| 8 | Plan version over named files | applied | A-003 responses (V2, V3) | Design item 3 ("Plan version"); plan reply text in item 4 and GitHub flow step 1; build table helper row | Before: plan sha256 of an unnamed plan file. After: helper computes SHA-256 over a named file list in a fixed order; list and hash printed in the plan reply |
| 9 | Dead or missing agent session | applied | A-006 responses (V2) | Design item 3; note under the failure table | New: row stays `recorded`, shown as "recorded, not delivered", reported to the person, never relaunched automatically |
| 10 | Duplicate approval reply on the issue | applied | owner's race scenario, C-007 | F1 row | New: short reply on the issue (for example "already approved in Orca at <time>, row <id>") and no action |
| 11 | GitHub channel trust rule | applied | V2 neutral recommendation, F8 | F8 row; Who may approve; GitHub flow step 3 | Before: mitigation offered as an option. After: approvals accepted only from approver account ids that are not the host's `gh` login, else the GitHub channel stays off until FU-6 or written owner acceptance of the forgery risk |
| 12 | Preconditions and owner trade-off | applied | A-001, A-005, C-005 responses | What stays unresolved (appended list) | New: coordinator scope and grants as preconditions; liveness trade-off left to the owner |

Consistency edits made while applying the plan (no new decisions; each follows from a planned change):

- Change 4: the base's approval comment and its marker were reused as the "approved, starting" marker and moved before the instruction; `stage=<S>` was added to the marker so it carries the full key. The Orca flow step 2 order was changed to row, marker, deliver, then mirror label and Status. Orca flow step 3 now reads "its own marker and mirror". F3 now says a GitHub approval with no row "and no marker for its key" is new. The grant list at the end of the build section gains "marker".
- Change 1: the first build row now reads "None to the claim trigger; the watcher's claim behaviour stays as built", and Cost and risk says the only new watcher-package code is the read-only verb, so neither contradicts the new verb row.
- Change 11: F3 points to the F8 account rule.
- Invariant rewritten as instructed: names the key (issue, stage, plan version), the write-ahead row, the coordinator as sole creator, and the agent acting only on a line naming the row and matching hash.

## Post-Merge Validation

**Structural.**
- One H1 (the required title), eight H2 sections in the base order: Design; How an approval flows; What happens in each failure mode; Who is allowed to approve and how that is verified; What the TUI and the issue show, and how they stay in step; What it adds to the build; Cost and risk; What stays unresolved. No skipped heading levels.
- Failure table has all ten rows, F1 to F10, in order; the dead-session note sits below the table and is labelled as not one of F1 to F10.
- Provenance header at the top; one `<!-- Source: ... -->` comment before each of the eight sections.
- "Nothing in this proposal is built" is the first line after the title.
- No em dashes or en dashes (grep for both characters: no match).

**References.**
- Code and doc references (`predicates.py` 253 to 255, `record.py` 403 and 310 to 313, `WORKER-CONTRACT.md` 136, launch-prompt quote) match the orchestrator-verified facts. Not re-read by the executor.
- Internal cross-references resolve: Design item 3 delivery route (cited by GitHub flow step 3), Design item 4 marker (cited by item 2), F8 account rule (cited by F3).
- Work-item ids used (WA-01 to WA-05, WA-07, SW-13, OB-09, FU-6, WC-16, A-001, A-005, C-005, U-008) all appear in the base, the shared facts or the debate files.
- UNVERIFIED kept or added on: Run mailbox delivery of a TUI message; `orca terminal send` impersonation; discovery source for a claimed issue; grant table shape in section 6.8.

**Contradictions.**
- Coordinator down: the merged text no longer claims an approval typed in the coordinator session can queue while it is down (F2 row and the flow paragraph both say it cannot be made). Checked: no remaining "replayed until acknowledged" text.
- Delivery: Design item 3 and the build table both name the "never answer a person prompt" veto and the two routes (narrow exception for the first release, SW-13 supervised worker as the durable route). No remaining bare "WC A3 rules" claim.
- Marker order: Design item 4, both flows and F1/F2 agree (row, then marker, then instruction; marker non-blocking).
- Revocation: Design item 4 and F5 agree (label removal revokes; Status move back reported only).
- Residual base ambiguity, not introduced by the merge: F5 keeps the base sentence "a later forward move needs a new row", while the helper refuses a second row for the same (issue, stage, plan version). Read together, a new row is only possible for a new plan version. The merged text does not say how a forward move for the same plan version after revocation proceeds; flagged for the orchestrator, not resolved, because the plan does not cover it.

## Summary

12 of 12 planned changes applied, 0 skipped, 0 rejected changes included. Consistency edits are listed above and add no new decision. Structural, reference and contradiction checks pass, with one pre-existing base ambiguity in F5 flagged for the orchestrator.
