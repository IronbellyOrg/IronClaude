<!-- Provenance: produced by /sc:adversarial (Mode A, 2 variants) -->
<!-- Base: Variant 1 (Proposal A), modified per fault-finder INV-005 -->
<!-- Merge date: 2026-06-02 -->

# DECISION — Step 11.2 Frontmatter-Parser Remediation

## Verdict: **Proposal A′** (relocate ONE canonical parser FUNCTION; do NOT add an envelope field)

Convergence 1.00. The analysis and an independent zero-trust fault-finder agree. Confidence: high (≈95% on "A over B"; ≥95% on "no `frontmatter` field").

## Why A beats B (evidence-grounded)

1. **B is infeasible as a local change.** At gate time the envelope reaches no semantic check — `pipeline/gates.py:84` dispatches `check.check_fn(content)`, `pipeline/executor.py:267` calls `gate_passed(gate_target, step.gate)` with no envelope, and `execute_pipeline` (L63) has no envelope parameter. B therefore also requires threading the envelope through the **generic** pipeline executor (shared with sprint, `sprint/executor.py:834,842`) **and** reordering the post-step extractor (which runs at `roadmap/executor.py:1491`, after the step) to populate frontmatter before the gate.
2. **B's blast radius is 8 modules.** `SemanticCheck(` is constructed **63×** across **8 gate modules** (roadmap, validate_gates, prd, tasklist, cleanup_audit, cli_portify, audit/wiring_gate, audit/reachability). Widening `SemanticCheck.check_fn` migrates all of them.
3. **The envelope-aware tier already exists.** `CodeAssertion` (`models.py:108`, dispatched `gates.py:100` with `(envelope, repo_root)`) is the deliberate R1.3/§MVR §2 mechanism for gates that need the envelope. B duplicates it and pressures NFR-007 (pipeline ⊥ roadmap import).
4. **None of the 24 checks need cross-step state.** All 24 `_parse_frontmatter` callsites in `roadmap/gates.py` validate the frontmatter of the file they gate (9 sampled, including the cross-gate-sounding `_deviation_counts_reconciled` → cross-field within the same artifact). So B's entire justification evaporates.

## Why the envelope FIELD is dropped (corrects task Step 11.2(a))

- `tests/roadmap/test_pipeline_envelope.py:312` (`test_field_set_matches_mvr_section_1`) asserts `PipelineEnvelope`'s field set is EXACTLY the §MVR §1 8 fields (`release_id, spec_hash, spec_ids, artifacts, findings, counts, convergence, accepted_deviations`). Adding `frontmatter` breaks it.
- `PipelineEnvelope` is `@dataclass(frozen=True)` (`envelope.py:127`).
- **Zero consumers** of `envelope.frontmatter` exist in `src/superclaude/cli/` (`grep -rn "\.frontmatter"` → none).
- The 24 checks parse their own `content`, so they need no field. The field is unnecessary AND illegal.

## Authoritative Implementation Plan (replaces Step 11.2 sub-steps a/d)

1. **Add `extract_frontmatter(content: str) -> dict[str, str] | None`** to `src/superclaude/cli/roadmap/envelope.py` — the single canonical frontmatter parser (port the chosen canonical behavior; document which historical variant's semantics it preserves). A FUNCTION only.
2. **Do NOT add a `frontmatter` field** to `PipelineEnvelope`. (Supersedes Step 11.2(a) and the C1-remediation "(a) add a typed `frontmatter: dict` field".) The frozen 8-field §MVR §1 canon is preserved; `test_pipeline_envelope.py:312` stays green.
3. **Repoint the 24 in-gate semantic checks** in `roadmap/gates.py` to `from superclaude.cli.roadmap.envelope import extract_frontmatter` and call it on their existing `content`. `SemanticCheck.check_fn` signature, `gate_passed`, and `execute_pipeline` are UNCHANGED.
4. **Delete the duplicate parsers** (Contract #6): `roadmap/gates.py:_parse_frontmatter` L178, `pipeline/gates.py:_check_frontmatter` L125, `spec_parser.py:parse_frontmatter` L114, `spec_patch.py:_extract_frontmatter` L285. For `pipeline/gates.py`: its STANDARD/STRICT frontmatter check must call the canonical parser (note NFR-007 — if `pipeline/gates.py` cannot import `roadmap.envelope`, keep its frontmatter handling as the ONE canonical impl and have roadmap import from pipeline instead; choose the import direction that respects NFR-007, and document it). Cross-cutting `cli_portify/utils.py:11` + `audit/wiring_gate.py:931` import the canonical parser or are flagged for the parser-consistency lint.
5. **Cross-step escape hatch:** any check that genuinely needs a PRIOR step's parsed state becomes a `CodeAssertion` (envelope-aware tier), NOT a widened SemanticCheck. None of the current 24 qualify.
6. **Create `tests/roadmap/test_parser_consistency.py`** (Contract #6): parametrized determinism of the ONE canonical parser across 50+ frontmatter blobs; seed with the disagreeing-parsers historical fixture (Phase 13).

### NFR-007 note (import direction)
`PipelineEnvelope` lives in `roadmap/`; `pipeline/` must not import `roadmap/`. So the canonical parser cannot live in `roadmap/envelope.py` if `pipeline/gates.py` must call it. Two compliant options — the executor must pick and document one in the cleanup inventory:
- **(i)** Canonical parser lives in `pipeline/gates.py` (or a `pipeline/` util); `roadmap` imports it. Simplest; respects NFR-007. The "owned by envelope module" §MVR §1 phrasing becomes "owned by the single pipeline-level parser module."
- **(ii)** Canonical parser in `roadmap/envelope.py`; `pipeline/gates.py`'s own frontmatter check stays as a separate pipeline-level parser (then there are 2 parsers — violates Contract #6). REJECTED.
→ Prefer **(i)**: one canonical parser at the pipeline level, imported by roadmap. This still deletes the divergent variants (Contract #6) and keeps NFR-007. The §MVR §1 "post-step extractor owns it" intent is satisfied by the extractor IMPORTING the one parser.

## Acceptance for this sub-step
- Exactly one frontmatter parser remains reachable from the pipeline; `test_parser_consistency.py` green; `test_pipeline_envelope.py:312` green (no field added); all 8 SemanticCheck modules + sprint untouched; ruff + `make verify-sync` clean.

## ERRATUM (2026-06-02, post-execution + sc:reflect UC-2 audit)
Implementation plan item 4 lists `spec_parser.py:parse_frontmatter` and `spec_patch.py:_extract_frontmatter` for deletion. **They were correctly RETAINED, not deleted** — these are DISTINCT-CONTRACT parsers (full `yaml.safe_load` → `dict[str, Any]` + warnings for spec ingestion; raw-`str` frontmatter block for the spec-patch emit), not gate-frontmatter parsers. Collapsing them onto the flat gate parser would regress (break `test_spec_parser.py`, lose nested-YAML / warnings / raw-block emit). Contract #6 ("one **gate** parser") is satisfied by canonicalizing the two GATE parsers only (`roadmap/gates.py:_parse_frontmatter` + `pipeline/gates.py:_check_frontmatter`'s parsing core → `pipeline/frontmatter.py:extract_frontmatter`). Both retained parsers carry in-code DISTINCT-PURPOSE docstrings and are enumerated by `tests/roadmap/test_parser_consistency.py`. A future reader should NOT "finish" the deletion. The canonical parser was also given line-ending normalization (CRLF/CR) to remain a true behavioral superset of the deleted `splitlines()`-based parser.
