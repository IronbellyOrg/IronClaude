# Phase 0: Decision-Locking Pass — Gate-System Remediation

Generated: 2026-03-25
Source: `claudedocs/workflow_gate-system-remediation-4phases.md`

---

## Key architectural decisions (locked before per-task specs)

### D-01: Canonical artifact file names
| Step ID | Canonical output file | Rationale |
|---------|----------------------|-----------|
| `deviation-analysis` | `spec-deviations.md` | Already referenced in `_check_annotate_deviations_freshness()` (executor.py:1100) and freshness hash logic. NOT `deviation-analysis.md`. |
| `remediate` | `remediation-tasklist.md` | Already used in `generate_remediation_tasklist()` (remediate.py:159), `build_certify_step()` (executor.py:770), `check_remediate_resume()` (executor.py:2034). |
| `certify` | `certification-report.md` | Already used in `generate_certification_report()` (certify_prompts.py:179), `build_certify_step()` (executor.py:757), `check_certify_resume()` (executor.py:2067). |

**Name drift found**: `executor.py:1037` references `certify.md` in `_print_terminal_halt()`. This is cosmetic (terminal output string), not a runtime artifact path — but should be fixed for consistency.

### D-02: Deviation-analysis prompt builder does NOT exist
No `build_deviation_analysis_prompt()` function exists anywhere in `src/superclaude/cli/roadmap/`. The convergence engine produces `spec-deviations.md` via the structural/semantic/fidelity checker pipeline (executor.py:539-690), not via an LLM prompt step. The deviation-analysis step is a **non-LLM deterministic step** (like `anti-instinct`), not a prompt-driven step.

### D-03: Remediate step execution model
The `remediate` step is NOT a standard prompt-driven Step. It uses `execute_remediation()` from `remediate_executor.py:732` which spawns parallel agents with ThreadPoolExecutor. The step wiring must use `prompt=""` (non-LLM) and a custom runner path, similar to how `anti-instinct` works with `prompt=""`.

### D-04: Certify step execution model
`build_certify_step()` (executor.py:735-772) already produces a fully-formed `Step` with `id="certify"`, `gate=CERTIFY_GATE`, `output_file=certification-report.md`, `inputs=[remediation-tasklist.md]`. This IS a prompt-driven step using `build_certification_prompt()`.

### D-05: Observability-first mechanism
Use `gate_mode=GateMode.TRAILING` for initial rollout. This is the established pattern (used by `wiring-verification` at executor.py:926). In Phase 3, enforcement means changing `gate_mode` from `GateMode.TRAILING` to the default `GateMode.BLOCKING`.

### D-06: Step ordering in `_build_steps()`
New steps insert AFTER `wiring-verification` (the current last step at executor.py:927), in this order:
1. `deviation-analysis` (non-LLM, like anti-instinct)
2. `remediate` (non-LLM, custom executor)
3. `certify` (LLM prompt-driven, via build_certify_step pattern)

---

## Phase 1 Task Specifications

### P1-T1: Build gate contract matrix
**Complexity:** 2 — Read-only extraction from existing gate definitions, no judgment needed.
**Adversarial review required:** No

**Mechanical specification:**
- File: `claudedocs/workflow_gate-system-remediation-4phases.md` (or a linked appendix)
- Symbol/location: New section "Appendix B — Gate Contract Matrix"
- Change: Add a table with the following data, extracted verbatim from `src/superclaude/cli/roadmap/gates.py`:

**DEVIATION_ANALYSIS_GATE** (gates.py:1022-1073):
- Required frontmatter: `schema_version`, `total_analyzed`, `slip_count`, `intentional_count`, `pre_approved_count`, `ambiguous_count`, `routing_fix_roadmap`, `routing_no_action`, `analysis_complete`
- min_lines: 20
- enforcement_tier: STRICT
- Semantic checks (7): `no_ambiguous_deviations`, `validation_complete_true`, `routing_ids_valid`, `slip_count_matches_routing`, `pre_approved_not_in_fix_roadmap`, `total_analyzed_consistent`, `deviation_counts_reconciled`

**REMEDIATE_GATE** (gates.py:941-964):
- Required frontmatter: `type`, `source_report`, `source_report_hash`, `total_findings`, `actionable`, `skipped`
- min_lines: 10
- enforcement_tier: STRICT
- Semantic checks (2): `frontmatter_values_non_empty`, `all_actionable_have_status`

**CERTIFY_GATE** (gates.py:966-993):
- Required frontmatter: `findings_verified`, `findings_passed`, `findings_failed`, `certified`, `certification_date`
- min_lines: 15
- enforcement_tier: STRICT
- Semantic checks (3): `frontmatter_values_non_empty`, `per_finding_table_present`, `certified_is_true`

- Verification: Grep each gate constant in `gates.py` and confirm field counts match table.
- Before state: No contract matrix exists.
- After state: Matrix table documenting all 3 gates with exact field/check specifications.

**Dependencies:** None
**Produces:** Reference table consumed by P1-T2, P1-T4, P1-T5, P2-T1.

---

### P1-T2: Map producers for each required field
**Complexity:** 2 — Trace function outputs to gate requirements, read-only.
**Adversarial review required:** No

**Mechanical specification:**
- File: `claudedocs/workflow_gate-system-remediation-4phases.md` (same appendix)
- Change: Extend the contract matrix with a "Producer" column:

**DEVIATION_ANALYSIS_GATE producers:**
- All 9 frontmatter fields: produced by `_run_checkers()` + `_write_convergence_report()` in executor.py:595-732. The convergence engine writes `spec-deviations.md` with these fields. **Gap**: `_write_convergence_report()` (executor.py:692-732) does NOT write deviation-analysis frontmatter — it writes spec-fidelity frontmatter. The deviation analysis output is produced by `_check_annotate_deviations_freshness()` which reads but does not write. **Resolution needed in P2-T3**: a `_write_deviation_analysis_report()` function must be created OR the existing convergence registry export must produce gate-compliant output.

