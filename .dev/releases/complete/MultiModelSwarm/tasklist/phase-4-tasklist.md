# Phase 4 -- Normalize & Recipe Registry (Wave 2)

**Goal:** Build Wave 2 — the Recipe Protocol + REGISTRY with 6 normalizers (bare_review_v1, findings_table_v1, hypothesis_table_v1, verdict_only_v1, passthrough, custom-py dynamic loader), per-worker normalization with §7.4 parse-error→success salvage promotion, and the per-lens output templates that validators assert recipes match. Exit when each worker output is normalized by its lens recipe, parse_error→success salvage works, all three amalgamation modes (`raw`/`normalize`/`normalize+merge`) select the correct recipe path, every non-custom lens has a matching output template, and `AC-011` recipe-no-judging boundary is asserted in CI.

### T04.01 -- Build `normalize` (Wave 2) dispatcher + Recipe Protocol invocation

| Field | Value |
|---|---|
| Roadmap | R-086 (COMP-008) |
| Deliverables | D-0068 |
| Effort | M |
| Risk | MEDIUM |
| Tier | STANDARD |
| Confidence | `[████████--] 85%` |
| MCP Tools | Read, Edit, auggie, serena |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/test_normalize.py` |

**Deliverables:**
1. `src/superclaude/cli/swarm/normalize.py` with `normalize_wave2(worker_results, recipe_name) -> list[WorkerResult]`.
2. Meta sidecar emission (`.meta.json`) per worker.

**Steps:**
1. [PLANNING] Locate Recipe Protocol from T04.02 (or design here if T04.02 not yet wired).
2. [EXECUTION] Implement `normalize_wave2` selecting recipe via REGISTRY lookup by name.
3. [EXECUTION] Apply recipe per worker, capture normalized output + meta sidecar.
4. [VERIFICATION] Run against stub-transport outputs from M3.
5. [COMPLETION] `make sync-dev && make verify-sync`.

**Acceptance Criteria:**
- `cli/swarm/normalize.py` selects recipe per worker by `NormalizationSpec.recipe`.
- Normalized output written via tmp+`os.replace` to `.final.md` path.
- `.meta.json` sidecar records recipe name, schema_version, salvage flag.
- `tests/swarm/test_normalize.py` covers happy-path and parse_error branches.

**Validation:**
- `uv run pytest tests/swarm/test_normalize.py -v` passes.
- Wave 2 output paths confined to `--output` directory.

**Dependencies:** T04.02 (Recipe Protocol). **Rollback:** revert normalize module.
**Notes:** AC-011 prohibits scoring/dedup/reorder transforms inside recipes.

### T04.02 -- Define Recipe Protocol + REGISTRY (+ custom-py loader entry)

| Field | Value |
|---|---|
| Roadmap | R-087 (COMP-015) |
| Deliverables | D-0069 |
| Effort | M |
| Risk | MEDIUM |
| Tier | STRICT |
| Confidence | `[████████--] 85%` |
| Critical Path Override | YES |
| MCP Tools | Read, Edit, context7 (Python Protocol), auggie |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/test_recipe_protocol.py` |

**Deliverables:**
1. `src/superclaude/cli/swarm/recipes/__init__.py` declaring `Recipe` Protocol and `REGISTRY` dict.

**Steps:**
1. [PLANNING] Define `Recipe.normalize(raw_output: str, args: dict) -> NormalizedResult` Protocol.
2. [EXECUTION] Implement REGISTRY dict mapping recipe_name → Recipe instance/class.
3. [EXECUTION] Wire custom-py:module:func dynamic loader path (consumer in T04.09).
4. [VERIFICATION] Add Protocol-conformance test.
5. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- `Recipe` Protocol defined with `normalize(raw_output, args) -> NormalizedResult` signature.
- `REGISTRY` dict exists with 6 entries (5 built-in + custom-py dispatcher).
- Custom-py loader resolves `custom-py:module:func` strings.
- `tests/swarm/test_recipe_protocol.py` asserts Protocol conformance for each entry.

**Validation:**
- `uv run pytest tests/swarm/test_recipe_protocol.py -v` passes.
- `from superclaude.cli.swarm.recipes import REGISTRY; assert len(REGISTRY) >= 6`.

**Dependencies:** T01.10 (NormalizationSpec). **Rollback:** revert recipes package.

### T04.03 -- Port `bare_review_v1` recipe (preserves t2_normalize.py logic)

