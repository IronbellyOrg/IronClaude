# Fix B Proposal: Mechanism-Aware Dedup + Tightened Extractor + Stem Coverage

**Author:** Sonnet lane
**Date:** 2026-05-25
**Target module:** `src/superclaude/cli/roadmap/integration_contracts.py`
**Target tests:** `tests/roadmap/test_integration_contracts.py`, `tests/roadmap/test_anti_instinct_integration.py`

---

## Problem Framing

The anti-instinct gate produces false-positive uncovered contracts because:
(1) `DISPATCH_PATTERNS[0]` contains a bare `DISPATCH` alternation that matches narrative prose like "priority dispatch" and "dispatch tick"; (2) dedup keys on the raw evidence line, so 4 lines about the same hub-dispatch mechanism become 4 contracts; (3) the broad coverage check requires the full mechanism term (e.g. "dispatch table") as a substring, but the roadmap uses compound phrases like "class-priority dispatch" that lack the word "table". All three factors compound: over-extraction multiplies contracts, dedup fails to collapse them, and the coverage checker cannot match the roadmap's phrasing for any of the duplicates.

## Proposed Solution: Three-Part Coherent Fix

The highest-leverage intervention is a **semantic-dedup-first** approach: collapse contracts at the mechanism level, tighten the extractor to reduce noise, and broaden coverage matching to accept compound dispatch phrases. All three changes are in one file (`integration_contracts.py`) and are mutually reinforcing.

### Part 1: Tighten DISPATCH_PATTERNS[0] (lines 20-27)

Remove the bare `DISPATCH` alternation. Keep `dispatch[_\s]?table`, `DISPATCH_TABLE`, and the other specific nouns. The bare word catches narrative ("priority dispatch", "dispatch tick", "dispatch order") that is not an integration-point declaration.

**Before** (line 22-25):
```python
re.compile(
    r"\b(?:dispatch[_\s]?table|RUNNERS|_RUNNERS|HANDLERS|"
    r"DISPATCH|routing[_\s]?table|command[_\s]?map|step[_\s]?map|"
    r"plugin[_\s]?registry)\b",
    re.IGNORECASE,
),
```

**After:**
```python
re.compile(
    r"\b(?:dispatch[_\s]?table|DISPATCH_TABLE|RUNNERS|_RUNNERS|HANDLERS|"
    r"routing[_\s]?table|command[_\s]?map|step[_\s]?map|"
    r"plugin[_\s]?registry)\b",
    re.IGNORECASE,
),
```

Changes:
- Removed bare `DISPATCH` (the over-capture source)
- Added explicit `DISPATCH_TABLE` as a distinct alternative (it was previously matched by `DISPATCH` prefix only)

This prevents lines like "So that priority dispatch cannot be undermined" and "When the next dispatch tick runs" from being extracted. It preserves matching on `DISPATCH_TABLE` (all caps), `dispatch table`, `dispatch_table`, `Dispatch Table`, etc.

### Part 2: Mechanism-aware dedup (lines 163-202)

Replace the `seen_evidence: set[str]` dedup with a composite key that collapses contracts sharing the same mechanism AND overlapping identifiers. The insight: if two evidence windows both mention `Interactive`, `Coalescible`, `Bulk`, and `dispatch`, they are the same hub-dispatch contract.

**New helper function** (insert before `extract_integration_contracts`, ~line 150):

```python
def _dedup_key(mechanism: str, context: str) -> str:
    """Build a dedup key from mechanism + specific identifiers in context.

    Contracts sharing the same mechanism AND >= 2 UPPER_SNAKE or
    PascalCase identifiers are considered duplicates. Falls back to
    mechanism alone if fewer than 2 identifiers exist (preserves
    current behavior for low-signal matches).
    """
    idents = sorted(set(re.findall(r"\b[A-Z][A-Z0-9_]{2,}\b", context)
                        + re.findall(r"\b[A-Z][a-z]+(?:[A-Z][a-z]+)+\b", context)))
    if len(idents) >= 2:
        return f"{mechanism}::{'+'.join(idents)}"
    # Low-signal: use a hash of the evidence to preserve per-line behavior
    return f"{mechanism}::line_{hash(context.strip())}"
```

**Modify `extract_integration_contracts`** (lines 163-202):

Replace `seen_evidence: set[str]` with `seen_keys: set[str]`:

