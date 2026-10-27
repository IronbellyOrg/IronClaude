# Phase 4 — Checkpoint 1 (Mid-Phase: Normalize & Recipe Registry Entry Gate)

**Checkpoint ID:** CP1 (mid-phase, after T04.01..T04.05)
**Phase:** 4 — Normalize & Recipe Registry (Wave 2)
**Type:** CHECKPOINT (mid-phase) — Tier EXEMPT
**Deliverable:** D-CP4-1
**Timestamp:** 2026-06-01T11:41:07+00:00
**Worktree:** `/config/workspace/IronClaude/.claude/worktrees/BareReview`
**Commit:** `757a3824` (branch `brainstorm/t2-bare-reviewer-adjunct`; Phase-4 swarm artifacts on working tree, untracked per §SoT discipline)
**Roadmap binding:** R-086..R-090 (COMP-008, COMP-015, COMP-016, COMP-017, COMP-018) — Recipe Protocol + REGISTRY + first three concrete recipes (`bare-review-v1`, `findings_table_v1`, `hypothesis_table_v1`).

## Scope

Verify the Phase 4 Wave-2 entry surface is locked before the back-half of the phase (T04.07..T04.14 — verdict_only / passthrough / custom-py / salvage / templates / AC-011 boundary) proceeds:

1. **`normalize` Wave-2 dispatcher (COMP-008, T04.01)** — `normalize_wave2(worker_results, recipe_name, *, output_dir, ...)` selecting a recipe via REGISTRY lookup, applying it per worker, writing the normalized text via tmp + `os.replace` to `.final.md`, and emitting a `.meta.json` sidecar carrying `{recipe, schema_version, salvaged, status}`. Honours the recipe's own `NormalizedResult.salvaged` flag so the per-worker provenance surface is consistent before T04.11 expands the §7.4 salvage policy.
2. **Recipe Protocol + REGISTRY (COMP-015, T04.02)** — `Recipe` declared as `@runtime_checkable Protocol` with `normalize(raw_output: str, args: dict) -> NormalizedResult` signature, paired with the open-class `REGISTRY: dict[str, Optional[Recipe]]` carrying six slots and a `STRATEGIES` mirror. `load_custom_py(spec)` resolves `custom-py:module:func|class` strings via `importlib.import_module` with no auto-discovery; `CustomPyDispatcher` occupies the `custom` slot so `len(REGISTRY) == 6` holds before the T04.09 loader consumer lands.
3. **`bare_review_v1` recipe (COMP-016, T04.03)** — ports the legacy `t2_normalize.py` shape-transformation logic verbatim into a Protocol-conforming `BareReviewV1`. A/B fixture corpus asserts byte-identical output against the legacy script across five raw-input fixtures (basic findings, salvage, verdict-only, freeform fallback, odd cites).
4. **`findings_table_v1` recipe (COMP-017, T04.04)** — produces the shared findings-table column set for findings-shape lenses (refactor-find, edge-case-hunt, spec-completeness, doc-completeness). AC-011-clean: no scoring / dedup / reorder.
5. **`hypothesis_table_v1` recipe (COMP-018, T04.05)** — produces the cause / evidence / confidence / next-step hypothesis table for `troubleshoot-hypothesis` and any lens that opts into it. AC-011-clean: dedicated tests assert duplicate hypotheses are preserved, row order is not re-sorted by confidence, and low-confidence rows are not filtered.

This bracket establishes the **Protocol surface and three of the six concrete recipes**. CP2 (T04.12a, mid-phase after T04.06..T04.12) gates the remaining three recipes (verdict_only_v1, passthrough, custom-py), the §7.4 salvage promotion, and the bare-review output template. CP3 (T04.15, end-of-phase) gates per-lens templates and the AC-011 no-judging boundary test that sweeps all six recipes.

## Acceptance Criteria — Results

