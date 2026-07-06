# Diff Analysis: PR #128 Medium-Remediation Strategy Comparison

## Metadata
- Generated: 2026-06-04T03:42:06Z
- Mode: compare (single-source, 4 strategies across 2 issues)
- Variants compared: Med-A {A-S1, A-S2}; Med-B {B-S1, B-S2}
- Focus: least-surprise, backward-compat, convention-fit, testability, blast-radius

## Content Differences

| # | Topic | Option 1 | Option 2 | Severity |
|---|-------|----------|----------|----------|
| C-001 | Med-A validation locus | A-S1: declarative at Click boundary (`exists=True, file_okay=False`) | A-S2: imperative `ClickException` in body | Medium |
| C-002 | Med-A error semantics | A-S1: Click usage error, exit code 2, generic message | A-S2: ClickException, exit code 1, branded message | Low |
| C-003 | Med-B inconsistency handling | B-S1: anchor relative `--output` to `root` (removes inconsistency) | B-S2: keep CWD-relative, document + echo (accepts inconsistency) | High |
| C-004 | Med-B behavioral risk | B-S1: changes behavior only when `root != cwd` AND output relative | B-S2: zero behavior change | Medium |

## Contradictions

| # | Point | A position | B position | Impact |
|---|-------|-----------|-----------|--------|
| X-001 | Does the strategy *resolve* the finding or *document* it? | B-S1 resolves (output lands under audited project) | B-S2 documents (surprise remains, only made visible post-write) | High — sufficiency-determining |

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---------|--------------|-------|
| U-001 | A-S1 | Exact match to repo convention `sprint/commands.py:179,390` | High |
| U-002 | A-S2 | Branded, on-message error consistent with module's other `ClickException`s | Low |
| U-003 | B-S1 | Couples `out_path` to validated `root`; composes with A-S1 | High |
| U-004 | B-S2 | Help-text/SKILL.md clarification of `--output` semantics | Medium (graftable) |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Status |
|-------|------------|------------------|--------|
| A-001 | An existing-but-empty project (zero SuperClaude surfaces) must still succeed with an empty audit — only *nonexistent / non-directory* roots should be rejected | All Med-A options reject only nonexistent/non-dir, never empty-but-real | STATED — both A-S1/A-S2 preserve it; **must not regress** |
| A-002 | `--output` is documented *trusted operator input* (review L2); escaping/`..` paths are the operator's choice, still bounded by `_is_protected_context_path` | Both Med-B options leave protected-path guard intact | STATED |

## Summary
- Content differences: 4 (1 High: C-003)
- Contradictions: 1 (High: X-001, sufficiency)
- Unique contributions: 4 (2 High, 1 graftable Medium)
- Shared assumptions: 2 STATED (A-001 is a regression tripwire)
- Highest-severity items: C-003, X-001
