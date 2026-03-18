# Gap #3: `domains_detected` Type Change -- Implementation Proposal

## Problem Statement

The source protocol in `src/superclaude/skills/sc-roadmap-protocol/refs/templates.md` (line 408) defines `domains_detected` as a **YAML array of domain names**:

```yaml
domains_detected: [<domain1>, <domain2>]
```

The CLI extract prompt in `src/superclaude/cli/roadmap/prompts.py` (line 89) requests it as an **integer count**:

```
- domains_detected: (integer) count of distinct technical domains identified
```

The generate prompt (line 146) references it ambiguously as:

```
- domains_detected: number of technical domains to address
```

This means domain identity is lost at extraction time, which has downstream consequences.

---

## Analysis of the Four Key Questions

### 1. Does the CLI pipeline currently do any template matching that needs domain names?

**No -- not in the Python CLI code.** The CLI pipeline (`prompts.py`, `gates.py`, executor) does not perform template compatibility scoring in Python. The template matching logic lives entirely in the skill protocol (`refs/scoring.md`, `refs/templates.md`) and is executed by the LLM as part of the sc:roadmap skill's Wave 2 (Planning & Template Selection).

However, the **source protocol's template compatibility scoring** uses domain names directly. From `refs/scoring.md` line 69:

> `domain_match` (weight 0.40): Jaccard similarity between template's `domains` field and spec's detected domains

This is the highest-weighted factor in template scoring. It requires actual domain names (e.g., `[backend, security]`) to compute Jaccard similarity against a template's `domains: [backend, performance]` field. An integer count cannot participate in set intersection/union.

The **milestone count formula** in `refs/templates.md` line 93 also uses domain count:

> `base + floor(domain_count / 2)`

This only needs a count, but the domain-specific milestone mapping (lines 99-109) needs domain names to determine milestone types (e.g., "security" domain generates a SECURITY-type milestone).

**Conclusion**: The skill protocol needs domain names. The CLI pipeline currently only validates field presence, not content, so it is agnostic to type.

### 2. Would changing from integer to array break the gate's frontmatter validation?

**No.** The `EXTRACT_GATE` in `gates.py` (line 523-541) lists `domains_detected` in `required_frontmatter_fields`. The gate validation in `src/superclaude/cli/pipeline/gates.py` only checks **field presence** -- it looks for `domains_detected:` as a key in the YAML frontmatter and verifies the key exists. It does not parse or validate the value type.

The `_check_frontmatter` function (pipeline `gates.py` lines 78-108) splits on `:` and checks if the key name appears. Both formats produce a valid `key: value` line:

- `domains_detected: 3` -- key `domains_detected` found
- `domains_detected: [backend, security, frontend]` -- key `domains_detected` found

The `_frontmatter_values_non_empty` semantic check (roadmap `gates.py` line 101-119) splits on `:` and checks that the value portion is non-empty. Both `3` and `[backend, security, frontend]` are non-empty strings after the colon.

**No existing semantic check inspects the value of `domains_detected`.**

**Conclusion**: Changing the type will not break any gate.

### 3. How does the generate prompt reference domains_detected -- does it expect a count or names?

The generate prompt (`build_generate_prompt`, line 146) says:

```
- domains_detected: number of technical domains to address
```

This is informational context for the LLM generating the roadmap. It tells the LLM "here is what this field means" so it can reference the extraction frontmatter. If `domains_detected` becomes an array, the LLM can still count it and additionally use the domain names for richer roadmap generation (e.g., creating domain-specific sections).

The generate prompt does not parse the value programmatically -- it just passes the extraction document as a `--file` input to Claude, which reads the frontmatter natively.

**Conclusion**: The generate prompt's description should be updated to match, but the LLM will handle either format gracefully.

### 4. What's the right balance between fidelity and simplicity for the CLI context?

**Recommendation: Change to array format, matching the source protocol.**

Rationale:

