# Diff Analysis: Merge-Conflict Resolution Comparison

## Metadata
- Generated: 2026-06-04
- Variants compared: 3 (A=resolved/proposed, B=ours, C=theirs)
- Total differences found: 4
- Categories: structural (0), content (3), contradictions (1), unique (0), shared assumptions (1)
- Note: Variant A (resolved) is byte-identical to Variant B (ours). Effective comparison is A/B vs C.

## Structural Differences
None. All three are valid 593-line / 598-line Python test modules with identical class/test topology.

## Content Differences

| #     | Topic | Variant A (resolved) | Variant B (ours) | Variant C (theirs) | Severity |
|-------|-------|----------------------|------------------|--------------------|----------|
| C-001 | Model assertion (line 296) | `"sonnet" in cmd` | `"sonnet" in cmd` | `"claude-sonnet-4-5" in cmd` | **High** |
| C-002 | Section comment (line 271) | `# Sonnet subprocess helper` | `# Sonnet subprocess helper` | `# Haiku subprocess helper` | Low |
| C-003 | Test class name (line 275) | `TestInvokeSonnet` | `TestInvokeSonnet` | `TestInvokeHaiku` | Low |

## Contradictions

| #     | Point of Conflict | Variant A/B Position | Variant C Position | Impact |
|-------|-------------------|----------------------|--------------------|--------|
| X-001 | Asserted `--model` value vs production runtime | Asserts alias `"sonnet"` — matches `SONNET_MODEL = "sonnet"` passed at summarizer.py:331 | Asserts literal `"claude-sonnet-4-5"` — production NEVER puts this in cmd; comment at summarizer.py:49 explicitly forbids it | **High — C's assertion fails against production (proven by pytest)** |

## Unique Contributions
None. C contributes no element absent from A/B; A/B is a strict superset of C's intent (both rename the call symbols; A/B additionally complete the rename and use the correct alias).

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|------------|------------------|--------|--------|
| A-001 | The test asserts the value actually passed to `claude --model`, and that value must equal what production emits | All variants assert *something* about `--model` | The whole conflict reduces to which string production emits | UNSTATED → resolved by ground-truth: production emits `"sonnet"` |

## Summary
- Total content differences: 3 (1 High, 2 Low)
- Total contradictions: 1 (High)
- The High-severity item C-001/X-001 is dispositive: it is empirically falsifiable, and was falsified for Variant C by executing the test against production.
- Highest-severity items: C-001, X-001
