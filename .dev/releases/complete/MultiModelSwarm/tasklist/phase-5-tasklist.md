# Phase 5 -- Reduce, Merge, Status & Result Contract (Wave 3)

**Goal:** Build Wave 3 — IMM-5 success-first status determination (`M==N` → success; `2≤M<N` → partial; `M<2` → failed; `M==N==2` → success), the ≤30 LOC mechanical-merge module behind four structural guards (docstring contract, LOC ceiling, PR-review discipline, boundary test), the three amalgamation modes dispatch (`raw`/`normalize`/`normalize+merge`), and the final `return-contract.yaml` emission with full DM-012 field surface. Exit when the IMM-5 status matrix is parametrized + green, merge produces all N sections in slot-index order with provenance header only (no scoring/dedup/reorder/rewrite/filter), boundary test is CI-protected, and `return-contract.yaml` contains every required field.

### T05.01 -- Build `reduce` (Wave 3) module with status + contract emission

| Field | Value |
|---|---|
| Roadmap | R-099 (COMP-009) |
| Deliverables | D-0081 |
| Effort | M |
| Risk | HIGH |
| Tier | STRICT |
| Confidence | `[████████--] 85%` |
| Critical Path Override | YES |
| MCP Tools | Read, Edit, auggie, serena |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/test_reduce.py` |

**Deliverables:**
1. `src/superclaude/cli/swarm/reduce.py` with `reduce_wave3(worker_results, mode) -> ResultContract`.
2. Status determination + contract emission + merge trigger in `normalize+merge` mode.

**Steps:**
1. [PLANNING] Auggie-retrieve sprint reduce-equivalent for any pattern parity.
2. [EXECUTION] Implement `reduce_wave3` calling status logic (T05.03) and contract emitter (T05.07).
3. [EXECUTION] Trigger merge module (T05.05) when mode == `normalize+merge`.
4. [VERIFICATION] Integration test against M4 normalized outputs.
5. [COMPLETION] `make sync-dev && make verify-sync`.

**Acceptance Criteria:**
- Computes status; emits contract; triggers merge in `normalize+merge` mode.
- All writes atomic and confined to `--output`.
- Contract emission gated behind status determination.
- `tests/swarm/test_reduce.py` covers all three amalgamation modes.

**Validation:**
- `uv run pytest tests/swarm/test_reduce.py -v` passes.
- Integration test reaches terminal state in each mode.

**Dependencies:** T05.02 (merge), T01.10 (ResultContract). **Rollback:** revert reduce module.

### T05.02 -- Build `merge` module (≤30 LOC, mechanical concat only)

| Field | Value |
|---|---|
| Roadmap | R-100 (COMP-010) |
| Deliverables | D-0082 |
| Effort | S |
| Risk | HIGH |
| Tier | STRICT |
| Confidence | `[████████--] 85%` |
| Critical Path Override | YES |
| MCP Tools | Read, Edit, auggie |
| Sub-Agent | tech-research (boundary review) |
| Verification | tests: `uv run pytest tests/swarm/test_merge_mechanical_only.py tests/swarm/test_merge_loc_ceiling.py` |

**Deliverables:**
1. `src/superclaude/cli/swarm/merge.py` body ≤30 LOC performing mechanical concat with provenance header.

**Steps:**
1. [PLANNING] Author docstring listing allowed ops (concat, frontmatter strip, provenance prepend) vs disallowed (sort/score/dedup/filter/rewrite).
2. [EXECUTION] Implement `mechanical_merge(worker_results) -> str` ≤30 LOC body.
3. [EXECUTION] Prepend `## From {model_label} ({elapsed_ms}ms)` per section.
4. [VERIFICATION] LOC ceiling test + 3-worker concat test.
5. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- Body ≤30 LOC (excluding imports + docstring); LOC-ceiling test asserts.
- Concats N sections in slot-index order with provenance header only.
- No sort/score/dedup/filter/rewrite operations.
- `tests/swarm/test_merge_mechanical_only.py` + `test_merge_loc_ceiling.py` green.

**Validation:**
- `uv run pytest tests/swarm/test_merge_mechanical_only.py tests/swarm/test_merge_loc_ceiling.py -v` passes.
- `awk '/^\"\"\"/{f=!f;next} !f && NF{c++} END{print c}' src/superclaude/cli/swarm/merge.py` returns ≤30.

**Dependencies:** none — pure-function. **Rollback:** revert merge.py; reduce falls back to raw-output emission.
**Notes:** Four structural guards: docstring (here), LOC ceiling (T05.08), PR review (CI rule), boundary test (T05.09).

### T05.03 -- Implement IMM-5 success-first status determination

