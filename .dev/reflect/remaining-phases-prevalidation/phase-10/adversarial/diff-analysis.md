<!-- Provenance: produced by /sc:adversarial Mode B (inline), Step 1 Diff Analysis -->

# Diff Analysis: Phase 10 (R1.5 verify-implementation) pre-execution validation

## Metadata
- Generated: 2026-06-02
- Mode: B (inline) — source = Phase 10 task items (L599-626) + BUILD-REQUEST §MVR §4 + R1.3 reflect correction
- Advocate stances: opus:architect (KEEP-leaning steelman), sonnet:analyzer (REFACTOR-leaning), haiku:qa (DISCARD/fragility-leaning)
- Items under review: 10.1, 10.2, 10.3, PG10.1, PG10.2

## Ground-truth facts established by Read/Grep (load-bearing)

- **GT-1 (CI-vs-runtime split is real and codified):** `code_assertions.py:assert_step_reachable(envelope, repo_root)` AST-parses `repo_root/"src"/"superclaude"/cli/roadmap/executor.py` and is fail-closed (missing file → HIGH Finding). It is a source-tree check. (`src/superclaude/cli/roadmap/code_assertions.py`)
- **GT-2 (the dispatch shim):** `cli/pipeline/gates.py:gate_passed(content, criteria, *, envelope=None, repo_root=None)` — at L93-98, if `code_assertions` exist but `envelope is None or repo_root is None`, it returns `(True, None)` (skips). Otherwise calls `assertion.check_fn(envelope, repo_root)`. CodeAssertions are dispatched WITH `repo_root` — a source-tree handle.
- **GT-3 (fidelity_checker scans a source tree):** `fidelity_checker.py:_scan_codebase` does `self.source_dir.rglob("*.py")` and AST-walks for FunctionDef/ClassDef names. `_extract_fr_mappings` reads `spec_path` (a run input artifact). The fail-open `found=True` is at L302 (no extractable names) and L320 (partial match), NOT L287-303/314-337 as the task/research cite — line numbers drifted ~3 lines.
- **GT-4 (production source_dir resolution is CWD-relative):** the existing call site `executor.py:1615-1619` sets `source_dir = Path("src/superclaude") if Path("src/superclaude").exists() else Path(".")`. At pipx-installed production runtime there is no `src/superclaude` in CWD → falls back to `Path(".")` = the user's arbitrary project dir. The scan target is undefined/wrong at production runtime.
- **GT-5 (step budget):** `_build_steps` has 13 `Step(` literals; `certify` is added dynamically via `build_certify_step()` (design §7.3 option a) → effective production count 14. `wiring-verification` step exists at `executor.py:2588`. Adding verify-implementation → 15 unless one consolidates. Acceptance Gate #6 cap = 14.
- **GT-6 (envelope.spec_ids is NOT a dict):** `envelope.spec_ids` is a `SpecIdRegistry` dataclass (`id_registry.py:43`) with `fr_ids: tuple[str,...]`. There is no `__getitem__`. The task's `envelope.spec_ids[FR]` subscript is a type error against the real envelope; the correct access is `envelope.spec_ids.fr_ids`.
- **GT-7 (envelope carries accepted_deviations):** `PipelineEnvelope.accepted_deviations: list[AcceptedDeviation]` exists (`envelope.py:202`), and `spec_ids.accepted_deviation_ids` carries the IDs — so the deviation-resolution branch CAN be runtime-grounded from the envelope.
- **GT-8 (sequencing prereq):** task L603 already encodes the H2 fix — Phase 10 must not ship before Step 11.4 (fail-open deletion) or must ship atomically with Phase 11.

## Structural Differences (spec intent vs task encoding)

