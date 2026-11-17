# Diff Analysis: Position paper comparison (slot C-02, ledger clearing and verdict authority)

## Metadata
- Generated: 2026-11-14
- Variants compared: 2 (Variant A = proposal-a.md, "Position A: guarded one-pass silence-clear, reviewer types blocking"; Variant B = proposal-b.md, "Position B: explicit per-row verification, script-predicate blocking")
- Total differences found: 22 diff points (debate denominator)
- Categories: structural (2), content (11), contradictions (4), unique (10), shared assumptions (5)
- Focus areas: correctness, risk, test-coverage
- Both variants are position papers on one conflict; "requirements" are the C-02 row (LG-1 clearing, VM-2 blocking authority, VM-4 defer policy, C-S9 semantics) plus the decided context rows (VM-1, VM-3, VM-5, VM-6, LG-3, LG-4).

## Agreement points (inputs to the shared-assumption scan)
- Silence-clears (`ledger.py:254-258`) is a reproduced defect; the docstring at `ledger.py:112` says the opposite of the code.
- The verdict is derived from rows on every read and never stored (decided VM-3); `defer` stops rewriting round records.
- A deferred blocking row counts as open; when only deferred rows remain the outcome is ESCALATE (both).
- `defer` is refused on rows that are not blocking-and-open-ish; a round after ESCALATE is refused (VM-6).
- `cli/reflect` does not import the review ledger; INV-A and INV-B are untouched; exit codes 0/10/11 are unchanged.
- The standard re-review is one reviewer (`panel.py:596-605`, `apply_to: ["first"]`).
- The quorum value is slot C-03 and is not decided here.
- Prior-line compliance and the quality of the strongest alternative are unmeasured; every E2 ledger is round 1 only.

## Structural Differences

| # | Area | Variant A | Variant B | Severity |
|---|------|-----------|-----------|----------|
| S-001 | Layout of the core-change description | Section 2 as a table (Part / Change / Where it lands), invariants as two severity tables | Section 2.1 as prose bullets B1-B7, invariants as Preserves / Endangers lists | Low |
| S-002 | Evidence-tag discipline | Tags taken-from-research claims as `[CODE-VERIFIED via research/NN]` | Tags the same class of claims `[UNVERIFIED here]`, including claims B relies on (the grading-check categories at `document_review_loop_prompts.md:31`) | Low |

## Content Differences

| # | Topic | Variant A Approach | Variant B Approach | Severity |
|---|-------|--------------------|--------------------|----------|
| C-001 | Clearing rule (LG-1) | A `resolved_check` row clears only if at least Q reviewers with `block_ok` true are complete AND at least Q of them typed `prior <lid> resolved`; any complete `open`/`regressed` prior withholds clearing; else the row stays `resolved_check` with a `held` event and is listed in `unverified_ids` | A row clears only on a `prior resolved` line from a reviewer with `block_ok` true whose `evidence` quote occurs in `doc_text` and with no re-find of the row in the round; no answer keeps `resolved_check` and counts as open | High |
| C-002 | Verifiability of the examination record | Self-report: `prior ... resolved` line attributed to a named complete reviewer and report hash; no quote | Optional `evidence` key on the prior line, checked mechanically with the anchor occurrence test against `doc_text` (B3) | High |
| C-003 | Binding the merged text to the revision output | Explicitly out of scope (new-text hash, research/03 I-6, "a separate defect") | Required (B4): `revise` stores `new_sha256`, `merge` refuses a round whose `doc_text` hash differs | Medium |
| C-004 | Blocking authority (VM-2) | Reviewer-typed boolean `blocking` stays the only authority; `verdict:` line stays parser-neutral; no predicate, no grader in the core | Lens-owned pure predicate `blocking(finding)`; typed value kept as `blocking_typed`, disagreements reported as warnings; blind grader an optional per-lens stage | High |
| C-005 | Effect of `prior open|regressed` and of a same-round re-find | Prior lines are an examination record and a veto; never a status writer (pinned test `test_prior_lines_never_change_a_status` stays true); a dissent holds the row at `resolved_check` and puts it in `brief_ids` | `prior open` sets the row to `open`, `prior regressed` to `regressed`; a re-find wins over a `resolved` answer | Medium |
| C-006 | `defer` policy (VM-4) | `defer(ledger, lid, reason, owner, expires_round)`; expiry is a round number; reaching the expiry round returns the row to `open`; counts as open meanwhile | `--owner` and `--reason` required; expiry optional and "has no machine meaning"; the row is terminal for the machine and counted open | Medium |
| C-007 | Re-find of a `deferred` row | Row returns to `open` with event `reopened_by_refind`; appears in `brief_ids` | Row stays `deferred`; the re-find is recorded and surfaced as `refound_deferred` in the merge output | Medium |
| C-008 | Output lists and Reviser brief | New `unverified_ids` and `held_ids`; rows withheld for `reviewer-dissent` go into `brief_ids` | New `verify_ids` (unanswered, not in the Reviser brief) and `held_ids`; `brief_ids` is open/regressed only | Low |
| C-009 | Ledger file shape and `review-ledger/1` | Round records stop carrying `verdict`, `decision`, `brief_ids`; readers made tolerant of old files; schema string kept; `/2` bump unsettled | Fields only added (`verify_ids`, `held_ids`, `new_sha256`, `blocking_typed`, owner); schema string kept; the meaning of `verdict` changes; `/2` bump unsettled | Medium |
| C-010 | Measurement and falsification | Multi-round seeded replay with three arms (current, A, quote-verified per-row = B semantics); wrongness rule registered before the run | M1 seeded multi-round replay (current vs B, with a fake-fix condition), M2 free pre-count of prior-line compliance in existing re-review reports, M3 predicate-agreement flip count | Low |
| C-011 | Prompt-text edits | One clause at `document_review_loop_prompts.md` line 70 naming the examination record (+ plugin mirror) | Line 61 gains the `evidence` key, line 70 rewritten to "clears on a quoted `resolved` answer" (+ plugin mirror) | Low |