- **Fidelity to source of truth**: The protocol spec (`templates.md`) is the contract. The CLI is a consumer. The consumer should match the contract.
- **Zero gate breakage**: As analyzed above, no gate validation inspects the value type.
- **Domain identity enables richer downstream use**: Even in CLI-only mode (no skill protocol), domain names let the generate step produce domain-aware roadmaps. An integer `3` tells the LLM nothing about *which* domains matter.
- **Existing precedent**: Historical extraction outputs already use array format in many releases (v2.01 through v2.13, unified-audit-gating, v4.xx-SprintReportScaffolding). The integer format only appeared after the v2.17 reliability release introduced the CLI prompts.
- **Benchmark evidence**: The v2.20 baseline test-3-cascade validation explicitly flagged this as a defect: `"FR-006 requires a domain list. Found domains_detected: 7 (a count, not a list)."` (line 44 of full grep results).
- **Test impact is minimal**: Only 3 test files use integer format for `domains_detected` and need updating.

---

## Implementation Plan

### Change 1: Update extract prompt (prompts.py line 89)

**File**: `src/superclaude/cli/roadmap/prompts.py`

**Current** (line 89):
```python
"- domains_detected: (integer) count of distinct technical domains identified\n"
```

**Proposed**:
```python
"- domains_detected: (list) array of distinct technical domain names identified, e.g. [backend, security, frontend]\n"
```

### Change 2: Update generate prompt (prompts.py line 146)

**File**: `src/superclaude/cli/roadmap/prompts.py`

**Current** (line 146):
```python
"- domains_detected: number of technical domains to address\n"
```

**Proposed**:
```python
"- domains_detected: list of technical domain names to address\n"
```

### Change 3: Update test fixtures (3 files)

**File**: `tests/roadmap/test_integration_v5_pipeline.py` (line 92)
```python
# Current
"domains_detected": "3",
# Proposed
"domains_detected": "[backend, security, frontend]",
```

**File**: `tests/roadmap/test_pipeline_integration.py` (line 87)
```python
# Current
"domains_detected": "2",
# Proposed
"domains_detected": "[backend, frontend]",
```

**File**: `tests/roadmap/test_executor.py` (line 103)
```python
# Current
"domains_detected": "2",
# Proposed
"domains_detected": "[backend, frontend]",
```

### No changes needed

- **`gates.py`**: `EXTRACT_GATE` lists `domains_detected` in `required_frontmatter_fields` -- this is correct for both types (presence-only check).
- **Pipeline `gates.py`**: `_check_frontmatter` is type-agnostic. No change needed.
- **`_frontmatter_values_non_empty`**: Works with both types (checks non-empty string after colon).
- **Source protocol `templates.md`**: Already correct -- it defines the array format.

---

## Risk Assessment

| Risk | Severity | Mitigation |
|------|----------|------------|
| LLM produces integer instead of array despite prompt change | LOW | The prompt explicitly shows example format `[backend, security, frontend]`. LLMs follow examples well. If it does produce an integer, gates still pass (presence-only). |
| Downstream consumer expects integer | LOW | The generate prompt is the only downstream consumer, and it's updated in Change 2. No Python code parses the value. |
| Test breakage from fixture changes | LOW | Exactly 3 test files need updating. Changes are straightforward string replacements. |
| YAML parsing of inline arrays | LOW | YAML natively supports `[a, b, c]` flow sequence syntax. The frontmatter parser in `gates.py` treats all values as strings after the colon, so `[backend, security, frontend]` is valid. |

---

## Scope

- **Files modified**: 4 (1 source, 3 tests)
- **Lines changed**: ~6
- **Risk level**: Low
- **Breaking changes**: None
- **Gate impact**: None

---

## Validation Plan

1. Run `uv run pytest tests/roadmap/test_gates_data.py -v` -- confirms `domains_detected` still in EXTRACT_GATE required fields
2. Run `uv run pytest tests/roadmap/test_integration_v5_pipeline.py -v` -- confirms updated fixtures pass
3. Run `uv run pytest tests/roadmap/test_pipeline_integration.py -v` -- confirms updated fixtures pass
4. Run `uv run pytest tests/roadmap/test_executor.py -v` -- confirms updated fixtures pass
5. Run `make test` -- full suite regression

---

## Validation Result

**Status: PASS -- proposal is sound, with minor clarifications added below.**

Validated 2026-03-18 by automated review against source files at HEAD of `v3.0-AuditGates`.

### 1. Line numbers and code references: ACCURATE

All line references verified against source:

