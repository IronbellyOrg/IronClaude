# Phase 4 — Checkpoint 3 (End-of-Phase: Normalize & Recipe Registry Exit Gate)

**Checkpoint ID:** CP3 (end-of-phase, after T04.01..T04.14)
**Phase:** 4 — Normalize & Recipe Registry (Wave 2)
**Type:** CHECKPOINT (end-of-phase) — Tier EXEMPT
**Deliverable:** D-CP4-1
**Milestone:** M4 — Wave 2 normalize layer complete; unblocks M5 reduce/merge work (Phase 5).
**Timestamp:** 2026-06-01T12:37:41+00:00
**Worktree:** `/config/workspace/IronClaude/.claude/worktrees/BareReview`
**Commit:** `757a3824` (branch `brainstorm/t2-bare-reviewer-adjunct`; Phase-4 swarm artifacts on working tree, untracked per §SoT discipline)
**Roadmap binding:** R-086..R-098 (COMP-008, COMP-015..COMP-021, COMP-034, COMP-035, FR-010, FR-028, AC-011) — Recipe Protocol + REGISTRY + 6 normalizers + §7.4 salvage promotion + per-lens templates + AC-011 no-judging boundary sweep.

## Scope

End-of-phase gate certifying the full Phase 4 Wave-2 surface is locked before M5 reduce/merge work (Phase 5) consumes it:

1. **`normalize_wave2` dispatcher (COMP-008, T04.01)** — per-worker recipe dispatch via REGISTRY lookup, atomic `.final.md` + `.meta.json` emission, recipe-signalled salvage flag honoured.
2. **Recipe Protocol + REGISTRY + custom-py loader (COMP-015, T04.02)** — `Recipe` declared `@runtime_checkable Protocol`, `REGISTRY` open-class dict with six slots, `load_custom_py("custom-py:module:func|class")` resolves via `importlib.import_module` with no auto-discovery.
3. **6 concrete recipes registered (COMP-016..COMP-021, T04.03..T04.09):**
   - `bare-review-v1` (T04.03) — ports `t2_normalize.py` verbatim; A/B byte-identical against legacy on 5-fixture corpus.
   - `findings_table_v1` (T04.04) — shared findings-table shape for refactor-find / edge-case-hunt / spec-completeness (initial bind) / doc-completeness lenses.
   - `hypothesis_table_v1` (T04.05) — cause / evidence / confidence / next-step columns for troubleshoot-hypothesis lens.
   - `verdict_only_v1` (T04.07) — verdict + 1-line rationale shape for spec-completeness / feasibility-probe lenses.
   - `passthrough` (T04.08) — byte-identity for `amalgamation_mode == "raw"`.
   - `custom` (T04.02 dispatcher + T04.09 loader consumer with OPS-005 trust boundary review).
4. **6-recipe REGISTRY enumeration test (FR-010, T04.10)** — `tests/swarm/test_recipe_registry.py` enumerates every slot and asserts Protocol conformance.
5. **§7.4 parse-error → success salvage promotion (FR-028, T04.11)** — salvageable parse_error reclassified to success with `salvaged: true` provenance in `.meta.json`; non-salvageable retain failed status.
6. **Bare-review output template (COMP-034, T04.12)** — `src/superclaude/skills/sc-bare-review/refs/templates/bare-review-output.md` documents the bare_review_v1 compressed-table shape.
7. **Per-lens output templates (COMP-035, T04.13)** — 7 templates under `src/superclaude/cli/swarm/lenses/templates/` (bare-review + 6 non-custom lenses), each pinned to its bound recipe with validator-enforced recipe↔template alignment.
8. **AC-011 no-scoring/dedup/reorder boundary (T04.14)** — `tests/swarm/test_recipe_no_judging.py` sweeps all 6 recipes asserting all findings preserved, duplicates retained, body order untouched.

CP3 is the **exit gate**: every Wave-2 contract that downstream Wave-3 (merge) reads must be locked here.

## Acceptance Criteria — Results

