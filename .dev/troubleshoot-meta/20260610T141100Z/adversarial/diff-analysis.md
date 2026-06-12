# Diff Analysis — Blind Compare of variant-A / variant-B / variant-C

## Metadata

| Field | Value |
|---|---|
| Generated | 2026-06-10 |
| Variants compared | 3 (variant-A, variant-B, variant-C) |
| Stage | Step 1 — diff-analysis (blind) |
| Total differences | 38 (S=7, C=9, X=8, U=6, A=8) |
| Structural diffs (S) | 7 |
| Content diffs (C) | 9 |
| Contradictions (X) | 8 |
| Unique contributions (U) | 6 |
| Shared assumptions (A) | 8 |
| total_diff_points | 30 (nS+nC+nX+nA = 7+9+8+8 +... see note) |

> Note: convergence denominator total_diff_points = nS+nC+nX+nA = 7+9+8+8 = **32**. (U is excluded from the contested-point denominator per pipeline convention; reported separately = 6.)

---

## Structural Differences

| # | Area | Variant A | Variant B | Variant C | Severity |
|---|---|---|---|---|---|
| S-001 | H2 section count / model | 7 numbered H2 (Executive Verdict → Bottom Line), efficacy-audit organization | 7 numbered H2 (Executive verdict → Blunt bottom line), efficacy-audit organization | 14+ H2, gate-approval / G1-readiness organization (Executive verdict, Frozen escape set, Root causes, Remediation, Refactor spec, Halt note, Recommendation) | High — L2 |
| S-002 | Report framing/title | "Meta-Efficacy Report — Whack-a-Mole Episode" (retrospective audit) | "Final Efficacy Report: Debug/Task/Reflect Stack" (retrospective audit) | "Final Report Pre-G1 — Troubleshoot Meta-Investigation" (forward gate-approval doc) | High — L2 |
| S-003 | Escape-set table position | §2 mid-doc, 8-row M1–M6+F-A+F-B with root-cause + surfaced-by columns | §2 prose-per-miss M1–M7 (no single dense table) | §"Frozen canonical escape set" 5-row E1–E5, two columns (escaped failure / general miss) | Medium — L2 |
| S-004 | Theatre scorecard presence | Present as dedicated scorecard table (5 rows, ratios) | Present as dedicated scorecard table (5 rows, ratios) | ABSENT — only a single global "41%/59%" line, no per-stage table | High — L3 |
| S-005 | Would-have-caught matrix | Present (§5, 8-row matrix, wave attributions) | Present (§5, 7-row matrix) | ABSENT — no per-miss caught matrix (implementation G1-pending) | High — L2 |
| S-006 | Rollback-replay section | Present (§6, table, round 2, 100%) | Present (§6, round 2, 100%) | ABSENT — replay explicitly "pending G1 approval" | High — L2 |
| S-007 | Systemic-cause hierarchy depth | 3 causes (SC-1..3) each → 1 remediation (R-1..3), 1:1 mapping | 4 causes (SC1..4) → 4 remediations (4.1–4.4) | 5 root causes (RC1..5) → 7 remediations (1–7), N:M mapping | Medium — L2 |

---

## Content Differences

