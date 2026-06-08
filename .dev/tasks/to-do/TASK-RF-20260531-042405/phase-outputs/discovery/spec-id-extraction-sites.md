# Spec-ID Extraction Sites Inventory (Phase 2 / Step 2.1)

**Scope:** `src/superclaude/cli/roadmap/*.py` only (Phase 2 R0.1 boundary).
**Method:** `grep -rn '(FR|NFR|SC|D|G)-\d'` plus targeted reads.
**Authority:** R1 file inventory `research/01-file-inventory.md` §A.7 (`spec_parser.extract_requirement_ids` L333) and §A.4 (`fidelity_checker._extract_fr_mappings`).

## Inventory Table

| File | Line | Pattern (regex literal) | Consumer (function/class) | Migrates to id_registry? |
|---|---|---|---|---|
| `spec_parser.py` | 325 | `r"\bFR-\d+(?:\.\d+)?\b"` | `_REQUIREMENT_PATTERNS["FR"]` (canonical ID extractor) | **Y (CANONICAL SOURCE)** — `id_registry.build_id_registry` REUSES this via `extract_requirement_ids`; no duplication. |
| `spec_parser.py` | 326 | `r"\bNFR-\d+(?:\.\d+)?\b"` | `_REQUIREMENT_PATTERNS["NFR"]` | Y (canonical) — reused by id_registry. |
| `spec_parser.py` | 327 | `r"\bSC-\d+\b"` | `_REQUIREMENT_PATTERNS["SC"]` | Y (canonical) — reused by id_registry. |
| `spec_parser.py` | 328 | `r"\bG-\d+\b"` | `_REQUIREMENT_PATTERNS["G"]` | Y (canonical) — reused by id_registry. |
| `spec_parser.py` | 329 | `r"\bD-?\d+\b"` | `_REQUIREMENT_PATTERNS["D"]` (lenient — matches both `D5` and `D-5`; master:§Recurrence #4 incident A12:F-A12-01 cites this asymmetry vs strict comparator producing 54 phantom_id HIGHs) | Y (canonical) — reused by id_registry. R1.1 may canonicalize via `superclaude.contracts.ID_PATTERNS`. |
| `spec_parser.py` | 333 | n/a — function | `extract_requirement_ids(text) -> dict[str, list[str]]` | Y (canonical extractor) — `id_registry.build_id_registry` calls into this. |
| `spec_parser.py` | 619 | n/a — call site | `parse_document` (consumes own extractor) | N — already canonical; not a new site. |
| `fidelity_checker.py` | 44 | `r"^#{1,6}\s+.*?\b(FR-\d+(?:\.\d+)?)\b"` | `_FR_HEADING_RE` — captures FR ID **co-located with section heading** for `_extract_fr_mappings` (FR→name→symbol traceability) | **N (SPECIALIZED CONSUMER)** — pattern includes heading-anchor context (`^#{1,6}\s+`), purpose is heading-binding not ID-extraction. R0.1 leaves it untouched; R1.5 verify-implementation step may consolidate when AST-link replaces text-link. |
| `structural_checkers.py` | 311 | n/a — comment only | comment cites `spec_parser.extract_requirement_ids` as the source of canonical IDs flowing downstream | N — already cites canonical source; no regex literal. PRESERVE per MVR §3. |

## Conclusions

1. **No new ID regex literals exist outside `spec_parser._REQUIREMENT_PATTERNS`.** The Contract #9 work is upstream-only: `id_registry` BUILDS a typed registry from `spec_parser.extract_requirement_ids`; it does NOT redefine patterns.
2. **The one specialized pattern (`fidelity_checker._FR_HEADING_RE`)** is heading-anchored (`^#{1,6}\s+`), not a general extractor. It survives R0.1 unchanged; consolidating it is R1.5 work (verify-implementation AST link).
3. **No anti-pattern hand-rolled regexes detected** in `cli/roadmap/` outside spec_parser. Contract #9 "ID set containment" can be enforced purely by:
   - `id_registry.build_id_registry(spec_path)` → calls `extract_requirement_ids(spec_text)` (no new regex).
   - MERGE_GATE SemanticCheck `_roadmap_ids_within_spec(content)` → calls `extract_requirement_ids(roadmap_text)` and asserts the merged set is a subset of `registry.union_of_known()`.
4. **R0.1 introduces ZERO new regex literals** — Contract #8 (anti-duplication) is satisfied by reuse.

## Migration Targets (production extractors that should consult `id_registry` in later phases)

- R1.1 (`superclaude.contracts.ID_PATTERNS`): Hoist `spec_parser._REQUIREMENT_PATTERNS` into `superclaude.contracts.ID_PATTERNS` and have `spec_parser` and `id_registry` BOTH import from there. R0.1 leaves a `# R0.3: import from superclaude.contracts.ID_PATTERNS` TODO in `id_registry.py` so the audit trail is visible.
- R1.5 (verify-implementation): `fidelity_checker._extract_fr_mappings` may be replaced by AST-link directly; the heading-anchored regex retires then.

## Source-Authority Citations

- master:§Recurrence #4 — phantom-ID HIGH recurrence (A12:F-A12-01) — 54 HIGHs from `\bD-?\d+\b` lenient extractor vs strict comparator (the canonical incident this phase prevents).
- master:§Flaw 4 — fail-open default in `fidelity_checker.py` L287-303 (separate phase, not Phase 2).
- BUILD-REQUEST §R0 item 1 — Spec-ID registry shipped.
- BUILD-REQUEST §Contract item #9 — roadmap_ids ⊆ spec_ids ∪ accepted_deviations.
- research/01-file-inventory.md §A.7 — `spec_parser.extract_requirement_ids` L333 (R0.1 primary site for ID_PATTERNS consumer).
- research/01-file-inventory.md §A.4 — `fidelity_checker._extract_fr_mappings` L283 currently consumes ad-hoc ID regexes.