| Field | Value |
|---|---|
| Roadmap | R-101 (IMM-5) |
| Deliverables | D-0083 |
| Effort | M |
| Risk | MEDIUM |
| Tier | STRICT |
| Confidence | `[████████--] 85%` |
| Critical Path Override | YES |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/test_imm5_status.py` |

**Deliverables:**
1. `reduce.py::determine_status(M, N, policy) -> str` with parametrized test covering all branches.

**Steps:**
1. [PLANNING] Author truth table: M==N→success, 2≤M<N→partial, M<2→failed, M==N==2→success.
2. [EXECUTION] Implement `determine_status` respecting `StatusPolicy.floor` (default 2) and `success_first` (default true).
3. [VERIFICATION] Parametrized test enumerates all matrix branches.
4. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- Parametrized status test covers M==N / 2≤M<N / M<2 / M==N==2 branches.
- StatusPolicy.floor and success_first respected (configurable).
- Edge case M==N==2 → success not partial.
- `tests/swarm/test_imm5_status.py` green.

**Validation:**
- `uv run pytest tests/swarm/test_imm5_status.py -v` passes (all parametrize cases).
- Test count matches matrix branch count.

**Dependencies:** T01.10 (StatusPolicy). **Rollback:** none — guard.

### T05.04 -- Implement three amalgamation modes dispatch

| Field | Value |
|---|---|
| Roadmap | R-102 (FR-011) |
| Deliverables | D-0084 |
| Effort | M |
| Risk | MEDIUM |
| Tier | STANDARD |
| Confidence | `[████████--] 85%` |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/test_amalgamation_modes.py` |

**Deliverables:**
1. `reduce.py::select_mode(amalgamation_mode) -> Callable` dispatch table.

**Steps:**
1. [PLANNING] Define behaviors per mode: raw (passthrough), normalize (recipe per worker), normalize+merge (normalize + mechanical concat).
2. [EXECUTION] Implement dispatch in `reduce.py`.
3. [VERIFICATION] Test each mode produces correct artifact set.
4. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- Each mode (`raw`/`normalize`/`normalize+merge`) produces correct artifact set.
- Mode dispatch tested independently.
- `normalize+merge` includes `merged.md`; `normalize` produces `.final.md` only; `raw` produces `.raw.md` only.
- `tests/swarm/test_amalgamation_modes.py` green.

**Validation:**
- `uv run pytest tests/swarm/test_amalgamation_modes.py -v` passes.
- Three modes verified with separate fixtures.

**Dependencies:** T05.01, T04.08 (passthrough). **Rollback:** disable merge mode, retain raw + normalize.

### T05.05 -- Implement mechanical merge module (4 guards)

| Field | Value |
|---|---|
| Roadmap | R-103 (FR-012) |
| Deliverables | D-0085 |
| Effort | M |
| Risk | HIGH |
| Tier | STRICT |
| Confidence | `[████████--] 85%` |
| Critical Path Override | YES |
| MCP Tools | Read, Edit |
| Sub-Agent | tech-research (4-guard validation) |
| Verification | tests: `uv run pytest tests/swarm/test_merge_mechanical_only.py` |

**Deliverables:**
1. Four structural guards wired: docstring allowed/disallowed enumeration, ≤30 LOC ceiling test, PR-review boundary note, boundary test file (CI-flagged).

**Steps:**
1. [PLANNING] Confirm T05.02 module body, T05.08 LOC test, T05.09 boundary test wiring.
2. [EXECUTION] Author docstring listing allowed (concat, frontmatter strip, provenance header) and disallowed (sort, score, dedup, filter, rewrite, reorder).
3. [EXECUTION] Add PR-review boundary note + CI rule path documentation.
4. [VERIFICATION] All 4 guards present and enforced.
5. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- All 4 guards present and enforced: docstring contract, ≤30 LOC ceiling, PR-review discipline, boundary test.
- Each guard has an enforcement mechanism (test, CI rule, doc).
- Boundary test file `test_merge_mechanical_only.py` flagged in CI on PR touches.
- Merge output preserves all worker sections verbatim in slot order.

**Validation:**
- `uv run pytest tests/swarm/test_merge_mechanical_only.py -v` passes.
- Docstring contains explicit allowed/disallowed enumeration.

**Dependencies:** T05.02, T05.08, T05.09. **Rollback:** none — boundary protection.
**Notes:** This is the single highest-risk boundary in the swarm — drift here violates caller-facing neutrality.

### T05.06 -- Checkpoint: Phase 5 mid-phase gate (tasks 1-5 verified)

| Field | Value |
|---|---|
| Type | CHECKPOINT (mid-phase) |
| Deliverables | D-CP5-1 |
| Tier | EXEMPT |

