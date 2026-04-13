# Phase 2 -- Certify Step Wiring (Mode-Aware Gate)

Wire the certify step into the pipeline and implement a pipeline-mode-aware gate per adversarial debate verdict (Solution B). The certify step is deterministic (no LLM). The gate adapts based on `remediation_mode` — `tasklist-only` validates report structure and passes with `certification_scope: analysis-only`; `applied` requires full `certified: true`.

---

### T02.01 -- Add certify Step to _build_steps and handler to roadmap_run_step

| Field | Value |
|---|---|
| Why | `_build_steps()` ends at remediate (line 1553 comment: "constructed dynamically" — but no code does this). `roadmap_run_step` has no `step.id == "certify"` handler. Pipeline silently ends after remediate. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | multi-file, gate-compliance |
| Tier | STRICT |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Verification Method | Unit test + pipeline run |
| MCP Requirements | None |
| Fallback Allowed | No |
| Sub-Agent Delegation | No |

**Files:**
- `src/superclaude/cli/roadmap/executor.py` (step construction + handler + implementation)

**Deliverables:**
1. Certify Step added to `_build_steps()` after remediate
2. Handler in `roadmap_run_step` dispatching to `_run_certify_step`
3. `_run_certify_step` function producing gate-compliant `certification-report.md`

**Steps:**
1. **[PLANNING]** Read `_build_steps()` (executor.py:1365-1556) to confirm insertion point after remediate Step
2. **[PLANNING]** Read existing `build_certify_step()` (executor.py:1325-1362) to understand intended Step shape
3. **[PLANNING]** Read `generate_certification_report()` (certify_prompts.py:175-248) to understand expected inputs/outputs
4. **[EXECUTION]** Add Step to `_build_steps()` at line ~1553:
   ```python
   # Step 12: Certify (deterministic, no LLM)
   Step(
       id="certify",
       prompt="",  # non-LLM step; prompt unused
       output_file=out / "certification-report.md",
       gate=CERTIFY_GATE,
       timeout_seconds=60,
       inputs=[remediation_file, spec_fidelity_file],
       retry_limit=0,
   ),
   ```
5. **[EXECUTION]** Add handler in `roadmap_run_step` after the remediate handler (~line 697):
   ```python
   if step.id == "certify":
       return _run_certify_step(step, config, started_at)
   ```
6. **[EXECUTION]** Implement `_run_certify_step(step, config, started_at) -> StepResult`:
   - Read `remediation-tasklist.json` sidecar from output_dir
   - Determine `remediation_mode`: if any finding has status FIXED or FAILED → `"applied"`, else → `"tasklist-only"`
   - In `tasklist-only` mode: build results list with all findings as PASS (analysis scope), set `certified=True`, `certification_scope="analysis-only"`
   - In `applied` mode: build results based on actual finding statuses, set `certified` based on whether all passed
   - Use `generate_certification_report(results, findings)` for markdown body
   - Inject `remediation_mode` and `certification_scope` into frontmatter
   - Write `certification-report.md` via atomic tmp+replace
   - Return StepResult with PASS status
   - Wrap in try/except returning FAIL StepResult on error
7. **[VERIFICATION]** Confirm function signature matches `roadmap_run_step` dispatch pattern (step, config, started_at) -> StepResult

**Acceptance Criteria:**
- `certification-report.md` is produced with valid YAML frontmatter containing: `findings_verified`, `findings_passed`, `findings_failed`, `certified`, `certification_date`, `remediation_mode`, `certification_scope`
- Per-finding results table present in markdown body
- File follows same atomic-write pattern as `_run_remediate_step` and `_run_deviation_analysis`

**Dependencies:** None (can be developed in parallel with Phase 1)
**Rollback:** Remove Step from `_build_steps`, remove handler and function; pipeline reverts to ending at remediate

---

### T02.02 -- Update CERTIFY_GATE to be mode-aware

| Field | Value |
|---|---|
| Why | Current `_certified_is_true` check requires `certified: true` unconditionally. In `tasklist-only` mode, certification is `true` with `certification_scope: analysis-only`. Gate must validate both fields to prevent gaming (e.g., setting `certified: true` without the scope qualifier). |
| Effort | S |
| Risk | Low |
| Risk Drivers | gate-contract |
| Tier | STRICT |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Verification Method | Unit test |
| MCP Requirements | None |
| Fallback Allowed | No |
| Sub-Agent Delegation | No |

**File:** `src/superclaude/cli/roadmap/gates.py`
**Lines:** ~414-429 (`_certified_is_true` function), ~1034-1061 (CERTIFY_GATE definition)

**Deliverables:**
1. Updated `_certified_is_true` with mode-aware logic
2. `remediation_mode` added to CERTIFY_GATE `required_frontmatter_fields`

**Steps:**
1. **[PLANNING]** Read `_certified_is_true` (gates.py:414-429) and CERTIFY_GATE (gates.py:1034-1061)
2. **[EXECUTION]** Add `"remediation_mode"` and `"certification_scope"` to CERTIFY_GATE `required_frontmatter_fields`
3. **[EXECUTION]** Update `_certified_is_true` logic:
   ```python
   def _certified_is_true(content: str) -> bool:
       fm = _parse_frontmatter(content)
       if fm is None:
           return False
       certified = fm.get("certified")
       if certified is None:
           return False
       mode = fm.get("remediation_mode", "applied")
       if mode == "tasklist-only":
           # In analysis-only mode: certified must be true AND scope must be analysis-only
           scope = fm.get("certification_scope", "")
           return certified.lower() == "true" and scope == "analysis-only"
       # Default/applied mode: certified must be true (existing behavior)
       return certified.lower() == "true"
   ```
4. **[VERIFICATION]** Verify fail-closed behavior: missing `remediation_mode` → defaults to `applied` → requires `certified: true`

**Acceptance Criteria:**
- `tasklist-only` mode: gate passes with `certified: true` + `certification_scope: analysis-only`
- `tasklist-only` mode: gate FAILS if `certification_scope` is missing (prevents gaming)
- `applied` mode: gate requires `certified: true` (unchanged behavior)
- Missing `remediation_mode`: falls back to strict `applied` behavior (fail-closed)

**Dependencies:** None (gate logic is independent of step implementation)
**Rollback:** Revert `_certified_is_true` to original; remove new required fields from CERTIFY_GATE

---

### T02.03 -- Test certify step and mode-aware gate

| Field | Value |
|---|---|
| Why | Verify certify wiring produces valid output and gate passes in both modes. |
| Effort | S |
| Risk | Low |
| Tier | STRICT |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Verification Method | pytest |
| MCP Requirements | None |
| Fallback Allowed | No |
| Sub-Agent Delegation | No |

**Steps:**
1. **[EXECUTION]** Run `uv run pytest tests/roadmap/ -v --tb=short` for roadmap test regression check
2. **[EXECUTION]** Run `uv run pytest tests/ -v --tb=short -q` for full suite
3. **[VERIFICATION]** Confirm no new failures
4. **[VERIFICATION]** If gate tests exist in `tests/roadmap/test_gates.py`, confirm they still pass and add cases for mode-aware behavior if practical

**Acceptance Criteria:**
- No new test failures from T02.01 or T02.02
- Pre-existing failures unchanged

**Dependencies:** T01.03 (Phase 1 tests must pass first), T02.01, T02.02
**Rollback:** N/A (test-only task)