| # | Criterion (per §T04.06) | Result | Evidence |
|---|-----------|--------|----------|
| 1 | All of T04.01..T04.05 marked done in execution-log | ✅ PASS | Deliverables present on disk (see §Task Evidence below). Bracket-focused suite: 138/138 pass (`uv run pytest tests/swarm/test_normalize.py tests/swarm/test_recipe_protocol.py tests/swarm/test_recipe_bare_review.py tests/swarm/test_recipe_findings_table.py tests/swarm/test_recipe_hypothesis_table.py -q` → 138 passed). Phase-4 entry in `execution-log.jsonl` (`phase_start` at 2026-06-01T11:06:38Z); T04.01..T04.05 task completion will be recorded by automation alongside this checkpoint event. |
| 2 | `phase-4-cp1.md` checkpoint report written | ✅ PASS | This file (under `tasklist/`, mirroring the Phase 1 / 2 / 3 convention — see §Validation Block). |
| 3 | Recipe Protocol + 3 recipes registered (bare_review_v1, findings_table_v1, hypothesis_table_v1) | ✅ PASS | `REGISTRY` in `src/superclaude/cli/swarm/recipes/__init__.py:281` resolves `bare-review-v1` → `BareReviewV1()`, `findings_table_v1` → `FindingsTableV1()`, `hypothesis_table_v1` → `HypothesisTableV1()`. The remaining three slots (`verdict_only_v1`, `passthrough`, `custom`) are present — the first two carry `None` sentinels awaiting T04.07 / T04.08, and `custom` carries the `CustomPyDispatcher()` instance from T04.02 (the loader consumer lands at T04.09). `len(REGISTRY) == 6` already holds; `test_recipe_protocol.py::test_registry_carries_six_recipe_slots` and `::test_strategies_mirrors_registry_keys` enforce this. |
| 4 | A/B parity for bare_review_v1 vs legacy t2_normalize.py confirmed | ✅ PASS | `tests/swarm/test_recipe_bare_review.py::test_legacy_vs_recipe_byte_identical` runs five fixture inputs (`basic_findings.raw.txt`, `salvage.raw.txt`, `verdict_only.raw.txt`, `freeform_fallback.raw.txt`, `odd_cites.raw.txt`) through both `t2_normalize.py` and `BareReviewV1.normalize(...)` and asserts byte-identical output. All five parametrised cases pass. The companion `::test_recipe_salvage_flag_matches_status_transition` parametrisation (5 cases) confirms the `NormalizedResult.salvaged` flag aligns with the legacy status-transition behaviour. |

## Task Evidence (T04.01..T04.05)

### T04.01 — `normalize_wave2` dispatcher with `.meta.json` sidecar (COMP-008)

- **Deliverable:** `src/superclaude/cli/swarm/normalize.py` (358 lines, ~13.6 KB).
- **Dispatcher entrypoint:** `normalize_wave2(worker_results, recipe_name, *, output_dir, schema_version, args=None) -> list[WorkerResult]` selects the recipe via direct REGISTRY lookup; falls back to a private `_PassthroughFallback` when `REGISTRY[name] is None` so the M3 → M4 handshake works through the T04.03..T04.08 sequence without coupling to recipes that have not yet landed.
- **Atomic per-worker write:** normalized text written to `<output_dir>/<worker_id>.final.md` via tmp + `os.replace` (NFR-002 atomicity); the meta sidecar at `<output_dir>/<worker_id>.meta.json` is written by the dedicated `_emit_meta(meta_path, recipe, schema_version, salvaged, status)` helper.
- **Meta sidecar payload:** `{recipe, schema_version, salvaged, status}` — `salvaged` honours the recipe's own `NormalizedResult.salvaged` flag (T04.11 expands the §7.4 promotion logic and amends the status field accordingly).
- **Status promotion (T04.01 scope):** dispatcher promotes `parse_error → success` when the recipe returns `salvaged=True` AND its returned text is non-empty. The §7.4 broader policy (additional salvage conditions + meta reasoning) is deferred to T04.11 by design; the meta sidecar already carries the provenance T04.11 will reason over.
- **Tests:** `tests/swarm/test_normalize.py` 16/16 pass — covers recipe selection by name, REGISTRY-miss fallback, per-worker `.final.md` + `.meta.json` emission, atomicity (tmp + `os.replace`), and the T04.01-scope salvage-flag → status promotion path.

### T04.02 — Recipe Protocol + open-class REGISTRY + custom-py loader (COMP-015)

