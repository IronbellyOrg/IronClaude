# Fix Proposal #1 — Minimal canonicalizer + drift demotion (Tier 1 / root-cause-analyst)

## Problem statement

`structural_checkers.py:380` computes `phantom_ids = roadmap_ids - spec_ids` via raw Python set difference of strings. The extraction regex at `spec_parser.py:329` (`\bD-?\d+\b`) is lenient (matches `D1` and `D01` and `D-01`) but emits raw matched form. TUIBBS has spec={D1,D3,D5}, roadmap={D01..D54}, producing 54 ACTIVE HIGH phantom_id findings whose only correct fix exceeds the 30% diff guard. The convergence loop has no MANUAL_TRIAGE escape, so it burns 3 runs and halts with a misleading TurnLedger budget message.

## Proposed change

ONE module: `src/superclaude/cli/roadmap/structural_checkers.py`.

1. Add `_canonicalize_requirement_id(pid: str) -> str` helper near `_make_finding` (~line 260). Pure function. Strips leading zeros within the numeric tail of the matched ID, preserves family prefix and sub-IDs (e.g. `D01` → `D1`; `FR-7.1` → `FR-7.1` unchanged; `NFR-02` → `NFR-2`).

2. In `check_signatures` lines 372-391, compute both:
   ```python
   spec_canon = {_canonicalize_requirement_id(p): p for p in spec_ids}
   roadmap_canon = {_canonicalize_requirement_id(p): p for p in roadmap_ids}
   drift = {raw for canon, raw in roadmap_canon.items() if canon in spec_canon and raw not in spec_ids}
   genuine_phantom = {raw for canon, raw in roadmap_canon.items() if canon not in spec_canon}
   ```

3. Emit `drift` findings via `_make_finding` with `mismatch_type="id_schema_drift"`, `severity="MEDIUM"`, `fix_guidance="Spec uses '{spec_form}' form; roadmap uses '{roadmap_form}' form. Either normalize roadmap to spec or canonicalize the comparator — does not block convergence."`

4. Emit `genuine_phantom` findings via the existing `_make_finding` call (current behavior, HIGH `phantom_id`).

## Evidence

- `src/superclaude/cli/roadmap/structural_checkers.py:380` — the raw set difference
- `src/superclaude/cli/roadmap/spec_parser.py:329` — lenient extraction regex
- `src/superclaude/cli/roadmap/integration_contracts.py:445` — `_canonicalize_identifiers` (precedent)
- `/config/workspace/TUIBBS-scp/.dev/releases/current/v1-MVP/deviation-registry.json` — 54 identical-shape findings

## Risks

- False normalization: collapsing `D1` and `D01` may hide a project where they mean different requirements (very rare; mitigated by canonical-form match check)
- Family-specific regex care needed for FR-7.1 vs FR-7-1 style sub-IDs
- Other rule_ids (function_missing, etc.) may exhibit similar drift; this fix only addresses phantom_id
- MEDIUM-spike side effects on downstream gates that count MEDIUMs

## Test plan

- New: `tests/cli/roadmap/test_structural_checkers.py::test_phantom_id_canonicalizes_zero_padded_d_ids` — spec={D1,D3,D5} roadmap={D01,D03,D05} → 0 HIGH, 3 MEDIUM id_schema_drift
- New: `tests/cli/roadmap/test_structural_checkers.py::test_phantom_id_genuine_phantom_still_emits_high` — spec={D1,D3} roadmap={D01,D99} → 1 HIGH (D99) + 1 MEDIUM (D01↔D1)
- New: `tests/cli/roadmap/test_convergence.py::test_id_schema_drift_does_not_block_pass` — registry with only id_schema_drift MEDIUMs → passes on Run 1
- Regression: existing genuine-phantom tests still emit HIGH

## Documented constraints to honor

(Verbatim from `doc-context.md` — Restrictions and Re-frame signals)

### Restrictions
1. Module ownership: comparator changes belong in `structural_checkers.py` (FR-1, FR-3). [COMPLIES]
2. Pure-function contract (NFR-4) — checkers are pure over frozen SpecData/RoadmapData. [COMPLIES — helper is pure str→str]
3. 30% diff guard is per-patch. [COMPLIES — ~15 LOC in a 700-line file = ~2% diff]
4. Pass condition is strictly binary: `active_highs == 0`. No MANUAL_TRIAGE; S6 stays deferred. [COMPLIES — does not touch convergence.py]
5. Spec is an input the agent cannot modify. [COMPLIES — no spec edits]
6. `max_runs=3` is the default. [COMPLIES — not touched]
7. Precedent for canonicalization exists locally at `integration_contracts.py:445`. [LEVERAGED — same pattern]

### Re-frame signals
1. No shipped fix has touched the comparator — this fix does. [ADDRESSES]
2. Failure shape has shifted again; surgical phantom_id fix without structural escape leaves next shape unguarded. [PARTIAL — does NOT add structural escape for next shape]
3. Chosen remediation surface is `structural_checkers.py`. [ALIGNED]
