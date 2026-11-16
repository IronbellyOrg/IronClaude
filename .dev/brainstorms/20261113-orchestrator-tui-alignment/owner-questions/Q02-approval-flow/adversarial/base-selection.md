# Base Selection

Scoring was done inline by the orchestrating worker (one evaluator), not by spawned scorers. The reverse-order pass was done by the same evaluator, so position-bias mitigation here is weaker than the protocol intends. The source requirements are the owner's Q2 answer (two channels, the race, single source or safeguards) and failure modes F1 to F10.

## Quantitative Scoring (50% weight)

| Metric | Weight | A (V1) | B (V2) | C (V3) | Basis |
|---|---|---|---|---|---|
| Requirement coverage | 0.30 | 0.90 | 0.95 | 0.85 | All cover F1 to F10 and both channels; A covers the "single source" option only as safeguards; C serves the Orca channel only as a proxy (X-002) |
| Internal consistency | 0.25 | 0.95 | 0.95 | 0.90 | A: the "no single point of failure" claim sits beside an unsolved self-approving actuator; B: the overstated mailbox claim (V2 concession 2); C: X-002 |
| Specificity ratio | 0.15 | 0.88 | 0.90 | 0.88 | All name files, functions, markers, keys and thresholds |
| Dependency completeness | 0.15 | 1.00 | 1.00 | 0.95 | C's key is stated two ways (event id; per plan version) |
| Section coverage | 0.15 | 1.00 | 1.00 | 1.00 | All eight required sections |
| **Quant score** | | **0.940** | **0.958** | **0.905** | |

## Qualitative Scoring (50% weight)

| Dimension | A | B | C | Deciding evidence (Claim, Evidence, Verdict condensed) |
|---|---|---|---|---|
| Completeness | 4/5 | 5/5 | 4/5 | All define invariant, flows, failure table, build delta; A and C omit an acknowledgement step, B has `ack <approval-id> applied|refused` |
| Correctness | 3/5 | 4/5 | 3/5 | A: reverses D2/NG-2 and keeps self-approval; B: mailbox overstatement and the person-prompt veto collision (both found in debate); C: X-002 and the two-way key |
| Structure | 5/5 | 5/5 | 5/5 | Identical skeleton |
| Clarity | 4/5 | 4/5 | 4/5 | All plain; each relies on F-ids defined in the shared file |
| Risk coverage | 4/5 | 5/5 | 4/5 | All name residual forgery; B also names that the helper must enforce the one-row rule mechanically because the coordinator is an LLM |
| Invariant and edge-case coverage | 3/5 | 4/5 | 3/5 | B: stale-version rejection, never-auto-restart, per-issue lock against two coordinators; A: two-store gap; C: duplicate label event behaviour unverified |
| **Qual score** | **23/30 = 0.767** | **27/30 = 0.900** | **23/30 = 0.767** | |

Edge-case floor: all variants at or above 1/5; all eligible.

## Position-Bias Mitigation

Pass 1 order A, B, C; pass 2 order C, B, A, by the same evaluator. No verdict changed between passes. Disagreements found: 0. Limitation: one evaluator.

## Combined Scoring

| Variant | Quant x 0.5 | Qual x 0.5 | Final |
|---|---|---|---|
| A (V1) | 0.470 | 0.383 | 0.853 |
| B (V2) | 0.479 | 0.450 | **0.929** |
| C (V3) | 0.453 | 0.383 | 0.836 |

Margin B over A: 7.6 points; no tiebreaker. Debate points agree (B 9, C 3, A 0).

## Selected Base: Variant 2 (proposal B, one actuator)

**Rationale.** B is the only variant that gives the owner a single source of consequential instructions without reopening the watcher decisions D2 and NG-2 and without an internal contradiction, and all three advocates recommended it as the base when asked to be neutral.

**Strengths to preserve.** One actuator; the locked approval-record helper; the hash-bound approval line with no bare `approved`; the watcher untouched; ack; stale-version rejection; never auto-restart.

**Strengths to incorporate.** From C: the read-only stage-status verb; label removal as the revocation signal; the label event id as evidence in the row; a public marker on the issue so a lost ledger cannot restart work. From A: build the helper on the watcher's existing lock and fsync store code. From the debate: correct the mailbox claim; resolve the person-prompt veto; new stage predicates; key on (issue, stage, plan version); dead-session rule; plan-version definition.