**Acceptance Criteria:**
- All of T05.01..T05.05 marked done in execution-log.
- `phase-5-cp1.md` checkpoint report written.
- reduce + merge + IMM-5 status all green.
- 4 structural guards on merge module present.

**Validation:**
- `uv run pytest tests/swarm/test_reduce.py tests/swarm/test_imm5_status.py tests/swarm/test_merge_mechanical_only.py -v` passes.
- Checkpoint file under `tasklist/checkpoints/`.

**Dependencies:** T05.01..T05.05.

### T05.07 -- Implement result contract emission (`return-contract.yaml`)

| Field | Value |
|---|---|
| Roadmap | R-104 (FR-018) |
| Deliverables | D-0086 |
| Effort | M |
| Risk | MEDIUM |
| Tier | STRICT |
| Confidence | `[████████--] 85%` |
| Critical Path Override | YES |
| MCP Tools | Read, Edit, context7 (PyYAML) |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/test_contract_emission.py` |

**Deliverables:**
1. `reduce.py::emit_contract(result) -> Path` writing `return-contract.yaml`.

**Steps:**
1. [PLANNING] Enumerate DM-012 fields: contract_version, status, job_id, lens, amalgamation_mode, output_files, merged_path, caller_metadata, recommended_next_command, artifacts.
2. [EXECUTION] Implement YAML serialization with atomic write.
3. [EXECUTION] Apply `recommended_next_command` template substitution from JobSpec.
4. [VERIFICATION] Field-completeness test against DM-012 schema.
5. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- Contract contains all DM-012 fields; valid YAML.
- `recommended_next_command` substituted from template + substitutions dict.
- Atomic write via tmp+`os.replace`.
- `tests/swarm/test_contract_emission.py` green.

**Validation:**
- `uv run pytest tests/swarm/test_contract_emission.py -v` passes.
- `yq '.contract_version, .status, .job_id, .lens' return-contract.yaml` returns non-null.

**Dependencies:** T01.10 (ResultContract), T05.01. **Rollback:** emit JSON sidecar fallback.

### T05.08 -- Enforce merge.py ≤30 LOC ceiling in CI

| Field | Value |
|---|---|
| Roadmap | R-105 (NFR-008), R-108 (AC-018) merged |
| Deliverables | D-0087 |
| Effort | S |
| Risk | MEDIUM |
| Tier | STRICT |
| Confidence | `[█████████-] 90%` |
| Critical Path Override | YES |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/test_merge_loc_ceiling.py` |

**Deliverables:**
1. `tests/swarm/test_merge_loc_ceiling.py` enforcing ≤30 LOC body assertion.

**Steps:**
1. [PLANNING] Define LOC counting rule: exclude imports, exclude docstring, count non-blank lines.
2. [EXECUTION] Write test reading `merge.py` and counting body LOC.
3. [EXECUTION] Assert ≤30.
4. [VERIFICATION] Run test.
5. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- LOC count assertion passes in CI for `merge.py`.
- Counting rule documented in test docstring (matches NFR-008).
- Test fails if body exceeds 30 LOC.
- `tests/swarm/test_merge_loc_ceiling.py` green.

**Validation:**
- `uv run pytest tests/swarm/test_merge_loc_ceiling.py -v` passes.
- LOC tool returns ≤30 for `merge.py`.

**Dependencies:** T05.02. **Rollback:** none — boundary guard.

### T05.09 -- Author boundary enforcement test (3-worker concat assertion)

| Field | Value |
|---|---|
| Roadmap | R-106 (NFR-009) |
| Deliverables | D-0088 |
| Effort | S |
| Risk | HIGH |
| Tier | STRICT |
| Confidence | `[████████--] 85%` |
| Critical Path Override | YES |
| MCP Tools | Read, Edit |
| Sub-Agent | tech-research (boundary verification) |
| Verification | tests: `uv run pytest tests/swarm/test_merge_mechanical_only.py` |

**Deliverables:**
1. `tests/swarm/test_merge_mechanical_only.py` asserting 3-worker concat preserves slot order + provenance header only.
2. CI rule flagging PRs that modify this test file.

**Steps:**
1. [PLANNING] Compose 3-worker fixture with distinct content.
2. [EXECUTION] Write boundary test: 3 sections in slot-index order, provenance header only, no other transforms.
3. [EXECUTION] Document CI rule on file path (`.github/workflows/ci.yml` PR-touch check).
4. [VERIFICATION] Run test; verify CI rule active.
5. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- 3-worker concat yields all 3 sections in slot-index order with provenance header only.
- No transforms beyond `## From {model_label} ({elapsed_ms}ms)` header.
- CI rule flags PRs touching this test file.
- `tests/swarm/test_merge_mechanical_only.py` green.

