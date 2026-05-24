# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | state_variables | The HEAD versions of skill/agent files are the canonical "current" state and should not be silently overwritten | ADDRESSED | HIGH | `git show HEAD:src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md \| grep -c test_is_wrong` returns 4; ANTI-C's recommendation explicitly preserves this by abandoning fcd28bfa cherry-pick |
| INV-002 | guard_conditions | Cherry-pick conflicts on files modified by intervening commits are predictable from `git log SHA..HEAD -- <path>` | ADDRESSED | MEDIUM | `git log 1550ea5f..HEAD -- src/superclaude/cli/eval/commands.py tests/cli/eval/test_eval_group.py` returns empty → guaranteed no conflict; same for e1c458bd |
| INV-003 | count_divergence | The diff metric (273 lines) accurately captures the cost of conflict resolution | ADDRESSED | LOW | The 273 figure is line-count from `git diff fcd28bfa HEAD --`, which is the actual surface a merge tool would present |
| INV-004 | collection_boundaries | When all 3 commits are the "collection," abandoning one is a legitimate subset operation | ADDRESSED | LOW | The shared assumption (A-002) from diff analysis is "the work is worth landing in some form" — preserved by HYBRID synthesis |
| INV-005 | interaction_effects | `.markdownlint.json` extraction does NOT depend on the rest of fcd28bfa | ADDRESSED | MEDIUM | `.markdownlint.json` is a single new file at repo root with no cross-references to skill/agent files; extraction is genuinely independent |
| INV-006 | sufficiency_challenge | Does the HYBRID recommendation (cherry-pick 1550ea5f + e1c458bd + new commit for .markdownlint.json) ALONE achieve the stated outcome (recover all valuable work without destroying HEAD's newer content)? | ADDRESSED | HIGH | Branch-trace: (a) 1550ea5f files have zero intervening commits → cherry-pick produces exact intended diff; (b) e1c458bd files have zero intervening commits → same; (c) `.markdownlint.json` is net-new at repo root → no conflict possible; (d) abandoning fcd28bfa's other 9 files preserves the 4 test_is_wrong contract refs in HEAD's SKILL.md. All four downstream conditions resolved positively. |

## Summary

- **Total findings**: 6
- **ADDRESSED**: 6
- **UNADDRESSED**: 0
  - HIGH: 0
  - MEDIUM: 0
  - LOW: 0

**Gate verdict**: PASS — convergence not blocked by invariant violations.
