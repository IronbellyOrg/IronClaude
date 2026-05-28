# Refactoring Plan

Base = Variant 3 (Analyzer). Incorporate framings from Architect (L3 pairing) and QE (evidence-rigor reframe).

## Overview

- Base variant: Analyzer (4-tier ranking framework)
- Incorporated variants: Architect (L3 + cluster), QE (schema vs validator)
- Total planned changes: 6
- Risk: low (this is a synthesis, not a runtime change)

## Planned Changes

### Change 1 — Adopt Analyzer's 4-tier ranking framework as the spine of the merged output

- **Source**: Variant 3 § "Differences I am championing as significant — ranked by behavior-shaping impact"
- **Target**: Main body of `merged-output.md`
- **Approach**: Promote to top-level structure: § "Differences ranked by significance" with sub-sections Tier 1 (behavior-shaping), Tier 2 (integration), Tier 3 (infrastructure), Tier 4 (instrumentation), + Shared-assumptions tail
- **Rationale**: Convergence at 92% on this ranking; user explicitly asked for top-10 ranked output
- **Risk**: Low — analyzer card already provides full ranking

### Change 2 — Annotate the 5-difference cluster downstream of execution-model choice

- **Source**: Variant 1 Round 2 statement + Variant 3 "If my framing is wrong" section
- **Target**: Tier 3 (infrastructure) sub-section of merged output
- **Approach**: Add explicit "Cluster A" annotation: C-004 (execution model) + C-005 (orchestrator role) + C-015 (CLI module) + U-002 (sprint/tfep.py) + U-003 (orchestrator dispatcher prohibition) → mark as downstream of forensic's "subprocess-pipeline + dispatcher" design choice
- **Rationale**: Reader needs to see that these 5 differences are *one decision* with 5 observable consequences
- **Risk**: Low — cluster framing endorsed by all 3 advocates

### Change 3 — Pair U-003 ↔ U-005 as same-problem-opposite-solution

- **Source**: Variant 1 Round 2 + Variant 2 refinement
- **Target**: Tier 1 / Tier 3 of merged output — the hallucination-contract entry
- **Approach**: Use "withhold access vs post-hoc validation" frame; cite forensic's `≤8k orchestrator-token cap + Phase 6 reads only 6 summary artifacts` against v2's `evidence-validator agent re-Reads every cited line and drops mismatches`
- **Rationale**: One of the most consequential L3 divergences; framing makes the comparison crisp
- **Risk**: Low — pairing accepted by all advocates

### Change 4 — Elevate C-013 (test strategy) to its own line item with QE's long-term framing

- **Source**: Variant 2 Round 2 statement
- **Target**: Tier 2 (integration) of merged output
- **Approach**: Note "forensic has 58 success criteria SC-001-SC-058 across 10 test files (D6.1-D6.13) gated at M6 with canned-artifact fixtures; v2 uses `.dev/eval-workspaces/sc-troubleshoot/`; this divergence is invisible on day 1 but shapes maintenance velocity"
- **Rationale**: QE flagged this as Tier 1 in Round 2; Architect+Analyzer kept it Tier 2 but accepted the long-term framing
- **Risk**: Low

### Change 5 — Add Analyzer Round 2 reframe of C-014 (failure handling) as High-severity divergence

- **Source**: Variant 3 Round 2 statement
- **Target**: Tier 2 (integration) of merged output
- **Approach**: Note "forensic has a coordinated three-level fallback chain (retry quick → Sonnet scoring agent → emit as-is with `debate_status: "skipped"`); v2 has a 10-row per-wave error matrix (per-component fallbacks). Coordinated vs per-component is the divergence."
- **Rationale**: Round 2 reframe accepted; was undersold in diff-analysis severity
- **Risk**: Low

### Change 6 — Preserve A-001 / A-002 shared assumptions in merged output

- **Source**: Diff-analysis § Shared Assumptions
- **Target**: Tail section of merged output
- **Approach**: Keep both UNSTATED preconditions visible: (A-001) adversarial-debate-as-adjudication, (A-002) static-Markdown-report-as-terminal-artifact
- **Rationale**: Round 2.5 invariant probe verified absence from both source artifacts' justifications; user asked for substantive divergences including the assumptions both share
- **Risk**: Low

## Changes NOT being made

- **No "which design is better" verdict.** The user explicitly framed this as differences-only. All scoring exists only as scaffolding-quality assessment for the merged output, not as a winner declaration.
- **No re-scoring of forensic vs v2 on quantitative metrics.** Variant 3 (Analyzer) made this point — they are not commensurable because they target different workloads.
- **No flattening of paired/clustered differences.** Round 2.5 INV-005 explicitly preserved cluster.

## Risk Summary

| Change | Risk | Mitigation |
|--------|------|-----------|
| 1 | Low | Ranking is the substance of what user asked for |
| 2 | Low | Cluster is a synthesis, not new content |
| 3 | Low | Pairing accepted by all 3 advocates |
| 4 | Low | QE long-term framing accepted in Round 2 |
| 5 | Low | Round 2 reframe accepted |
| 6 | Low | Shared assumptions verified by invariant probe |

## Review Status

- Auto-approved