| Field | Value |
|---|---|
| Roadmap | R-088 (COMP-016) |
| Deliverables | D-0070 |
| Effort | M |
| Risk | MEDIUM |
| Tier | STRICT |
| Confidence | `[████████--] 80%` |
| Critical Path Override | YES |
| MCP Tools | Read, Edit, auggie (locate t2_normalize.py) |
| Sub-Agent | tech-research (verbatim port verification) |
| Verification | tests: `uv run pytest tests/swarm/test_recipe_bare_review.py` |

**Deliverables:**
1. `src/superclaude/cli/swarm/recipes/bare_review_v1.py` porting `t2_normalize.py` logic.
2. A/B fixture corpus + parity assertions vs current `t2_normalize.py` output.

**Steps:**
1. [PLANNING] Locate legacy `t2_normalize.py` in `src/superclaude/skills/sc-bare-review/scripts/`.
2. [EXECUTION] Port shape-transformation logic verbatim into `bare_review_v1.py`.
3. [EXECUTION] Register in REGISTRY as `bare_review_v1`.
4. [VERIFICATION] A/B test: identical input → byte-identical output between legacy and ported.
5. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- Output matches bare-review compressed-table shape exactly.
- A/B parity: legacy `t2_normalize.py` vs `bare_review_v1` byte-identical on corpus.
- Recipe registered in REGISTRY under `bare_review_v1`.
- `tests/swarm/test_recipe_bare_review.py` green.

**Validation:**
- `uv run pytest tests/swarm/test_recipe_bare_review.py -v` passes.
- Legacy vs ported byte-identical on fixture corpus.

**Dependencies:** T04.02. **Rollback:** disable bare_review_v1 entry; legacy script remains operational.
**Notes:** Gates TEST-003 bare-review parity gate (M8).

### T04.04 -- Implement `findings_table_v1` recipe

| Field | Value |
|---|---|
| Roadmap | R-089 (COMP-017) |
| Deliverables | D-0071 |
| Effort | S |
| Risk | LOW |
| Tier | STANDARD |
| Confidence | `[████████--] 85%` |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/test_recipe_findings_table.py` |

**Deliverables:**
1. `src/superclaude/cli/swarm/recipes/findings_table_v1.py` producing findings-table output.

**Steps:**
1. [PLANNING] Define findings-table column set (lens-shared).
2. [EXECUTION] Implement recipe producing markdown table.
3. [EXECUTION] Register in REGISTRY.
4. [VERIFICATION] Test against fixture input.
5. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- Recipe produces findings-table normalized output for findings-shape lenses.
- AC-011 holds: no scoring/dedup/reorder.
- Registered in REGISTRY.
- `tests/swarm/test_recipe_findings_table.py` green.

**Validation:**
- `uv run pytest tests/swarm/test_recipe_findings_table.py -v` passes.
- REGISTRY contains `findings_table_v1`.

**Dependencies:** T04.02. **Rollback:** remove entry; lenses fall back to passthrough.

### T04.05 -- Implement `hypothesis_table_v1` recipe

| Field | Value |
|---|---|
| Roadmap | R-090 (COMP-018) |
| Deliverables | D-0072 |
| Effort | S |
| Risk | LOW |
| Tier | STANDARD |
| Confidence | `[████████--] 85%` |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/test_recipe_hypothesis_table.py` |

**Deliverables:**
1. `src/superclaude/cli/swarm/recipes/hypothesis_table_v1.py` producing hypothesis-table output.

**Steps:**
1. [PLANNING] Define hypothesis-table column set.
2. [EXECUTION] Implement recipe and register.
3. [VERIFICATION] Run fixture test.
4. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- Recipe produces hypothesis-table output (cause, evidence, confidence, next-step columns).
- AC-011 holds.
- Registered in REGISTRY.
- `tests/swarm/test_recipe_hypothesis_table.py` green.

**Validation:**
- `uv run pytest tests/swarm/test_recipe_hypothesis_table.py -v` passes.
- REGISTRY contains `hypothesis_table_v1`.

**Dependencies:** T04.02. **Rollback:** remove entry.

### T04.06 -- Checkpoint: Phase 4 mid-phase gate (tasks 1-5 verified)

| Field | Value |
|---|---|
| Type | CHECKPOINT (mid-phase) |
| Deliverables | D-CP4-1 |
| Tier | EXEMPT |

