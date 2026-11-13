# Tier 1 reflection card (UC-1 pre, corpus: archived work unit TASK-WF-implementFrOnb1O-20261023-180618)

## Context
- Spec input is a 1-line source.md pointing at .dev/releases/backlog/ironclaude-onboarding-deck/spec.md (FR-ONB.1 Part A). That file does not exist in any reachable checkout (grounding constraint C-01).
- Tasklist: 7 tasks, 2 phases, constraints embed the spec's authoritative wording verbatim (plan:19-31).
- The work unit was EXECUTED 2026-10-23 (progress.md: all 7 tasks compliant, FINAL: pass) and archived. This shadow re-audit checks (a) plan-vs-spec coverage, (b) plan internal quality/fidelity, (c) recorded-evidence corroboration.

## Findings (candidates; reviewers pressure-test)
- C-01 [constraint] Driving spec absent on disk everywhere (main checkout backlog dir lacks it; never committed under that name). Audit grounding = tasklist-embedded verbatim quotes + package artifacts. No contradiction found between embedded quotes and recorded diffs.
- C-02 [fidelity, positive] All 7 tasks have compliant ledger rows with per-AC file:line anchors; t3-consistency.log records 8 prose-vs-routing-row AGREE checks; t7-tests.log records verify-sync rc=0 and 5/5 tie-break lines carrying the exception; t7-regression.log proves the helper fails on both old fixtures.
- C-03 [residue] Current master evolved past the plan's pinned wording (A1/A3/A4/A8 empty; CHANGELOG entry gone). Expected for archived corpus; ACs are not re-runnable against HEAD. Severity judgment belongs to reviewers: is a plan whose ACs are frozen against a moved baseline still "good"? (It was correct at execution time; later PRs reworked the wording.)
- C-04 [process, minor candidate] progress.md records extras=test:fail for T1 and T2 (md-only edits, no test AC) alongside verdict=compliant; T3-T7 record test:pass. Ledger test-extras semantics on non-test tasks are ambiguous; a reader may misread test:fail as a failed gate.
- C-05 [plan-quality, minor candidate] Task 4's walk-through AC and Task 7's fixture AC are both satisfied by on-disk artifacts (t4-recommend-walk.md, t7-regression.log) — good self-proving design.
- C-06 [open] Plan line 30 (stacked branch, open PR only after #285 merges) is a process constraint outside the package; PR landing is not evidenced inside the package (return-contract has no PR field). Not a defect; noted.

## Coverage
parsed=0, inferred=6, all matched; coverage_pct_union=1.0; parsed-sparse -> Tier 2 (pinned anyway).
