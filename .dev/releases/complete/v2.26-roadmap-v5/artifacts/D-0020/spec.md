# D-0020: build_spec_fidelity_prompt() Deviation Awareness Modification

## Location
`src/superclaude/cli/roadmap/prompts.py`

## Change
Added optional `spec_deviations_path: Path | None = None` parameter (FR-016).

## New Signature
```python
def build_spec_fidelity_prompt(
    spec_file: Path,
    roadmap_path: Path,
    spec_deviations_path: Path | None = None,
) -> str:
```

## Backward Compatibility
When `spec_deviations_path=None`, behavior is identical to pre-v2.25. No existing callers break.

## Deviation-Aware Instructions (FR-017, when spec_deviations_path provided)
1. VERIFY CITATIONS: Check D-XX + round citations in INTENTIONAL_* annotations
2. EXCLUDE VERIFIED INTENTIONAL: Deviations with valid citations excluded from report
3. REPORT INVALID ANNOTATIONS AS HIGH: Unverifiable citations → HIGH severity
4. ANALYZE NOT_DISCUSSED INDEPENDENTLY: Apply normal severity classification
5. SCOPE_ADDITION DEVIATIONS: Report as LOW unless contradicting requirements