**Acceptance Criteria:**
- All of T04.01..T04.05 marked done in execution-log.
- `phase-4-cp1.md` checkpoint report written.
- Recipe Protocol + 3 recipes registered (bare_review_v1, findings_table_v1, hypothesis_table_v1).
- A/B parity for bare_review_v1 vs legacy t2_normalize.py confirmed.

**Validation:**
- `uv run pytest tests/swarm/test_recipe_protocol.py tests/swarm/test_recipe_bare_review.py -v` passes.
- Checkpoint file under `tasklist/checkpoints/`.

**Dependencies:** T04.01..T04.05.

### T04.07 -- Implement `verdict_only_v1` recipe

| Field | Value |
|---|---|
| Roadmap | R-091 (COMP-019) |
| Deliverables | D-0073 |
| Effort | S |
| Risk | LOW |
| Tier | STANDARD |
| Confidence | `[████████--] 85%` |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/test_recipe_verdict_only.py` |

**Deliverables:**
1. `src/superclaude/cli/swarm/recipes/verdict_only_v1.py` producing single-verdict output.

**Steps:**
1. [PLANNING] Define verdict-shape: yes/no/uncertain + 1-line rationale.
2. [EXECUTION] Implement recipe and register.
3. [VERIFICATION] Fixture test.
4. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- Recipe produces verdict-only output.
- AC-011 holds.
- Registered in REGISTRY.
- `tests/swarm/test_recipe_verdict_only.py` green.

**Validation:**
- `uv run pytest tests/swarm/test_recipe_verdict_only.py -v` passes.
- REGISTRY contains `verdict_only_v1`.

**Dependencies:** T04.02. **Rollback:** remove entry.

### T04.08 -- Implement `passthrough` recipe (raw-mode shape)

| Field | Value |
|---|---|
| Roadmap | R-092 (COMP-020) |
| Deliverables | D-0074 |
| Effort | S |
| Risk | LOW |
| Tier | STRICT |
| Confidence | `[█████████-] 95%` |
| Critical Path Override | YES |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/test_recipe_passthrough.py` |

**Deliverables:**
1. `src/superclaude/cli/swarm/recipes/passthrough.py` returning input unchanged.

**Steps:**
1. [PLANNING] Confirm raw-mode contract requires byte-identity.
2. [EXECUTION] Implement `Passthrough.normalize(raw, args) -> raw`.
3. [EXECUTION] Register in REGISTRY.
4. [VERIFICATION] Byte-identity assertion test.
5. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- Recipe returns input bytes unchanged (byte-identical).
- Used by `amalgamation_mode == raw`.
- Registered in REGISTRY.
- `tests/swarm/test_recipe_passthrough.py` green.

**Validation:**
- `uv run pytest tests/swarm/test_recipe_passthrough.py -v` passes.
- Output bytes == input bytes for random fixture.

**Dependencies:** T04.02. **Rollback:** none — used by raw mode.

### T04.09 -- Implement `custom-py` dynamic loader recipe

| Field | Value |
|---|---|
| Roadmap | R-093 (COMP-021) |
| Deliverables | D-0075 |
| Effort | M |
| Risk | MEDIUM |
| Tier | STRICT |
| Confidence | `[████████--] 80%` |
| Critical Path Override | YES |
| MCP Tools | Read, Edit, context7 (importlib) |
| Sub-Agent | tech-research (security boundary review) |
| Verification | tests: `uv run pytest tests/swarm/test_recipe_custom_py.py` |

**Deliverables:**
1. `src/superclaude/cli/swarm/recipes/custom.py` resolving `custom-py:module:func` recipes.

**Steps:**
1. [PLANNING] Define safe load semantics: explicit module:func only, no auto-discovery.
2. [EXECUTION] Implement `load_custom_py(spec: str) -> Recipe` via `importlib.import_module`.
3. [EXECUTION] Document trust boundary in module docstring.
4. [VERIFICATION] Test loads fixture module:func and refuses invalid specs.
5. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- Loader resolves `custom-py:module:func` strings to callable Recipe.
- Invalid specs (missing colon, missing module, missing func) raise clear errors.
- No auto-discovery / no walking of filesystem.
- `tests/swarm/test_recipe_custom_py.py` green.

**Validation:**
- `uv run pytest tests/swarm/test_recipe_custom_py.py -v` passes.
- Module docstring documents trust boundary.