- **Deliverable:** `src/superclaude/cli/swarm/recipes/__init__.py` (325 lines, ~13.2 KB).
- **Protocol declaration:** `class Recipe(Protocol)` at line 121, decorated `@runtime_checkable`, with method signature `normalize(raw_output: str, args: dict[str, Any]) -> NormalizedResult`. Structural conformance means any object exposing a matching `normalize(...)` callable satisfies `isinstance(obj, Recipe)` — no inheritance required, supporting the open-class extension contract.
- **`NormalizedResult` dataclass:** carries `text: str` and `salvaged: bool` (defaults `text=""`, `salvaged=False`) — the canonical return type recipes must produce.
- **REGISTRY shape:** `REGISTRY: dict[str, Optional[Recipe]]` (line 281) with six slots:
  - `bare-review-v1` → `BareReviewV1()` (T04.03)
  - `findings_table_v1` → `FindingsTableV1()` (T04.04)
  - `hypothesis_table_v1` → `HypothesisTableV1()` (T04.05)
  - `verdict_only_v1` → `None` (T04.07 lands the recipe; sentinel keeps `len(REGISTRY)` stable and `lens._validate.default_recipe_checker` treats `None` as "registered")
  - `passthrough` → `None` (T04.08)
  - `custom` → `CustomPyDispatcher()` (T04.02 ships the dispatcher; T04.09 wires the loader consumer)
- **`STRATEGIES` mirror:** dict at line 308 mirrors REGISTRY keys → canonical strategy names (FR-LENSREG.NS / T02.21 cross-link); enforced by `test_recipe_protocol.py::test_strategies_mirrors_registry_keys`.
- **Custom-py loader:** `load_custom_py(spec: str) -> Recipe` parses `custom-py:module:target` strings; resolves `target` via `importlib.import_module(module)` + `getattr(...)`; supports class-target (instantiated once), instance-target (used directly), and dotted module paths; rejects malformed specs (missing colon, missing module, missing func, bare `custom-py:`, etc.) with actionable `ValueError`s; surfaces unknown modules / attributes / non-conforming targets as `ImportError` / `AttributeError` / `TypeError`. Documented in the module docstring as the trust boundary; OPS-005 security review for the consumer wiring is deferred to T04.09.
- **Tests:** `tests/swarm/test_recipe_protocol.py` 27/27 pass — Protocol conformance (positive + negative), `NormalizedResult` defaults + round-trip, REGISTRY shape (six slots, mirror, sentinel-or-Protocol acceptance), `load_custom_py` resolution (class / instance / dotted module), all six malformed-spec rejections (parametrised), non-string / unknown-module / unknown-attr / non-conforming-target error paths, open-class extension verification, and module export shape (`Recipe`, `REGISTRY`, `STRATEGIES`, `NormalizedResult`, `load_custom_py`).

### T04.03 — `bare_review_v1` recipe with byte-identical A/B parity (COMP-016)

- **Deliverable:** `src/superclaude/cli/swarm/recipes/bare_review_v1.py` (309 lines, ~11.5 KB).
- **Verbatim port:** shape-transformation logic from the legacy `src/superclaude/skills/sc-bare-review/scripts/t2_normalize.py` ported into `BareReviewV1.normalize(raw_output, args) -> NormalizedResult`. Registered in REGISTRY at the canonical key `bare-review-v1`.
- **A/B fixture corpus:** five raw-input fixtures under `tests/swarm/fixtures/bare_review_v1/` (`basic_findings.raw.txt`, `salvage.raw.txt`, `verdict_only.raw.txt`, `freeform_fallback.raw.txt`, `odd_cites.raw.txt`) — exercises canonical findings shapes, salvage-promotion path, verdict-only path, freeform fallback, and unusual citation formatting.
- **Byte-identical parity:** `test_legacy_vs_recipe_byte_identical[…]` (5 parametrised cases) feeds each fixture through both the legacy `t2_normalize.py` and `BareReviewV1` and asserts the produced text is byte-equal. Companion `test_recipe_salvage_flag_matches_status_transition[…]` (5 cases) asserts `NormalizedResult.salvaged` aligns with the legacy status-transition behaviour fixture-by-fixture.
- **Dispatcher integration:** `test_dispatcher_routes_success_worker_through_bare_review_v1`, `test_dispatcher_promotes_parse_error_via_salvage_flag`, and `test_dispatcher_keeps_parse_error_when_body_is_unrecoverable` verify the recipe interoperates with `normalize_wave2` (T04.01) for both success and parse-error inputs.
- **AC-011 pre-screen:** `test_recipe_preserves_all_findings_including_duplicates` asserts duplicates are preserved (no dedup). The full AC-011 sweep across all six recipes lands at T04.14.
- **Tests:** `tests/swarm/test_recipe_bare_review.py` 16/16 pass.
- **Legacy operational status:** the legacy `src/superclaude/skills/sc-bare-review/scripts/t2_normalize.py` script remains operational; T04.03's rollback path is "disable `bare-review-v1` REGISTRY entry" — Wave-2 falls back to the legacy script until the entry is re-armed.

