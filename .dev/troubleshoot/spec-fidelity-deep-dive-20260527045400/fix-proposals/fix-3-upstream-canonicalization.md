# Fix Proposal #3 — Upstream canonicalization in spec_parser (Tier 2 / refactoring-expert)

## Problem statement

The recurrence is the visible failure mode of a MISSING DOMAIN ABSTRACTION. Raw `str` flows from `spec_parser.extract_requirement_ids` (lines 333-344) into `check_signatures` (lines 372-391) and is compared with raw `set`-difference at line 380. The extractor's regex is lenient (`\bD-?\d+\b`); the comparator's `==` is strict. **That asymmetry is inevitable whenever a primitive crosses a module seam without a canonicalization owner.** Tier 1's checker-side fix re-introduces the same primitive obsession one rule_id over (next checker that consumes `parsed.requirement_ids` will repeat the bug). The structurally correct move is to canonicalize at the SOURCE so canonical IDs flow downstream by construction.

## Proposed change

ONE module: `src/superclaude/cli/roadmap/spec_parser.py`. Refactoring move: Extract Helper + Move Method (Fowler).

1. Add module-private `_canonicalize_requirement_id(family: str, raw: str) -> str` helper directly above `_REQUIREMENT_PATTERNS` (~line 324). Strips leading zeros from numeric tail while preserving family prefix and sub-ID structure (`D01` → `D1`; `FR-7.1` → `FR-7.1` unchanged; `NFR-02` → `NFR-2`). Pure function, no I/O.

2. Modify `extract_requirement_ids` at lines 333-344:
   ```python
   for family, pattern in _REQUIREMENT_PATTERNS.items():
       raw_ids = pattern.findall(text)
       canonical = [_canonicalize_requirement_id(family, r) for r in raw_ids]
       ids = sorted(set(canonical))
       if ids:
           result[family] = ids
   ```

3. **`structural_checkers.py` is NOT modified.** Because `spec_parsed.requirement_ids` and `roadmap_parsed.requirement_ids` now both contain canonical forms, `phantom_ids = roadmap_ids - spec_ids` becomes correct as written.

~12 lines added, 3 modified in `spec_parser.py`. Zero changes elsewhere.

## Evidence

- `src/superclaude/cli/roadmap/spec_parser.py:329` — lenient regex
- `src/superclaude/cli/roadmap/spec_parser.py:333-344` — `extract_requirement_ids` returns raw matched strings
- `src/superclaude/cli/roadmap/structural_checkers.py:372-391` — seam where primitive obsession surfaces
- `src/superclaude/cli/roadmap/integration_contracts.py:445-469` — `_canonicalize_identifiers` precedent (same pattern, sibling module)
- `historical-context.md` Section 4 — "ID-schema normalization not present in any backlog" (the missing-abstraction signal)

## Risks

- **Round-trip surprise**: callers downstream of `extract_requirement_ids` that expect verbatim source form (e.g. for `Finding.roadmap_quote` at structural_checkers.py:389) will now receive canonical form. Mitigation: store both, or accept canonical-only.
- **Hidden cross-family collisions**: if `D1` and `D01` legitimately mean different requirements, they collide. Mitigation: emit warning at parse time when `extract_requirement_ids` collapses two distinct raw forms into one canonical.
- **Family-specific canonicalization**: must dispatch on `family`, not blanket zero-strip. Unit-tested across all 5 families.
- **Doesn't address binary pass condition brittleness** — S6 latent defect for non-ID failure shapes remains.

## Test plan

- New: `tests/cli/roadmap/test_spec_parser.py::test_canonicalize_zero_padded_d_ids` — feed `"D1, D01, D5"`, assert `{"D": ["D1", "D5"]}`
- New: `tests/cli/roadmap/test_spec_parser.py::test_canonicalize_idempotent_on_unpadded` — feed `"D1, D3, D5"`, assert `{"D": ["D1", "D3", "D5"]}`
- New: `tests/cli/roadmap/test_structural_checkers.py::test_phantom_id_no_false_positive_on_zero_pad_drift` — spec with `D1,D3,D5`, roadmap with `D01..D54` → `D02,D04,D06..D54` HIGH; `D01,D03,D05` not flagged
- Regression: existing `_REQUIREMENT_PATTERNS` tests pass; regex unchanged

## Documented constraints to honor

### Restrictions
1. Module ownership — parser owns FR-2/FR-5 (extraction); canonicalization-as-part-of-extraction is within mandate. Checker code untouched. [RESPECTED]
2. Pure-function contract — `_canonicalize_requirement_id(family, raw) → str` is pure. [RESPECTED]
3. 30% diff guard — ~12 LOC in `spec_parser.py` (~700+ LOC file). [RESPECTED]
4. Binary pass condition — fix produces 0 phantom_id HIGHs for drift; pass condition unmodified. [RESPECTED]
5. Spec is input. [RESPECTED]
6. `max_runs=3`. [RESPECTED]
7. Canonicalization precedent — structurally identical to `integration_contracts.py:445`. Two sibling canonicalizers emerge as a consistent project pattern. [LEVERAGED]

### Re-frame signals
1. No shipped fix has touched the comparator — this fix removes the seam ENTIRELY rather than patching the comparator. [ADDRESSES at a deeper level]
2. Failure shape has shifted — eliminating the asymmetric-seam pattern forecloses the recurrence VECTOR across all 5 checker consumers of `parsed.requirement_ids`. [ADDRESSES]
3. Chosen remediation surface is `structural_checkers.py` — DEVIATES — this fix locates in `spec_parser.py` instead. **Justification**: the re-frame signal lists the *expected* remediation surface based on the bug's visible symptom (the checker); the refactoring lens argues the structural fix belongs UPSTREAM. The two are not strict contradictions — the re-frame signal is advisory, not constraining. [DEVIATES with explicit justification]