**REMEDIATE_GATE producers:**
- `type`: `generate_remediation_tasklist()` in remediate.py:178 — writes `type: remediation-tasklist`
- `source_report`: remediate.py:181
- `source_report_hash`: remediate.py:182 (SHA-256 of source content)
- `total_findings`: remediate.py:184
- `actionable`: remediate.py:185
- `skipped`: remediate.py:186
- All fields covered. No gaps.

**CERTIFY_GATE producers:**
- `findings_verified`: `generate_certification_report()` in certify_prompts.py:206
- `findings_passed`: certify_prompts.py:207
- `findings_failed`: certify_prompts.py:208
- `certified`: certify_prompts.py:209 (bool, `true`/`false`)
- `certification_date`: certify_prompts.py:210
- All fields covered. No gaps.

- Verification: For each producer, confirm the frontmatter field name in the producer matches the gate requirement exactly (string equality).
- Before state: No producer mapping exists.
- After state: Producer map with exact function:line references and one identified gap (deviation-analysis output writer).

**Dependencies:** P1-T1
**Produces:** Gap list consumed by P2-T3.

---

### P1-T3: Lock canonical artifact names/paths
**Complexity:** 2 — Inventory + one cosmetic fix identification.
**Adversarial review required:** No

**Mechanical specification:**
- File: `claudedocs/workflow_gate-system-remediation-4phases.md` (appendix)
- Change: Document canonical names per D-01 above, plus document the `certify.md` drift:
  - `executor.py:1037`: `certify_path = output_dir / "certify.md"` — this is in `_print_terminal_halt()` and is a display string only, not a runtime artifact producer. Should be changed to `"certification-report.md"` in P2-T1 for consistency.
- Verification: `grep -rn 'certify\.md' src/superclaude/cli/roadmap/` — confirm only the one hit at executor.py:1037.
- Before state: One non-canonical reference exists.
- After state: Documented with fix deferred to P2-T1.

**Dependencies:** None
**Produces:** Canonical name decisions consumed by P2-T1, P3-T3.

---

### P1-T4: Define entry/exit invariants per post-fidelity step
**Complexity:** 2 — Derived from gate contracts and step ordering.
**Adversarial review required:** No

**Mechanical specification:**
- File: `claudedocs/workflow_gate-system-remediation-4phases.md` (appendix)
- Change: Add invariant table:

| Step | Entry invariant | Exit invariant |
|------|----------------|----------------|
| `deviation-analysis` | `spec-fidelity.md` exists and was produced (status PASS or FAIL in state). `roadmap.md` exists. | `spec-deviations.md` has parseable YAML frontmatter with all 9 DEVIATION_ANALYSIS_GATE fields. |
| `remediate` | `spec-deviations.md` exists. `remediation-tasklist.md` does not yet exist OR is stale. | `remediation-tasklist.md` has parseable frontmatter with all 6 REMEDIATE_GATE fields. |
| `certify` | `remediation-tasklist.md` exists and passes REMEDIATE_GATE. | `certification-report.md` has parseable frontmatter with all 5 CERTIFY_GATE fields. |

- Verification: Each exit invariant maps 1:1 to the gate's `required_frontmatter_fields`.
- Before state: No invariant documentation.
- After state: Invariant table.

**Dependencies:** P1-T1, P1-T2
**Produces:** Reference for P2-T1 (step wiring inputs/outputs).

---

### P1-T5: Create objective contract verification checklist
**Complexity:** 1 — Reformatting existing data as checklist.
**Adversarial review required:** No

**Mechanical specification:**
- File: `claudedocs/workflow_gate-system-remediation-4phases.md` (appendix)
- Change: Add checklist section:

```markdown
### Contract Verification Checklist
- [ ] DEVIATION_ANALYSIS_GATE has exactly 9 required_frontmatter_fields
- [ ] DEVIATION_ANALYSIS_GATE has exactly 7 semantic_checks
- [ ] DEVIATION_ANALYSIS_GATE enforcement_tier == "STRICT"
- [ ] REMEDIATE_GATE has exactly 6 required_frontmatter_fields
- [ ] REMEDIATE_GATE has exactly 2 semantic_checks
- [ ] REMEDIATE_GATE enforcement_tier == "STRICT"
- [ ] CERTIFY_GATE has exactly 5 required_frontmatter_fields
- [ ] CERTIFY_GATE has exactly 3 semantic_checks
- [ ] CERTIFY_GATE enforcement_tier == "STRICT"
- [ ] generate_remediation_tasklist() produces all 6 REMEDIATE_GATE fields
- [ ] generate_certification_report() produces all 5 CERTIFY_GATE fields
- [ ] Deviation-analysis output writer gap is documented with resolution plan
```

- Verification: Each item is objectively pass/fail by reading code.
- Before state: No checklist.
- After state: 12-item checklist.

**Dependencies:** P1-T1, P1-T2
**Produces:** Acceptance criteria for Phase 1 checkpoint.

---

## Phase 2 Task Specifications

### P2-T1: Add runtime step wiring in `_build_steps()`
**Complexity:** 5 — Cascading architectural decision: step ordering, input/output wiring, gate mode, timeout, and interaction with convergence mode.
**Adversarial review required:** Yes

**Mechanical specification:**
- File: `src/superclaude/cli/roadmap/executor.py`
- Symbol/location: `_build_steps()`, after the `wiring-verification` Step (line 927), before `return steps` (line 930)

**Import additions** (at top of file, in the existing `.gates` import block, line 27-39):
- Add `DEVIATION_ANALYSIS_GATE` to the import from `.gates`
- Add `REMEDIATE_GATE` to the import from `.gates` (currently not imported at top level)
- `CERTIFY_GATE` is already imported (line 29)