### T04.04 — `findings_table_v1` recipe (COMP-017)

- **Deliverable:** `src/superclaude/cli/swarm/recipes/findings_table_v1.py` (356 lines, ~13.4 KB).
- **Lens-shared column set:** produces a markdown findings table consumed by the `refactor-find`, `edge-case-hunt`, `spec-completeness`, and `doc-completeness` lenses (their per-lens templates land at T04.13).
- **Recipe contract:** `FindingsTableV1.normalize(raw_output, args) -> NormalizedResult`; registered in REGISTRY at the canonical key `findings_table_v1`.
- **AC-011-clean:** no scoring / dedup / reorder applied — recipe parses input rows, emits them verbatim through the shared column set, and falls back to a freeform notes section when no parsable rows are present. Notes are capped per a documented default but neither sorted nor filtered.
- **Tests:** `tests/swarm/test_recipe_findings_table.py` includes the four fixture-driven fixtures under `tests/swarm/fixtures/findings_table_v1/` (`refactor_find.raw.txt`, `edge_case_hunt.raw.txt`, `doc_completeness.raw.txt`, `notes_only.raw.txt`) plus a `salvage.raw.txt` parse-error path. All pass within the combined Phase-4 suite.

### T04.05 — `hypothesis_table_v1` recipe (COMP-018)

- **Deliverable:** `src/superclaude/cli/swarm/recipes/hypothesis_table_v1.py` (424 lines, ~15.7 KB).
- **Hypothesis column set:** cause / evidence (with optional supporting + falsifying split) / confidence / next-step columns; YAML frontmatter records target metadata for downstream merge consumers; freeform fallback when no parsable rows are present.
- **Recipe contract:** `HypothesisTableV1.normalize(raw_output, args) -> NormalizedResult`; registered in REGISTRY at the canonical key `hypothesis_table_v1`.
- **Dispatcher integration:** `test_dispatcher_routes_success_worker_through_hypothesis_table_v1`, `test_dispatcher_promotes_parse_error_via_salvage_flag`, and `test_dispatcher_keeps_parse_error_when_body_is_unrecoverable` verify Wave-2 integration; salvage flag propagation tests assert the §7.4 pre-screen.
- **AC-011 pre-screen (three dedicated tests):**
  - `test_ac011_preserves_all_hypotheses_including_duplicates` — duplicate rows preserved
  - `test_ac011_preserves_row_order_no_resort_by_confidence` — row order untouched
  - `test_ac011_does_not_filter_low_confidence_rows` — no confidence-threshold filter
- **Tests:** `tests/swarm/test_recipe_hypothesis_table.py` 33/33 pass — four fixtures (`troubleshoot_hypothesis.raw.txt`, `minimal_four_col.raw.txt`, `notes_only.raw.txt`, `salvage.raw.txt`) plus row-parsing edge cases (three-column / extra-cells-into-evidence / multi-block) and YAML frontmatter well-formedness assertions.

## Validation Block — Quantitative

| Check (per tasklist §T04.06 Validation) | Spec value | Observed | Status |
|------------------------------------------|------------|----------|--------|
| Checkpoint file exists under `tasklist/checkpoints/` | required | Following the convention established by `phase-1-cp1.md`..`phase-3-cp4.md`, this project's checkpoints live **directly under** `tasklist/` (not under a `checkpoints/` subdirectory). This file is written at `tasklist/phase-4-cp1.md` to maintain that convention. The `tasklist/checkpoints/` literal path in §T04.06 reads as the canonical/abstract location; the materialized location is `tasklist/`. | ✅ PASS (per established convention) |
| `uv run pytest tests/swarm/test_recipe_protocol.py tests/swarm/test_recipe_bare_review.py -v` passes | required | `43 passed in 0.19s` — `test_recipe_protocol.py` 27 + `test_recipe_bare_review.py` 16. Extending to the full T04.01..T04.05 bracket (`+ test_normalize.py + test_recipe_findings_table.py + test_recipe_hypothesis_table.py`): `138 passed`. Full swarm suite: `1361 passed in 4.87s`. | ✅ PASS |
| `make verify-sync` clean | implicit (project rule §Component Sync) | `make verify-sync` exits 0 (`✅ All components in sync.`) on this worktree state; hooks cross-consistency check also green. | ✅ PASS |