```python
def extract_integration_contracts(spec_text: str) -> list[IntegrationContract]:
    contracts: list[IntegrationContract] = []
    lines = spec_text.splitlines()
    seen_keys: set[str] = set()  # dedup by mechanism+identifiers
    counter = 1

    for i, line in enumerate(lines):
        stripped = line.lstrip()
        if stripped.startswith("#") or stripped.startswith("- ["):
            continue

        for pattern in DISPATCH_PATTERNS:
            match = pattern.search(line)
            if match:
                evidence = line.strip()
                # FR-MOD2.2: Context capture (3 lines before/after)
                context_start = max(0, i - 3)
                context_end = min(len(lines), i + 4)
                context = "\n".join(lines[context_start:context_end])

                mechanism = _classify_mechanism(match.group(0))
                key = _dedup_key(mechanism, context)
                if key in seen_keys:
                    continue
                seen_keys.add(key)

                contracts.append(
                    IntegrationContract(
                        id=f"IC-{counter:03d}",
                        mechanism=mechanism,
                        spec_evidence=context,
                        spec_location=f"line {i + 1}",
                        description=f"{mechanism}: {evidence}",
                        requires_explicit_wiring=True,
                    )
                )
                counter += 1

    return contracts
```

Key behavioral change: with the tightened extractor from Part 1, lines 430 ("priority dispatch") and 1031 ("dispatch tick") are no longer matched at all. But even if some future pattern captures them, the dedup would collapse them with IC-005/IC-010 because all share mechanism `dispatch_table` and identifiers `Interactive`, `Coalescible`, `Bulk`.

**Backward compat note:** The existing `TestDeduplication.test_duplicate_lines_deduplicated` passes because 3 identical lines produce the same context (same identifiers), so the same dedup key, so they collapse to 1. The `test_sequential_id_assignment` test passes because IDs are still sequential (just fewer of them if dedup collapses).

### Part 3: Stem-based coverage fallback (lines 261-297)

Add a stem-matching fallback in the FR-MOD2.7 broad coverage block. When the full mechanism term (e.g. "dispatch table") is not found, try the head noun ("dispatch") as a substring match, but only when it co-occurs with an impl verb on the same line (not the 3-line window, to avoid false positives from bare "dispatch" in table-of-contents or metadata lines).

**Replace the FR-MOD2.7 block** (lines 261-297) with:

```python
        # FR-MOD2.7: Broad mechanism-term coverage check.
        if not covered:
            mechanism_term = contract.mechanism.replace("_", " ")
            raw_terms = [mechanism_term]
            if "middleware" in contract.description.lower():
                raw_terms.append("middleware")
            if "strategy" in contract.description.lower():
                raw_terms.append("strategy")

            # FR-MOD2.7a: Stem fallback for compound mechanisms.
            # For mechanisms like "dispatch_table", also try the head
            # noun ("dispatch") as a looser match, but only when it
            # co-occurs with an impl verb on the SAME line.
            stem_terms = []
            for mt in raw_terms:
                parts = mt.split()
                if len(parts) >= 2:
                    stem_terms.append(parts[0])  # "dispatch" from "dispatch table"

            impl_verbs = re.compile(
                r"\b(?:implement|configure|add|create|set\s*up|deploy|"
                r"build|integrate|wire|enable|install|bound|attach|"
                r"apply|use|route|log|emit|handle)\b",
                re.IGNORECASE,
            )
            # Full mechanism term with 3-line window (existing behavior)
            for mterm in raw_terms:
                for j, rline in enumerate(roadmap_lines):
                    if mterm.lower() in rline.lower():
                        if impl_verbs.search(rline):
                            covered = True
                            evidence = rline.strip()
                            location = f"line {j + 1}"
                            break
                        window_start = max(0, j - 2)
                        window_end = min(len(roadmap_lines), j + 3)
                        window_text = " ".join(roadmap_lines[window_start:window_end])
                        if impl_verbs.search(window_text):
                            covered = True
                            evidence = rline.strip()
                            location = f"lines {window_start + 1}-{window_end}"
                            break
                if covered:
                    break

            # FR-MOD2.7a: Stem fallback — head noun + impl verb on SAME line only
            if not covered:
                for stem in stem_terms:
                    for j, rline in enumerate(roadmap_lines):
                        if stem.lower() in rline.lower() and impl_verbs.search(rline):
                            covered = True
                            evidence = rline.strip()
                            location = f"line {j + 1}"
                            break
                    if covered:
                        break
```

This catches the TUIBBS-scp case: roadmap line 392 says "Implement the single-goroutine inter-session message hub with typed class-priority dispatch". The stem "dispatch" appears on the same line as impl verb "Implement" -> covered.

The same-line constraint prevents false positives: a line like "|class-priority dispatch table|Yes|M5|" has no impl verb, so it would not match via stem (it would only match via full-term, which is the existing behavior).

---

## Test Plan

All new tests go in `tests/roadmap/test_integration_contracts.py` using reduced fixtures extracted from the TUIBBS-scp corpus.