**Output path variables** (add after `spec_fidelity_file` at line 796):
```python
deviation_file = out / "spec-deviations.md"
remediation_file = out / "remediation-tasklist.md"
certification_file = out / "certification-report.md"
```

**Step wiring** (insert after wiring-verification Step, before `return steps`):

Step 10: deviation-analysis (non-LLM deterministic step):
```python
Step(
    id="deviation-analysis",
    prompt="",  # non-LLM step; runs via convergence engine
    output_file=deviation_file,
    gate=DEVIATION_ANALYSIS_GATE,
    timeout_seconds=120,
    inputs=[spec_fidelity_file, merge_file],
    retry_limit=0,
    gate_mode=GateMode.TRAILING,  # Phase 2: observability-first
),
```

Step 11: remediate (non-LLM, custom executor):
```python
Step(
    id="remediate",
    prompt="",  # non-LLM step; runs via execute_remediation()
    output_file=remediation_file,
    gate=REMEDIATE_GATE,
    timeout_seconds=600,
    inputs=[deviation_file],
    retry_limit=0,
    gate_mode=GateMode.TRAILING,  # Phase 2: observability-first
),
```

Step 12: certify (LLM prompt-driven):
```python
Step(
    id="certify",
    prompt=build_certification_prompt(findings=[], context_sections={}),
    output_file=certification_file,
    gate=CERTIFY_GATE,
    timeout_seconds=300,
    inputs=[remediation_file],
    retry_limit=1,
    gate_mode=GateMode.TRAILING,  # Phase 2: observability-first
),
```

**Also fix** `certify.md` reference at line 1037:
- Before: `certify_path = output_dir / "certify.md"`
- After: `certify_path = output_dir / "certification-report.md"`

- Before state: `_build_steps()` returns 10 entries (11 steps including parallel pair), ending at `wiring-verification`.
- After state: `_build_steps()` returns 13 entries (14 steps), ending at `certify`. All three new steps use `gate_mode=GateMode.TRAILING`.
- Verification: `uv run pytest tests/roadmap/test_eval_gate_ordering.py -v` (will need test updates in P2-T5)

**Dependencies:** P1-T1 through P1-T5 (contract lock complete)
**Produces:** Runtime step list consumed by P2-T2, P2-T3, P2-T5, all of Phase 3.

---

### P2-T2: Align ordered step IDs
**Complexity:** 2 — Mechanical update to match new _build_steps output.
**Adversarial review required:** No

**Mechanical specification:**
- File: `src/superclaude/cli/roadmap/executor.py`
- Symbol/location: `_get_all_step_ids()` (line 992-1010)
- Change: The function already includes `"remediate"` and `"certify"` (lines 1008-1009). Add `"deviation-analysis"` between `"wiring-verification"` and `"remediate"`.

Before state (lines 1006-1009):
```python
        "wiring-verification",
        "remediate",
        "certify",
```

After state:
```python
        "wiring-verification",
        "deviation-analysis",
        "remediate",
        "certify",
```

- Verification: Assert `_get_all_step_ids(config)` length equals flattened `_build_steps(config)` length, and IDs match in order.

**Dependencies:** P2-T1
**Produces:** Correct step ID list consumed by resume logic in Phase 3.

---

### P2-T3: Ensure each new step has executable producer path
**Complexity:** 5 — The deviation-analysis step has no existing output writer; remediate step requires custom runner integration; certify step needs prompt populated with actual findings at runtime.
**Adversarial review required:** Yes

**Mechanical specification:**
This task has three distinct sub-tasks:

**P2-T3a: deviation-analysis producer**
- File: `src/superclaude/cli/roadmap/executor.py`
- Problem: No function currently writes `spec-deviations.md` with the 9 frontmatter fields required by `DEVIATION_ANALYSIS_GATE`. The freshness checker reads it (executor.py:1084-1173) but nothing writes it.
- Change: Add a `_write_deviation_analysis_output()` function that takes the DeviationRegistry (from the convergence engine) and writes `spec-deviations.md` with gate-compliant frontmatter. This function should be called from the step runner when `step.id == "deviation-analysis"`.
- The function must produce YAML frontmatter with exactly these fields: `schema_version`, `total_analyzed`, `slip_count`, `intentional_count`, `pre_approved_count`, `ambiguous_count`, `routing_fix_roadmap`, `routing_no_action`, `analysis_complete`.
- Data source: `DeviationRegistry` already tracks these counts (see `convergence.py` imports at executor.py:552-557).
- Before state: No writer exists.
- After state: Writer produces gate-compliant `spec-deviations.md`.

**P2-T3b: remediate producer**
- File: `src/superclaude/cli/roadmap/executor.py`
- Problem: `execute_remediation()` (remediate_executor.py:732) is already called from the convergence engine (executor.py:560, 656), but it does not write `remediation-tasklist.md` — that's done by `generate_remediation_tasklist()` (remediate.py:154). The step runner for `remediate` must call `generate_remediation_tasklist()` and write the result to the step's `output_file`.
- Change: In the step runner (`roadmap_run_step` or a branching handler), when `step.id == "remediate"`, call `generate_remediation_tasklist()` with findings from the current state, write result to `step.output_file`.
- Before state: `generate_remediation_tasklist()` exists but is not connected to a Step runner path.
- After state: Step runner produces `remediation-tasklist.md` that passes `REMEDIATE_GATE`.

