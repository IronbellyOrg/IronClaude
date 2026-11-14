# Refactoring Plan: Merge into Base (Variant B)

Status of this file: drafted by the orchestrator, written incrementally; reviewed by a separate analytical agent (see Plan Review below) before it is handed to the merge-executor.

## Overview
- Base: Variant B (`variant-2-original.md`, Option B "find once, then verify-only")
- Incorporating strengths from: Variant A (`variant-1-original.md`, Option A "re-find and cluster every round, D2/D3/D16 fixed"), the debate (Round 1-2 concessions and self-fixes of both advocates) and the Round 2.5 invariant probe (20 findings, `invariant-probe.md`)
- Planned changes: 20, numbered Change 1 to Change 20 below, in four groups: Stage 0 (Changes 1-3), repairs to the base that the debate established (Changes 4-7), row identity, scope and persistence (Changes 8-14), claims, tests, delivery order and the two registers (Changes 15-20)
- Overall risk: Medium to High (the base is an XL design with a spec-panel-specific predicate; four changes alter policy that needs an owner decision)
- Design intent of the merge: keep B's skeleton for rounds 2 and 3 (find once, evidenced clearing, frozen identity, computed stop), deliver it in stages whose first stage is A's cap and quorum work (needed by every option), carry B's answer semantics only after the C15/C02 boundary, the `merge`/prompt compatibility and the sweep wiring are fixed, and keep every unresolved conflict and every unaddressed invariant visible as an explicit register in the merged text.
- Selection basis: combined score 0.9804 (B) versus 0.9724 (A), margin 0.8 points, tiebreaker level 1 (14 versus 10 points won); the selection is narrow and the plan does not present B's design as better in every respect.

### Planning rules applied (from the protocol)
1. Concrete-over-generic: where A and B state the same requirement, the more concrete version is kept (file:line, numbers, named tests, field names); governance prose never replaces a concrete anchor.
2. Threshold preservation: every numeric threshold from either variant is listed in the Threshold Preservation table with a disposition.
3. Anchor-level rule: every requirement-level anchor of Variant A is either preserved (Planned Changes), replaced by a documented equivalent, or listed in Changes NOT Being Made with its reason and the debate evidence.
4. Unresolved conflicts (S-006, C-013, A-002, A-004) and unaddressed invariants (INV-001 to INV-017, INV-019) are carried into the merged proposal as a visible register, not resolved by editing.

## Planned Changes

Format per change: Source, Target (section of the base), Integration approach (replace | append | insert | restructure), Rationale (debate evidence), Anchors preserved, Risk. "Base" = `variant-2-original.md`; "A" = `variant-1-original.md`. Debate evidence cites `debate-transcript.md` (R1/R2 = round, adv = advocate) and the scoring-matrix point ids.

### Group 1: Stage 0 (land first; needed by every option)

#### Change 1: Cap by refusal in `merge_round`, `--cap` conflict error, `--round` help fix (from Variant A) [AMENDED: PR-005, PR-017, PR-021]
- **Source**: A, "Core changes" 1 and 2 (`ledger.py:114-118`, `:93-96`; `merge_cmd.py:36-42,64-70,101-104`)
- **Target**: Base, "Core (shared module code)" new item 0 ("Stage 0: round bounds") and "CLI surface" row `review merge`; "Order of work" step 1
- **Integration**: insert
- **Rationale**: C-004 won by A at 75% (both advocates agree; B-adv conceded its `E-CAP` is a subset in effect). Probe INV-015 refines it: an explicit `--cap` equal to the stored value is not a conflict; caps 1, 2 and 3 are tested with a refusal at `n == cap`; a merge after a recorded PASS or ESCALATE is refused; the reviewer's `review: N of cap` header is compared with `--round` and a mismatch warns.
- **Anchors preserved**: `n > cap_reviews` refusal before anything is recorded; `--cap` default `None`, round 1 creates the ledger with `cap or 3`; `--round` help "1 up to the ledger's cap"; ESCALATE path at `n == cap` and `test_escalate_still_prints_verdict_fail` unchanged; about 15 lines in `merge_cmd.py`.
- **Risk**: Low (refusals only); a caller passing a conflicting `--cap` on a later round now errors, which is intended.

#### Change 2: Round-1 quorum, degraded rounds and the `--resolution` denominator (from Variant A, hardened by the probe) [AMENDED: PR-001, PR-013]
- **Source**: A, "Core changes" 3-5, "Contract fields" (round entry `panel_size`, `quorum`, `valid`, `degraded`, `not_cleared`; merged-report `degraded:` header line), unique contribution U-001; probe INV-007 and INV-016
- **Target**: Base, Core item 3 ("A round-1 find path in `superclaude review merge --round 1`"), "Contract fields" (Round reviewer entry), Risk 4
- **Integration**: replace the one-clause quorum in Core 3 with the full rule; append the fields
- **Rationale**: C-003 SPLIT (A's denominator is better at round 1; B's `E-INCOMPLETE` covers later rounds). INV-007: `panel_size = len(resolution.reviewers)`; refuse a report id not in the resolution, a `review_kind` that does not match the round (`first` for n = 1, `re-review` for n >= 2) or an empty list; record `panel_size`, `quorum`, `valid`, `denominator_source`; more than one round-1 report and no `--resolution` marks the round `degraded`. INV-016: `degraded = valid < panel_size`, `quorate = valid >= quorum`; a would-be PASS is refused when any reviewer's block was invalid and a dropped line existed (`dropped_lines > 0`); a quorate FAIL is recorded.
- **Anchors preserved**: `quorum = min(2, panel_size)`; a lone reviewer has quorum 1 (today's behaviour exactly); zero valid blocks stays refused (`ledger.py:150-157`); a degraded would-be PASS is refused with nothing recorded, so only the missing reviewer is re-run; a degraded FAIL is recorded with `degraded: true` and consumes a review number (A's accepted cost); `test_review_ledger.py:376-385` rewritten into two tests (A tests 5-9).
- **Risk**: Medium (reverses the stated intent of `test_one_valid_block_is_enough...`, named in the debate as a deliberate earlier decision; needs owner awareness).

#### Change 3: Atomic refusal inside `merge_round` (debate and probe) [AMENDED: PR-005]
- **Source**: debate, Advocate A Round 2 "Fixes A needs" 1; probe INV-020 (ADDRESSED in principle), INV-019
- **Target**: Base, Core item 3 and 3a; "Test coverage needed" (new test group)
- **Integration**: insert
- **Rationale**: `merge_round` mutates rows, members, history and clearing (`ledger.py:204,209,232,254-258`) before the verdict (`:273-275`); A's "nothing is recorded" holds for the CLI (`merge_cmd.py:109-116`) but not for an in-memory caller. Implementation rule from INV-020: commit by writing the work copy back into the caller's dict (or return the new dict and make the CLI use it) so `render_merged_report` (`ledger.py:412`) still finds the round; INV-019: save the ledger first, then write `--out` (or temp-and-rename); an identical replay (same `report_sha256`) returns the stored result.
- **Anchors preserved**: `ledger.py:204,209,232,254-258,273-276`; `merge_cmd.py:109-116`.
- **Risk**: Low.

### Group 2: Repairs to the base that the debate established