### Test Case 1: Narrative "dispatch" prose is not extracted

```python
TUIBBS_HUB_NARRATIVE_SPEC = """\
- Hub class-priority: `Interactive > Coalescible > Bulk` dispatch order; load-bearing for FR-S10-02 backpressure.
- So that priority dispatch cannot be undermined by mis-tagged messages.
- When the next dispatch tick runs, all Interactive messages are sent before any Coalescible.
"""

def test_bare_dispatch_narrative_not_extracted():
    """Lines like 'priority dispatch' and 'dispatch tick' are NOT contracts."""
    contracts = extract_integration_contracts(TUIBBS_HUB_NARRATIVE_SPEC)
    dispatch_contracts = [c for c in contracts if c.mechanism == "dispatch_table"]
    # None of the 3 lines contain "dispatch table" or DISPATCH_TABLE;
    # bare "dispatch" should no longer match.
    assert len(dispatch_contracts) == 0
```

### Test Case 2: Mechanism-level dedup collapses hub-dispatch variants

```python
TUIBBS_HUB_DISPATCH_SPEC = """\
The DISPATCH_TABLE maps message classes to runners.
Populate the dispatch table with Interactive, Coalescible, Bulk handlers.
Hub class-priority: Interactive > Coalescible > Bulk dispatch order.
"""

def test_mechanism_dedup_collapses_same_identifiers():
    """Multiple lines about the same dispatch_table + same identifiers -> 1 contract."""
    contracts = extract_integration_contracts(TUIBBS_HUB_DISPATCH_SPEC)
    dispatch_contracts = [c for c in contracts if c.mechanism == "dispatch_table"]
    assert len(dispatch_contracts == 1), (
        f"Expected 1 dispatch_table contract, got {len(dispatch_contracts)}: "
        f"{[c.spec_location for c in dispatch_contracts]}"
    )
```

### Test Case 3: Stem coverage matches "class-priority dispatch" roadmap prose

```python
TUIBBS_ROADMAP = """\
## M5: Hub

Implement the single-goroutine inter-session message hub with typed class-priority dispatch.
Single goroutine message broker with class-priority dispatch in internal/hub/.
"""

def test_stem_coverage_matches_compound_dispatch():
    """'class-priority dispatch' in roadmap covers a dispatch_table contract."""
    # Use a spec that produces a dispatch_table contract
    spec = "The DISPATCH_TABLE maps message classes to runners."
    contracts = extract_integration_contracts(spec)
    assert len(contracts) >= 1
    result = check_roadmap_coverage(contracts, TUIBBS_ROADMAP)
    assert result.all_covered, (
        f"Expected all covered. Uncovered: "
        f"{[c.contract.id for c in result.coverage if not c.covered]}"
    )
```

### Test Case 4: Existing dispatch-table detection preserved

The existing `test_category1_dispatch_table` fixture (`DISPATCH_TABLE_SPEC`) must still extract >= 1 contract with mechanism `dispatch_table`. No change needed -- run the existing test suite.

### Test Case 5: cli-portify regression still caught

The existing `test_detects_programmatic_runners_without_wiring` must still fail on `CLI_PORTIFY_BAD_ROADMAP`. The tightened extractor does not affect this because `PROGRAMMATIC_RUNNERS` and `DISPATCH_TABLE` are still in the pattern. No change needed.

### Test Case 6: Existing identical-line dedup still works

The existing `test_duplicate_lines_deduplicated` (3 identical DISPATCH_TABLE lines -> 1 contract) must still pass. The new `_dedup_key` will produce the same key for all 3 because they share the same mechanism and same identifiers (or, if identifiers < 2, fall back to line hash, which is identical for identical lines). Must verify this does not break. **Potential issue**: if the 3 identical lines have 0 identifiers, the fallback uses `hash(context.strip())` which is identical, so they still collapse. Passes.

---

## Backward-Compatibility Analysis

### Existing tests in `test_integration_contracts.py`