**P2-T3c: certify producer**
- File: `src/superclaude/cli/roadmap/executor.py`
- Problem: `build_certify_step()` (executor.py:735-772) exists and produces a well-formed Step, but it's not called from `_build_steps()`. In the static `_build_steps()` wiring, the prompt is built with empty findings. At runtime, the step runner must either: (a) rebuild the prompt with actual findings, or (b) accept the empty-findings prompt and let the LLM certification agent read the remediation-tasklist as an input file.
- Decision: Use approach (b). The `certify` Step's `inputs=[remediation_file]` means the LLM receives the remediation tasklist content via `_embed_inputs()`. The prompt from `build_certification_prompt(findings=[], context_sections={})` already contains the output format template. The LLM will read the embedded input and produce the certification report. This matches how other LLM steps work (prompt + embedded inputs).
- Before state: `build_certify_step()` exists but is unreachable from main pipeline.
- After state: Certify step is wired in `_build_steps()` with static prompt + runtime input embedding.

- Verification: Write a test that constructs `_build_steps()` and confirms `deviation-analysis`, `remediate`, `certify` steps each have non-empty `output_file` and at least one input.

**Dependencies:** P2-T1
**Produces:** Executable producer paths consumed by step runner.

---

### P2-T4: Lock exact observability-first control path
**Complexity:** 2 — Decision already locked (D-05): use `GateMode.TRAILING`.
**Adversarial review required:** No

**Mechanical specification:**
- File: `src/superclaude/cli/roadmap/executor.py`
- Symbol/location: The three new Steps added in P2-T1
- Change: Already specified in P2-T1 — all three steps have `gate_mode=GateMode.TRAILING`.
- Mechanism: `GateMode.TRAILING` is defined in `pipeline/models.py:46-55`. When a step has `gate_mode=GateMode.TRAILING`, the `TrailingGateRunner` (pipeline/trailing_gate.py) evaluates the gate asynchronously. Failures are logged but do not block the pipeline.
- Verification: Add assertion in P2-T5 tests:
  ```python
  for step_id in ("deviation-analysis", "remediate", "certify"):
      step = next(s for s in flat if s.id == step_id)
      assert step.gate_mode == GateMode.TRAILING
  ```

- Before state: No observability mechanism decision.
- After state: `GateMode.TRAILING` locked for all 3 new steps.

**Dependencies:** P2-T1
**Produces:** Baseline for Phase 3 enforcement promotion (changing TRAILING to BLOCKING).

---

### P2-T5: Add targeted wiring tests
**Complexity:** 3 — Multi-file test updates with well-defined assertions.
**Adversarial review required:** No

**Mechanical specification:**

**File 1: `tests/roadmap/test_eval_gate_ordering.py`**

Changes needed:
1. `TestStepOrdering.test_step_count`: Change `assert len(flat) == 11` to `assert len(flat) == 14`
2. `TestStepOrdering.test_sequential_order_after_generate`: Add `"deviation-analysis", "remediate", "certify"` to `expected_order` list after `"wiring-verification"`.
3. Add new test `test_deviation_analysis_after_wiring`:
   - Assert `ids.index("deviation-analysis") > ids.index("wiring-verification")`
4. Add new test `test_remediate_after_deviation_analysis`:
   - Assert `ids.index("remediate") > ids.index("deviation-analysis")`
5. Add new test `test_certify_after_remediate`:
   - Assert `ids.index("certify") > ids.index("remediate")`
6. `TestGateAssignment.test_all_steps_have_gates`: No change needed (new steps all have gates).
7. `TestStepMetadata`: Add test `test_new_steps_trailing_gate_mode` asserting all 3 new steps have `GateMode.TRAILING`.

**File 2: `tests/roadmap/test_executor.py`**

Changes needed:
1. `test_step_ids_in_order`: Add assertions for indices 11, 12, 13:
   ```python
   assert ids[11] == "deviation-analysis"
   assert ids[12] == "remediate"
   assert ids[13] == "certify"
   ```
2. `test_build_steps_returns_correct_count`: Change `len(steps) == 10` to `len(steps) == 13` (10 + 3 new entries).

**File 3: `tests/roadmap/test_eval_gate_ordering.py` (TestInputDependencies)**

Add three new tests:
1. `test_deviation_analysis_inputs_fidelity_and_merge`: Assert `spec_fidelity_file in step.inputs` and `merge_file in step.inputs`.
2. `test_remediate_inputs_deviation`: Assert `deviation_file in step.inputs`.
3. `test_certify_inputs_remediate`: Assert `remediation_file in step.inputs`.

- Before state: Tests assert 11 steps, ending at wiring-verification.
- After state: Tests assert 14 steps with correct ordering and input dependencies for all 3 new steps.
- Verification: `uv run pytest tests/roadmap/test_eval_gate_ordering.py tests/roadmap/test_executor.py -v`

**Dependencies:** P2-T1, P2-T2
**Produces:** Test coverage confirming wiring correctness.

---

### P2-T6: Run targeted tests
**Complexity:** 1 — Execute commands and capture results.
**Adversarial review required:** No

**Mechanical specification:**
- Run exactly:
```bash
uv run pytest tests/roadmap/test_eval_gate_ordering.py tests/roadmap/test_executor.py -v
uv run pytest tests/roadmap -k "step or wiring" -v
uv run pytest tests/roadmap -k "gate" -v
```
- Pass criteria: All tests pass.
- Flake policy: On first failure, rerun once. If still failing, treat as real, capture output, block phase.

**Dependencies:** P2-T5
**Produces:** Phase 2 checkpoint evidence.

---

## Phase 3 Task Specifications

### P3-T1: Audit resume logic for new step IDs
**Complexity:** 4 — Must trace all resume paths touching shared state for new step IDs.
**Adversarial review required:** Yes

**Mechanical specification:**
- File: `src/superclaude/cli/roadmap/executor.py`

**Functions to audit and their current state:**

1. `_apply_resume()` (line 2166-2234+): Generic — iterates all steps from `_build_steps()` and calls `_step_needs_rerun()`. **No changes needed** — it works on any Step list generically.

