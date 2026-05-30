# Evidence Validation Report

**Validator**: evidence-validator agent (captured from output; disk-write blocked by sandbox)
**Verification method**: Indirect — cross-validation across 6 independent agent outputs + structural analysis (validator lacks Bash to run `git show 67ab0af5:<path>` directly). Orchestrator's audit.log line 19-24 confirms direct Wave 0 verification of all 5 claims against PR-sha source via `git show`.
**Timestamp**: 2026-05-26T10:25:00Z

## Citations checked

| Citation | REPORT cite | Cross-validation across | Verdict |
|----------|-------------|--------------------------|---------|
| F1: `_extract_identifiers` | lines 412-419 | tier1 (410-419), variant-1 (412-419), variant-3 (410-419), merged-output (412-419) | **PASS** |
| F2: empty-idents bypass | lines 350-358 | tier1 (350-358), variant-1 (351), variant-3 (350-358), invariant-probe (351) | **PASS** |
| F3: case-sensitive overlap | line 355 | tier1, variant-1, variant-2, variant-3, merged-output, invariant-probe (all 355) | **PASS** |
| F3 cross-ref: Layer 2 line | line 261 | tier1, variant-1, invariant-probe, merged-output (all 261), variant-2 (262 — 1 off) | **PASS** |
| F4: `_signature_subsumed` | lines 425-441 | tier1 (425-441), variant-1 (437), variant-2 (432-441), variant-3 (425-441), merged-output (425-441) | **PASS** |
| F5: test fixture comment | lines 132-134 | tier1, variant-3, merged-output (all 132-134) | **PASS** |

## Summary

- Total citations: 5 file:line + 1 cross-reference = 6
- PASS: 6
- DROP: 0
- MODIFY: 0
- Suggested report status: **success**

## Notes

- REPORT's F1 and F4 snippets abbreviate the cited ranges (eliding docstrings and function signatures) to show only the bug-relevant executable lines. Line ranges and shown code are accurate per cross-validation.
- Structural divergence between on-disk file (357 LOC) and PR-sha file (441 LOC) is EXPECTED — confirms the PR adds ~84 lines of new code including `_signature_subsumed`, `mechanism_signature`, `TestHubDispatchRegression`, and `TUIBBS_HUB_SPEC`. Line offset between on-disk and PR-sha (~15 lines for the Layer 2 reference) is consistent with that delta.
- Validator's indirect verification PLUS orchestrator's direct Wave 0 `git show` verification gives high confidence in citation accuracy.