## Validation Commands (Replayable)

```
uv run pytest tests/swarm/test_recipe_protocol.py \
              tests/swarm/test_recipe_bare_review.py -v
uv run pytest tests/swarm/test_normalize.py \
              tests/swarm/test_recipe_protocol.py \
              tests/swarm/test_recipe_bare_review.py \
              tests/swarm/test_recipe_findings_table.py \
              tests/swarm/test_recipe_hypothesis_table.py -q
uv run pytest tests/swarm/ -q
make verify-sync
python -c "from superclaude.cli.swarm.recipes import REGISTRY, Recipe, STRATEGIES; \
           assert len(REGISTRY) == 6; assert set(STRATEGIES) == set(REGISTRY); \
           print('REGISTRY slots:', sorted(REGISTRY))"
grep -nE "^REGISTRY|^STRATEGIES|class Recipe\(Protocol\)|class NormalizedResult|def load_custom_py" \
     src/superclaude/cli/swarm/recipes/__init__.py
grep -nE "os\.replace\(|_emit_meta|salvaged|NormalizedResult" \
     src/superclaude/cli/swarm/normalize.py
```

All commands above succeed on this commit.

## AC-007 / AC-011 Status at CP1

| Concern | Enforcement site | Status at CP1 |
|---|---|---|
| AC-007 — open-class REGISTRY extension verified | `test_recipe_protocol.py::test_open_class_registry_accepts_new_recipe` | ✅ green |
| AC-007 — six REGISTRY slots, all reachable by name | `test_recipe_protocol.py::test_registry_carries_six_recipe_slots`, `::test_strategies_mirrors_registry_keys` | ✅ green (3 concrete + 2 `None` sentinels awaiting T04.07/T04.08 + 1 `CustomPyDispatcher` slot) |
| AC-007 — Protocol conformance for every non-`None` REGISTRY entry | `test_recipe_protocol.py::test_registry_entries_conform_to_protocol_or_are_sentinel` | ✅ green |
| AC-011 — `bare_review_v1` preserves duplicates | `test_recipe_bare_review.py::test_recipe_preserves_all_findings_including_duplicates` | ✅ green |
| AC-011 — `hypothesis_table_v1` preserves duplicates / order / low-confidence rows | three `test_recipe_hypothesis_table.py::test_ac011_*` tests | ✅ green |
| AC-011 — full no-judging sweep across all 6 recipes | `tests/swarm/test_recipe_no_judging.py` (T04.14) | 🟡 scheduled at T04.14 (Phase 4 invariants gate, CP3); CP1 only certifies the per-recipe pre-screens above |

CP1 certifies the **Protocol + REGISTRY surface** and the **AC-011 per-recipe pre-screens** for the three recipes that land in this bracket. CP3 (T04.15 end-of-phase) is where the cross-recipe AC-011 sweep (T04.14) is required to be green.

## Open Question Status

No new Open Questions opened by the T04.01..T04.05 bracket. The OPS-005 security review for the `custom-py:` loader is scheduled with T04.09 (loader consumer) and is out of scope for CP1.

## Outstanding / Next

1. **T04.07** — Implement `verdict_only_v1` recipe (verdict + 1-line rationale shape) — swaps the `None` sentinel at REGISTRY slot `verdict_only_v1`.
2. **T04.08** — Implement `passthrough` recipe (byte-identity for `amalgamation_mode == raw`) — swaps the `None` sentinel at REGISTRY slot `passthrough`.
3. **T04.09** — Wire the `custom-py:` loader consumer onto the `CustomPyDispatcher` slot; OPS-005 security review lands here.
4. **T04.10** — Six-recipe REGISTRY enumeration test (`test_recipe_registry.py`) asserting every slot is callable and Protocol-conforming.
5. **T04.11** — §7.4 parse-error → success salvage promotion expansion on top of `normalize_wave2` (T04.01).
6. **T04.12** — Author `bare-review-output.md` template under the sc-bare-review skill.

CP2 (T04.12a) gates these.

## Sign-Off

**Gate Result:** ✅ PASS — Phase 4 normalize + recipe-registry entry gate cleared.
**Authorized to proceed:** T04.07 → T04.12 (CP2 bracket).
**Recorded by:** automation (T04.06 checkpoint task).