2. `_step_needs_rerun()` (line 2115-2163): Generic — checks gate, inputs, force_extract. **No changes needed** — works for any Step with a gate.

3. `check_remediate_resume()` (line 2019-2050): Already exists and correctly references `"remediation-tasklist.md"` and `REMEDIATE_GATE`. **No changes needed.**

4. `check_certify_resume()` (line 2053-2072): Already exists and correctly references `"certification-report.md"` and `CERTIFY_GATE`. **No changes needed.**

5. `_check_annotate_deviations_freshness()` (line 1084-1173): References `"spec-deviations.md"` — matches canonical name. Resets gate pass state for `"deviation-analysis"` key (line 1168). **No changes needed.**

6. `_check_tasklist_hash_current()` (line 2075-2112): Correctly compares `source_report_hash` in remediation-tasklist.md. **No changes needed.**

**Result of audit:** All resume functions already handle the new step IDs correctly. The generic `_apply_resume` + `_step_needs_rerun` pattern works for any Step with `gate` and `inputs` defined. No code changes required — only verification.

- Before state: Resume functions exist but have not been verified against the new steps.
- After state: Audit confirms no changes needed; documented.
- Verification: Read each function body and confirm step ID references match canonical names.

**Dependencies:** P2-T1, P2-T2
**Produces:** Confirmation that resume is safe, consumed by P3-T4 test design.

---

### P3-T2: Fix stale-artifact invalidation rules
**Complexity:** 4 — Hash-chain logic where incorrect invalidation can silently skip stale data or block all resumes.
**Adversarial review required:** Yes

**Mechanical specification:**
- File: `src/superclaude/cli/roadmap/executor.py`

The current `_step_needs_rerun()` already implements input-dependency invalidation:
- Line 2130: `if any(inp in dirty_outputs for inp in (step.inputs or []))` — if any input was regenerated, step must rerun.
- The `dirty_outputs` set propagates through the step list in `_apply_resume()`.

**Chain analysis for new steps:**
1. If `spec-fidelity` is re-run → its output is in `dirty_outputs` → `deviation-analysis` has `spec_fidelity_file` as input → triggers rerun. Correct.
2. If `deviation-analysis` is re-run → its output `spec-deviations.md` is in `dirty_outputs` → `remediate` has `deviation_file` as input → triggers rerun. Correct.
3. If `remediate` is re-run → its output `remediation-tasklist.md` is in `dirty_outputs` → `certify` has `remediation_file` as input → triggers rerun. Correct.

**One potential gap:** `_check_annotate_deviations_freshness()` (line 1084) uses `roadmap_hash` in `spec-deviations.md` to detect stale deviations. This is called from... let me check:

- Change: Verify that `_check_annotate_deviations_freshness()` is called during resume flow and its result feeds into `dirty_outputs` or gate pass state. If it's not called during `_apply_resume`, the generic `_step_needs_rerun` gate check at line 2146-2160 handles staleness anyway (if the gate fails due to hash mismatch, the step is marked for rerun). **No code change needed** — the gate check is the primary staleness detector.

- Before state: Invalidation chain untested for new steps.
- After state: Chain verified as correct by analysis; no code changes.
- Verification: P3-T4 scenario tests will exercise these paths.

**Dependencies:** P2-T1, P3-T1
**Produces:** Invalidation correctness confirmation, consumed by P3-T4.

---

### P3-T3: Align `.roadmap-state.json` metadata writing/reading
**Complexity:** 3 — Multi-location verification with well-defined key names.
**Adversarial review required:** No

**Mechanical specification:**
- File: `src/superclaude/cli/roadmap/executor.py`

**`_save_state()`** (line 1273-1385):
- Line 1340-1350: Writes `steps` dict keyed by `r.step.id`. New steps will automatically be included because they produce `StepResult` objects with `step.id` set. **No change needed.**
- Lines 1374-1383: Preserves `remediate` and `certify` metadata keys. **Already handles both keys.**

**`build_remediate_metadata()`** (line 1452-1478): Already exists, produces correct dict.
**`build_certify_metadata()`** (line 1481-1501): Already exists, produces correct dict.
**`derive_pipeline_status()`** (line 1504-1532): Already handles `certify` and `remediate` keys.

**One key-name issue to verify:**
- State uses `"remediate"` and `"certify"` as top-level keys (lines 1374, 1380).
- Step IDs are `"remediate"` and `"certify"` — matching.
- `"deviation-analysis"` has no dedicated top-level state key (unlike remediate/certify). It uses the generic `steps["deviation-analysis"]` path. This is correct — deviation analysis does not need its own metadata block.

- Change: No code changes needed. Document the state schema for the new steps:
  - `steps["deviation-analysis"]`: `{status, attempt, output_file, started_at, completed_at}`
  - `steps["remediate"]`: `{status, attempt, output_file, started_at, completed_at}`
  - `steps["certify"]`: `{status, attempt, output_file, started_at, completed_at}`
  - Top-level `"remediate"`: metadata dict from `build_remediate_metadata()`
  - Top-level `"certify"`: metadata dict from `build_certify_metadata()`

- Before state: State schema undocumented for new steps.
- After state: Schema documented; no code changes.
- Verification: Write P3-T4 test that inspects state file after mock pipeline run.

**Dependencies:** P2-T1, P2-T2
**Produces:** State schema documentation consumed by P3-T4.

---

### P3-T4: Add resume scenario tests
**Complexity:** 3 — Well-defined scenarios with existing test patterns to follow.
**Adversarial review required:** No

**Mechanical specification:**
- Files: Add new tests to existing test files (prefer `tests/roadmap/test_resume_restore.py` which already tests `_step_needs_rerun`).

