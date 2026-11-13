# Diff Analysis: reflect Tier-2 reviewer cards (UC-1 pre-execution audit)

## Metadata
- Generated: 2026-11-13T00:12Z
- Variants compared: 3 (analyzer/sonnet, qa/haiku, refactorer/opus)
- Total differences found: 9 (structural 1, content 4, contradictions 1, unique 3 (+1 shared assumption))
- Focus: correctness, coverage, deviation-classification

## Structural Differences

| # | Area | V1 analyzer | V2 qa | V3 refactorer | Severity |
|---|------|------------|-------|---------------|----------|
| S-001 | Card shape | prose + findings | prose + adherence table + findings | prose verdict + findings | Low (same findings-block shape) |

## Content Differences

| # | Topic | V1 | V2 | V3 | Severity |
|---|-------|----|----|----|----------|
| C-001 | Wording-claim finding | F1 medium (read all 4 agents, confirms; notes dropped Grep-floor + index-misses caution) | F2 low (confirms; stresses error is attribution not inclusion) | F3 medium (confirms; adds "two versions of shared rule across 14 agents") | Low (full substantive agreement; severity spread low-medium) |
| C-002 | AC-strength finding | F2 low (grep-count ACs; no checked_at/worktree_root) | F1 medium (token presence + diff shape insufficient) | F1 low (style mismatch + AC cannot verify) + F4 low (unnamed tests) | Low (agreement on substance) |
| C-003 | Ten-file list verification | covered via brief quote (file outside root) | verification-blocked (explicitly unconfirmable in-root) | not addressed as such (verified placements instead) | Medium (different verification postures) |
| C-004 | Task 11 assessment | verify-sync compares mirrors not rule text | covered for maintenance claim; does not close acceptance gap | runs repo sync correctly; misses plugins/ mirror; unnamed tests | Low |

## Contradictions

| # | Conflict | V1 | V2 | V3 | Impact |
|---|----------|----|----|----|--------|
| X-001 | Deviation classification of plan-quality findings | findings, no deviation class | both findings classified **Drift** (deviation taxonomy) | findings, no deviation class | Medium: UC-1 has no executor work; "Drift" is a UC-2 executor-deviation class. V2's classification imports UC-2 semantics into a UC-1 plan audit. |

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---------|-------------|-------|
| U-001 | V3 | plugins/superclaude/agents tracked mirror (22 files, incl. all ten targets) never synced by any make target; build-plugin ships it verbatim into dist; all ten copies lack the rule | High |
| U-002 | V3 | "one bullet" vs numbered bold-label list style mismatch; executor had to invent "6. **Use Codegraph Safely**" | Medium |
| U-003 | V1 | Spec self-contradiction surfaced as its own finding (follow-4-agents vs require-3-fields; tasklist resolves silently) | Medium |
| U-004 | V1 | Dropped from the four agents' wording: native Grep floor detail + "Index misses do not prove absence" caution | Medium |

## Shared Assumptions

| # | Assumption | Source agreement | Classification | Promoted |
|---|------------|------------------|-----------------|----------|
| A-001 | The ten-file enumeration in the tasklist matches issue-summary.md:24 (no card could Read it in-worktree; V1 trusted the brief quote, V2 declared blocked, orchestrator verified in main checkout) | all three treated the list as given | UNSTATED | yes |
| A-002 | The Constraints rule text is what an executor pastes verbatim | all three | STATED (tasklist Constraints) | no |

## Summary
- Structural 1, content 4, contradictions 1, unique 4, shared assumptions 2 (UNSTATED 1, STATED 1)
- Highest-severity items: U-001 (plugin mirror, High), C-003 (Medium), X-001 (Medium)
- Note: variants substantially overlap on C-001/C-002 (same finding, three independent confirmations); the debate's real work is severity calibration, the X-001 classification question, and whether U-001's plugin gap is a plan defect or out-of-scope for this tasklist.
