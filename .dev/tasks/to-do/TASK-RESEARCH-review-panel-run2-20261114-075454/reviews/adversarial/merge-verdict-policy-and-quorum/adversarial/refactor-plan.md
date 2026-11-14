# Refactoring Plan: Merge into Base (Variant A = Proposal A)

## Overview
- Base: Variant A (Proposal A, `adversarial/variant-1-original.md`), selected in `base-selection.md` (A 0.9007, B 0.8590, margin 4.17%, tiebreaker level 1: debate performance A 9 points, B 3).
- Incorporating strengths from: Variant B (Proposal B, `adversarial/variant-2-original.md`) and from the Round 2 negotiated hybrids (`round2-advocate-A.md` "Hybrid terms acceptable to A", `round2-advocate-B.md` "Counter-hybrid terms").
- Planned changes: 14
- Risk level: Medium overall (changes 2, 3, 4 alter the mechanism text of the base; every change is a text change to a position paper, none touches code)
- Output file: `<output>/merged-output.md` (one level above `adversarial/`).
- Content rule for the merge-executor: every new or replaced sentence must come from the sources named in the change (the variants and the debate files). No new design decisions, numbers, file:line citations or claims may be added. Where a change says "state as open", the text must say it is open. Preserve the base's tag convention ([CODE-VERIFIED], [CODE-CONTRADICTED], [UNVERIFIED]) and add the tag `[DEBATE-VERIFIED]` for facts that an advocate verified in the code during the debate (cite the debate file, e.g. `round1-advocate-A.md` code log), and `[UNVERIFIED]` for anything taken from a research file that no advocate re-read.
- The document is the merged position for slot C-03, titled "Merged resolution: slot C-03 (merge-verdict-policy-and-quorum)". It keeps the base's seven sections and adds section 8.

## Planned Changes

### Change 1: Position paragraph and claims discipline (from Variant A, modified by debate)
- **Source**: Variant A section 1 and 4.1 (Fail-closed row); `round2-advocate-A.md` Hybrid bullet 1, 9, 12; `round2-advocate-B.md` Counter-hybrid terms 1, 9; diff points X-001, X-005.
- **Target**: Base section 1 (replace) and the Fail-closed row of 4.1 (replace wording).
- **Rationale**: Both advocates agreed the default is `union` for every panel module, reflect keeps `legacy-adversarial` authoritative with `shortfall: visible`, no LLM stage in `review merge`, and that "fail-closed at every panel size" overclaims. Scoring matrix C-001 Hybrid 65%, X-001 Hybrid 63%, X-005 B 55%.
- **Integration point**: Replace the position paragraph. Required content: union default; quorum is a merge-time gate (see change 2), not a derived outcome; reflect keeps its chain; no calibrator, debate or grader in the default path; the default "rests on fail-closed asymmetry and on the absence of any measurement, not on measured superiority"; fail-closed is claimed "in every profile that sets `degrade`", and reflect keeps its pinned PASS-eligible 2-of-3 shortfall; the only shipped-behaviour change in the spec loop is a refusal of rounds below quorum; Variant B's `adjudicated`-as-default is recorded as a hypothesis awaiting a measurement.
- **Risk**: Low. Wording only.