**Scenario 1: Fresh run — all new steps appear in results**
- Call `_build_steps()`, verify `deviation-analysis`, `remediate`, `certify` are in flattened list.
- Already covered by P2-T5. No additional test needed.

**Scenario 2: Fail at deviation-analysis → resume skips prior steps**
- Create state file with `deviation-analysis` status FAIL.
- Create passing outputs for steps 1-9 (extract through wiring-verification).
- Call `_apply_resume()` → assert deviation-analysis is NOT skipped (FAIL gate), prior steps ARE skipped.

**Scenario 3: Fail at remediate → resume skips prior steps including deviation-analysis**
- Same as above but with deviation-analysis PASS and remediate FAIL.

**Scenario 4: Fail at certify → resume skips prior including remediate**
- Same pattern with certify FAIL.

**Scenario 5: Stale spec-fidelity → cascading rerun of deviation-analysis, remediate, certify**
- Create all outputs. Mark spec-fidelity output as dirty (in `dirty_outputs`). Assert all 3 new steps are marked for rerun due to input dependencies.

Follow the existing pattern in `test_resume_restore.py`:
- Use `_step_needs_rerun()` directly for unit-level tests.
- Use mock `gate_fn` that returns `(True, "passes")` or `(False, "gate failed")`.

- Before state: No resume tests for new steps.
- After state: 4 new test functions covering scenarios 2-5.
- Verification: `uv run pytest tests/roadmap/test_resume_restore.py -v`

**Dependencies:** P3-T1, P3-T2, P3-T3
**Produces:** Resume correctness evidence.

---

### P3-T5: Enforce gates incrementally
**Complexity:** 5 — Changing gate_mode from TRAILING to BLOCKING has cascading pipeline-halt implications.
**Adversarial review required:** Yes

**Mechanical specification:**

This task is a sequence of 3 atomic edits, each requiring test verification before proceeding.

**Stage A: Enforce deviation-analysis gate**
- File: `src/superclaude/cli/roadmap/executor.py`
- Symbol: The `deviation-analysis` Step in `_build_steps()` (added in P2-T1)
- Change: Remove `gate_mode=GateMode.TRAILING` from the Step constructor (defaults to `GateMode.BLOCKING`).
- Before: `gate_mode=GateMode.TRAILING,`
- After: Line removed (or explicitly `gate_mode=GateMode.BLOCKING,`)
- Verification: `uv run pytest tests/roadmap -k "deviation" -v` — all pass.
- Also update P2-T5 test `test_new_steps_trailing_gate_mode` to expect BLOCKING for deviation-analysis.

**Stage B: Enforce remediate gate**
- Same file, same pattern.
- Change: Remove `gate_mode=GateMode.TRAILING` from remediate Step.
- Verification: `uv run pytest tests/roadmap -k "remediate or remediation" -v` — all pass.

**Stage C: Enforce certify gate**
- Same file, same pattern.
- Change: Remove `gate_mode=GateMode.TRAILING` from certify Step.
- Verification: `uv run pytest tests/roadmap -k "certify or certification" -v` — all pass.

**Critical constraint:** Do NOT proceed from Stage A to Stage B unless Stage A tests pass. Each stage is an independent commit point.

- Before state: All 3 new steps use `GateMode.TRAILING` (non-blocking).
- After state (Stage C complete): All 3 new steps use `GateMode.BLOCKING` (pipeline halts on gate failure).
- Final verification: `uv run pytest tests/roadmap -v` — full suite passes.

**Dependencies:** P3-T4 (resume tests pass first)
**Produces:** Fully enforced post-fidelity gate chain.

---

### P3-T6: Run tests + real evals
**Complexity:** 1 — Execute pre-defined commands.
**Adversarial review required:** No

**Mechanical specification:**
Commands exactly as specified in workflow file. No changes needed — already well-specified with pre-eval CLI verification.

**Dependencies:** P3-T5
**Produces:** Phase 3 checkpoint evidence.

---

## Phase 4 Task Specifications

### P4-T1: Normalize cleanup-audit import style
**Complexity:** 1 — Single-line change.
**Adversarial review required:** No

**Mechanical specification:**
- File: `src/superclaude/cli/cleanup_audit/gates.py`
- Symbol/location: Line 14
- Change:
  - Before: `from superclaude.cli.pipeline.models import GateCriteria, SemanticCheck`
  - After: `from ..pipeline.models import GateCriteria, SemanticCheck`
- Verification: `uv run python -c "from superclaude.cli.cleanup_audit.gates import GATE_G001; print('OK')"`

**Dependencies:** None (independent of Phases 1-3)
**Produces:** Import consistency.

---

### P4-T2: Add regression guard for import-style drift
**Complexity:** 2 — One new test function.
**Adversarial review required:** No

**Mechanical specification:**
- File: Create `tests/audit/test_import_style.py` (the `tests/audit/` directory already exists per git status showing `tests/audit/test_ac_validation.py`)
- Change: Add test:
```python
def test_gate_modules_use_relative_imports():
    """All gate modules must use relative imports for pipeline.models."""
    import ast
    from pathlib import Path

    gate_files = list(Path("src/superclaude/cli").rglob("gates.py"))
    for gate_file in gate_files:
        source = gate_file.read_text()
        assert "from superclaude.cli.pipeline" not in source, (
            f"{gate_file} uses absolute import; must use relative import"
        )
```
- Verification: `uv run pytest tests/audit/test_import_style.py -v`

**Dependencies:** P4-T1
**Produces:** Regression guard.

---

### P4-T3: Run targeted + broader tests
**Complexity:** 1 — Execute commands.
**Adversarial review required:** No

Already well-specified in workflow. No changes needed.

**Dependencies:** P4-T1, P4-T2
**Produces:** Test evidence.

---