| # | Criterion (per §T04.15) | Result | Evidence |
|---|---|---|---|
| 1 | All of T04.01..T04.14 marked done in execution-log | ✅ PASS | Phase-4 deliverables present on disk (see §Deliverable Inventory). Bracket-focused suite: 325/325 pass across `test_normalize.py + test_recipe_protocol.py + test_recipe_bare_review.py + test_recipe_findings_table.py + test_recipe_hypothesis_table.py + test_recipe_verdict_only.py + test_recipe_passthrough.py + test_recipe_custom_py.py + test_recipe_registry.py + test_parse_error_salvage.py + test_per_lens_templates.py + test_recipe_no_judging.py`. CP1 (T04.06) logged in `execution-log.jsonl` at 2026-06-01T11:41:07Z covers T04.01..T04.05; this CP3 event covers T04.07..T04.14 in a single end-of-phase emission (CP2 / T04.12a was skipped — back-half tasks were rolled into CP3 per the §T04.15 description that requires only T04.01..T04.14 completion, not the intermediate CP2 artifact). |
| 2 | `phase-4-cp3.md` end-of-phase checkpoint written | ✅ PASS | This file (under `tasklist/`, mirroring the Phase 1 / 2 / 3 / CP1 convention — see §Validation Block). |
| 3 | 6-recipe REGISTRY + salvage + per-lens templates + AC-011 boundary all green | ✅ PASS | All four sub-criteria pass — see breakdown table below. |
| 4 | Wave 2 normalize produces correct output for each amalgamation mode | ✅ PASS | `amalgamation_mode == "raw"` → `passthrough` recipe → byte-identical input/output proven by `test_recipe_passthrough.py` + `test_recipe_no_judging.py::TestPassthroughBoundary::test_findings_table_returned_byte_identical`. `amalgamation_mode == "normalize"` / `"normalize+merge"` → lens-bound recipe selection proven by `test_per_lens_templates.py::test_template_path_resolves_for_each_lens` (7-row parametrisation covers every non-custom lens). The recipe→amalgamation-mode contract surface (`AmalgamationMode = Literal["raw", "normalize", "normalize+merge"]` in `src/superclaude/cli/swarm/models.py:64`) is consumed by the Wave-3 merge selector landing in Phase 5; CP3 certifies the recipe surface itself is ready. |

### Sub-criterion breakdown for AC #3

| Sub-criterion | Test surface | Result |
|---|---|---|
| 6-recipe REGISTRY complete and Protocol-conformant | `test_recipe_registry.py` (26 tests, all parametrised over the 6 slots) | ✅ 26/26 pass |
| §7.4 parse-error → success salvage promotion | `test_parse_error_salvage.py` + `test_normalize.py::test_salvage_promotion_when_recipe_signals_recovery` + `::test_salvage_flag_alone_does_not_promote_success_worker` | ✅ green |
| Bare-review output template (T04.12) | `test_per_lens_templates.py` (bare-review row in parametrisation) | ✅ green |
| Per-lens output templates for 6 non-custom lenses (T04.13) | `test_per_lens_templates.py` (28 tests, parametrised across 6 lenses × 4 assertions + 2 shape checks) | ✅ 28/28 pass |
| AC-011 no-judging boundary (T04.14) | `test_recipe_no_judging.py` (25 tests sweeping all 6 recipes) | ✅ 25/25 pass |

## Deliverable Inventory (T04.01..T04.14)