### Change 2: Quorum as a merge-time refusal (from Variant A, modified by both Round 2 advocates)
- **Source**: Variant A section 2.1 (quorum bullet, outcome-function bullet), 3.1 item 1; `round2-advocate-A.md` Hybrid bullet 3, 5, 6 and R7; `round2-advocate-B.md` bullet 3, 5, 6 evaluation and Counter-hybrid terms 2, 4; diff points C-003, C-004, C-006.
- **Target**: Base section 2.1 (replace the "derive_panel_outcome ... DEGRADED" and quorum bullets).
- **Rationale**: Both advocates converged on a merge-time gate: it needs no derive-on-read, avoids clearing rows on a mostly failed panel (A K2), and avoids a new decision value that would raise `KeyError` at `ledger_cmd.py:109` (A K6, B bullet 6). Scoring matrix C-004 A 65%, C-006 A 68%.
- **Integration point**: Required content: in a `degrade` profile (spec-review default) a round needs `complete >= min(2, requested)` where `complete` counts reviewers whose findings block parsed (`complete` state; `findings_v2.py:40`; the caller supplies `failed` and `timed_out`); below it `merge_round` raises a `LedgerError` subtype before any mutation, in the same place as the zero-valid refusal (`ledger.py:150-157`), recording nothing (ledger JSON byte-identical, no round appended, cap not consumed, no `resolved_check` row cleared); the zero-valid refusal uses the same class and the same exit code; floor value (2-of-3, majority, all) is declared unmeasured; the outcome function remains pure over rows, the round's recorded quorum result and the policy name and returns PASS, REVISE or ESCALATE; the derive-on-read statement (decided, VM-3) stays. State the `shortfall: visible` mode for reflect only. Keep the base text on `COMPLETION_STATES`, manifest counts and `cluster_v2` `valid_blocks`.
- **Risk**: Medium. Replaces the base's DEGRADED-outcome mechanism.

### Change 3: Source of `requested` and the retry rule (from Variant B's Round 2 evaluation; A did not reply)
- **Source**: `round2-advocate-B.md` bullet 3, 4, 12 evaluation and Counter-hybrid term 3, New evidence 1-2; `round2-advocate-A.md` Hybrid bullet 4 and New evidence 4; diff point A-003, X-004.
- **Target**: Base section 2.1 (new bullet after the quorum bullet).
- **Rationale**: B rejected A's "quorum not measured" fallback with code evidence: existing callers pass no `--resolution` (`document_review_loop_prompts.md:70`; `commands/spec-panel.md` has no `resolution`), so that fallback would leave the reproduced one-valid-block-of-N defect (D-2) open for every existing caller. A's Round 2 came first and did not answer this. Mark this change in the merged text as "proposed by B's Round 2, not answered by A".
- **Integration point**: Required content: `requested = max(len(resolution.reviewers), len(--report))`; with no resolution, enforce against `len(--report)` as a lower bound and print a warning that absent reviewers are not counted (single-report re-reviews are unaffected because `min(2, 1) = 1`); the loop prompt (`src/superclaude/rules/prompts/document_review_loop_prompts.md` and its `plugins/superclaude/rules/prompts/` mirror) must always pass `--resolution`, and say "re-run only the missing reviewers once; if the quorum is still not met, stop and escalate to the user"; the retry bound is prose only and the text must say so; D-2 is closed for callers that supply reports for every dispatched reviewer, and the variant where a reviewer wrote no file is closed only when the coordinator passes `--resolution`. State the formula exactly as the advocates agreed it, and add the sentence that the agreed formula does not mention `skipped_slots` (see change 11, INV-007).
- **Risk**: Medium. Single-advocate-verified mechanism; the open HIGH invariant INV-007 concerns exactly this formula.

### Change 4: Recorded data, no outcome-bearing flags (from Variant B's Round 2 change to A's bullet 2)
- **Source**: Variant A section 2.1 (round entry gains `requested`, `resolved`, `completion`; single-reviewer findings are display fields); Variant B section 2.1 item 2; `round2-advocate-A.md` Hybrid bullet 2; `round2-advocate-B.md` bullet 2 evaluation and Counter-hybrid term 5; diff points C-001, C-012.
- **Target**: Base section 2.1 (replace the round-entry and cluster-display bullets).
- **Rationale**: Both advocates accepted recording non-outcome data. B showed from code that v1 ledger rows have no `support` or citation-gate result (`findings.py` has no such symbol), that most flags are derivable offline from stored rows (`ledger.py:86-90, 172-179`), that the Reviser reads rendered text (`ledger.py:429-435, 473`) so a rendered flag is not "non-outcome", and that the table header is pinned (`test_review_ledger.py:451`). A had proposed row flags and had no chance to reply.
- **Integration point**: Required content: round entries gain `requested`, `complete`, the quorum result, per-reviewer requested model id (already stored, `ledger.py:141-149`) and a vendor class, labelled "requested, not served"; no new row columns and no change to the rendered merged report; the evidence-gate analogue (`span is None`), `confidence` and member-level blocking disagreement are computed by the replay script from stored rows; `support` and the snapshot-citation gate wait for findings-v2 in the ledger (slot C-01); single-reviewer findings are kept and marked unconfirmed in the offline analysis, never discarded. Record in the residual list (change 14) that A proposed rendered flags and B proposed none.
- **Risk**: Medium. Disputed mechanism; adopted on code evidence.