**Dependencies:** T04.02. **Rollback:** disable custom-py entry; document workaround.
**Notes:** Security review per OPS-005 lens contribution policy.

### T04.10 -- Verify Recipe Protocol REGISTRY has 6 normalizers

| Field | Value |
|---|---|
| Roadmap | R-094 (FR-010) |
| Deliverables | D-0076 |
| Effort | S |
| Risk | LOW |
| Tier | STANDARD |
| Confidence | `[█████████-] 90%` |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/test_recipe_registry.py` |

**Deliverables:**
1. `tests/swarm/test_recipe_registry.py` enumerates and validates each REGISTRY entry.

**Steps:**
1. [PLANNING] Enumerate expected 6 entries.
2. [EXECUTION] Write test iterating REGISTRY and asserting Protocol conformance.
3. [VERIFICATION] Run test.
4. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- All 6 recipes resolvable by name from REGISTRY.
- Each entry implements `Recipe` Protocol (callable signature).
- Custom-py loads dynamically when given fixture spec.
- `tests/swarm/test_recipe_registry.py` green.

**Validation:**
- `uv run pytest tests/swarm/test_recipe_registry.py -v` passes.
- `len(REGISTRY) == 6` asserted.

**Dependencies:** T04.03..T04.09. **Rollback:** none — registration guard.

### T04.11 -- Implement parse-error→success salvage promotion (§7.4)

| Field | Value |
|---|---|
| Roadmap | R-095 (FR-028) |
| Deliverables | D-0077 |
| Effort | S |
| Risk | MEDIUM |
| Tier | STANDARD |
| Confidence | `[████████--] 85%` |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/test_parse_error_salvage.py` |

**Deliverables:**
1. `normalize.py::salvage_parse_error(worker_result) -> WorkerResult` promoting salvageable parse_error→success.
2. Meta sidecar records salvage provenance.

**Steps:**
1. [PLANNING] Enumerate §7.4 salvage conditions.
2. [EXECUTION] Implement salvage logic in `normalize.py`.
3. [EXECUTION] Mark `.meta.json` with `salvaged: true` when promotion fires.
4. [VERIFICATION] Test salvageable parse_error → success; non-salvageable → failed.
5. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- Salvageable parse_error reclassified as success.
- Meta sidecar records `salvaged: true` with reason.
- Non-salvageable parse_errors retain failed status.
- `tests/swarm/test_parse_error_salvage.py` green.

**Validation:**
- `uv run pytest tests/swarm/test_parse_error_salvage.py -v` passes.
- Two fixtures: salvageable + non-salvageable both correctly classified.

**Dependencies:** T04.01. **Rollback:** disable salvage; emit failed for all parse_errors.

### T04.12 -- Author bare-review output template

| Field | Value |
|---|---|
| Roadmap | R-096 (COMP-034) |
| Deliverables | D-0078 |
| Effort | S |
| Risk | LOW |
| Tier | STANDARD |
| Confidence | `[█████████-] 90%` |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | tests: render assertion against fixture |

**Deliverables:**
1. `src/superclaude/skills/sc-bare-review/refs/templates/bare-review-output.md` compressed-table template.

**Steps:**
1. [PLANNING] Confirm shape from `bare_review_v1` recipe output.
2. [EXECUTION] Author markdown template with documented placeholders.
3. [VERIFICATION] Recipe output renders against template without unbound vars.
4. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- `bare-review-output.md` template exists with compressed findings table shape.
- Validator U-008 (T02.16) asserts template path resolves.
- Template references match bare_review_v1 recipe output schema.
- Render test against fixture passes.

**Validation:**
- `uv run pytest tests/swarm/test_bare_review_template.py -v` passes.
- `make verify-sync` finds template in both src and `.claude/` paths.

**Dependencies:** T04.03 (bare_review_v1). **Rollback:** revert template.

### T04.12a -- Checkpoint: Phase 4 mid-phase gate (tasks 6-12)

| Field | Value |
|---|---|
| Type | CHECKPOINT (mid-phase) |
| Deliverables | D-CP4-1 |
| Tier | EXEMPT |

**Acceptance Criteria:**
- All of T04.06..T04.12 marked done in execution-log.
- `phase-4-cp2.md` checkpoint report written.
- 6-recipe REGISTRY complete; salvage promotion working; bare-review template authored.
- AC-011 boundary deferred to T04.14.