#### Change 4: `review merge` keeps working for round >= 2; `ledger revise` keeps working and records what it did (from Variant A, conceded by B) [AMENDED: PR-012, PR-013]
- **Source**: A, "CLI surface", "Consumer modules"; X-006 (A won at 80%, B-adv conceded); C-011 (A won at 75%); C-017 (A won at 75%); probe INV-006, INV-018, INV-013
- **Target**: Base, Core item 3a, "CLI surface" rows `review merge`, `review ledger revise`, `review ledger verdict`; Risk 7
- **Integration**: replace the unconditional refusal in 3a
- **Rationale**: `document_review_loop_prompts.md:70` tells the coordinator to call `review merge` for every round "also for a single reviewer"; B's shim covers `revise` only. Rule: either (a) `review merge --round k>=2` becomes an adapter that turns the findings block plus `prior` lines into `verify` input, or (b) the CLI refusal and the prompt edit ship in the same change with a skill-text pin test; the plan records both and lets the owner choose (open decision D-4). `ledger revise` additionally records `revised: {round, old_sha256, new_sha256}`; a second revise for the same round and a merge whose doc hash differs from `revised.new_sha256` are refused (INV-006, which also lists the four refusals required by INV-018). One shared decision-to-exit-code table for `ledger.py` and `ledger_cmd.py` with a test that every value `_decision` can return has a code (INV-013).
- **Anchors preserved**: exit codes 0/10/11 (12 PENDING only where the sweep is required); `fixmap-v1` `applied`/`rejected`; `--old` sha256 refusal (`ledger.py:308-314`); prompt line 70 text pinned by `test_review_rules_text.py:34-42,65-73` and `test_review_loop_extension.py:49-55,120-127`; the `plugins/superclaude/rules/prompts/` mirror (A U-006).
- **Risk**: Medium (the adapter is new code; option (b) is a coordinated prompt-and-CLI change).

#### Change 5: Verify boundary follows C02 and C15; bounded refusal recorded in the ledger (from Variant A's semantics, conceded by B) [AMENDED: PR-005, PR-007, PR-019]
- **Source**: A "Seams" table and Risks ("Decider pre-empted"); X-003 (A won at 80%, B-adv "conceded in full"); C-012 SPLIT; probe INV-002, INV-008
- **Target**: Base, Core item 4 (`ledger verify`), "How it works > Data flow", P5, P6, Risk 3 and Risk 6, "CLI surface" row `review ledger verify`
- **Integration**: restructure `check_verify` rules: answers stay all-or-nothing (an unanswered or invalid answer is `E-INCOMPLETE`/`E-SCHEMA`, nothing written); a new row with a missing or doubly occurring anchor, or a malformed new row, is returned in a `problems` list and kept as a flagged deferred row while the valid answers and valid new rows are written. Replace the "one re-ask then X item" of P5 by: a refusal appends `refusals: [{round, reason, report_sha256s}]` (the only write on refusal); after two refusals for a round the loop records an ESCALATE round itself with flag `refused_twice`, so `verdict` exits 11 (INV-002).
- **Anchors preserved**: `E-ANCHOR`, `E-ANCHOR-AMBIGUOUS`, `E-INCOMPLETE`, `E-FROZEN`, `E-SCHEMA` codes and `review_ledger.py:1778-1794`; C15 "keep valid lines, mark the reviewer partial"; C02 "flag a missing anchor"; `--dry-run`.
- **Risk**: Medium (the plan changes ported semantics of an all-or-nothing validator; needs tests for each refusal class).

#### Change 6: Spanless and ambiguous-anchor rows are visible and cannot silently clear (from Variant A's A-006 position, plus probe) [AMENDED: PR-003, PR-007, PR-019]
- **Source**: A (test `test_missing_anchor_is_kept_without_a_span`, `test_review_ledger.py:408-417`, kept open and blocking); debate point A-006 (A won at 68%); probe INV-008; orchestrator verification `hunks_touch(None)` is False (`findings.py:445-447`)
- **Target**: Base, Core items 3 and 4; "Contract fields" (row proposed additions); Risk 4 and Risk 6
- **Integration**: insert
- **Rationale**: a row with no span can never reach the verify clearing condition through a hunk (`hunks_touch(None)` is False) and ends in ESCALATE; a duplicated anchor keeps the first occurrence. Rule: store `anchor_status` and `anchor_ambiguous` on the row and render them in the merged report; a spanless blocking row gets `unanchored: true` and the decision text says "needs a human defer or re-anchor"; an ambiguous row may clear only through an answer whose evidence quote overlaps an occurrence a hunk touched; C02's demotion to a deferred row with a warning at the round-1 merge boundary stays.
- **Anchors preserved**: `test_review_ledger.py:408-417` pins (replaced by the C02 demotion test and a new `unanchored` test, as B already lists); `findings.py:350-352`.
- **Risk**: Medium.

#### Change 7: Evidence rules for the answer, and what each `prior` status does (debate and probe; carries B's semantics into the container) [AMENDED: PR-009, PR-011]
- **Source**: B Core 5 and 11 (evidence quote); debate: Advocate A Round 2 fix 3 and Advocate B Round 2 item "prior line is a bare assertion"; probe INV-003, INV-004, INV-009; C-008 (B won at 80%), A-007 (CONTRADICTED by current code), orchestrator verification (`findings.py:23,175-187`, `findings_v2.py:279-283`)
- **Target**: Base, Core items 5 and 11, "Contract fields" (Answer table), P3
- **Integration**: replace the one-line statement of the answer protocol with explicit rules
- **Rationale**: only `status == "resolved"` can clear; `open` or `regressed` keeps the row out of `resolved` and, when no finding line accompanies it, records an inconsistency warning (INV-003). Priors count only from reviewers with `block_ok`; duplicate prior ids inside one block collapse to the most blocking status and flag the block; across several reviewers a row clears only if every answering valid reviewer said `resolved` and none re-reported it (INV-004). The `evidence` field is a flat string of 12 to 200 characters, required for `resolved`; the quote must `locate` in the new text AND overlap `map_span(row.span, ops)` widened by 3 lines or touch a changed hunk on the new side; for a deletion-only hunk the script checks that the row's anchor no longer `locate`s and accepts a neighbouring-line quote; missing evidence counts as no answer (INV-009). The v1 parser must keep the new keys (today it stores only `{prior, status}`) and the v2 container must accept `prior` lines (A-007; C01 is the owner).
- **Anchors preserved**: `{"prior": "L3", "status": "resolved"}` example line kept in the rules file so the token pins hold; statuses resolved/open/regressed plus `cannot-verify` (`review_ledger.py:1591`, correcting the base's `:65` cite); `touched_ok`; every plan row answered (`review_ledger.py:1752-1754`).
- **Risk**: High (touches the findings container, two parsers and the model-facing prompt; compliance is unmeasured).

### Group 3: Row identity, blocking, scope and persistence

#### Change 8: One-way blocking with a regrade path and a re-attack path; field classes (base defect conceded by B; probe) [AMENDED: PR-004, PR-010, PR-015]
- **Source**: debate: Advocate B Round 2 concessions and "Fixes B needs" 4 and 6, Advocate A Round 1 weakness 3 (frozen round-1 under-grade) and weakness 1 (verified rows immune); C-005 (B won at 95%), C-006 (B won at 80%); probe INV-011, INV-012
- **Target**: Base, Core item 2 (frozen rows), Core item 5, "Contract fields" (Row, frozen at creation; New row)
- **Integration**: restructure
- **Rationale**: keep B's frozen identity and one-way `blocking`, because the re-find path un-blocks a row through a non-blocking note within 3 lines (`ledger.py:166-171,213-218`, `findings.py:367-379`; A-adv conceded the adjacency path in Round 2). Add: a new row whose `parent` is a non-blocking row may regrade it upward when the lens predicate says so; a new row whose `parent` is a `verified` row reopens it when it carries a quote (the base's `E-NOT-CHANGED` becomes "no answer on an untouched verified row; a parented new row is allowed"). INV-011: only blocking calls from valid-block reviewers set `blocking`; a blocking call from a reviewer with an invalid block opens the row as `provisional`; order with the C05 decider is fixed (decider output is `current`, one-way rule applies after it, un-blocking only through a named, logged `unblock` event). INV-012 (relevant at the round-1 merge and in any hybrid): frozen = `lid`, `claim_origin`, `anchor_origin`, `fp`, `category`; mutable = `span`, `span2` (revise or begin mapping only), `status`; `last_seen: {round, claim, anchor}` holds the current text; a 3-line re-find adds an `adjacent_refind` member instead of overwriting `span`.
- **Anchors preserved**: thirteen frozen fields and `E-FROZEN` (`review_ledger.py:1592-1606,1669-1675`); `caused_by`; `blocking` computed by the lens predicate (`:884-897`).
- **Risk**: Medium (new row semantics need tests; it softens "frozen" for two named cases).