### P4-T4: Final real pipeline validation
**Complexity:** 1 — Execute commands.
**Adversarial review required:** No

Already well-specified in workflow. No changes needed.

**Dependencies:** P4-T3
**Produces:** Pipeline validation evidence.

---

### P4-T5: Update status docs and operator notes
**Complexity:** 1 — Edit documentation.
**Adversarial review required:** No

**Mechanical specification:**
- File: `docs/generated/gate-system-deep-analysis.md`
- Symbol/location: Section "7.1 Revalidation Snapshot"
- Change: Update each finding's status:
  - Finding #1: `Not remediated` → `Remediated` with evidence: `_build_steps()` now includes `deviation-analysis`, `remediate`, `certify` steps.
  - Finding #2: `Partially evolved` → `Remediated` with evidence: All gates imported, wired, and enforced.
  - Finding #3: `Not remediated` → `Remediated` with evidence: `cleanup_audit/gates.py` now uses relative import.
- Verification: Read the updated file and confirm status changes.

**Dependencies:** P4-T1, P3-T5
**Produces:** Updated documentation.

---

### P4-T6: Execute rollback playbook dry-run checklist
**Complexity:** 2 — Document review, no code changes.
**Adversarial review required:** No

Already well-specified in workflow. Mechanical steps:
1. Run `git log --oneline -20` to capture last known-good commit SHA.
2. List modified files: `executor.py`, `cleanup_audit/gates.py`, test files.
3. Confirm all changes are on feature branch, not master.
4. Document rollback as: `git revert <SHA>` for each commit in reverse order.

**Dependencies:** All prior tasks
**Produces:** Rollback documentation.

---

### P4-T7: Prepare final go/no-go handoff summary
**Complexity:** 1 — Summarize evidence.
**Adversarial review required:** No

Already well-specified. No changes needed.

**Dependencies:** P4-T3 through P4-T6
**Produces:** Final deliverable.

---

## Complexity Summary

| Task | Complexity | Adversarial? |
|------|-----------|-------------|
| P1-T1 | 2 | No |
| P1-T2 | 2 | No |
| P1-T3 | 2 | No |
| P1-T4 | 2 | No |
| P1-T5 | 1 | No |
| P2-T1 | **5** | **Yes** |
| P2-T2 | 2 | No |
| P2-T3 | **5** | **Yes** |
| P2-T4 | 2 | No |
| P2-T5 | 3 | No |
| P2-T6 | 1 | No |
| P3-T1 | **4** | **Yes** |
| P3-T2 | **4** | **Yes** |
| P3-T3 | 3 | No |
| P3-T4 | 3 | No |
| P3-T5 | **5** | **Yes** |
| P3-T6 | 1 | No |
| P4-T1 | 1 | No |
| P4-T2 | 2 | No |
| P4-T3 | 1 | No |
| P4-T4 | 1 | No |
| P4-T5 | 1 | No |
| P4-T6 | 2 | No |
| P4-T7 | 1 | No |

**Tasks requiring adversarial review:** P2-T1, P2-T3, P3-T1, P3-T2, P3-T5 (5 tasks)

---

## Phase 0.5: Adversarial Review Results

### P2-T1 — Wire 3 new steps into `_build_steps()`
**Verdict: REFACTOR**
**Confidence: High**

**Key risks identified:**
1. **Empty-prompt Claude invocation.** `roadmap_run_step()` has no dispatch branch for `deviation-analysis` or `remediate`. Without handlers, these steps fall through to `ClaudeProcess` with `prompt=""`, launching broken/wasteful Claude CLI subprocesses.
2. **Certify prompt constructed with empty findings.** `build_certification_prompt(findings=[], ...)` produces a prompt saying "verify these findings" with no findings listed. The embedded remediation-tasklist input provides data in a different format than the prompt template expects.
3. **`deviation-analysis` missing from `_get_all_step_ids()`.** Listed `remediate` and `certify` but not `deviation-analysis`.
4. **Remediate inputs incomplete.** Only `deviation_file` listed; `execute_remediation()` also needs access to spec-fidelity and merge outputs.
5. **Deviation-analysis timeout too low.** 120s insufficient for multi-round convergence engine.

**Accepted alternative specification:**
- Add `step.id` dispatch branches in `roadmap_run_step()` for `deviation-analysis` and `remediate` BEFORE wiring into `_build_steps()`
- Do NOT construct certify Step statically with empty findings. Construct dynamically after remediate completes using `build_certify_step(config, findings=actual_findings)`
- Add `"deviation-analysis"` to `_get_all_step_ids()`
- Expand remediate inputs to include `spec_fidelity_file` and `merge_file`
- Increase deviation-analysis timeout to 300s
- Canonical output file for deviation-analysis: `spec-deviations.md` (not `deviation-analysis.md`)

---

### P2-T3 — Ensure each new step has executable producer path
**Verdict: REFACTOR**
**Confidence: High**

**Key risks identified:**
1. **DeviationRegistry does not expose aggregated frontmatter fields.** The writer needs ~40-50 lines of aggregation logic computing `routing_fix_roadmap`, `routing_no_action`, etc. from per-finding `deviation_class` values. Not a thin adapter.
2. **No finding-extraction pipeline.** `generate_remediation_tasklist()` takes `(findings, source_report_path, source_report_content)` but the Step runner only has file paths. Parsing markdown back into structured `Finding` objects is fragile.
3. **Empty-prompt Claude invocation (same as P2-T1).** Non-LLM steps need dispatch branches.
4. **Certify prompt/input semantic gap.** Empty findings prompt + embedded markdown tasklist creates contradictory LLM instructions.