| Claim | File | Claimed Line | Actual Line | Match |
|-------|------|-------------|-------------|-------|
| Extract prompt `domains_detected` | `src/superclaude/cli/roadmap/prompts.py` | 89 | 89 | Yes |
| Generate prompt `domains_detected` | `src/superclaude/cli/roadmap/prompts.py` | 146 | 146 | Yes |
| `EXTRACT_GATE` definition | `src/superclaude/cli/roadmap/gates.py` | 523-541 | 523-541 | Yes |
| `_check_frontmatter` function | `src/superclaude/cli/pipeline/gates.py` | 78-108 | 78-108 | Yes |
| `_frontmatter_values_non_empty` | `src/superclaude/cli/roadmap/gates.py` | 101-119 | 101-119 | Yes |
| Test fixture `test_integration_v5_pipeline.py` | `tests/roadmap/` | 92 | 92 | Yes |
| Test fixture `test_pipeline_integration.py` | `tests/roadmap/` | 87 | 87 | Yes |
| Test fixture `test_executor.py` | `tests/roadmap/` | 103 | 103 | Yes |
| Protocol `templates.md` `domains_detected` | `src/superclaude/skills/sc-roadmap-protocol/refs/` | 408 | 408 | Yes |
| Protocol `scoring.md` `domain_match` | `src/superclaude/skills/sc-roadmap-protocol/refs/` | 69 | 69 | Yes |

### 2. Frontmatter parser handling of YAML arrays: SAFE

The `_check_frontmatter` function in `src/superclaude/cli/pipeline/gates.py` (lines 78-108) uses regex `_FRONTMATTER_RE` to extract frontmatter, then splits each line on `:` taking `key = line.split(":", 1)[0]`. For `domains_detected: [backend, security, frontend]`, this correctly extracts key `domains_detected`. The value portion is never inspected for type.

The `_parse_frontmatter` function in `src/superclaude/cli/roadmap/gates.py` (lines 129-149) similarly splits on `:` with `line.split(":", 1)` and stores the value as a string. For `[backend, security, frontend]`, the string value is non-empty and no code attempts `int()` conversion on it.

The `_frontmatter_values_non_empty` semantic check (lines 101-119) checks `if not value.strip()` -- `[backend, security, frontend]` is non-empty, so this passes.

The `EXTRACT_GATE` has `enforcement_tier="STRICT"` but defines **no `semantic_checks`**, so no value-type inspection runs on extraction output.

**Risk note**: The `_FRONTMATTER_RE` regex requires each frontmatter line to match `\w[\w\s]*:.*` (key-colon-value on a single line). The YAML block-sequence format (multiline with `- item` per line) would break this regex. However, the proposed prompt explicitly instructs inline/flow-sequence format (`e.g. [backend, security, frontend]`) which stays on one line, mitigating this risk. This is consistent with how the proposal already handles it.

### 3. Generate prompt reference: CONFIRMED needs updating

The generate prompt at line 146 says `"number of technical domains to address"` which implies integer semantics. The proposal correctly identifies this as needing an update to `"list of technical domain names to address"`.

### 4. Downstream consumers parsing as integer: NONE FOUND

Searched all files under `src/` and `tests/` for `domains_detected`. No code path calls `int()` on the `domains_detected` value. The only consumers are:

- **Gate presence check** (`_check_frontmatter`): type-agnostic, checks key existence only.
- **`_frontmatter_values_non_empty`**: checks non-empty string, type-agnostic.
- **Generate prompt description** (line 146): informational text for LLM, no parsing.
- **Test fixtures** (3 files): string values in dicts, used to construct frontmatter for gate tests. These need updating as proposed.
- **`test_gates_data.py`** (line 57): asserts `"domains_detected" in EXTRACT_GATE.required_frontmatter_fields` -- checks field name presence, not value. No change needed.

### 5. YAML array format parseability: CONFIRMED SAFE

The simple `:` split in `_parse_frontmatter` (`line.split(":", 1)`) handles `domains_detected: [backend, security, frontend]` correctly because it splits only on the first colon. The value `[backend, security, frontend]` is stored as-is as a string. No downstream code attempts to parse it as YAML or convert to a Python list.

### Additional finding: `test_gates_data.py`

The proposal lists 3 test files needing changes. A 4th test file (`tests/roadmap/test_gates_data.py`, line 57) references `domains_detected` but only checks field name presence in `EXTRACT_GATE.required_frontmatter_fields` -- no value change needed. The proposal correctly omits this file from the change list.

### Conclusion

The proposal is complete, accurate, and safe to implement as written. No corrections required.