| # | Topic | A Approach | B Approach | C Approach | Severity |
|---|---|---|---|---|---|
| C-001 | Executive verdict tone | "almost pure theatre for the registry miss class"; nuanced "theatre ≠ did nothing" | "mostly theatre"; "failed as a preventive quality system" | "real value but mis-targeted"; deliberately less absolute (41% value) | Medium — L2 |
| C-002 | Theatre ratio (aggregate) | 16 obligations / 1 catch = 6.25%; stack ratio ≈0.94 | 33 expected / 1 catch = 3.0%; theatre 97.0% | 41% value / 59% theatre (no obligation-count basis) | High — L3 |
| C-003 | Escape-set size & IDs | M1–M6 + F-A + F-B = 8 items | M1–M7 = 7 items (F-A→"M7"; no F-B as miss) | E1–E5 = 5 items (no F-A/F-B, no M6/M7 separation) | High — L3 |
| C-004 | Per-stage scoring denominators | should_have_caught: 2/4/3/4/3 per stage | should_have_caught: 6/6/7/7/7 per stage | no per-stage denominators at all | High — L3 |
| C-005 | The single adversarial catch | F-A, credited to "human PR reviewer downstream of adversarial pass," NOT debate | M7, credited to "PR review / adversarial review activity during #154" (debate-adjacent) | E-level: no per-stage catch credited; adversarial value = E5 wrong-diff/base trap (sc:reflect, not adversarial) | High — L3 |
| C-005b | M4 fix commit identity | "REAL FIX = local b97c9960; PR #158 does NOT exist in git" (explicit) | "local / PR #158-equivalent commit b97c9960" (treats #158 as equivalent) | E4 maps to PRD/generic evaluator divergence; no commit SHA / #158 claim | High — L3 |
| C-006 | M6 / resume fix status | "UNCOMMITTED — not in git at all" | "no committed fix found in supplied evidence" | No distinct M6; resume mismatch not separately frozen as escape | Medium — L3 |
| C-007 | Remediation framing | 3 issue-agnostic remediations, deep generality (TDD/wet-lab/chaos analogies), cost+residual per item | 4 boundary-oracle remediations, mechanism bullets, lighter generality | 7 reusable closure controls + 6-wave H0–H5 protocol spec (most operational/prescriptive) | Medium — L2 |
| C-008 | Evidence basis claimed | git commits 7601ad25→07cb149f, git-forensics F-A/F-B, replay round 2 | PR/commit refs + git grep, replay round 2 | base commit 94d5baa0, G0/Phase-0 evidence, NO replay (pre-implementation) | Medium — L3 |

---

## Contradictions

| # | Point of Conflict | A Position | B Position | C Position | Impact |
|---|---|---|---|---|---|
| X-001 | Who/what made the one pre-runtime adversarial catch | "single catch (F-A) was actually delivered by the **human PR reviewer downstream of the adversarial pass**, not by the debate itself" (line 11/21) | adversarial "caught only M7"; M7 surfaced by "PR review / adversarial review activity during #154" — credits the adversarial/review surface, not an external human tail | Neither — C credits sc:reflect with the distinct catch (E5 wrong-diff/base), and does not score adversarial as catching anything | High — L3 (attribution of the lone catch directly opposes between A and B) |
| X-002 | Theatre ratio / preventive catch rate | 6.25% catch (1/16), stack theatre ≈0.94 | 3.0% catch (1/33), theatre 97.0% | 59% theatre / 41% value — materially lower theatre figure | High — L3 (same episode, three incompatible quantifications) |
| X-003 | Escape-set cardinality & completeness | 8 items (M1–M6 + F-A + F-B) | 7 items (M1–M7) | 5 items (E1–E5) | High — L3 (the denominator of "what should have been caught" differs by set membership) |
| X-004 | Is F-A a "miss" or a forensic rider | F-A is a git-forensics finding caught by EXTERNAL human review (a catch, not a stack miss); F-B is bisection-hygiene, "not a pipeline bug" | F-A promoted to M7, counted as a stack-scope miss the adversarial DID catch | C folds completion-substring issue into E2/E3 mechanism; no standalone F-A/M7 | High — L3 (A: external-caught forensic; B: in-scope miss that was caught) |
| X-005 | Does PR #158 exist | "seed's 'PR #158' does not exist in git history — confirmed; only b97c9960" (line 42) | "local / PR #158-equivalent commit b97c9960" — treats #158 as a real/equivalent ref | Silent (no #158 reference) | High — L3 (falsifiable git-history claim; A denies, B asserts equivalence) |
| X-006 | Scope of the report | Pure retrospective efficacy audit; ends at "would it have caught all" + irreducibility analysis | Pure retrospective efficacy audit + refactor + replay | G1 gate-approval document: "G1-ready, implementation pending approval"; refactor is a SPEC awaiting sign-off, not a completed/replayed change | High — L2 (efficacy-audit vs gate-approval scope — different deliverable contract) |
| X-007 | Is the refactor implemented & validated | Refactor done, rollback-replay run, 100% round 2 (8/8) | Refactor done, rollback-replay run, 100% (7/7) | Refactor NOT implemented; "Implementation and backtest are pending G1 approval"; explicit HALT | High — L3 (A/B assert a completed validated refactor; C asserts it is not yet built) |
| X-008 | Coverage achievability by static analysis | "yes for static coverage, with caveat — not all in a single purely static shot"; 3 misses need execute/simulate waves | "Yes... provided run in production-facing pipeline-health mode and gates enforced not waived" | Makes no 100%/coverage claim; defers to post-G1 backtest | Medium — L3 (A and B both claim 100% but disagree on the static-vs-runtime caveat framing; C makes no claim) |

---

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---|---|---|
| U-001 | A | Patch-relative vs baseline-relative distinction + three dedicated patch-relative waves (4.7 Patched-Shadow Re-Sweep, 4.8 Fix-Patch Adversarial Linter, 6.5 Commit-Scope Auditor) closing M3/F-A/F-B | High — L3 |
| U-002 | A | "Negative-witness admission" / falsifiability discipline (revert-and-rerun, positive+negative witness pair) as a gate property, with cross-domain generality (TDD red-green, wet-lab assay controls, chaos engineering) | High — L3 |
| U-003 | A | Explicit irreducibility analysis (§7): enumerates what is un-catchable by static reading alone (map-vs-territory, shadowed downstream, unmasking) | Medium — L2 |
| U-004 | B | F-B-equivalent NOT treated as a miss at all (deliberate exclusion of bisection-hygiene from the efficacy denominator) and 4-cause SC1–SC4 split isolating "human-readable taxonomy vs executable API identity" (SC4) | Medium — L3 |
| U-005 | C | Full operational protocol spec: H0–H5 waves, machine-checkable output statuses, named auditor agents, `--pipeline-health` flag, NOT PROVEN blocker semantics, and an explicit G1 HALT + paste-ready approval prompt | High — L2 |
| U-006 | C | "Highest-leverage stage to fix = task-builder first" ecosystem-prioritization claim (shapes downstream evidence) | Medium — L2 |

---

## Shared Assumptions

| # | Assumption | Source Agreement | Classification | Promoted |
|---|---|---|---|---|
| A-001 | The frozen escape set (E/M-series) is COMPLETE and correctly attributed — no escape outside the enumerated set | All 3 (each freezes a set and reasons only within it) | UNSTATED | [SHARED-ASSUMPTION] — L3 (set-completeness is a claim-mechanics/evidence-sufficiency assumption) |
| A-002 | "should-have-caught" is a fair denominator for each review stage | A & B (build ratios on it); C implicitly via 59% theatre | UNSTATED | [SHARED-ASSUMPTION] — L3 (denominator fairness = evidence-sufficiency) |
| A-003 | Live runtime execution was the decisive/ground-truth oracle; reading-based review is structurally weak for this class | All 3 (A §7, B §7, C RC1) | STATED | No — L3 (explicit in all three) |
| A-004 | The root cause of each escape is correctly validated (not merely plausible) | All 3 present "validated root cause" per item | UNSTATED | [SHARED-ASSUMPTION] — L3 (causal-mechanics correctness asserted, not independently proven in-doc) |
| A-005 | The five review surfaces (troubleshoot/task-builder/reflect-PRE/reflect-POST/adversarial) are the correct, exhaustive stage inventory | A & B enumerate exactly these 5; C names same stack | UNSTATED | [SHARED-ASSUMPTION] — L3 (stage-set completeness is an invariant claim) |
| A-006 | A boundary/contract/runtime oracle is the right remediation primitive | All 3 (A R-1, B 4.1, C control 1) | STATED | No — L2 |
| A-007 | Hardening `sc:troubleshoot` is the correct locus of the fix | All 3 (all target troubleshoot.md + SKILL.md) | STATED | No — L2 |
| A-008 | The defect chain is a genuine serial-unmasking "whack-a-mole" (each fix exposes the next), not independent coincident bugs | All 3 (A "serial unmasking chain"; B SC3 scope-freezing; C RC3 sibling-surface) | UNSTATED | [SHARED-ASSUMPTION] — L3 (causal-mechanics of the chain ordering) |

---

## Summary

| Category | Count |
|---|---|
| Structural (S) | 7 |
| Content (C) | 9 |
| Contradictions (X) | 8 |
| Unique (U) | 6 |
| Shared Assumptions (A) | 8 |
| **total_diff_points (S+C+X+A)** | **32** |

### High-severity IDs
- Structural: S-001, S-002, S-004, S-005, S-006
- Content: C-002, C-003, C-004, C-005, C-005b
- Contradictions: X-001, X-002, X-003, X-004, X-005, X-006, X-007
- Unique: U-001, U-002, U-005

### Taxonomy levels present
- **L1 (surface/wording/format):** ZERO points — no purely cosmetic diffs were material enough to log; all differences rise to L2 or L3.
- **L2 (structural/scope/framing):** present (S-001, S-002, S-003, S-005, S-006, S-007, C-001, C-007, X-006, U-003, U-005, U-006, A-006, A-007).
- **L3 (state-mechanics/counts/attribution/evidence):** present and dominant (S-004, C-002..C-006, X-001..X-005, X-007, X-008, U-001, U-002, U-004, A-001, A-002, A-004, A-005, A-008).

> NOTE: L1 has ZERO points. The variants diverge structurally and on claim-mechanics, not on wording/style.