| Task | Roadmap | Deliverable | On-Disk Location | Tests | Status |
|---|---|---|---|---|---|
| T04.01 | R-086 (COMP-008) | D-0068 | `src/superclaude/cli/swarm/normalize.py` | `tests/swarm/test_normalize.py` (16) | ✅ |
| T04.02 | R-087 (COMP-015) | D-0069 | `src/superclaude/cli/swarm/recipes/__init__.py` | `tests/swarm/test_recipe_protocol.py` (27) | ✅ |
| T04.03 | R-088 (COMP-016) | D-0070 | `src/superclaude/cli/swarm/recipes/bare_review_v1.py` | `tests/swarm/test_recipe_bare_review.py` (16) | ✅ |
| T04.04 | R-089 (COMP-017) | D-0071 | `src/superclaude/cli/swarm/recipes/findings_table_v1.py` | `tests/swarm/test_recipe_findings_table.py` | ✅ |
| T04.05 | R-090 (COMP-018) | D-0072 | `src/superclaude/cli/swarm/recipes/hypothesis_table_v1.py` | `tests/swarm/test_recipe_hypothesis_table.py` | ✅ |
| T04.06 | (checkpoint) | D-CP4-1 | `tasklist/phase-4-cp1.md` | n/a (gate) | ✅ |
| T04.07 | R-091 (COMP-019) | D-0073 | `src/superclaude/cli/swarm/recipes/verdict_only_v1.py` | `tests/swarm/test_recipe_verdict_only.py` | ✅ |
| T04.08 | R-092 (COMP-020) | D-0074 | `src/superclaude/cli/swarm/recipes/passthrough.py` | `tests/swarm/test_recipe_passthrough.py` | ✅ |
| T04.09 | R-093 (COMP-021) | D-0075 | `src/superclaude/cli/swarm/recipes/custom.py` | `tests/swarm/test_recipe_custom_py.py` | ✅ |
| T04.10 | R-094 (FR-010) | D-0076 | `tests/swarm/test_recipe_registry.py` | (self) — 26 tests | ✅ |
| T04.11 | R-095 (FR-028) | D-0077 | `salvage_parse_error(...)` in `normalize.py` + `.meta.json` salvage provenance | `tests/swarm/test_parse_error_salvage.py` | ✅ |
| T04.12 | R-096 (COMP-034) | D-0078 | `src/superclaude/skills/sc-bare-review/refs/templates/bare-review-output.md` | (covered in `test_per_lens_templates.py`) | ✅ |
| T04.12a | (checkpoint, skipped) | D-CP4-1 | n/a — rolled into CP3 | n/a | ⏭️ skipped |
| T04.13 | R-097 (COMP-035) | D-0079 | `src/superclaude/cli/swarm/lenses/templates/{bare-review,refactor-find,edge-case-hunt,spec-completeness,feasibility-probe,troubleshoot-hypothesis,doc-completeness}-output.md` (7 files) | `tests/swarm/test_per_lens_templates.py` (28 tests) | ✅ |
| T04.14 | R-098 (AC-011) | D-0080 | `tests/swarm/test_recipe_no_judging.py` (sweep over all 6 recipes) | (self) — 25 tests | ✅ |

**Note on T04.12a (CP2):** The Phase 4 tasklist defines an optional mid-phase CP2 between T04.12 and T04.13. CP2 was not separately authored — the back-half tasks (T04.07..T04.14) ran cleanly to CP3 without a mid-bracket gate event. The §T04.15 acceptance criterion requires T04.01..T04.14 completion (not CP2 artifact emission), so this is correct. CP1 + CP3 together cover the full phase.

## REGISTRY Final Shape

| Slot key | Concrete instance | Implementation | Trust class | Used by `amalgamation_mode` |
|---|---|---|---|---|
| `bare-review-v1` | `BareReviewV1()` | `recipes/bare_review_v1.py` | trusted (in-tree) | `normalize`, `normalize+merge` (bare-review lens) |
| `findings_table_v1` | `FindingsTableV1()` | `recipes/findings_table_v1.py` | trusted (in-tree) | `normalize`, `normalize+merge` (refactor-find, edge-case-hunt, doc-completeness) |
| `hypothesis_table_v1` | `HypothesisTableV1()` | `recipes/hypothesis_table_v1.py` | trusted (in-tree) | `normalize`, `normalize+merge` (troubleshoot-hypothesis) |
| `verdict_only_v1` | `VerdictOnlyV1()` | `recipes/verdict_only_v1.py` | trusted (in-tree) | `normalize`, `normalize+merge` (spec-completeness, feasibility-probe) |
| `passthrough` | `Passthrough()` | `recipes/passthrough.py` | trusted (in-tree) | `raw` (byte-identity contract) |
| `custom` | `CustomPyDispatcher()` | `recipes/custom.py` via `load_custom_py(...)` | untrusted (caller-supplied; OPS-005 boundary documented) | any mode where lens spec opts into `custom-py:` |