### Change 5: Named modules (from Variant A, with B's reflect note)
- **Source**: Variant A section 2.2; Variant B section 2.2 and `round2-advocate-B.md` W4; `round2-advocate-A.md` R9 and Hybrid bullet 9.
- **Target**: Base section 2.2 (keep; edit the reflect bullet and add one sentence).
- **Rationale**: C-007 Hybrid 55%, C-004 A 65%. Both advocates keep `derive_verdict`, the 36 tests and the 42-contract replay untouched.
- **Integration point**: Keep spec-review, tasklist/workflow, PR-review and rf-qa bullets; change the spec-review bullet from "one-valid-of-three PASS (D-2) becomes DEGRADED" to "becomes a merge-time refusal (change 2)". In the reflect bullet, delete the sentence beginning "Note for the debate" and move its content into the evidence section as a labelled finding; add: "At floor 2, `degrade` would also pass `test_i3` and the FX7 witness; reflect keeps `visible` until the deferred human decision at `ensemble.py:762-764` is made" (A K4). Add one sentence: Variant B's four consumer-read contract names (`confidence_calibrated`, `evidence_validator_ran`, `reviewer_cards`, `calibrator_diversity`) need a producer, which is a reflect-module concern outside C-03 (both advocates agreed).
- **Risk**: Low.

### Change 6: Exit codes (from Variant A, modified by both Round 2 advocates)
- **Source**: Variant A section 2.3; `round2-advocate-A.md` Hybrid bullet 6; `round2-advocate-B.md` bullet 6 evaluation and Counter-hybrid term 4, New evidence 7; diff points S-003, C-006.
- **Target**: Base section 2.3 (replace the last two sentences).
- **Rationale**: A's "new additive DEGRADED ledger exit code" is replaced by a refusal exit code with no new decision value, because `EXIT_BY_DECISION[v["decision"]]` raises `KeyError` on an unknown decision (`ledger_cmd.py:13, 109`; DEBATE-VERIFIED by both advocates).
- **Integration point**: Required content: `ledger verdict` keeps 0/10/11 and gains no decision value; `merge` exits 12 on a quorum refusal and prints a `{"refusal": "quorum_shortfall", requested, complete, invalid}` object with no `decision` key (B's change, because `ledger verdict` would otherwise show the previous round's stored decision); 12 is unused inside `cli/review` (B grep; `sys.exit` values 1, 10, 11) and does not collide with reflect's codes (A's reading of `models.py:34-48`; B did not re-read it, mark that part [UNVERIFIED] by B); any non-zero code is non-PASS. Keep the existing paragraph on the clash between ledger 10/11 and reflect 10/11 and the pins `test_review_cli.py:245, 349, 369`.
- **Risk**: Low to Medium.