| # | Area | Spec (§MVR §4) intent | Task (Phase 10) encoding | Severity |
|---|---|---|---|---|
| S-001 | Resolution substrate | "for each FR in `envelope.spec_ids[FR]`, finds importable callable OR finds via fidelity AST scan OR matches accepted deviation" — ambiguous whether AST scan targets the run's artifacts or the pipeline source tree | Step 10.2 explicitly routes FR resolution through `fidelity_checker._scan_codebase` (a source-tree scan) | High |
| S-002 | Gate placement | terminal, CodeAssertion-only gate after tasklist/certify | Step 10.1/10.2 place it terminal, gate `VERIFY_IMPLEMENTATION_GATE` with `code_assertions=[...]` only | Low |
| S-003 | Budget consolidation | not specified by §MVR §4 (a task-acceptance constraint, Gate #6) | Step 10.1/10.2 require consolidating wiring-verification OR certify to hold ≤14 | Medium |

## Content Differences (per-item approach)

| # | Topic | Approach in task | Severity |
|---|---|---|---|
| C-001 | What `assert_all_frs_resolved` inspects | Step 10.2: iterate FRs, try `_scan_codebase`, try `importlib.import_module`, check `accepted_deviations`; fail-closed default | High |
| C-002 | Gate field decl | `required_envelope_fields=["spec_ids"]`, `enforcement_tier="STRICT"`, `code_assertions=[CodeAssertion(...)]` | Low |
| C-003 | Test coverage | Step 10.3: all-resolve PASS, unresolved HALT, deviation PASS, dispatch-reachable, step-count≤14 | Low |
| C-004 | FR access pattern | `envelope.spec_ids[FR]` subscript | High (type error, GT-6) |

## Contradictions

| # | Point of conflict | Position A (task as written) | Position B (R1.3 correction) | Impact |
|---|---|---|---|---|
| X-001 | Can a source-tree FR→AST assertion gate a production run? | Step 10.2 wires `_scan_codebase` (source-tree) into a runtime `CodeAssertion` dispatched with `repo_root` (GT-2) | R1.3 merged-rec INV-001: source-tree assertions MUST NOT fire at production runtime (pipx package has no src/); they are CI-only | High |
| X-002 | Does the gate fire at runtime at all? | Step 10.2 implies a live terminal gate that HALTS on unmatched FR | If verify-implementation's assertion is source-tree CI-only, the envelope-None shim (GT-2) keeps it dormant at runtime → it gates nothing live; if it's wired to fire, it fails-closed on every installed run (GT-4) | High |
| X-003 | importlib resolution target | Step 10.2: `importlib.import_module` to find callable | At runtime the FR's "name binding" lives in the USER's generated project, not importable from the pipeline's namespace → import resolution is also source-tree/dev-only | High |

## Unique Contributions (task items adding value beyond spec)

| # | Item | Contribution | Value |
|---|---|---|---|
| U-001 | Step 10.3 `test_step_count_budget` | Adds a regression guard asserting `len(_build_steps()) <= 14` | High |
| U-002 | Step 10.3 `test_step_in_dispatch_map` | Reuses R1.3 `assert_step_reachable` to prove verify-implementation is wired | High |
| U-003 | Step 10.1 consolidation-choice design doc | Forces an explicit budget decision with rationale before coding | Medium |
| U-004 | PG10.1 adversarial rf-qa with fix_authorization | Independent fragility/false-halt probe | High |

## Shared Assumptions (UNSTATED preconditions — promoted)

| A-NNN | Assumption | Source agreement | Impact | Status |
|---|---|---|---|---|
| A-001 | The FR→implementation resolution can run meaningfully at production runtime | All three steps assume verify-implementation is a live gate | If FALSE (GT-1/GT-4), the step is either CI-only (dormant via shim) or fails-closed-spuriously | UNSTATED → **CONTRADICTED by GT-1/GT-4** |
| A-002 | `envelope.spec_ids` is subscriptable by FR id | Steps 10.2/10.3 use `spec_ids[FR]` | If FALSE (GT-6), implementation is a `TypeError` | UNSTATED → **CONTRADICTED by GT-6** |
| A-003 | The run's own artifacts (tasklist/roadmap) contain the FR→code link to verify at runtime | Implied by "Tasklist → AST link" naming | If TRUE, a runtime-safe formulation EXISTS (verify the run's tasklist asserts each FR maps to a named binding, AST-checked against the run's OWN emitted artifacts/accepted_deviations) | UNSTATED — this is the rescue path |

## Summary
- Structural: 3 (1 High). Content: 4 (2 High). Contradictions: 3 (all High). Unique: 4. Shared assumptions: 3 (2 CONTRADICTED, 1 rescue path).
- Highest-severity items: S-001, C-001, C-004, X-001, X-002, X-003, A-001, A-002.
- Central fault line: the task encodes verify-implementation's FR-resolution against the **pipeline source tree** (via `fidelity_checker._scan_codebase` + `importlib`), which is a CI-only substrate that cannot gate a production run — the exact hazard the R1.3 reflect correction flags.
