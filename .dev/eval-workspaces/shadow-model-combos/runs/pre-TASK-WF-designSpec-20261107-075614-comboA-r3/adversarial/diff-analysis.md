# Diff Analysis: reflect reviewer-card comparison (comboA-r3)
- Variants: 3 (analyzer/sonnet, qa/haiku, refactorer/opus); slices disjoint by design (FR-1..11, FR-12..23, INF-1..7)
- Total findings: 21 (5 + 10 + 6). Cross-card content diff:

## Cross-card overlaps (agreement points)
| ID | Cards | Point | Verdict |
|----|-------|-------|---------|
| O-1 | rv1-F5 + rv3-F4 | Wave 0 bullet must state "at L3 with --merge-guard off ... no draft call" while its test rejects "L3 only or draft gate wording" — ambiguous literal-check risk | DUPLICATE, cross-validated by 2 classes |
| O-2 | rv2-F7 + rv3-F6 | Release-gate PR obligations (PR body states gate; open run passes --merge-guard off) recorded in Task 1 but owned by no task | DUPLICATE, cross-validated by 2 classes |

## Contradictions / severity disputes
| ID | Cards | Dispute | Resolution evidence |
|----|-------|---------|---------------------|
| X-1 | rv2-F2 (blocking) vs rv3 (implicit) | "Scenario tests verify a test-owned driver, not the SKILL; checks self-verifying" | Spec section 8 + Constraints: build has NO GitHub calls by owner decision; live behavior is the release gate. A plan AC can only check the deliverable it produces (text + pure-core tests). Downgrade blocking -> non-blocking MAJOR; the driver-vs-SKILL gap is real and recorded. |
| X-2 | rv2-F7 (blocking) vs rv3-F6 (MINOR) | severity of unowned PR obligations | Spec:326 places the PR-body/open-with-off duties in the RELEASE gate (owner-run, disposable PR) — outside this build plan's task scope by the owner's accepted decision. Downgrade to MINOR advisory. |
| X-3 | rv2-F1 ("name-existence only") vs plan ACs | Task 11 AC asserts 12 names; 3 content-bearing ACs exist (trace order, forbidden calls, no-push-after-halt) | Partially rebutted: 3 of the 12 tests DO have content ACs; 9 are name-only. Finding stands narrowed. |

## Unique contributions
rv1-F1 (cycle_id sharing unasserted, highest calibration 0.80), rv1-F2/F3/F4 (thin-coverage MINORs), rv2-F3/F5/F6/F8/F9/F10, rv3-F1 (transitive-only depends), rv3-F2 (start-text vs whole-sentence constants), rv3-F3 (git write verbs uncovered by per-task classification wording), rv3-F5 (fixed-decisions bullet drops the trigger).

## Shared assumptions
A-001 [SHARED-ASSUMPTION] All three cards assume plan-text ACs are the only enforceable unit (no live GitHub). STATED in Constraints. Accept.
A-002 The base commit for the audit is the authoring-time repo, not HEAD. STATED in briefs (attribution rule). Accept.
