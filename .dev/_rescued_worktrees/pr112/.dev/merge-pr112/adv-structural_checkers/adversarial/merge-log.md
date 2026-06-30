# Merge Log: structural_checkers.py Resolution

## Metadata
- Base: Variant 3 (proposed-resolution)
- Merged output: `.dev/merge-pr112/structural_checkers.py.resolved`
- Executor: manual (resolution authored before adversarial validation; adversarial run = stress-test of the single proposal vs ours-only / theirs-only)
- Changes applied: 3 (comment-only)
- Status: success
- Date: 2026-06-04

## Changes Applied
| # | Change | Status | Provenance Tag |
|---|--------|--------|----------------|
| 1 | Hunk 1 comment = V1 rich text + TASK-RF ref | applied | ours + theirs(ref) |
| 2 | Hunk 2 comment = PR#111 + TASK-RF ref; foreign abs-path dropped | applied | ours + theirs(ref), V2 liability rejected |
| 3 | Hunk 3 comment = PR#111 + TASK-RF ref | applied | ours + theirs(ref) |

## Post-Merge Validation
- **Syntax (ast.parse)**: PASS
- **Conflict markers**: 0 (none remain)
- **Structural integrity**: PASS — symbol set/order identical to both parents
- **Executable-code equivalence**: PASS — comment-stripped diff vs ours/theirs = 0 lines (no behavioral change introduced by merge)
- **No duplicate definitions/comments**: PASS — exactly 1 "We also track source family" block (git-auto-merge duplicate avoided by building from clean OURS stage)
- **Foreign-repo path removed**: PASS — `TUIBBS-scp` absent
- **Provenance preserved**: PASS — PR #111 (×3) AND TASK-RF-20260531-044100 (×3) both present across the 3 hunks
- **Contract consistency**: PASS — MD canonicalizer + allowlist-extension regex empirically verified (18/18) against `ID_PATTERNS["MD"]=r"M\d+-D-?\d+"`
- **New contradictions introduced**: 0

## Summary
- Planned: 3 | Applied: 3 | Failed: 0 | Skipped: 0
- Rejected (transparency): 1 (V2 foreign-repo absolute path, U-001)
- Out-of-scope left as-is: redundant local `import re` (present identically in both parents)