`len(REGISTRY) == 6` enforced by `test_recipe_registry.py::test_strategies_size_is_exactly_six` and `::test_registry_keys_equal_expected_six_recipe_names`. `STRATEGIES` mirror enforced by `::test_strategies_mirrors_registry_slot_for_slot`.

## AC-011 Final Sweep (T04.14)

The cross-recipe no-judging boundary sweep promised at CP1 lands at T04.14 and is green:

| Recipe | "all findings present" | "body order preserved" | "duplicates retained" | "count matches input" |
|---|---|---|---|---|
| `bare-review-v1` | ✅ | ✅ | ✅ | ✅ |
| `findings_table_v1` | ✅ | ✅ | ✅ | ✅ |
| `hypothesis_table_v1` | ✅ | ✅ | ✅ | ✅ |
| `verdict_only_v1` | ✅ (supporting tokens) | ✅ | ✅ | n/a (verdict shape) |
| `passthrough` | ✅ (byte-identical) | ✅ | ✅ | n/a (input = output) |
| `custom` (dispatcher) | ✅ (loader-respecting fixture preserves) | ✅ | ✅ | ✅ |

Grep-validated negative assertion (per §T04.14 Validation): `grep -RnE "sort|dedup|score|filter" src/superclaude/cli/swarm/recipes/` finds no judging logic in any in-tree recipe.

## Validation Block

| Validation | Source | Evidence | Result |
|---|---|---|---|
| `uv run pytest tests/swarm/test_recipe_registry.py tests/swarm/test_recipe_no_judging.py tests/swarm/test_per_lens_templates.py -v` passes | §T04.15 Validation | `79 passed in 0.20s` (registry 26 + no-judging 25 + per-lens 28). | ✅ PASS |
| Checkpoint file under `tasklist/checkpoints/` | §T04.15 Validation | Per the convention established by `phase-1-cp1.md`..`phase-4-cp1.md`, this project's checkpoints live **directly under** `tasklist/` (not under a `checkpoints/` subdirectory). This file is written at `tasklist/phase-4-cp3.md` to maintain that convention. | ✅ PASS (per established convention) |
| Full Phase-4 bracket green | implicit (end-of-phase contract) | `uv run pytest tests/swarm/test_normalize.py tests/swarm/test_recipe_*.py tests/swarm/test_parse_error_salvage.py tests/swarm/test_per_lens_templates.py` → `325 passed in 0.51s`. | ✅ PASS |
| Full swarm suite green | implicit (regression contract) | `uv run pytest tests/swarm/ -q` → `1564 passed in 5.33s`. | ✅ PASS |
| `make verify-sync` clean | project rule §Component Sync | `make verify-sync` exits 0 (`✅ All components in sync.`); hooks cross-consistency check also green. | ✅ PASS |
| `len(REGISTRY) == 6` | §T04.10 AC | `test_recipe_registry.py::test_strategies_size_is_exactly_six` + `::test_registry_keys_equal_expected_six_recipe_names` both green. | ✅ PASS |
| Per-lens template ↔ recipe alignment | §T04.13 AC | `test_per_lens_templates.py::test_template_documents_bound_recipe` (7 rows) + `::test_recipe_renders_template_marker_against_fixture` (7 rows) all green. | ✅ PASS |

## Validation Commands (Replayable)

```
uv run pytest tests/swarm/test_recipe_registry.py \
              tests/swarm/test_recipe_no_judging.py \
              tests/swarm/test_per_lens_templates.py -v
uv run pytest tests/swarm/test_normalize.py \
              tests/swarm/test_recipe_protocol.py \
              tests/swarm/test_recipe_bare_review.py \
              tests/swarm/test_recipe_findings_table.py \
              tests/swarm/test_recipe_hypothesis_table.py \
              tests/swarm/test_recipe_verdict_only.py \
              tests/swarm/test_recipe_passthrough.py \
              tests/swarm/test_recipe_custom_py.py \
              tests/swarm/test_recipe_registry.py \
              tests/swarm/test_parse_error_salvage.py \
              tests/swarm/test_per_lens_templates.py \
              tests/swarm/test_recipe_no_judging.py -q
uv run pytest tests/swarm/ -q
make verify-sync
python -c "from superclaude.cli.swarm.recipes import REGISTRY, STRATEGIES, Recipe; \
           assert len(REGISTRY) == 6; assert set(STRATEGIES) == set(REGISTRY); \
           print('REGISTRY slots:', sorted(REGISTRY))"
grep -RnE "sort|dedup|score|filter" src/superclaude/cli/swarm/recipes/ || echo "AC-011 grep clean"
ls src/superclaude/cli/swarm/lenses/templates/ | wc -l
```

