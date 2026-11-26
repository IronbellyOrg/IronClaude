# Base Selection

## Quantitative Scoring (50% weight)

Computed by script over the blind copies (`blind/variant-A.md`, `-B.md`, `-C.md`). Metrics and weights as in the protocol.

| Metric | Weight | A | B | C |
|---|---|---|---|---|
| Requirement coverage (14 markers from the seed brief) | 0.30 | 1.00 | 1.00 | 1.00 |
| Internal consistency (no intra-variant contradiction found) | 0.25 | 1.00 | 1.00 | 1.00 |
| Specificity ratio (concrete vs vague indicators) | 0.15 | 1.00 | 1.00 | 1.00 |
| Dependency completeness (ids referenced vs defined) | 0.15 | 1.00 | 1.00 | 1.00 |
| Section coverage (8 H2 sections each) | 0.15 | 1.00 | 1.00 | 1.00 |
| **quant_score** | | **1.00** | **1.00** | **1.00** |

**Limitation, stated plainly:** the quantitative layer is saturated. All three variants score 1.00 on every metric, so it does not separate them. The requirement markers are loose keyword matches (for example `public`, `error`), so a full match proves a mention, not a correct requirement. The base choice therefore rests on the qualitative layer and the tiebreaker rules.

## Qualitative Scoring (50% weight): additive binary rubric

Two independent passes (order A, B, C and order C, B, A) scored 30 criteria per variant with an evidence citation for each; full lines are in `rounds/qual-pass1.md` and `rounds/qual-pass2.md`.

| Dimension | A | B | C |
|---|---|---|---|
| Completeness | 5/5 | 5/5 | 5/5 |
| Correctness | 5/5 | 3/5 | 5/5 |
| Structure | 5/5 | 5/5 | 5/5 |
| Clarity | 5/5 | 4/5 | 2/5 |
| Risk Coverage | 5/5 | 4/5 | 4/5 |
| Invariant & Edge Case Coverage | 4/5 | 5/5 | 4/5 |
| **Total** | **29/30** | **26/30** | **25/30** |

### Position-bias log: 5 disagreements out of 90 criterion-variant pairs

| Criterion | Pass 1 | Pass 2 | Final | Reason |
|---|---|---|---|---|
| A E1 (collection boundaries) | NOT MET | MET | NOT MET | T-06 covers odd and even median counts only; no empty, single or maximum collection case is named |
| A K1 (no invented claims) | MET | NOT MET | MET | `tests/troubleshoot/` exists in the repository (checked with `ls`) and is cited in the issue summary; not an invented path |
| B E3 (guard condition gaps) | NOT MET | MET | MET | T-04 (gate runs before the environment read), FR-006 and T-13 (alias rejected) are real guard conditions |
| C K1 (no invented claims) | NOT MET | MET | MET | "The lead has already approved" matches the seed brief's recorded owner decision; the pinned revision and blob match the source |
| C S4 (navigation aids) | NOT MET | MET | MET | The rubric text given to both scorers counts ids as navigation aids; C has FR ids (weak, noted) |

Verdicts changed by re-evaluation: 5 of 5 resolved from the evidence above (no third scoring pass was run).

### Edge Case Floor Check

A 4/5, B 5/5, C 4/5. All are at or above the 1/5 floor; all are eligible.

## Combined Scoring

variant_score = 0.50 x quant + 0.50 x qual

| Variant | quant | qual | combined |
|---|---|---|---|
| A | 1.0000 | 0.9667 | 0.9833 |
| B | 1.0000 | 0.8667 | 0.9333 |
| C | 1.0000 | 0.8333 | 0.9167 |

Margin A over B: 0.0500 (exact fraction 1/20). The tiebreaker applies when the margin is **strictly below** 0.05. The margin is exactly 0.05, so the tiebreaker does NOT apply by the protocol's text. This is a knife-edge result and is flagged for a person to see.

For information only (not used): had the tiebreaker applied, level 1 (debate performance, points won outright after Round 2) would favour B: B won S-001, S-002, S-003, C-009, X-001, A-005 outright (6); C won C-007, A-002, A-004 (3); A won C-001 (1); the other 10 points were MERGE. All three advocates named B's structure as the frame to merge into.

## Selected Base: Variant A (blind label A)

- Selection rationale: highest combined score (0.9833 vs 0.9333 vs 0.9167) on the protocol's rule; strongest on correctness (5/5), completeness and clarity.
- Strengths to preserve: label basis and blind labeller (FR-003, FR-004); blind table applier with cue records (FR-011); seen-by-table flag with split report (FR-005); paired breakdown (FR-020); latency basis (FR-019); RUN_INVALID states (section 4); test cases T-01 to T-10.
- Strengths to incorporate from non-base variants: B's no-default rule file, table answers stored before any Jev call, corpus check in the scorer, append-only run ids with offline rescoring (marked non-decisional), one-job-per-file folder and README, tests linked to FRs, whole-run spend estimate; C's comparison-scope gate, persisted gate result, dated event log, verbatim owner words beside the interpretation, per-request spend bound, recorded issue updates, local versus remote measurement labels.
- Weaknesses of the base to fix: no-retry rule (X-001), spec-fixed error scoring (X-002), no table-before-Jev ordering, no event log, folder name not matching `.dev/README.md`, no tests linked to FRs, six HIGH invariant gaps from the probe (INV-001, 002, 003, 013, 014, 017).
