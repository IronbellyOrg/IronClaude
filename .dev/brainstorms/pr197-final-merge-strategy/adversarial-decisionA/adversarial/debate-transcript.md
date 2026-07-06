# Adversarial Debate Transcript — Decision A (3 options, deep, 3 rounds)

## Metadata
- Depth: deep · Rounds completed: 3 + invariant probe (Round 2.5)
- Convergence threshold: 0.80 · Final convergence: ~0.86 (CONVERGED after R3)
- Focus: anti-self-confirmation-strength, diversity-guarantee, robustness, enforceability, merge-cost
- Advocates: A=exclusion (reliability lens), B=instance-level (analyzer lens), C=hybrid (architect lens) — independent subagents
- Convergence was BLOCKED after R2 by HIGH invariants INV-201 + INV-207 → forced Round 3 → both ADDRESSED.

## Round 1 — opening statements (summary)
- **A:** representational bias lives in the weights (§1:29 Mehta; §1:33 mechanism #1); only exclusion forces a weight-disjoint reviewer; #197 concedes same-class shares the stack; loud-degrade > silent same-class; smallest merge.
- **B:** the §1 failure is the *instance carrying formation context* → fresh spawn defeats it; exclusion only shrinks the frame and can KILL the ensemble on collision; master's resolver fails open via commit-author heuristic; deleted telemetry was non-stable.
- **C:** only C covers BOTH failure axes (context floor + weight-level hard preference); removes A's tier-collapse-on-a-guess and B's silent same-class pass; concedes C is not built.
- Cross-concessions already in R1: A says adopt B's formation-context guarantee regardless; B says class diversity has independent value ("C's strongest claim over B").

## Round 2 — rebuttals (summary)
- **A:** decorrelation argument — 3 same-class reviewers ≈ correlated votes, so a T1 pass on a disjoint class can beat a same-class T2. Concedes C dominates on merits *once built*; A's edge is merge-readiness. Recommends ship-A-now → A→C.
- **B:** concedes two defects of pure #197 — must RETAIN `t2_model_class_diversity` telemetry (over-deletion of observability is indefensible) and `--executor-model` should WARN not silently ignore. Narrows B to "correct, lowest-risk shippable now"; concedes C dominates if built.
- **C:** **DECOMPOSITION_VERDICT — C is NOT a merge blocker**; ship floor now + retain dormant scaffolding + fast-follow gating. (This claim is later falsified by INV-201.)

## Round 2.5 — invariant probe
See `invariant-probe.md`. Two HIGH findings (INV-201 dormant-scaffolding-false-to-tree; INV-207 sufficiency-depends-on-funding) blocked convergence and forced Round 3.

## Round 3 — final arguments (summary)
- **A:** probe vindicates A near-term; near-term ballot is binary A-or-B (INV-201); INV-207 settles it for A (safer-by-default). Final: **merge A now; fund A→C next.** Reservation: if tier-collapse fires more than rarely, prioritize the fast-follow.
- **B:** **A if fast-follow unfunded** (concedes INV-207); B only if funded same-cycle + telemetry retained + `--executor-model` warns. Reservation: A's resolver hit-rate (commit-author fail-open) is unmeasured — "enforced-at-merge" is itself probabilistic.
- **C:** **REVERSED to near-term A.** From A the fast-follow is subtractive editing of *existing graded machinery*; from B it is re-authoring into hostile regions. C remains the end-state, non-blocking. Reservation: A's log-heuristic fail-open is live until the fast-follow lands.

## Scoring matrix (per diff point)

| Diff point | Winner | Confidence | Evidence |
|-----------|--------|-----------|----------|
| C-001 failure mode targeted | C (concept) / A (near-term) | 80% | weight-level miss is real (unanimous); A defends it now, C defends both axes as end-state |
| C-002 diversity enforcement | A (near-term) | 78% | exclusion+backfill forces weight-disjoint reviewer in rich-alias env; B soft-preference can pass same-class |
| C-003 tier-on-collision | C (end-state) | 72% | never-collapse is correct end-state; A's collapse is rare here but real → fast-follow removes it |
| C-004 graded invariant | A | 82% | A retains a graded, observable invariant; B deletes it (conceded defect); C conditions it (end-state) |
| C-005 merge cost / path-to-C | A | 85% | INV-201: path to C is subtractive from A, re-authoring from B (C-advocate reversal) |
| X-001 does freshness defeat §1 | A | 75% | freshness defeats context bias only; weight-level bias persists (B + #197:629 concede) |
| X-002 collapse: feature or bug | C | 70% | bug to collapse on a guess (loud-warn-stay-T2 is better) → fast-follow item, not a reason to pick B |
| X-003 deleted telemetry load-bearing | A | 80% | INV-201: it was a live enforcer, not dead telemetry |
| X-004 heuristic decisive vs A | split → MEDIUM open | 55% | frontmatter reliable on primary path; bare-heuristic hit-rate unmeasured (B's standing reservation) |

## Convergence assessment
- Resolved: 8 / 9 core points. Unresolved (MEDIUM, non-blocking): X-004 — the empirical resolver hit-rate of the commit-author fallback.
- Unanimous: C is the right END-STATE; C is NOT a merge blocker; the weight-level miss is REAL; pure #197 over-deleted observability.
- Majority (A+C, B-conditional): **near-term merge = Option A** (keep master's exclusion), with a **funded A→C fast-follow**.
- Status: **CONVERGED** (~0.86 ≥ 0.80; both HIGH invariants ADDRESSED).
