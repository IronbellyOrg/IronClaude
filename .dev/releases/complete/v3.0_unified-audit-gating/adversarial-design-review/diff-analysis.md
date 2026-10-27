# Diff Analysis: Solution C Design Spec Comparison

## Metadata
- Generated: 2026-03-18
- Variants compared: 3
  - **Variant A**: `design-integration-plan.md` — Integration & testing plan (full-spectrum)
  - **Variant B**: `design-provenance-injection-fix.md` — Provenance injection hardening
  - **Variant C**: `design-sanitize-output-fix.md` — Sanitize output fix
- Total differences found: 18
- Categories: structural (3), content (8), contradictions (2), unique (5), shared assumptions (3)

---

## Structural Differences

| # | Area | Variant A | Variant B | Variant C | Severity |
|---|------|-----------|-----------|-----------|----------|
| S-001 | Document scope | Full integration plan: both fixes + tests + verification + rollback + checklist | Focused on `_inject_provenance_fields` + `_inject_pipeline_diagnostics` hardening only | Focused on `_sanitize_output` fix only | Medium |
| S-002 | Code presentation | Code shown as diff fragments (before/after snippets) | Code shown as diff fragments + full idempotency implementation | Full rewritten function body (3 versions: initial, simplified, minimal recommended) | Medium |
| S-003 | Section organization | 6 sections: integration sequence, regression tests, E2E verification, rollback, checklist, files modified | 7 sections: problem, design, idempotency, edge cases, test plan, sequence, risk | 6 sections: problem, code change, edge cases, impact, tests, checklist | Low |

## Content Differences

| # | Topic | Variant A Approach | Variant B Approach | Variant C Approach | Severity |
|---|-------|-------------------|-------------------|-------------------|----------|
| C-001 | lstrip character set | `content.lstrip()` (all whitespace) | `.lstrip("\n\r\t ")` (explicit charset) | `.lstrip("\n\r")` (newlines only) | Medium |
| C-002 | _sanitize_output fix detail | Proposes atomic write with tmp file + os.replace, returns preamble_bytes | Defers to Part 1 (this spec is Part 2) — mentions line 101-102 change needed | Full function rewrite with 3 alternative implementations; recommends "minimal fix" | High |
| C-003 | _inject_provenance_fields fix detail | One-liner: add `content = content.lstrip()` before startswith check | Detailed: `.lstrip("\n\r\t ")` + idempotency guards (check field existence before insert) | Defers to Part 2 — mentions as defense-in-depth | High |
| C-004 | Idempotency handling | Not addressed | **Comprehensive**: check each field exists before insertion, preventing duplicate YAML keys on retry | Not addressed | High |
| C-005 | _inject_pipeline_diagnostics | Identified as needing same fix (line 134); included in checklist | Detailed code change provided; idempotency guard added | Identified as affected; mentioned in "Impact" section | Medium |
| C-006 | Test count & coverage | 12 tests across 3 classes + E2E | 10 tests across 3 classes (full pytest code provided) | 6 tests in 1 class (full pytest code provided) | Medium |
| C-007 | Atomic write pattern | Preserves existing tmp + os.replace pattern | Relies on existing write_text rewrite (no separate atomic write concern) | Explicitly implements tmp + os.replace atomic writes | Medium |
| C-008 | Rollback plan | Detailed per-fix rollback with independent fix analysis + full rollback | Not provided | Not provided | Medium |

## Contradictions

| # | Point of Conflict | Variant A Position | Variant B Position | Variant C Position | Impact |
|---|-------------------|-------------------|-------------------|-------------------|--------|
| X-001 | lstrip scope | Uses bare `.lstrip()` (all Unicode whitespace) | Uses `.lstrip("\n\r\t ")` — explicitly excludes broader Unicode whitespace, includes tabs and spaces | Uses `.lstrip("\n\r")` — only newlines, no tabs or spaces | Medium — must decide: are leading tabs/spaces before frontmatter realistic LLM output? |
| X-002 | Whitespace-only file handling | Not explicitly addressed | Case 9: whitespace-only file left unchanged (returns 0) | Test 5: whitespace-only file left unchanged (returns 0) | Low — B and C agree; A does not address |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | Variant A | Rollback plan with per-fix independence analysis | High — production safety net |
| U-002 | Variant A | E2E integration tests simulating full pipeline with mock subprocess | High — catches interaction bugs |
| U-003 | Variant A | Existing test regression guard list (names 9 specific tests that must keep passing) | Medium — prevents silent regression |
| U-004 | Variant B | Idempotency guards preventing duplicate YAML keys on retry | High — correctness for retry scenarios |
| U-005 | Variant B | False positive analysis for `"spec_source:" in frontmatter` substring check | Medium — acknowledges a known limitation with acceptable risk |

## Shared Assumptions

| # | Agreement Source | Assumption | Classification | Promoted |
|---|-----------------|-----------|----------------|----------|
| A-001 | All variants agree on root cause | `_sanitize_output` returns 0 without writing stripped content when content has leading whitespace before `---` | STATED | No |
| A-002 | All variants agree `_inject_pipeline_diagnostics` has same bug | The extract step could be affected by the same leading-whitespace issue | UNSTATED — no variant provides evidence the extract step has actually failed | Yes |
| A-003 | All variants agree atomic write is needed | Leading whitespace removal must use atomic write (tmp + os.replace) to prevent partial file states | UNSTATED — no variant explains why simple write_text would be insufficient (Python's write_text is already atomic at the OS level for small files) | Yes |

## Summary
- Total structural differences: 3
- Total content differences: 8
- Total contradictions: 2
- Total unique contributions: 5
- Total shared assumptions surfaced: 3 (UNSTATED: 2, STATED: 1, CONTRADICTED: 0)
- Highest-severity items: C-002, C-003, C-004 (all High)