**Accepted alternative specification:**
- **Add JSON sidecar strategy.** When writing `spec-deviations.md`, also write `spec-deviations.json` with full finding data. When writing `remediation-tasklist.md`, also write `remediation-tasklist.json`. Machine-readable sidecars eliminate fragile markdown parsing.
- **P2-T3a:** Create `_write_deviation_analysis_output(registry, output_file)` that aggregates by `deviation_class`, validates cross-field consistency pre-write (fail-fast), writes both `.md` and `.json`.
- **P2-T3b:** Step runner reads `spec-deviations.json`, converts to `Finding` objects, calls `generate_remediation_tasklist()`, writes both `.md` and `.json`.
- **P2-T3c:** Certify step is constructed dynamically with populated `findings` from `remediation-tasklist.json`, not empty list.
- **Add dispatch branches** in `roadmap_run_step()` for both non-LLM steps.

---

### P3-T1 — Resume logic audit: "No changes needed"
**Verdict: REFACTOR**
**Confidence: High**

**Key risks identified:**
1. **`check_remediate_resume()` and `check_certify_resume()` are dead code.** Defined at executor.py:2019 and :2053, tested in isolation, but NEVER called from any production code path. `_apply_resume()` does not invoke them. The assessment's claim that they "already handle correct artifact names" is true but irrelevant.
2. **False mental model.** The assessment assumes deviation-analysis/remediate/certify are already pipeline steps that `_apply_resume` iterates over. They are not — `_build_steps()` currently ends at wiring-verification. The assessment describes a future state as if it were current.

**Accepted alternative:**
- The "no changes needed" conclusion is correct AFTER P2-T1 wires the steps, because `_apply_resume()` IS generic and will handle them. But the audit must:
  - Document that `check_remediate_resume()` and `check_certify_resume()` are dead code
  - Determine whether to wire them into the resume flow or delete them
  - Recommend: wire `check_remediate_resume()` into the remediate step's resume check (for the hash-freshness logic that the generic path doesn't provide)
  - Verify that TRAILING-mode steps are handled correctly by `_step_needs_rerun()` (confirmed: gate-mode-agnostic check)

---

### P3-T2 — Stale-artifact invalidation: "No changes needed"
**Verdict: ACCEPT (with caveat)**
**Confidence: Medium**

The `dirty_outputs` propagation mechanism in `_apply_resume()` is genuinely generic and correct. No code changes needed.

**Caveat:** The Phase 0 spec described a propagation chain (spec-fidelity -> deviation-analysis -> remediate -> certify) that does not match the CURRENT architecture (where these steps don't exist yet). The chain is correct for the POST-P2-T1 state. The assessment should be re-framed as: "After P2-T1 wiring, dirty_outputs propagation will work correctly because the mechanism is generic." Not "it already works."

---

### P3-T5 — Enforce gates incrementally (TRAILING -> BLOCKING)
**Verdict: REFACTOR**
**Confidence: Medium**

**Key risks identified:**
1. **No observability data before enforcement.** Jumping from TRAILING to BLOCKING without analyzing TRAILING-mode failure rates. If `ambiguous_count > 0` is frequent, enforcement causes routine halts.
2. **No deviation-resolution mechanism.** Unlike spec-fidelity (which has spec-patch auto-resume), deviation-analysis BLOCKING failures have no guided recovery path. Users must manually fix and re-run.
3. **Late-stage halt frequency unquantified.** Three consecutive BLOCKING steps at positions 10-12 significantly increases halt probability after 80%+ of pipeline work is complete.

**Accepted alternative specification:**
Add two prerequisites before Stage A:

**P3-T5-pre1: Analyze TRAILING-mode gate failure logs**
- Collect gate evaluation results from at least 2 TRAILING-mode runs (from P3-T6 evals)
- Document failure rate per gate and most common failure reasons
- If any gate fails in >20% of observed runs, document resolution path before enforcing
- Complexity: 2. Analysis only, no code.

**P3-T5-pre2: Add `--gate-mode=soft` CLI override (optional, recommended)**
- Allow users to downgrade BLOCKING to warn-only per-run via CLI flag
- Provides escape hatch when enforcement causes unexpected halts
- Follows existing pattern from `cli_portify` (SHADOW/SOFT/FULL modes)
- Complexity: 3. Can be deferred if eval data shows low failure rates.

With these additions, the A-B-C enforcement staging proceeds as originally specified. Each stage still requires passing tests before promotion.

---

## Phase 0.6: Reconciliation Summary

### Final decisions per reviewed task

| Task | Original Verdict | Reconciled Action |
|------|-----------------|-------------------|
| P2-T1 | REFACTOR | Replace with adversarial alternative: dispatch branches first, dynamic certify, expanded inputs, increased timeout |
| P2-T3 | REFACTOR | Replace with JSON sidecar strategy + dispatch branches + dynamic certify construction |
| P3-T1 | REFACTOR | Reframe as audit + dead-code triage + recommendation to wire hash-freshness checks |
| P3-T2 | ACCEPT (caveat) | Keep as-is, add caveat note about temporal framing |
| P3-T5 | REFACTOR | Add P3-T5-pre1 (failure log analysis) as mandatory prerequisite; P3-T5-pre2 (soft override) as recommended |

### New tasks surfaced by adversarial review

| New Task | Phase | Description | Complexity |
|----------|-------|-------------|-----------|
| P2-T1a | 2 | Add `roadmap_run_step()` dispatch branches for `deviation-analysis` and `remediate` | 4 |
| P2-T3-sub0 | 2 | Design JSON sidecar strategy for deviation/remediation outputs | 3 |
| P3-T1a | 3 | Triage dead code: wire or remove `check_remediate_resume()` and `check_certify_resume()` | 3 |
| P3-T5-pre1 | 3 | Analyze TRAILING-mode failure logs before enforcement | 2 |
| P3-T5-pre2 | 3 | (Recommended) Add `--gate-mode=soft` CLI override | 3 |
