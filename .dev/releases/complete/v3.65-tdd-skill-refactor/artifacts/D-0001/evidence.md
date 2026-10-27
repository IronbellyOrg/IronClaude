# D-0001: SKILL.md Line Count Evidence

**Task:** T01.01 -- Count Actual SKILL.md Lines via wc -l
**Date:** 2026-04-03
**Status:** COMPLETE

## Command & Output

```
$ wc -l src/superclaude/skills/tdd/SKILL.md
1387 src/superclaude/skills/tdd/SKILL.md
```

## Baseline Comparison

| Metric | Value |
|---|---|
| Observed line count | 1,387 |
| Spec baseline (fidelity index) | 1,364 |
| Delta | +23 lines |
| Spec baseline (master prompt) | 1,387 |
| Delta vs master prompt | 0 |

## Pending Edits Check

```
$ git status --porcelain src/superclaude/skills/tdd/SKILL.md
(no output -- file is clean)
```

No uncommitted changes to `src/superclaude/skills/tdd/SKILL.md`. The count is deterministic and repeatable.

## Discrepancy Analysis

The spec contains two conflicting baselines:
- **1,364** -- cited in the fidelity index as the spec baseline
- **1,387** -- cited in the master prompt / actual file

The actual file is **1,387 lines**. The +23 line discrepancy against the 1,364 baseline is a known issue tracked as **GAP-TDD-01**. Downstream tasks (T01.02 re-anchoring) must use **1,387** as the true file length.

## Conclusion

The canonical SKILL.md at `src/superclaude/skills/tdd/SKILL.md` is **1,387 lines**. All fidelity index ranges referencing 1,364 as the upper bound will need adjustment in T01.02.