## Contradictions

| # | Point of Conflict | Variant A Position | Variant B Position | Impact |
|---|-------------------|--------------------|--------------------|--------|
| X-001 | Does letting `prior` lines decide status break the pinned rule `test_prior_lines_never_change_a_status` (`tests/review/test_review_ledger.py:318-338`)? | Stays true: prior is a record and a veto, never a status writer | B1 makes `prior resolved` clear a row and `prior open|regressed` set status; B's E7 pin list does not name this test | Medium |
| X-002 | Is a quote that occurs in the new text evidence that the defect was examined or fixed? | Not needed; concedes its own record is a self-report but says the removed failure set is larger than the residue | Says the quote is "attributed, mechanically checkable"; concedes it is not proof of a correct fix and names M1 as the measurement that could show it adds no power | High |
| X-003 | Is A's quorum guard workable in the default flow? | Guard needs `>= Q` complete reviewers with a typed prior; says the examination record, not the count, does the work in the default one-reviewer re-review, Q taken from C-03 | Notes the default re-review is one reviewer who may not have been a finder; does not need a count | Medium |
| X-004 | Is a spec-lens blocking predicate implementable on `findings-v1` and consistent with the grading check? | `findings-v1` has no `rule` or `wrong_outcome`; predicate needs new typed fields or an unknown-key convention | B6 reads `severity` and `category` only (MAJOR blocking for contradiction, unpassable-check, data-loss, safety), marks the category list UNVERIFIED, and concedes it can flip a reviewer's typed non-blocking MAJOR to blocking against `spec-panel.md:259` ("blocking only if it names a concrete wrong outcome") | High |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|-----------------|
| U-001 | A | Examination record as a veto (dissent withholds clearing) plus additive `held` event with reason codes and `unverified_ids` / `held_ids` in merge output | Medium |
| U-002 | A | Expiry as a round number so `verdict` stays a pure function of the file, and expiry reopens the row | Medium |
| U-003 | A | Refusal of `defer` on rows that are not blocking-open; reproduces D-11 A/B/C as test cases | Medium |
| U-004 | A | Replay design that includes the opposing semantics (quote-verified arm) as a measured arm; states what would show A has the wrong strength | Medium |
| U-005 | B | New-text hash binding at `revise` / `merge` (closes research/03 I-6 and makes any `doc_text` check meaningful) | High |
| U-006 | B | Lens-owned blocking predicate with `blocking_typed` kept and disagreement reported; optional blind grader that the core does not depend on | High |
| U-007 | B | Fail-closed gate requirement: the answer check must gate clearing, not warn (E15, stoprule's `EXIT_OK` in every branch) | Medium |
| U-008 | B | M2 free pre-measurement: count prior-line compliance in existing re-review reports before writing code | Medium |
| U-009 | B | Detailed rf-qa mapping (R7 regression/monotonicity, R2 VERIFIED/UNCHECKED) and PR-review dependency on C-01 locator | Medium |
| U-010 | B | Honest asymmetry argument: bounded visible failure (cap escalation) vs invisible wrong PASS | Medium |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|------------|------------------|--------|--------|
| A-001 | The re-review reviewer is shown the prior blocking rows under the same ledger ids the ledger keys on, and those ids are stable across rounds, so a typed `prior <lid>` line maps to the right row | Both rely on `prior` lines as the answer record | A mis-keyed or id-less prior line holds or clears the wrong row | UNSTATED (promoted) |
| A-002 | The text the re-review reviewer actually examined is the `doc_text` the ledger merges against | Both attribute clearing to a reviewer's examination; only B (B4) binds the text | If the texts differ, a `resolved` answer (quoted or not) certifies text the ledger never saw | UNSTATED (promoted) |
| A-003 | ESCALATE (exit 11), including "only deferred or held rows remain", is a safe terminal outcome that a caller or human acts on; no caller loops on it | Both route held-only and deferred-only states to ESCALATE | An unhandled ESCALATE turns fail-closed into a stuck loop | UNSTATED (promoted) |
| A-004 | The shared core's consumers stay as today: reflect will not adopt the review ledger, so "no effect on reflect" holds | Both state "reflect: no effect" from current imports | The research task designs a unified Review Panel; if reflect Tier 2 becomes a consumer, INV-A/INV-B/DEGRADED interactions open | UNSTATED (promoted) |
| A-005 | Clearing strength and the quorum / partial-panel rule (C-03, D-2) can be decided independently | A takes Q as a parameter; B defers quorum | The guard's effective strength (Q = 1 vs more) and round-1 PASS from one valid block are set elsewhere | UNSTATED (promoted) |
| (not promoted) | Reviewers are honest-but-lazy rather than adversarial | Both discuss the rubber-stamp risk explicitly | n/a | STATED |

## Summary
- Total structural differences: 2
- Total content differences: 11
- Total contradictions: 4
- Total unique contributions: 10
- Total shared assumptions surfaced: 6 (UNSTATED: 5, STATED: 1, CONTRADICTED: 0)
- Highest-severity items: C-001, C-002, C-004, X-002, X-004, U-005, U-006
- Debate denominator: S(2) + C(11) + X(4) + A(5) = 22 diff points
- Similarity check: differences are well above 10% of comparable items; debate proceeds.