### Change 7: `pending`, contested rows and the adjudicated policy (from Variant B, reduced)
- **Source**: Variant B section 2.1 items 1-4, section 4 Endangered, section 5 failure conditions; `round2-advocate-A.md` Hybrid bullet 7; `round2-advocate-B.md` Counter-hybrid terms 6, 7, 12; diff points C-002, C-005, C-012.
- **Target**: Base section 2.1 (new bullet) and section 2.2 (policy registry line).
- **Rationale**: B withdrew `pending` (W1, W2 conceded: a pending-only round has an empty brief, computes PASS at `ledger.py:273-275`, prints "Blocking finding ids: none." at `:487-492`, and `defer` rewrites the stored verdict to PASS at `:356-360`). Both converged: no `pending` state; `adjudicated` exists as a named policy run offline on stored reviewer outputs.
- **Integration point**: Required content: a contested blocking row is a blocking row and fails the round as today; no `pending` state; "contested" for the offline analysis is defined as single-reviewer AND (anchor unresolved OR code gate failed OR members disagree on blocking), and plain single-reviewer is not contested (B term 7); `adjudicated` is a named policy run offline on stored outputs, not in production rounds and not inside `review merge`; promotion needs a pre-registered rule and the transitions nobody has specified (brief entry, exit code, cap accounting, `defer`); if ever promoted, `rejected` is allowed only on a deterministic evidence failure or a quoted re-read, and every rejection is recorded and counted; the adjudicator's served model must differ from the reviewers' served models or the run is recorded as not independently adjudicated; calibration enters only through a separate `calibration_map` keyed by finding id.
- **Risk**: Low. Additive text.

### Change 8: Independence and served model ids (from Variant B, corrected by the debate)
- **Source**: Variant B section 2.1 item 5 and E11, E16; `round1-advocate-A.md` W3 and code log row 16; `round1-advocate-B.md` C3; `round2-advocate-B.md` Counter-hybrid term 12; diff points X-003, A-005.
- **Target**: Base section 2.1 (quorum bullet addition) and section 3.1 (new evidence item).
- **Rationale**: Both advocates agree that the Tier-2 gate counts the configured id: `fallback.py:161-179` reads `worker.model_id`, which `openai_compat.py:468` sets to `self._model`; `model_observed` is only a telemetry column (`review/telemetry.py:364`). Scoring matrix X-003 A 77%, A-005 rejected as an assumption by both.
- **Integration point**: Required content: independence (distinct model ids, vendor class) is recorded as data labelled "requested, not served" now and becomes a quorum predicate only after the transport records `model_observed` (slot C-08); until then "adjudicator or calibrator served by a reviewer's model" is a falsifier, not a gate; B's E11 wording "computed from served model ids" is recorded as wrong.
- **Risk**: Low.

### Change 9: Evidence section corrections (from the debate)
- **Source**: Variant A section 3.1 item 4, section 7; Variant B E7-E10; `round1-advocate-B.md` Strength 5, W5 (A), C-items; `round2-advocate-A.md` R1, R5, New evidence 2; `round2-advocate-B.md` New evidence 1, 3-6; diff point X-004.
- **Target**: Base section 3.1 (edit item 4; add items), section 3.2 (keep), section 3.3 (keep).
- **Rationale**: A conceded that "a PASS on that path rests on defaults" is true only for the pre-supplied-score path and for `merge_method` (`ensemble.py:442-465, 773`), and withdrew it as an argument; both confirmed the reflect verdict also needs convergence >= 0.80 and healthy sub-status (`contract.py:299-326`). B's E7 is correct on that point.
- **Integration point**: Edit item 4 to the narrowed claim and add B's E7 as the reflect fact; add a numbered item stating the traced fact that a Reviser `rejected` fix-map item leaves the row `open` (`ledger.py:340-342`), only `resolved_check` rows clear (`:254-258`), an open row is re-presented every round (`:457-466`) and stays in the brief (`:99-104`), the only exit is the human `defer` (`:350-360`) and `prior` notes cannot clear a row (`:259-272`); add that v1 findings carry no confidence, calibration or support (`findings.py`), that existing callers pass no `--resolution`, and that a refusal records nothing by construction (`merge_cmd.py:109-116`; `test_review_cli.py:448-449`). Tag each `[DEBATE-VERIFIED]` with the debate file.
- **Risk**: Low.