**Validation:**
- `uv run pytest tests/swarm/test_merge_mechanical_only.py -v` passes.
- `.github/workflows/` references the test file in PR-touch check.

**Dependencies:** T05.02, T05.05. **Rollback:** none — boundary guard.
**Notes:** This file is one of two with explicit PR-review-discipline guards (the other is the recipe boundary).

### T05.10 -- Enforce AC-012 no-new-merge/diff/scoring-engine guard

| Field | Value |
|---|---|
| Roadmap | R-107 (AC-012) |
| Deliverables | D-0089 |
| Effort | S |
| Risk | LOW |
| Tier | STRICT |
| Confidence | `[█████████-] 90%` |
| Critical Path Override | YES |
| MCP Tools | Read, Edit, Bash (grep) |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/test_no_scoring_engine.py` |

**Deliverables:**
1. `tests/swarm/test_no_scoring_engine.py` grep audit for scoring/diff engine code.

**Steps:**
1. [PLANNING] Enumerate forbidden patterns: scoring engines, diff libraries, ranking algorithms in swarm.
2. [EXECUTION] Write grep-based test scanning swarm package.
3. [VERIFICATION] Run test.
4. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- No scoring/diff engine code in swarm package.
- Test fails if such code introduced.
- `/sc:adversarial` referenced as the canonical scoring-merge pipeline.
- `tests/swarm/test_no_scoring_engine.py` green.

**Validation:**
- `uv run pytest tests/swarm/test_no_scoring_engine.py -v` passes.
- `grep -RnE "rank|score|judge|adversarial" src/superclaude/cli/swarm/merge.py` returns empty.

**Dependencies:** T05.05. **Rollback:** none — guard.

### T05.10a -- Checkpoint: Phase 5 boundary gate (tasks 7-10 verified)

| Field | Value |
|---|---|
| Type | CHECKPOINT (mid-phase) |
| Deliverables | D-CP5-1 |
| Tier | EXEMPT |

**Acceptance Criteria:**
- All of T05.07..T05.10 marked done in execution-log.
- `phase-5-cp2.md` checkpoint report written.
- Contract emission complete; LOC ceiling + boundary test + scoring-engine guard all green.
- 4 merge boundary guards verified.

**Validation:**
- `uv run pytest tests/swarm/test_contract_emission.py tests/swarm/test_merge_loc_ceiling.py tests/swarm/test_no_scoring_engine.py -v` passes.
- Checkpoint file under `tasklist/checkpoints/`.

**Dependencies:** T05.07..T05.10.

### T05.11 -- Enforce AC-011 merge-no-transforms boundary variant test

| Field | Value |
|---|---|
| Roadmap | R-109 (AC-011 — merge context) |
| Deliverables | D-0090 |
| Effort | S |
| Risk | MEDIUM |
| Tier | STRICT |
| Confidence | `[████████--] 85%` |
| Critical Path Override | YES |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/test_merge_no_transforms.py` |

**Deliverables:**
1. `tests/swarm/test_merge_no_transforms.py` complementary boundary test for merge path.

**Steps:**
1. [PLANNING] Compose duplicate-finding fixture across 2 workers.
2. [EXECUTION] Write test asserting duplicates preserved across worker sections.
3. [EXECUTION] Write test asserting no sort/reorder of within-section findings.
4. [VERIFICATION] Run test.
5. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- Merge output preserves every worker section verbatim + ordered.
- Duplicates across workers not deduplicated.
- No within-section reordering.
- `tests/swarm/test_merge_no_transforms.py` green.

**Validation:**
- `uv run pytest tests/swarm/test_merge_no_transforms.py -v` passes.
- Fixture with duplicates produces output with duplicates retained.

**Dependencies:** T05.02. **Rollback:** none — boundary guard variant.
**Notes:** Complementary to T05.09; provides AC-011 surface specifically for merge (vs T04.14 which covers recipes).

### T05.12 -- Checkpoint: Phase 5 exit gate (end-of-phase)

| Field | Value |
|---|---|
| Type | CHECKPOINT (end-of-phase) |
| Deliverables | D-CP5-1 |
| Tier | EXEMPT |

**Acceptance Criteria:**
- All of T05.01..T05.11 marked done in execution-log.
- `phase-5-cp3.md` end-of-phase checkpoint written.
- IMM-5 status + merge (≤30 LOC + 4 guards) + contract emission all green.
- M5 pipeline ready for M6 resume work.

**Validation:**
- `uv run pytest tests/swarm/ -v` Phase 5 surface passes.
- Checkpoint file under `tasklist/checkpoints/`.

**Dependencies:** T05.01..T05.11. **Rollback:** none — phase exit gate.
**Notes:** M5 exit unblocks M6 (resume) and M7 (observability/CLI).