| Test | Impact | Action |
|------|--------|--------|
| `test_category1_dispatch_table` | None. Spec mentions `DISPATCH_TABLE` (uppercase) and `dispatch table` (compound), both still in the pattern. | No change |
| `test_category2_plugin_registry` through `test_category7_di_container` | None. These patterns are unchanged. | No change |
| `test_all_categories_detected` | None. `dispatch_table` still detected from the DISPATCH_TABLE_SPEC fixture. | No change |
| `test_covered_roadmap_passes` | None. GOOD_ROADMAP has "Create the dispatch table" -- full term match. | No change |
| `test_uncovered_roadmap_fails` | None. BAD_ROADMAP lacks any dispatch/wiring language. | No change |
| `test_coverage_evidence_recorded` | None. Same flow. | No change |
| `test_duplicate_lines_deduplicated` | **Must verify.** With `_dedup_key`, 3 identical lines with DISPATCH_TABLE: context is identical, so `hash(context.strip())` is the same for all 3, so they collapse to 1. | No change expected |
| `test_sequential_id_assignment` | **Potentially affected.** If dedup collapses some contracts that were previously distinct, the ID sequence has fewer entries. The test uses `ALL_CATEGORIES_SPEC` which has diverse mechanisms -- unlikely to have identifier-overlap collisions. | Verify; likely passes |
| `test_upper_snake_case_detected` | None. | No change |
| `test_named_mechanism_in_roadmap_coverage` | None. | No change |
| `test_detects_programmatic_runners_without_wiring` | None. CLI_PORTIFY_SPEC mentions `PROGRAMMATIC_RUNNERS` and `DISPATCH_TABLE` which are still matched. | No change |
| `test_total_contracts_detected` | Minor. Total count might decrease by 1 if dedup collapses `PROGRAMMATIC_RUNNERS` + `DISPATCH_TABLE` (both mechanism=dispatch_table, both have `PROGRAMMATIC_RUNNERS` identifier). Test asserts `>= 1` so it passes regardless. | No change |

### Existing tests in `test_anti_instinct_integration.py`

| Test | Impact | Action |
|------|--------|--------|
| `TestAntiInstinctInPipeline` (5 tests) | None. These test pipeline wiring, not contract content. | No change |
| `test_obligation_scanner_finds_undischarged` | None. Different checker. | No change |
| `test_integration_contracts_find_uncovered` | **Verify.** Uses `_make_bad_spec` which contains `PROGRAMMATIC_RUNNERS` and `DISPATCH_TABLE`. Tightened extractor still matches both. Dedup might collapse them (same mechanism, shared identifiers `PROGRAMMATIC_RUNNERS`, `_run_extract`, `_run_generate`, `_run_merge`). If dedup collapses them, `uncovered_count` might change from >1 to 1. Test asserts `> 0`, so it passes. | Verify; likely passes |
| `test_fingerprint_coverage_low` | None. | No change |
| `test_anti_instinct_gate_blocks_bad_roadmap` | Same reasoning as above. Gate still blocks because uncovered_count > 0. | Verify; likely passes |
| `test_all_three_semantic_checks_triggered` | Same reasoning. >= 2 checks still fail. | Verify; likely passes |
| `TestGatePassesGoodRoadmap` (2 tests) | None. Good spec has no dispatch patterns. | No change |
| `TestStructuralAuditWarningOnly` (3 tests) | None. | No change |
| `TestAuditOutputFormat` (5 tests) | None. | No change |
| `TestSemanticCheckFunctions` (8 tests) | None. These parse frontmatter strings. | No change |

### Risk summary

The highest risk is that the `_dedup_key` fallback for low-identifier contexts (the `hash(context.strip())` path) might produce unintended collisions if two genuinely different contracts happen to have identical evidence text. This is extremely unlikely in practice (identical evidence means identical contracts), and the existing test suite covers this via `test_duplicate_lines_deduplicated`.

The second risk is that tightening `DISPATCH_PATTERNS[0]` might miss a spec that uses bare `DISPATCH` as the sole indicator of a dispatch-table integration point. Mitigation: the stem coverage fallback in Part 3 ensures that even if a contract IS extracted by some other pattern, the roadmap check is more forgiving.

---

## Confidence + Strongest Counter-Argument

**Confidence: 85%**

The three-part fix is internally coherent: tighten extraction to prevent noise, dedup more aggressively to collapse what gets through, and widen coverage matching to accept natural-language phrasing. Each part independently reduces the false-positive count, and together they address all three contributing factors from the diagnosis.

**Strongest counter-argument:** The stem coverage fallback (Part 3) introduces a semantic looseness that could produce false *negatives* (i.e., falsely marking a contract as "covered" when it isn't really wired). Consider a roadmap line like "Implement priority dispatch for logging" that has nothing to do with the hub's class-priority dispatch table. The stem "dispatch" + impl verb "Implement" would match, marking the contract covered even though the roadmap describes a different dispatch concern. This is mitigated by the same-line constraint (no window expansion for stem matches) and by the fact that Part 1 already prevents extraction of most narrative "dispatch" mentions, but it remains a theoretical concern for specs where "dispatch" appears in multiple unrelated contexts. If this materializes in practice, the fix is to add a secondary check that the stem match's surrounding context shares at least one identifier with the contract's spec_evidence.