#### Change 9: Per-lens predicate, key set and honest sizing of the port (base overstated; conceded by B) [AMENDED: PR-010]
- **Source**: debate: Advocate B Round 2 concession 5 (`_blocking_spec_panel` reads `rule in {FR-8, FR-9}` and `wrong_outcome`, `review_ledger.py:41-49`; row input keys `:64`; unified `findings-v1` line has `severity`, `blocking`, `category`, `refs`, `claim`); X-007 (NEITHER at 60%), C-014 (A won at 83%); A "Seams" table row "Decider"
- **Target**: Base, Core item 9 (lens profile registry), "Contract fields" (New row), "Cost" table and the sentence "B is mostly a port"
- **Integration**: replace the sentence, extend item 9
- **Rationale**: C16 (decided) keeps the reviewer's flag as an input and records the effective flag; the experiment's new-row key set has no `blocking` key. The merged text states that the lens registry needs a per-lens predicate and key set for the unified container (a new predicate for the non-spec lenses, the reviewer flag carried as a candidate input, `effective_blocking` recorded), and that the port covers the document-lens core, with new code for the predicate, the click CLI, multi-path snapshots and the round-1 hand-off.
- **Anchors preserved**: 2,668 lines, byte-identical in three places (orchestrator confirmed the installed copy against the bundle copy), 77 test functions and 1,578 test lines (B's figures, not re-verified by the orchestrator beyond the line count), about 650 reviser-side lines (`:940-1590`).
- **Risk**: Medium.

#### Change 10: Late-finding visibility; the outside-hunk deferral policy waits for a measurement (from Variant A, conceded by B) [AMENDED: PR-002, PR-016, PR-019]
- **Source**: A, Correctness P6, Risks "late findings", unique contribution U-004; debate: C-007 (A won at 70%), X-004 (A won at 73%); Advocate B Round 2 concession 7 and "Fixes B needs" 3; probe INV-013
- **Target**: Base, Core items 6 and 8, "How it works" (decision formula and "brief for a round k reviewer" paragraph), P4, Risks 1 and 2, "Order of work"
- **Integration**: restructure
- **Rationale**: in the base a `deferred`, `scope=outside` row never blocks and `decide` has no sweep term (`review_ledger.py:1696-1698,1900-1914`, B-adv verified), so on a lens whose sweep is off an outside-hunk blocker is stored and the loop can PASS. Rule: (a) each outside row found during verify records `would_block`, listed in the merged report; (b) `decide` gains a term: a would-block outside row on a lens whose sweep is off gives a visible non-PASS, expressed as ESCALATE with `reason: outside_would_block` so no new exit code is needed unless the owner wants PENDING (INV-013: a new decision string is a `KeyError` at `ledger_cmd.py:109` unless the table is shared); (c) the unconditional "new blocking rows only inside changed hunks" policy, and the reversal of the RE-REVIEW clause "record a severe defect you newly discover even if it is older" (`document_review_loop_prompts.md:48`), are NOT the default: until the late-row rate is measured from existing ledgers (round of first appearance from `row["history"][0]["round"]`, reviewer from `members`, changed new-text ranges stored as observation only), outside rows that would block count toward U. Adoption of the deferral policy is owner decision D-1.
- **Anchors preserved**: `scope=in`/`scope=outside`, `caused_by` (`review_ledger.py:1856-1881`); 89% (review 2) and 100% (review 3) of new findings with `origin=changed`, n = 2 + 2, tags read in one arm and re-derived in the other (`AB-REPORT.md:30`), kept as bounding the cost, not as evidence of safety; sweep `sweep: required|none` switch and exit 12 PENDING.
- **Risk**: High (policy change with an owner decision; both advocates disagree on how much recall is lost).

#### Change 11: `defer` goes through the same decision function (probe) [AMENDED: PR-003]
- **Source**: probe INV-001 (orchestrator confirmed `ledger.py:350-360`: `defer` removes the lid from `brief_ids` and rewrites the stored round to PASS when the list is empty)
- **Target**: Base, Core item 7 (decision by formula), "CLI surface" rows `review ledger defer` and `verdict`
- **Integration**: insert
- **Rationale**: in the base the decision is computed by `decide` (`review_ledger.py:1900-1914`), but the master `defer` recomputes PASS inline and never looks at cap, degraded or refused state, so `review ledger defer --lid <any row>` is a second, ungated path to PASS. Rule: `defer` accepts only a live blocking row, calls the shared `decide()` and records `deferred_lids` on the round; a deferred PASS says so in the verdict output.
- **Anchors preserved**: `defer` and `capture` kept (both variants); `test_review_ledger.py:396-405` (status becomes `deferred`).
- **Risk**: Low.

#### Change 12: Rounds 2 and 3 are one reviewer by default; multi-reviewer re-review is an explicit limit (from Variant A's C-010, with B's concatenation rule) [AMENDED: PR-015]
- **Source**: A, "How it works" and "A three-round example"; C-010 (A won at 80%); B Risk 8 and unique contribution U-019
- **Target**: Base, Core item 10 ("No new panel kind"), Consumer modules, Risk 8
- **Integration**: replace the Risk 8 residual with an explicit limit
- **Rationale**: all 8 packaged templates have `apply_to: ["first"]` (`panel.py:600-616`, orchestrator verified), so a re-review resolves one anchor reviewer; the shipped loop never needs several answer sets. Rule: `review merge` and `ledger verify` refuse a round >= 2 whose resolution lists more than one reviewer until the concatenation rule (disjoint answer sets accepted, overlapping sets refused, `open` or `regressed` wins) is built and tested; A's multi-reviewer merge remains the model for round 1 (Change 2).
- **Anchors preserved**: `--kind first|re-review` unchanged; A test 6 and 7 (single-reviewer round and resolution-listed missing reviewer); B test group 11 (concatenation) stays "only if adopted".
- **Risk**: Low.

#### Change 13: Persistence contract: keep B's schema bump, add A's migration fixture, record the writing version (C-009 SPLIT; probe) [AMENDED: PR-006]
- **Source**: B Core 1 (`review-ledger/2`, hash, lock, snapshots); A "Contract fields" (additive keys under `review-ledger/1`), U-002 (fixture generated at HEAD `792cf8c52`); probe INV-014; scoring point C-009 (SPLIT at 58%)
- **Target**: Base, Core item 1, Risk 7, Test group 13 (migration)
- **Integration**: append
- **Rationale**: an older installed binary continuing a new-key `review-ledger/1` ledger would apply the old rules (silence clears, re-find un-blocks) while the file still looks valid; a schema bump fails closed (INV-014). A's additive route is therefore recorded as rejected for the base, but its HEAD-generated fixture is kept as the migration test: a ledger written by the current code loads under the converter or is refused with a message that names the migration; the writing version is printed in the merged-report header. Whether to ship a one-shot /1-to-/2 converter or only the refusal message is owner decision D-5.
- **Anchors preserved**: `load` checks the schema string today (`ledger.py:41-49`); body hash and `E-TAMPERED` (`review_ledger.py:104`, `SKILL.md:40`); the HEAD fixture requirement from A test 13.
- **Risk**: Medium.

#### Change 14: Measure what both sides left unmeasured (from Variant A's telemetry idea, adapted to the base) [AMENDED: PR-019]
- **Source**: A, U-003 (`unanswered_priors`), U-004 (late-row measurement), U-005 (E2 flip fixture); B Risk 3 (compliance unmeasured, whole-input refusal rate)
- **Target**: Base, Risks (monitoring column of Risk 3), "Test coverage needed" (new test groups), "Cost"
- **Integration**: append
- **Rationale**: in the base an unanswered plan row is refused, so A's telemetry-only `unanswered_priors` is replaced by a per-round refusal log (code, count, whether a second refusal occurred) that measures the compliance rate B's Risk 3 calls unknown; A's E2-shaped fixture (a blocking line with an over-length anchor and no other blocking row, 49 `3-dropped-blocking` lines of which 48 were length rejections, 3 measured verdict flips) is kept as a round-1 test that a dropped blocking line cannot yield PASS (conditional on C15 `rejected[]`).
- **Anchors preserved**: `summary.md:20` (three verdict flips), 49 and 48 counts, `row["history"][0]["round"]`.
- **Risk**: Low.

### Group 4: Claims, terminology, tests, delivery order, registers

#### Change 15: Evidence hygiene: remove what the debate showed was overstated (both variants) [AMENDED: PR-018, PR-019]
- **Source**: debate: X-005 (B won at 90%; A-adv conceded), C-016 (NEITHER at 68%; both withdrew claims), A-adv Round 2 "P4 holds for the cap and quorum changes only"; B-adv concession on "mostly a port"
- **Target**: Base, "Position in one paragraph", Evidence D (E-19 to E-23), Correctness P3 and P4, the A-versus-B table
- **Integration**: replace
- **Rationale**: the merged text must not say that round-1 faithfulness (E2, 0 violations over 264 merges) supports a round-2-3 design; must not say A is "strictly safer" or B "better on the evidence"; must state that no completed loop reached a clean PASS, that E-19 is n = 2 + 2, and that the ledger arm's improvement of 3 is below the control spread of 4 while its final-review count (3) is below both controls (8 and 4) and the report itself says "not a ranking".
- **Anchors preserved**: 11 / 9 / 8, 12 / 7 / 4 and 13 / 9 / 3 new CRITICAL+MAJOR labels at reviews 1 / 2 / 3; improvement 3 versus spread 4; 264 merges; `FINAL-REPORT.md:75,97-98,105,135`.
- **Risk**: Low.

#### Change 16: Terminology, citations and glossary (scorer defects) [AMENDED: PR-019, PR-020]
- **Source**: scoring defects R1 and R3 (pass 2) and L4 (pass 1); orchestrator verification of `review_ledger.py:65` versus `:1591`
- **Target**: Base, Core 11, "Contract fields", the first use of D-codes, CLI table
- **Integration**: replace
- **Rationale**: Core 11 cites `review_ledger.py:65` (`ANSWER_ACTIONS`, the reviser's actions) for the verifier's status words; the right cite is `:1591` (`VERIFY_RESULTS`). The word "answer" names two things (`ledger answer`, the reviser's claim step, and the verifier's per-row answer): rename the reviser step `ledger claim` in the merged text, subject to owner decision D-7. Add a four-line glossary box (D1 parser drop count, D2 clearing ignores `block_ok`, D3 pass on one valid reviewer, D16a/b/c cap and `--cap` and verify-only-as-prompt) and gloss the test groups G9/G10 once.
- **Anchors preserved**: all file:line cites that were verified; `ANSWER_ACTIONS` and `VERIFY_RESULTS` values.
- **Risk**: Low.

#### Change 17: One test plan (both variants' tests plus the probe's acceptance tests) [AMENDED: PR-008, PR-015, PR-016]
- **Source**: A "Test coverage needed" (15 new tests, 1 rewritten into 2, gate commands `uv run pytest tests/review/test_review_ledger.py tests/review/test_review_cli.py` = 37 tests today = 24 + 13, G10 178 skill-text tests); B "Test coverage needed" (9 replaced, 15 renamed, 77 ported, 15 new groups, the falsifier run); S-005 (B won at 73%); probe acceptance tests
- **Target**: Base, "Test coverage needed"
- **Integration**: restructure into one table keyed by change number
- **Rationale**: the merged list must contain: A tests 1-9 and 14-15 (cap 1, 2 and 3, `n > cap`, `--cap` cases, quorum k-1 versus k, refused would-be PASS, degraded header, skill-text pin); B's characterization pair for the near-row misbooking (pin today's `regressed` booking, then assert `caused_by` in the new design); an in-memory atomicity test (a refusal leaves `ledger == deepcopy_before`, a success leaves the round in the caller's object); a CLI byte-identical test; INV acceptance tests (defer after a refused or degraded state stays non-PASS; prior `open` does not clear; duplicate prior ids; revise twice is refused; `--resolution` mismatch cases; duplicate-anchor and spanless rows; the title-quote refusal; deletion-fix acceptance; shared exit-code table; refusal log and bounded refusal; a path-closure test that enumerates every writer of `status` and `blocking` and asserts each is gated); A test 10 becomes B's verify tests; A test 12 is dropped (see Not Being Made).
- **Anchors preserved**: `test_review_ledger.py:376-385` (rewritten into two), `:193-217`, `:220-252`, `:255-274`, `:277-304`, `:318-338`, `:345-373`, `:388-393`, `:476-490`, `:518-566`; `test_review_cli.py:196,328,425`; `test_review_rules_text.py:34-42,65-73`; `test_review_loop_extension.py:49-55,120-127`; the 77 ported tests.
- **Risk**: Low (it is a list), Medium to execute.

#### Change 18: Staged delivery with a decision gate between "A plus fixes" and "B port" (resolves C-001 SPLIT and C-013 only as a plan, not as a verdict) [AMENDED: PR-006, PR-014, PR-016, PR-019]
- **Source**: debate: both advocates' Round 2 "merged proposal" lists; A "Cost" sequencing row; B "Order of work"; C-001 (SPLIT at 58%), C-013 (UNRESOLVED)
- **Target**: Base, "Order of work", "Decisions this proposal asks of the owner", "How it works" (intro)
- **Integration**: replace "Order of work"
- **Rationale**: Stage 0 = Changes 1, 2, 3, 11 (cap, quorum, atomic refusal, `defer`; needed by every option; about 50 to 70 lines in `ledger.py` and 15 in `merge_cmd.py` per A's estimate). Stage 1 = round-1 hand-off (C02, C15, C12, C05 hook, Change 6) and the late-row measurement (Change 14). Stage 2 = decision gate between (i) "Option A plus fixes" (re-find engine with atomic refusal, one-way blocking, `prior`-gated clearing, bounded refusal; it keeps the INV-003/004/005/017 class of problems open) and (ii) the verify-only port for the document lens (Changes 4, 5, 7, 8, 9, 10, 13; closes that class by construction because the plan names every live blocking row and an unanswered row is refused). The gate is decided by the falsifier run (needs the C20 portable runner) or by the owner (D-6). Stage 3 = port or finish, then switch the loop prompt in the same change as the CLI (Change 4). The plan does not assert which side of the gate wins.
- **Anchors preserved**: A: "land changes 1 to 5 first", M effort, Medium risk; B: XL effort, High risk, "round-1 fixes first, then port the verify path for the document lens, then switch the prompt, then run the falsifier"; B's three owner decisions.
- **Risk**: Medium.

#### Change 19: Open-decision and unresolved-conflict register (new section in the merged proposal) [AMENDED: PR-013, PR-020]
- **Source**: debate: unresolved points S-006, C-013, A-002, A-004; owner decisions D-1 to D-10 named in Changes 4, 10, 13, 16, 18
- **Target**: Base, new section after "Cost"
- **Integration**: insert
- **Rationale**: the merge must keep every unresolved conflict visible. For each: both advocates' final positions and why they differ. S-006 (A-adv: B 55, B-adv: SPLIT 55) built-versus-new framing; C-013 (A-adv: B 65, B-adv: SPLIT 60) falsifier versus the late-row measurement, both kept; A-002 (A-adv: NEITHER 65, B-adv: B 55) fix locality, B's `touched_ok` child-row rule versus both being fail-closed; A-004 (A-adv: NEITHER 55, B-adv: B 55) coordinator retry compliance. D-1 outside-hunk policy default; D-2 older-defect clause; D-3 mandatory sweep for blocking consumers; D-4 adapter versus same-change prompt edit; D-5 converter versus refusal message; D-6 authorise the falsifier and the C20 runner; D-7 `claim` versus `answer`; D-8 PENDING exit 12 versus ESCALATE with reason; D-9 decider and one-way order (C05); D-10 multi-reviewer re-review scope.
- **Anchors preserved**: B's "Decisions this proposal asks of the owner" (1) to (3), mapped to D-1/D-2, D-3 and D-6.
- **Risk**: Low.

#### Change 20: Invariant register and the restated sufficiency claim (new section; probe) [AMENDED: PR-009]
- **Source**: `invariant-probe.md` (20 findings: 10 HIGH UNADDRESSED, 7 MEDIUM UNADDRESSED, 1 LOW UNADDRESSED, 2 ADDRESSED in principle)
- **Target**: Base, new section after Correctness; the claims made in P1 to P4
- **Integration**: insert; replace the unconditional sentences in P1 and P2
- **Rationale**: INV-010 shows the claim "cannot certify PASS wrongly, cannot clear wrongly, always terminates" is false for the consensus package alone (F1 to F6). The merged text restates it as "no PASS and no clear without a positive, script-checked signal on the recorded-round path, given INV-001 to INV-009 closed", lists F4 (a quorate panel with a dropped blocking line; owner: C05 hook), F5 (an all-empty round-1 PASS under the v1 container; owner: C01) and F6 (version skew) as accepted residual risks with owners, and carries a table of the 20 probe findings with, for each, the closure rule adopted into a numbered change of this plan or the statement "open". Items that are closed by construction in the base (INV-005, INV-017: plan rows are the live blocking in-scope rows and an unanswered row is refused, not recorded) are marked as such, and as open for the Stage-2 option "A plus fixes". The probe status stays UNADDRESSED for every HIGH item because none was debated; the register states that.
- **Anchors preserved**: all INV ids and severities; F1 to F6.
- **Risk**: Low (documentation), but it is the item that keeps `unaddressed_invariants` honest.

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach (Variant A) | Rationale for Keeping Base | Debate evidence |
|------------|-------------------------------|----------------------------|-----------------|
| C-001, X-002 | Re-find and cluster every round as the default model for rounds 2 and 3; D16c "closed as by design" | Not adopted into the base text. It stays in the merged proposal only as the Stage-2 alternative "Option A plus fixes" (Change 18), because the advocates ended SPLIT (58%): A is the shippable first step, B is the better rounds 2-3 target, and prompt-only verification has no code check (X-002, B won at 70%) | Round 2, both advocates; scoring matrix C-001, X-002 |
| C-002, X-001 | Clearing a `resolved_check` row when a quorate valid reviewer does not re-report it | An empty findings block is valid (`parse_block` `ok` True; `document_review_loop_prompts.md:58`, orchestrator-verified), so a skim and a clean read look identical to the script; A-adv conceded C-002 and X-001 in Round 2 | Round 2 A "Concessions"; scoring matrix C-002 (93%), X-001 (90%) |
| C-005 | Recompute `blocking` from the current round's group (`ledger.py:213-218`), left to C05 | One non-blocking note within 3 lines of a blocking row un-blocks it without re-reporting that row's defect; A-adv: "A's P2 is false as written"; kept: frozen, one-way blocking with the regrade path of Change 8 | Round 2 A item 3; scoring matrix C-005 (95%) |
| C-006 | Re-cluster and re-match every round with `same_defect` (3-line rule); the stored `claim` is not updated on a match | Misbooks a fix-induced defect as a regression with a stale claim (`ledger.py:199` versus `:208-234`); kept: frozen ids, `caused_by`, characterization test | Round 2 A item 5; scoring matrix C-006 (80%) |
| C-008 | `prior` lines as inert notes (`test_prior_lines_never_change_a_status`) | The invariant "only the script changes a status" is kept; what changes is that the script validates an evidence-bearing answer (Change 7). The pinned test is reversed for round 2 onwards, as B listed | scoring matrix C-008 (80%); Round 2 both |
| C-009 (partial) | Additive keys under an unchanged `review-ledger/1` | An older installed binary continuing a new-key ledger applies the old rules while the file looks valid (INV-014); the HEAD fixture is kept as the migration test (Change 13) | probe INV-014; scoring matrix C-009 (SPLIT) |
| C-012 | Refuse a degraded would-be PASS with no bound on re-runs, and mutate before refusing | Replaced by a recorded bounded refusal (Change 5) and atomic refusal (Change 3) | Round 2 A concessions; probe INV-002, INV-020 |
| X-005, C-016 | Round-1 E2 faithfulness (0 violations over 264 merges) offered as support for the round engine; the reading that the #346 bundle "does not favour verify-only" | Both advocates withdrew these claims; the merged text states the no-convergence facts without a ranking (Change 15) | Round 2 A item 4 and B item 6; scoring matrix X-005 (90%), C-016 (NEITHER) |
| (claims) | P3 "Status is truthful... only by the four-step chain" and P4 "strictly safer than today" as general properties | P4 holds for the cap and quorum changes only (Round 2 A: "does not hold for D4"); P3's third step is a valid reviewer's silence (X-001) | Round 2 A "Concessions" |
| A change 4 | The clearing loop runs only when the round is not degraded | The base has no silence-clearing loop; the degraded concept is kept for round 1 and multi-reviewer first reviews only (Change 2) | scoring matrix C-002, C-003 |
| U-003 | `unanswered_priors` recorded as telemetry only, no gate | In the base an unanswered plan row is refused (`E-INCOMPLETE`), so the lapse cannot pass; the measurement need is met by the refusal log (Change 14) | Round 1 B strength 1, Round 2 B "Updated assessment" |
| A test 10, test 12 | Clearing-positive-case test; `unanswered_priors` does not stop a clearing round | Replaced by B's verify tests (positive clearing with a quote, silence refused); test 12 has no subject once silence cannot clear | Change 17 |
| C-010 | Merge supports several reviewers in rounds 2 and 3 | The default is one anchor reviewer (all 8 templates `apply_to: ["first"]`); the merged text states multi-reviewer re-review as an explicit limit until the concatenation rule is tested (Change 12); A's multi-reviewer merge stays as the round-1 model | scoring matrix C-010 (A won at 80%): the benefit is real but unused in the shipped configuration |

### Base elements NOT carried unchanged (what the plan modifies in Variant B, with the debate evidence)

| Base element | Defect established in the debate | Change |
|--------------|----------------------------------|--------|
| Core 3a: `review merge --round k>=2` refused while the loop prompt calls `review merge` every round | X-006, B-adv conceded; prompt line 70 verified | 4 |
| `check_verify`: whole-input refusal including new rows with a bad anchor | X-003, B-adv "conceded in full"; `review_ledger.py:1778-1794` | 5 |
| First-pass `blocking` frozen with no upward path; a verified row cannot be re-attacked | B-adv concessions; `:1699-1705` | 8 |
| New rows outside changed hunks stored `deferred`, immutable, never block; `decide` has no sweep term | B-adv concession 7; `:1696-1698,1900-1914` | 10 |
| "Mostly a port"; byte-identical predicate and key set | B-adv concession 5; `:41-49,64` | 9 |
| "Applied the spread screen better than A" | B-adv withdrew | 15 |
| `review_ledger.py:65` cited for the verifier's status words; "answer" used for two steps; D-codes unglossed | scoring R1, R3, L4 | 16 |
| `defer` recomputes PASS inline | probe INV-001 (orchestrator-confirmed `ledger.py:350-360`) | 11 |

## Threshold Preservation

Every numeric threshold, limit or count inherited from either variant, with the target disposition. "exact" = preserved verbatim; "modified" = changed with the stated rationale; "dropped" = removed with the stated rationale.

| Source variant | Value | Target disposition |
|----------------|-------|--------------------|
| A, B | cap 3 reviews (`cap_reviews` default; two fix cycles; ESCALATE at the cap) | preserved-exact (Change 1) |
| A | `--cap` default `None`, round 1 creates with `cap or 3` | preserved-exact (Change 1) |
| A | `quorum = min(2, panel_size)`; quorum 1 for a lone reviewer; panel of 3 gives quorum 2 | preserved-exact (Change 2); the meaning of `degraded` is modified: `valid < panel_size` (INV-016) |
| A | about 50 to 70 added lines in `ledger.py`, about 15 in `merge_cmd.py` | preserved-exact as the Stage 0 estimate only; dropped as an estimate for the whole design (Change 18) |
| A | 37 tests in the two gate files (24 + 13), 178 skill-text tests (G10) | preserved-exact as gate commands (Change 17) |
| A | 1 test rewritten into 2, about 14 new, 15 listed | modified: the merged list is larger (Change 17) |
| B | 24 existing ledger tests: 9 replaced, 15 renamed | preserved-exact; the two that A also rewrites (`:376-385`) are listed once |
| B | 2,668-line script; 1,578-line test file with 77 test functions; about 650 reviser-side lines (`:940-1590`) | preserved-exact; the "mostly a port" wording is modified (Change 9) |
| B | 13 frozen row fields | preserved-exact with two named exceptions: the upward regrade and re-attack through a parented new row (Change 8) |
| B | exit codes 0 PASS, 10 REVISE, 11 ESCALATE, 12 PENDING (only where the sweep is required); refusal exit codes 1, 2, 3, 4 | preserved-exact; a new decision value must have a code in the shared table (Change 4) |
| B | `E-CAP`: refuse a fourth review or a third fix cycle | preserved-exact (Change 1 adds the master-ledger equivalent) |
| B | "one re-ask, a second refusal is an X item and ESCALATE" | preserved in effect: two refusals for a round record an ESCALATE round (Change 5) |
| B | 89% (review 2) and 100% (review 3) of new findings `origin=changed`, n = 2 + 2 | preserved-exact with its limits (Changes 10 and 15) |
| A, B | new CRITICAL+MAJOR labels 11 / 9 / 8 and 12 / 7 / 4 (controls), 13 / 9 / 3 (ledger arm); improvement 3 versus spread 4 | preserved-exact (Change 15) |
| A, B | 264 merges, 0 violations; 49 `3-dropped-blocking` lines, 48 length rejections; 3 measured verdict flips; 195 chained rows and 83 mega-rows | preserved-exact as sourced figures; the misbooking claim they motivate stays an [inference] until the characterization test runs (Change 17) |
| B | sweep costs about 10 to 15 minutes and a loop is 13 to 17 script calls | preserved-exact as estimates, not measurements |
| B | M effort and Medium risk (A), XL and High (B) from the synthesis | preserved-exact, attached to the stages (Change 18) |
| probe | evidence quote 12 to 200 characters, widened by 3 lines around the mapped span (from the finding-anchor bounds at `findings.py:104` and the 3-line rule at `:377`) | new, labelled proposed (Change 7) |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|----------|------|------------------|----------|
| 1 | Low | A later-round caller passing a conflicting `--cap` errors | Revert `default=None` and the refusal; ledgers are unchanged |
| 2 | Medium | Legitimate single-reviewer rounds refused through a wrong denominator (INV-007) | Fall back to the report count, mark rounds with unknown denominator `degraded` |
| 3 | Low | In-memory callers see a mutated ledger after a refusal | Revert to the existing refusal order; CLI path stays safe |
| 4 | Medium | The loop prompt calls a refused command | Keep the adapter or hold the prompt edit and CLI refusal in one commit |
| 5 | Medium | Valid answers accepted next to a flagged bad row change the state machine's phases | Revert to whole-input refusal and accept C15 non-conformance on verify rows |
| 6 | Medium | Spanless rows pile up as non-clearing blockers | Human `defer` path (Change 11) |
| 7 | High | Model-facing prompt and two parsers change; compliance unmeasured | Hold behind the refusal log (Change 14) and keep the v1 `prior` line as is |
| 8 | Medium | A parented new row is misused to reopen verified rows | Restrict to rows with a quote that `locate`s; log `parent` use |
| 9 | Medium | Predicate for non-spec lenses is wrong | Single lens (document) first, as B's order of work |
| 10 | High | Outside rows block loops that would have passed; or hide real defects if D-1 is decided the other way | Keep outside rows `deferred` plus the sweep term; owner decides |
| 11 | Low | Existing `defer` callers see refusals | Keep the old behaviour behind a flag for one release |
| 12 | Low | A consumer needs overlapping verifiers | Build the concatenation rule |
| 13 | Medium | Existing `review-ledger/1` files stop loading | Ship the converter (D-5) |
| 14 | Low | None (observation) | Remove the log |
| 15 | Low | None (text) | n/a |
| 16 | Low | Rename churn | Keep `answer` (D-7) |
| 17 | Low | Test list too large to run in one change | Stage by change number |
| 18 | Medium | The gate is never decided and Stage 2 stalls | Owner decision D-6 forces it |
| 19 | Low | None | n/a |
| 20 | Low | A reader treats the register as resolved | The register states "UNADDRESSED" per item |

## Plan Review and Amendments (binding)

Reviewer: `c13-plan-reviewer`, a separate zero-trust `general-purpose` agent that did not write the plan (full text in `refactor-plan-review.md`). It checked the plan against both variants, the debate, the probe and the code, verified 16 of 20 spot-checked file:line claims (none wrong; four unverified by it), and returned APPROVE WITH CHANGES with 21 findings. By its entries the count is 5 BLOCKER (PR-001 to PR-005), 11 MAJOR (PR-006 to PR-016) and 5 MINOR (PR-017 to PR-021); its own footer says 6/10/5, the orchestrator uses the entry-level count. The orchestrator accepted all 21; no finding was declined. Application rule for the merge-executor: where an Amendment below names a clause of a Change, the Amendment text REPLACES that clause and the replaced clause must not be applied; changes marked `[AMENDED: ...]` in their heading are affected. Apply the Changes in the order given in A-16.

### Amendments to Changes (one per review finding)

**A-01 (PR-001, BLOCKER) Change 2, degraded-round rule.** Delete from Change 2 the "Anchors preserved" clause "a degraded would-be PASS is refused with nothing recorded" and the rationale clause "a would-be PASS is refused when any reviewer's block was invalid and a dropped line existed". Replace both by this table (record both booleans `degraded` and `below_quorum` on the round entry):

| valid blocks versus panel | Would-be PASS | FAIL |
|---|---|---|
| `valid = 0` | refused (unchanged, `ledger.py:150-157`) | refused |
| `valid < quorum` (`below_quorum`) | refused; no round recorded (only write: Amendment A-05) | recorded with `degraded: true` |
| `quorum <= valid < panel_size` (`degraded`, INV-016) | refused only if a non-valid reviewer had `dropped_lines > 0` or a rejected line with `blocking: true`; otherwise recorded with the `degraded:` header line | recorded with `degraded: true` |
| `valid = panel_size` | as today | as today |

A tests 7, 8 and 9 are rewritten to this table (k-1 versus k at quorum; a second pair at `panel_size - 1` with and without a dropped line). The `--resolution` membership and `review_kind` checks of INV-007 apply only when `--resolution` is given (the CLI round-trip test at `tests/review/test_review_cli.py:196` runs round 2 with one `--report` and no `--resolution`). Threshold table: add the row "A: denominator `max(report count, resolution count)` -> modified to `len(resolution.reviewers)` when a resolution is given, else the report count with the round marked `degraded` when more than one round-1 report exists; rationale INV-007" (PR-013d).

**A-02 (PR-002, BLOCKER) Change 10, outside rows.** Delete the clause "outside rows that would block count toward U" and every statement that an outside row enters U. Replace clauses (b) and (c) by: "An outside row records `would_block = predicate(row)` (as sweep rows do, `review_ledger.py:2253`). `decide` gets a fourth term W = the number of would-block outside rows found in rounds >= 2 on a lens with `sweep: none`; W > 0 gives ESCALATE with `reason: outside_would_block` (no new exit code; the INV-013 shared table). W never enters U, never enters the plan, and is listed in the merged report. The owner decision (OD-1) decides only whether W is ignored (the deferral policy) or counted." In the Risk Summary row for Change 10 add: "W > 0 ends a loop at round 2 without a fix cycle; that is the visible cost." Change 10 is split for application into 10a (record `would_block` and list it in the merged report), 10b (the W term and exit mapping), 10c (the default and OD-1).

**A-03 (PR-003, BLOCKER) Change 11 and Change 6, `defer`.** Replace Change 11's rationale and rule by: "Stage 0 (master engine): `defer` goes through the shared decision function: it accepts only a live blocking row, calls the shared `decide()`, records `deferred_lids` on the round. Stage 3 (port): the ported `defer` stays words-only (`review_ledger.py:2359-2386`, phase `terminal` or `swept`, no status change), because the ported `decide` needs `plan_answered` and snapshots. A human release of a row that cannot clear (spanless, ambiguous) is a separate command `ledger release --id --quote`, allowed only in phase `verify`, recording the quote, setting status `deferred` and counted in the delivery outcome like a sweep row; the owner may decline that command (decision OD-11)." In Change 6, replace "needs a human defer or re-anchor" by "needs `ledger release` (Stage 3; `defer` at Stage 0) or a re-anchor", and the Risk Summary rollback for Change 6 by the same.

**A-04 (PR-004, BLOCKER) Change 8, regrade and re-attack paths.** Delete the sentences that give `parent` the two new meanings and the sentence "`E-NOT-CHANGED` becomes ...". Replace by named new-row inputs: `reattack_of: <verified row id>` (requires `evidence` that locates and a changed hunk overlapping the quote; otherwise the row is stored `deferred` and counted in W of A-02) and `regrade_of: <non-blocking row id>`. Required code changes, stated in the merged text: (a) validation at `review_ledger.py:1769` accepts those two ids, which today fall outside `plan_ids` (live blocking in-scope rows only, `:1654-1658`, `LIVE_STATUSES` at `:66`); `parent` keeps its existing meaning (the child row required by an answer with `touched_ok: no`, `:1746-1751`); (b) the transition table gains `verified -> reopened` through `reattack_of` only; (c) `E-FROZEN` lists `blocking` with these two named exceptions; (d) a reopened row enters the next round's plan, not the current one. In P2 and in "Strengths to Preserve" the guarantee "accepted text cannot be re-attacked" (`:1703`) is restated as "cannot be re-attacked except through `reattack_of` with a located quote over changed text". The Change 8 risk is HIGH (A-15), with impact "a reopen loop is bounded by the cap only".

**A-05 (PR-005, BLOCKER) Changes 1, 3, 5, 14, 17, "nothing is recorded".** Wherever Changes 1, 3 or 17 say that nothing is recorded on a refusal, write: "no row, member, history, round or clearing change is recorded; the only permitted write is an append to `refusals[]`, saved by the CLI in its `except LedgerError` path before it re-raises (`merge_cmd.py:111-116`; INV-019: save the ledger first, then write `--out`)". The atomicity test is `ledger_without_refusals == deepcopy_before`. In Change 5 add: a refusal for a replayed identical input (same `report_sha256s`) does not append a second entry, so a lost-response retry does not count toward "refused twice".

**A-06 (PR-006) Changes 13 and 18, Stage 0 schema.** Add to Change 13 and Change 18: Stage 0 writes an additive `min_writer` key on every save (about five lines); new code refuses to append a round to a ledger whose `min_writer` it does not know; the writing version is printed in the merged-report header. This keeps INV-014 closed from Stage 0 until the `review-ledger/2` bump arrives with the port. If the owner declines, the skew is accepted for Stages 0 to 2 and the merged text says so.

**A-07 (PR-007) Change 5, partial acceptance.** Add to Change 5: "A new row that is the required child of an answer with `touched_ok: no` (`review_ledger.py:1746-1751`) is never demoted; its problem refuses the whole input. Every other bad new row is stored once with `status: deferred`, `scope: outside`, `origin: unanchored`, `flag: <code>`, in the same atomic write as the valid answers; the input hash is recorded so an identical replay returns the stored result." Reword P1 and Core 4 to "invalid answers refuse the input; invalid new rows are demoted". Add three tests to Change 17: the required child is not demoted; the replay with demoted rows returns the stored result; a demoted row with no `at` is stored in its declared form.

**A-08 (PR-008) Change 17, which tests stay.** Split the "Anchors preserved" list by stage: "Stage 0 to 2 (master engine): these stay green: `test_review_ledger.py:193-217`, `:220-252`, `:255-274`, `:277-304`, `:318-338`, `:345-373`, `:388-393`, `:476-490`, `:518-566` (A's list), except `:376-385`, which is rewritten into two tests. Stage 3 (port): the nine tests of the base's table are replaced (`:193`, `:220`, `:255`, `:318` reversed for round 2 onwards, `:376`, `:408`, `:493`, `:518`, `:547`); `:277-304`, `:345-373`, `:388-393`, `:476-490` and the other renamed tests stay." The key of the merged test table is (test, stage).

**A-09 (PR-009) Change 20, register status.** Make the register a three-state column: `closed-in-port (pinned by test X)`, `closed-by-Change-N`, `open`. Mark INV-003, INV-004, INV-005, INV-006 and INV-017 `closed-in-port` and state the four conditions: (1) the only writer of a round decision is the ported `close`/`decide`; (2) the `ledger revise` shim runs the ported `answer`/`begin`, not master `apply_revision`, which moves any open or regressed `applied` row to `resolved_check` without checking `blocking` (`ledger.py:328-339`); (3) demoted rows (A-07) stay outside the plan; (4) rows reopened by A-04 enter the next plan. For Stage 2 option "A plus fixes" those items are `open`. Replace the sentence "the probe status stays UNADDRESSED" by: "probe status is UNADDRESSED because none was debated; the design status is the column above; no row is `closed` until its acceptance test exists". Add INV-005 and INV-017 acceptance tests to Change 17.

**A-10 (PR-010) Change 8, vocabulary.** For the base keep the 13 frozen fields (plus the two exceptions of A-04) and delete the master field list (`lid`, `claim_origin`, `anchor_origin`, `fp`, `category`, `span`, `span2`, `last_seen`, `adjacent_refind`) from the base text. State that INV-011 and INV-012 apply to the round-1 merge and to Stage 2 "A plus fixes" only, and keep the field-class list inside that scope. Add `members[]` (reviewer id, finding id, block-valid flag, round), written by `find` from the clusterer, to the "Row, proposed additions" table in Change 9 so that the measurements of Changes 10 and 14 have a source.

**A-11 (PR-011) Change 7, vocabulary and refusal.** Reword in two parts. (a) "In the port: answers use `result` in `resolved, open, regressed, cannot-verify` (`review_ledger.py:1591`); a missing or non-locating quote is a whole-input refusal (`E-ANCHOR`, `:1711-1722`; the same input otherwise fails `E-INCOMPLETE`); add (proposed) a minimum quote length of 12, a maximum of 200, and the overlap-with-hunk rule for `resolved` on top of the existing touching-hunk requirement (`:1723-1730`)." (b) "In the adapter of Change 4(a) and in Stage 2 'A plus fixes': a `prior` line with status `resolved` is the only status that can clear; duplicate prior ids collapse to the most blocking status; several reviewers clear only by unanimity." Delete the claim that INV-003 and INV-004 need new rules inside the port.

**A-12 (PR-012) Change 4, engine behind `ledger revise`.** Add: "Stages 0 to 2: `ledger revise` is master `apply_revision` plus the `revised` bookkeeping and the four INV-018 refusals. Stage 3: `ledger revise` is the shim over `answer` and `begin`; the `--old` hash check is `begin`'s snapshot check and the `revised` key is dropped. The exit-code table is shared (INV-013) in both." Add the Stage 3 removal to the rollback of the Change 4 Risk Summary row. Add the A "Seams" table (parse, cluster and match, decider, verdict mapping, naming C01, C02, C12, C05, C15, C16, C19) as one paragraph under Core 3 (PR-013c).

**A-13 (PR-013) "Changes NOT Being Made" and registers.** Add rows: C-015 (keep B's consumer table; A's PR-bots objection "every round is a re-find by construction" and its tasklist-module row are recorded in the register of Change 19 as an open point, SPLIT at 55); A-005 (register item: no addressee for an unattended ESCALATE or PENDING; owner C19); A-001 and A-003 (kept as in the base: evidence quote, served-model flag, `touched_ok`; no change needed); the seams table (preserved, A-12). Threshold row for the denominator is in A-01.

**A-14 (PR-014) Change 18 and the C-001 row, neutrality.** (1) In "Changes NOT Being Made" replace "B is the better rounds 2-3 target" by "the advocates ended SPLIT (58%): A is the shippable first step, B has the stronger clearing rule on the evidence of the code; no measurement separates them". (2) In Change 18 restate the invariant sentence symmetrically: "(i) inherits INV-005 and INV-017 as open unless the probe's `unverified` rule is adopted; (ii) closes them in the port under the four conditions of A-09". (3) Add this specification of option (i) to Change 18: "Option (i), A plus fixes = Changes 1, 2, 3, 11 (Stage 0 form), plus clustering with the sticky one-way blocking rule (Change 8 without the new inputs), `prior`-gated clearing (A-11(b)), bounded refusal (A-05, Change 5's refusal log), and the probe's INV-005 fix (`unverified` ids rendered in a separate merged-report section and named in the RE-REVIEW instruction, with a distinct RE-REVIEW decision or an explicit statement that REVISE with an empty id list is accepted)." The merged text must be able to argue both sides of the gate.

**A-15 (PR-015) Change 17 test groups and Change 8 risk.** Add to Change 17 the seven groups: (a) `reattack_of`/`regrade_of`, `provisional`, the logged `unblock` event, an `adjacent_refind` member; (b) W > 0 gives ESCALATE with the reason and W never enters the plan; (c) a round >= 2 whose resolution lists more than one reviewer is refused; (d) the converter or refusal-message test (depends on OD-5); (e) a predicate test per non-spec lens; (f) three refusal classes for Change 5 (the three tests of A-07); (g) the decision table of A-01. Change the Change 8 row of the Risk Summary to HIGH with the rationale "touches the frozen-field rule and the no-re-attack guarantee".

**A-16 (PR-016) Application order and splits.** Apply in this order: 16 -> 9 -> 15 -> 13 -> 1 -> 2 -> 3 -> 11 -> 4 -> 12 -> 5 (with Change 6 merged into it as one edit of `check_verify` and the Row table) -> 7 -> 8 -> 10 (as 10a, 10b, 10c) -> 14 -> 17 -> 18 -> 19 -> 20 last, because 19 and 20 cite every other change by number. For Change 17 build the table skeleton with columns change, test, stage, source (A/B/probe), status (new/replaced/renamed/kept). For Change 18 build a stage table (stage, changes, exit condition). Keep each Change's text inside the section it targets; do NOT add a changelog paragraph at the top of the merged proposal.

**A-17 (PR-017) Change 1.** Replace "caps 1, 2 and 3 are tested with a refusal at `n == cap`" by "round `cap + 1` is refused and round `cap` is recorded as ESCALATE (caps 1, 2 and 3)".

**A-18 (PR-018) Change 15.** Add "(the report's own line 135 counts 6 loop-only unresolved labels, not 3)" after the claim about the ledger arm's final-review count, and state that with 6 the arm is above the second control (4).

**A-19 (PR-019) Targets.** Change 14: target the Mitigation cell of Risk 3 (no monitoring column exists). Change 18: target the sentence after the Data flow diagram, or add a one-paragraph intro and say so. Change 1: "Order of work" is one paragraph, not numbered steps. Change 15: Evidence D is E-19 to E-24. Changes 5 and 6: drop Risk 6 from the Targets; the relevant risks are 3 and 4. Change 16: gloss G9/G10 only after Change 17 has brought them in, or drop that clause.

**A-20 (PR-020) Names.** Number the owner decisions OD-1 to OD-11 (OD-11 is the `ledger release` command of A-03) instead of D-1 to D-10, to avoid the collision with the defect codes D1/D2/D3/D16 and the gaps-log `D-nn` ids. In Change 16 the executor default is: keep `ledger answer` for the reviser's step and write "plan answer" or "verifier answer" for the other; rename to `ledger claim` only if OD-7 is decided before the merge.

**A-21 (PR-021) Labels.** In the Overview state "Groups are application groups; Stages (Change 18) are delivery stages", and list the Stage membership of each change in the Risk Summary (Stage 0: Changes 1, 2, 3, 11 in its Stage-0 form; Stage 1: 5, 6, 14; Stage 2: gate; Stage 3: 4, 7, 8, 9, 10, 12, 13; always: 15 to 20). Add Threshold rows for the changed denominator (A-01) and for the 12-to-200 quote bound (A-11).

## Review Status
- [x] Reviewed by a separate analytical agent (`c13-plan-reviewer`): APPROVE WITH CHANGES, 21 findings (5 BLOCKER, 11 MAJOR, 5 MINOR), all accepted and written as Amendments A-01 to A-21
- [x] Auto-approved (default; `--interactive` not set) after the review amendments
- [ ] User-approved (--interactive): not applicable
- Approved by: auto (orchestrator), conditional on the Amendments above being applied by the merge-executor
- Approval timestamp: 2026-11-14T01:34:00Z
