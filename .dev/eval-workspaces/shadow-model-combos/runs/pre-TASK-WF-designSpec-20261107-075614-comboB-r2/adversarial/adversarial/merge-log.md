# Merge Log

Base: variant-1-original.md. Plan: refactor-plan.md. Output: merged-output.md.

## Changes
### Change #1: Remove variant 1's withdrawn F9
- Status: applied
- Before: variant 1 listed F9 (Task 5 over-claims `_NEW_KEY_DEFAULTS`). After: no such finding in prose or block.
- Provenance: `<!-- Source: Base (original, modified) - variant 1 F9 removed (Change #1) -->`
- Validation: PASS (merged ids F1 to F12 contain no `_NEW_KEY_DEFAULTS` claim).

### Change #2: Fix variant 1's wrong line numbers
- Status: applied
- Before: spec cites such as source.md:73, :43-47, :49-51 and plan cites about 87 lines low. After: source.md:112, :82-85, :88-91, :107-109, :165-166; plan 60-62, 70-77, 124, 137-140, 76.
- Provenance: `<!-- Source: Base (original, modified) - ... line anchors corrected per Change #2 -->` on F2, F4, F6, F8, F9, F10.
- Validation: PASS (every anchor matches the plan's list and the jsonl citations).

### Change #3: F1 and F2 blocking with INV-001 and INV-002 detail
- Status: applied
- Before: F1 "reuse `_repo_scoped`"; F2 "add three arguments". After: F1 also needs `_command_lines`, `_GH_CMD` and the runtime-log clause relaxed; F2 says the arguments are necessary but not sufficient.
- Provenance: `<!-- Source: Base (original, modified) - ... per Change #3 -->`
- Validation: PASS (F1 and F2 blocking true in prose and jsonl).

### Change #4: New blocking finding, stale guard cycle id
- Status: applied
- Before: absent. After: F3 (MAJOR, blocking) with source.md:108, :139, :166, :190-206 and plan 62, 77.
- Provenance: `<!-- Source: Variant 3, F8 - merged per Change #4 -->`
- Validation: PASS.

### Change #5: Untested producer payload
- Status: applied
- Before: absent. After: F5 (MAJOR, not blocking) with source.md:184-185 and plan 62, 124, 168-172; fix text names spec 4.2 and the Task 11 trace test.
- Provenance: `<!-- Source: Variant 2, F5 - merged per Change #5 -->`
- Validation: PASS.

### Change #6: Calibrated severities
- Status: applied
- Before: variant 1 F3 blocking-ish, F7 and F4 as stated. After: F4 MAJOR not blocking with the status-override fix; F9 MINOR; F6 MINOR with settle, fold and status test.
- Provenance: `<!-- Source: Base (original, modified) - ... per Change #6 -->`
- Validation: PASS (severities match the jsonl).

### Change #7: Keep three variant-1 MINOR findings
- Status: applied
- Before: F5, F6, F8 of variant 1. After: F7 (baseline, variant 3 bound), F8 (mapping), F10 (row 3 order, variant 2 correction).
- Provenance: `<!-- Source: Base (original, modified) - ... per Change #7 -->`
- Validation: PASS.

### Change #8: Add variant 3's two MINOR findings
- Status: applied
- Before: absent. After: F11 (classification keys, narrowed) and F12 (pinned sentences by start text).
- Provenance: `<!-- Source: Variant 3, F10 / F9 - merged per Change #8 -->`
- Validation: PASS.

### Change #9: Open invariants section
- Status: applied
- Before: absent. After: INV-003 to INV-006, one line each, labelled warnings.
- Provenance: `<!-- Source: Invariant probe INV-003 to INV-006 - merged per Change #9 -->`
- Validation: PASS (none appears in the findings block).

## Post-Merge Validation
- Heading hierarchy: PASS. merged-output.md has one comment header and five H2 sections in the required order (Verdict, Findings (prose), Open invariants (warnings, not findings), Coverage note, Findings block); no skipped levels.
- Internal references: PASS. F2 points to F3 and the verdict points to F1 to F3; both resolve. INV-001 and INV-002 are cited by the verdict and by the jsonl `refs`, and INV-003 to INV-006 appear only in the open-invariants section.
- Findings block: PASS. Read back after the edit: exactly 12 JSON lines, each a complete object with balanced braces and quotes, ids F1 to F12 in order, byte-for-byte the content of merged-findings-block.jsonl; the closing fence and the `reviewer_model_self_report` line follow.
- Contradiction re-scan: PASS. The prose and the jsonl agree on id, severity and blocking flag for all 12 findings. Blocking is true for F1, F2 and F3 only. F2's "necessary but not sufficient" points to F3 and does not contradict it. The verdict counts (5 MAJOR, 7 MINOR, 3 blocking) match the jsonl.

## Summary
- Planned: 9
- Applied: 9
- Failed: 0
- Skipped: 0
- Verdict: PASS