### Change 10: Invariants (from Variant A, with B's table content)
- **Source**: Variant A section 4; Variant B section 4; diff points X-006, C-008.
- **Target**: Base section 4.1 and 4.2.
- **Rationale**: With a union default and an offline adjudicated arm, INV-L holds (X-006 A 55%: B's tension dissolves). B's Endangered risks that survive in the merge are kept.
- **Integration point**: 4.1: INV-A, INV-B, INV-C, INV-D, INV-F, INV-I (narrowed as in change 1), INV-J, INV-K, INV-L stay Preserved; add INV-H (no document text in telemetry) for the recorded data. 4.2: keep the four base items; reword INV-D to include the rewrite of `test_review_ledger.py:376-385` and the unchanged pins (`defer` `:396-405`, exit 0/10/11); add B's risks that remain if the adjudicated policy is ever promoted: INV-I (an adjudicator that rejects a true blocker is a new fail-open path, HIGH), INV-G (adjudicator and debate agents must be read-only), INV-J (`pending` must never become a third severity).
- **Risk**: Low.

### Change 11: Open invariants left unaddressed by the debate (new section 4.3, from `invariant-probe.md`)
- **Source**: `invariant-probe.md` (17 findings; 12 UNADDRESSED) and `round2.5-fault-finder-raw.md`.
- **Target**: Base section 4, new subsection "4.3 Left unaddressed by the debate".
- **Rationale**: Convergence is BLOCKED_BY_INVARIANTS (INV-006, INV-007 HIGH UNADDRESSED). The debate did not resolve them and standard depth has no Round 3, so the merged document must carry them as open, not fix them.
- **Integration point**: A table with columns ID, Category, Assumption, Severity, one-sentence evidence, copied from `invariant-probe.md` for the 12 UNADDRESSED rows, HIGH first (INV-006, INV-007), then MEDIUM (INV-001, 002, 003, 004, 005, 009, 010, 016), then LOW (INV-012, 013). Below it list the 5 ADDRESSED findings (INV-008, 011, 014, 015, 017) with the residual each leaves (INV-014: the refusal closes D-2 only for `complete < floor`; INV-017: caveat of change 3). State that no resolution is proposed for any of them here.
- **Risk**: Low. Copy, no new claims.

### Change 12: Test and measurement plan (from Variants A and B, consolidated)
- **Source**: Variant A section 5; Variant B section 5; `round2-advocate-A.md` Hybrid bullet 10, 11; `round2-advocate-B.md` bullet 10, 11 evaluation and Counter-hybrid terms 10, 11; diff point C-011.
- **Target**: Base section 5 (replace).
- **Rationale**: C-011 Hybrid 65%. B showed A's "2-of-3 support flag shown, non-gating" arm cannot be computed from stored v1 data (support is None) and that rendered flags make that arm a treatment, not a control.
- **Integration point**: Code tests: quorum matrix over requested N in 1..5 and the five completion states (below floor in a `degrade` profile gives refusal, never PASS; seeded from D-2: 4 requested, 1 valid); monotonic property (adding a failed or timed-out reviewer never turns a non-PASS into PASS); refusal leaves ledger JSON byte-identical (pattern `test_review_ledger.py:345-361`, `test_review_cli.py:448-449`); CLI D-2 with four `--report` args, one valid, three broken, no resolution, exit 12 and no files; CLI with a four-reviewer `--resolution` and one `--report`, exit 12; replacement-reviewer id counts toward `complete`, not `requested`; rewrite `test_review_ledger.py:376-385` (delete the "legacy-mode copy" A proposed, per B); keep the `defer` pin (`:396-405`) and the 0/10/11 exit pins unchanged; add an exit-12 test; regression gates: `test_verdict_mapping.py` (36), `scripts/reflect_verdict_replay.py` (0 differences), the two shortfall pins. Measurement: arms computable from stored v1 data (union; union minus `span is None` rows; union requiring two reviewers on a row; adjudicated only on a new run); pre-registered decision rule before the first run; TPR and FPR per rule; held-out package; measures: defects found, real blocking found, wrong blockers per row, control defects found, reviews-to-cap (with the C-02 exit present) and escalate-at-cap rate. Falsifiers: for the union default (wrong blockers drive escalate-at-cap above the filtered arms with no recall gain); for adjudication (B's (a) confirms essentially every contested blocker, (b) rejects any real blocker, (c) adjudicator served by a reviewer's model, (d) contested set so large the validator is the verdict); for the floor (2-of-3 indistinguishable from 3-of-3 on defect misses). State B's replay limit: E2 holds no validator output, so the replay measures contested volume, not adjudication quality.
- **Risk**: Low.

### Change 13: PR-review and rf-qa effects, and the objection (from Variants A and B)
- **Source**: Variant A sections 6 and 7; Variant B section 6; `round2-advocate-A.md` R2, R1, Hybrid bullet 8; `round2-advocate-B.md` bullet 8 evaluation, New evidence 5; diff points C-009, C-010.
- **Target**: Base sections 6 and 7.
- **Rationale**: C-009 Hybrid 56%, C-010 Hybrid 57%. A conceded the union's unit cost is "to the cap" not "one fix cycle", and that support, disputed and confidence change no outcome so FX-10 is priced, not addressed.
- **Integration point**: Section 6: keep A's PR-review and rf-qa text; replace "DEGRADED visible so the module can re-dispatch" with the refusal wording; add B's note that v1 ledgers cannot feed an rf-qa confidence gate until findings-v2 reaches the ledger (slot C-01) and that single-reviewer re-review has `requested = 1`; add B's claim limit (a union of four automated reviewers passed 41.5% of tests built from human reviews; web-01 D4, tag [UNVERIFIED]); keep the code-backed evidence gate before findings enter a fix round (shared). Section 7: keep the objection (FX-10) and edit the answer: replace "a wrong blocker costs at most one fix cycle" with "to the cap, then a human decision", state the precondition that the union is the cheap-error side only while a Reviser-rejected row has a non-human exit (slot C-02 dependency; `prior` notes are history only), and state that the default prices FX-10 and does not satisfy it. Keep the remaining answer points (calibrator unmeasured; k-of-n correlated voters; agreement and verification kept apart; policy swappable by name).
- **Risk**: Low.

### Change 14: Resolution status and residual disagreements (new section 8, from the debate record)
- **Source**: `debate-transcript.md` Scoring Matrix and Convergence Assessment; `base-selection.md`.
- **Target**: New final section "8. Resolution status of this merge".
- **Rationale**: The merged document must show what is decided, what is hybrid, and what remains open.
- **Integration point**: Required content: the base selection and scores quoted from `base-selection.md` (A 0.9007, B 0.8590, margin 4.17%, tiebreaker level 1, A 9 points, B 3, 8 Hybrid, 1 Neither); convergence 25 of 26 points (96%) and status BLOCKED_BY_INVARIANTS (INV-006, INV-007 HIGH UNADDRESSED); A-003 label split (A REJECT, B QUALIFY) with substance converged; the four residual mechanism disagreements (rendered flags, "not measured" fallback versus lower-bound enforcement, shadow arm location, refusal JSON key) with the choice made and the reason; dependencies on other slots (C-02 clearing, C-01 findings-v2 in the ledger, C-07/C-08 retry and served model id).
- **Risk**: Low.

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|------------|-------------------|---------------------------|
| C-001, X-001 | `adjudicated` as the default for panels of 2 or more | Variant B conceded (Round 1 C1) that no measurement shows adjudication beating the union; the merge keeps `union` as default and the adjudicated policy as an offline arm. |
| C-002 | Core-owned adjudication stage reusing the legacy chain, callable from the core | The chain is skill-orchestrated agents, not a stage a one-call deterministic `review merge` can host (`merge_cmd.py:71-118`); Variant B conceded W5. |
| C-005 | `pending` / `uncalibrated` row state that blocks PASS without entering the brief | No brief entry, verdict, exit code or `defer`-safe place (`ledger.py:99-104, 273-275, 356-360, 487-492`); Variant B withdrew it. |
| C-003, X-003 | Served-model-id quorum predicate now | Not available on the shipped path (`openai_compat.py:467-468`); recorded as data until `model_observed` exists (slot C-08). |
| C-004 | "DEGRADED never PASS for a partial panel" as common ground for every module | Contradicted for reflect by `ensemble.py:755-770` and two pins; holds only in `degrade` profiles (X-002 A 73%). |
| C-006 | A new DEGRADED decision value / additive ledger exit code | A new stored decision value raises `KeyError` at `ledger_cmd.py:109`; replaced by a refusal and exit 12. |
| C-007 | Core-populated `confidence_calibrated`, `evidence_validator_ran`, `reviewer_cards`, `calibrator_diversity` | A reflect-module concern; both advocates moved it out of C-03. |
| C-012 (partly) | Calibrator in the default path | The calibrator is unmeasured (6 of 15 combo runs without a class, B E16 [UNVERIFIED]); calibration channel exists only as separate data. |
| C-001 (A's own R2 bullet 2) | Rendered evidence-gate, support, disputed, contested columns on ledger rows | v1 rows carry no support; the Reviser reads rendered text; the table header is pinned (`test_review_ledger.py:451`); replaced by round-entry data and offline flags (change 4). |
| C-011 (A's own R2 bullet 7) | Adjudicated arm running in shadow inside production rounds | The ledger CLI has no write path for it and it costs a model call per round (`ledger_cmd.py`); moved offline. |
| C-003 (A's own R2 bullet 4) | "Quorum not measured" fallback when no `--resolution` | Leaves D-2 open for every existing caller; replaced by lower-bound enforcement (change 3), single-advocate-verified. |
| C-011 (A's own R2 bullet 10 v) | Legacy-mode copy of `test_review_ledger.py:376-385` | Quorum is a merge-time gate, so the pin is rewritten, not copied (B bullet 4, 10d). |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|----------|------|------------------|----------|
| 1 | Low | Overclaim wording left in | Restore base section 1 and 4.1 text |
| 2 | Medium | Mechanism text inconsistent with exit-code and refusal text | Revert to base 2.1 bullets (DEGRADED outcome) and flag |
| 3 | Medium | Formula for `requested` stated differently from the advocates' agreed text | Remove the bullet; record as open in section 8 |
| 4 | Medium | Disputed mechanism misreported as agreed | Restore base bullets and list both mechanisms in section 8 |
| 5 | Low | Reflect statements drift from the pins | Restore base 2.2 reflect bullet |
| 6 | Low-Medium | Exit-12 claim stated more strongly than verified | Mark `models.py` non-collision as A-only |
| 7 | Low | `adjudicated` misread as production stage | Remove the bullet |
| 8 | Low | Served-id wording regresses | Restore B's quoted wording with a [CODE-CONTRADICTED] tag |
| 9 | Low | Evidence tag wrong | Remove the tag, keep the claim as [UNVERIFIED] |
| 10 | Low | Invariant list incomplete | Restore base 4.1/4.2 |
| 11 | Low | Open invariants dropped or softened | Re-copy from `invariant-probe.md` |
| 12 | Low | Test list contradicts a pin | Restore base section 5 |
| 13 | Low | Objection answer weakened | Restore base section 7 and add the correction as a note |
| 14 | Low | Scores or status misquoted | Re-copy from `base-selection.md` and the transcript |

## Review Status
- [x] Auto-approved (default)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-11-14 (orchestrator, `--interactive` not set)
