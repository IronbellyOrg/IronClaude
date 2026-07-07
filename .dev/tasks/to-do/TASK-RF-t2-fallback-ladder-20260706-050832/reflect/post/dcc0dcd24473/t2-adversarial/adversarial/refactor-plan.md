# Refactoring Plan

## Overview
- **Base:** Variant 1 (qwen3.6-plus) — complete scaffold
- **Incorporated from:** Variant 2 (glm-5.2) — H1, H2, H3-framing, file:line discipline
- **Change count:** 9 (4 incorporate, 3 correct/drop, 2 reconcile)
- **Overall risk:** Low (report-merge; no code mutated)

## Planned Changes

| # | Title | Source | Target in base | Approach | Rationale | Risk |
|---|-------|--------|----------------|----------|-----------|------|
| 1 | Add H2 as top finding | V2 H2 | Concrete Findings §1 | insert (renumber) | CONFIRMED gate substitution; qwen missed it; highest-value catch (debate C-003, INV-001) | Low |
| 2 | Add H1 as finding | V2 H1 | Concrete Findings | insert | Real carve-out label mismatch (debate C-002, INV-002) | Low |
| 3 | Re-frame HALT finding | V2 H3 | V1 #4 | replace tag | Drop "Security" tag (project norm `feedback_no_security_framing`); add non-reconciliation + operator-attested-only (INV-006) | Low |
| 4 | Adopt file:line citations | V2 | all findings | append field | CEV rigor; each finding gets a File:line anchor | Low |
| 5 | Drop metadata-drift finding | V1 #3 | remove | delete | False positive: head==start_commit is working-tree-diff by design (frontmatter L46) | Low |
| 6 | Downgrade untracked-test | V1 #1 / V2 M2 | severity edit | modify | IMPORTANT→MINOR: 8 files exist, green, documented over-delivery (L515/L527) | Low |
| 7 | Downgrade H1 severity | V2 H1 | severity edit | modify | CRITICAL→IMPORTANT: contract clean (regression 0, tier 2, full diversity); memory `reference_reflect_exit11_degraded_benign` | Low |
| 8 | Downgrade + disposition xpassed | V2 H4 | severity edit | modify | HIGH→LOW: dispositioned at `final-fulltest-summary.md:23` (pre-existing/unrelated) | Low |
| 9 | Reconcile verdict | debate | Verdict line | replace | CONDITIONAL PASS + mandatory follow-ups (neither V1's unqualified PASS nor V2's FAIL) | Medium |

## Changes NOT Being Made (considered and rejected)

| Diff point | Non-base (V2) approach | Why base approach kept |
|-----------|------------------------|------------------------|
| C-001 verdict | Adopt V2's CONDITIONAL FAIL | Ground truth refutes FAIL: load-bearing additive-only guarantee holds, suite green, degrade environmentally benign against a clean contract. FAIL would over-gate. |
| S-002 taxonomy | Adopt V2's High/Medium-confidence tiering wholesale | Base (V1) numbered+severity scheme is complete and clearer for a downstream scorer; V2 tiering folded in as severity labels only. |
| H2 severity | Keep V2's CRITICAL | Green suite + additive-only 0-diff means H2 is an anti-bias *process* gap, not a correctness defect → IMPORTANT. Executor self-disclosed the substitution ("6.G11-equivalent, inline"), which is honest but does not close the gap. |

## Risk Summary
All changes are report-content merges; no source code, tests, or task frontmatter are touched by this pipeline. The one Medium-risk item (#9 verdict reconciliation) is defensible from the debate + invariant probe and is fully evidenced.

## Review Status
Auto-approved (non-interactive). Timestamp: 2026-07-07.