**Validation:**
- `uv run pytest tests/swarm/test_recipe_registry.py tests/swarm/test_parse_error_salvage.py -v` passes.
- Checkpoint file under `tasklist/checkpoints/`.

**Dependencies:** T04.06..T04.12.

### T04.13 -- Author per-lens output templates (6 non-custom lenses)

| Field | Value |
|---|---|
| Roadmap | R-097 (COMP-035) |
| Deliverables | D-0079 |
| Effort | M |
| Risk | MEDIUM |
| Tier | STANDARD |
| Confidence | `[████████--] 80%` |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/test_per_lens_templates.py` |

**Deliverables:**
1. 6 template files under `src/superclaude/cli/swarm/lenses/templates/` (refactor-find, edge-case-hunt, spec-completeness, feasibility-probe, troubleshoot-hypothesis, doc-completeness).

**Steps:**
1. [PLANNING] Map each non-custom lens to its expected recipe (findings_table/hypothesis_table/verdict_only).
2. [EXECUTION] Author 6 templates matching each lens's recipe shape.
3. [VERIFICATION] U-008 validator (T02.16) asserts each template path resolves.
4. [VERIFICATION] Recipe↔template alignment test.
5. [COMPLETION] `make sync-dev && make verify-sync`.

**Acceptance Criteria:**
- Each non-custom bundled lens has a matching output template.
- Validator asserts recipe↔template alignment for every lens.
- Templates render against recipe fixture without unbound vars.
- `tests/swarm/test_per_lens_templates.py` green.

**Validation:**
- `uv run pytest tests/swarm/test_per_lens_templates.py -v` passes.
- `ls src/superclaude/cli/swarm/lenses/templates/ | wc -l` reports ≥6.

**Dependencies:** T04.04, T04.05, T04.07, T02.16. **Rollback:** revert templates; lenses fail validation.

### T04.14 -- Enforce AC-011 no-scoring/dedup/reorder boundary in recipes

| Field | Value |
|---|---|
| Roadmap | R-098 (AC-011) |
| Deliverables | D-0080 |
| Effort | S |
| Risk | HIGH |
| Tier | STRICT |
| Confidence | `[████████--] 85%` |
| Critical Path Override | YES |
| MCP Tools | Read, Edit, Bash (grep) |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/test_recipe_no_judging.py` |

**Deliverables:**
1. `tests/swarm/test_recipe_no_judging.py` boundary test ensuring recipes preserve all findings.

**Steps:**
1. [PLANNING] Enumerate forbidden recipe behaviors.
2. [EXECUTION] Write fixture with 5 findings; assert all 5 present in normalized output.
3. [EXECUTION] Write fixture with duplicates; assert duplicates preserved.
4. [VERIFICATION] Run boundary test across all 6 recipes.
5. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- Recipe output preserves all findings; no judging transforms applied.
- Fixture with duplicate findings retains duplicates.
- Fixture with N findings retains N findings.
- `tests/swarm/test_recipe_no_judging.py` green for all 6 recipes.

**Validation:**
- `uv run pytest tests/swarm/test_recipe_no_judging.py -v` passes.
- `grep -RnE "sort|dedup|score|filter" src/superclaude/cli/swarm/recipes/` finds no judging logic.

**Dependencies:** T04.10. **Rollback:** none — boundary guard.
**Notes:** This guards the same neutrality boundary as merge module (FR-012).

### T04.15 -- Checkpoint: Phase 4 exit gate (end-of-phase)

| Field | Value |
|---|---|
| Type | CHECKPOINT (end-of-phase) |
| Deliverables | D-CP4-1 |
| Tier | EXEMPT |

**Acceptance Criteria:**
- All of T04.01..T04.14 marked done in execution-log.
- `phase-4-cp3.md` end-of-phase checkpoint written.
- 6-recipe REGISTRY + salvage + per-lens templates + AC-011 boundary all green.
- Wave 2 normalize produces correct output for each amalgamation mode.

**Validation:**
- `uv run pytest tests/swarm/test_recipe_registry.py tests/swarm/test_recipe_no_judging.py tests/swarm/test_per_lens_templates.py -v` passes.
- Checkpoint file under `tasklist/checkpoints/`.

**Dependencies:** T04.01..T04.14. **Rollback:** none — phase exit gate.
**Notes:** M4 exit unblocks M5 reduce/merge work.