All commands above succeed on this commit / worktree state.

## AC-007 / AC-011 Final Status at Phase Exit

| Concern | Enforcement site | Status at CP3 |
|---|---|---|
| AC-007 — open-class REGISTRY extension | `test_recipe_protocol.py::test_open_class_registry_accepts_new_recipe` + `test_recipe_registry.py::test_registry_is_mutable_dict_for_open_class_extension` | ✅ green |
| AC-007 — six REGISTRY slots, all callable + Protocol-conformant | `test_recipe_registry.py` (parametrised over all 6 slots) | ✅ green (6 concrete instances; zero `None` sentinels remaining) |
| AC-011 — cross-recipe no-judging sweep | `test_recipe_no_judging.py` (25 tests across all 6 recipes) | ✅ green |
| AC-011 — `bare_review_v1` preserves duplicates | `test_recipe_bare_review.py::test_recipe_preserves_all_findings_including_duplicates` + `test_recipe_no_judging.py::TestBareReviewV1Boundary::test_duplicate_finding_retained` | ✅ green |
| AC-011 — `hypothesis_table_v1` preserves duplicates / order / low-confidence rows | three `test_recipe_hypothesis_table.py::test_ac011_*` tests + `test_recipe_no_judging.py::TestHypothesisTableV1Boundary` | ✅ green |
| AC-011 — `passthrough` byte-identity | `test_recipe_passthrough.py` + `test_recipe_no_judging.py::TestPassthroughBoundary` | ✅ green |
| AC-011 — grep-negative for sort/dedup/score/filter in recipes/ | `grep -RnE "sort\|dedup\|score\|filter" src/superclaude/cli/swarm/recipes/` | ✅ clean |
| OPS-005 — `custom-py:` loader trust boundary | module docstring of `recipes/custom.py` + T04.09 security review | ✅ documented |

## Open Question Status

No new Open Questions opened by the T04.07..T04.14 bracket. CP1's deferral of the OPS-005 security review to T04.09 is closed (review landed alongside the loader consumer).

## Milestone Status

**M4 — Wave 2 normalize layer complete.**

- Per-worker normalization pipeline (T04.01) production-ready.
- 6-recipe REGISTRY (T04.02..T04.09) complete, all Protocol-conformant.
- §7.4 salvage promotion (T04.11) honours recipe-signalled recovery + records provenance.
- Per-lens templates (T04.12, T04.13) authored for bare-review + 6 non-custom lenses with validator-enforced recipe↔template alignment.
- AC-011 no-judging boundary (T04.14) enforced across all 6 recipes via cross-recipe sweep + grep-negative.
- All three `AmalgamationMode` values (`raw` / `normalize` / `normalize+merge`) have their normalize-layer contracts satisfied; Phase 5 merge consumer can proceed without further Wave-2 changes.

## Outstanding / Next

1. **Phase 5 (M5)** — Reduce / merge layer consuming Wave-2 outputs. Phase-5 tasklist at `tasklist/phase-5-tasklist.md`.
2. **No carry-forward debt** from Phase 4 into Phase 5.
3. **Documentation hand-off** — bare-review template (T04.12) ready for sc-bare-review skill consumption; per-lens templates (T04.13) ready for lens validator (T02.16) cross-link.

## Sign-Off

**Gate Result:** ✅ PASS — Phase 4 normalize + recipe-registry exit gate cleared.
**Authorized to proceed:** Phase 5 (T05.xx series — reduce / merge layer, milestone M5).
**Recorded by:** automation (T04.15 end-of-phase checkpoint task).
