# Adjudication: F-17 — STRICT gate failures in structural-qa / qualitative-qa not propagated to outcome

**Mode**: B (3-persona: analyzer / refactorer / architect)
**Preliminary severity**: MEDIUM
**Adjudicator**: Mode-B convergence
**Date**: 2026-05-20
**Sources**:
- Finding: `.dev/eval-workspaces/prd-cli-audit/findings/F-17-strict-gate-failures-not-propagated.md`
- `src/superclaude/cli/prd/executor.py:380-409` (run loop propagation)
- `src/superclaude/cli/prd/executor.py:520-552` (_execute_step gate evaluation)
- `src/superclaude/cli/prd/executor.py:684-705` (Stage B tail: assembly + struct-qa + qual-qa)
- `src/superclaude/cli/prd/executor.py:808-892` (_execute_qa_fix_cycle, the "good" pattern)
- `src/superclaude/cli/prd/gates.py:475-499` (STRICT declarations for structural-qa, qualitative-qa)

---

## Re-verification

### V1. Where STRICT failures are produced

`_execute_step` → `_run_subprocess_step` at `executor.py:530-538`:
```python
gate = GATE_CRITERIA.get(step_id)
if gate and status.is_success:
    gate_passed = self._evaluate_gate(step_id, gate, gate_content)
    if not gate_passed:
        if gate.enforcement_tier == "STRICT":
            status = PrdStepStatus.HALT
        else:
            status = PrdStepStatus.VALIDATION_FAIL
```
A STRICT gate fail in structural-qa or qualitative-qa correctly produces `PrdStepStatus.HALT` on the step result. The writer side is intact.

### V2. STRICT declarations confirmed

`gates.py:475-498`:
- `structural-qa`: `enforcement_tier="STRICT"` (line 478)
- `qualitative-qa`: `enforcement_tier="STRICT"` (line 491)

Both gates demand HALT-on-fail semantics by contract.

### V3. The propagation gap

`executor.py:691-705` (Stage B tail):
```python
# Step 14b: Structural QA
if result.outcome != "halt" and not self._signal_handler.shutdown_requested:
    struct_qa = self._execute_step(
        "structural-qa", "Structural QA", "build_structural_qa_prompt"
    )
    self._step_results.append(struct_qa)
    result.step_results.append(struct_qa)

# Step 14c: Qualitative QA
if result.outcome != "halt" and not self._signal_handler.shutdown_requested:
    qual_qa = self._execute_step(
        "qualitative-qa", "Qualitative QA", "build_qualitative_qa_prompt"
    )
    self._step_results.append(qual_qa)
    result.step_results.append(qual_qa)
```

There is no `if struct_qa.status.is_failure: ... result.outcome = "halt"` block. Compare the immediately-preceding assembly branch at `executor.py:684-689`, which **does** propagate STRICT failures:
```python
if assembly_result.status.is_failure:
    gate = GATE_CRITERIA.get("assembly")
    if gate and gate.enforcement_tier == "STRICT":
        result.outcome = "halt"
        result.halt_step = "assembly"
        return
```

After the qualitative-qa block, control returns to `run()` at `executor.py:395-408`. The next two `if result.outcome != "halt":` guards both succeed (because outcome was never flipped), so `present-complete` runs and finally `result.outcome = "success"` is set. The HALT status on the qa step survives only in `result.step_results[]`.

### V4. Assembly halt branch is NOT exercised by qa-step failures

The halt branch at `:684-689` keys on `assembly_result.status`, not on the prior qa steps' status. structural-qa and qualitative-qa run **after** assembly in the Stage B flow (`:691-705`), so by construction the assembly check cannot catch their failures.

**Verification verdict: finding is reproducible and accurately diagnosed.**

---

## Persona 1 — Analyzer (reproducibility)

A real qualitative-qa STRICT failure produces this user-visible outcome:

1. `_execute_step("qualitative-qa", …)` runs subprocess; gate evaluation at `:530-538` fails the semantic `qa_verdict` check (`gates.py:493-497`); status set to `PrdStepStatus.HALT`.
2. Result appended to `result.step_results` (`executor.py:704`) and `_step_results` (`:703`).
3. Control returns from `_execute_stage_b` to `run()` at `:393`.
4. `if result.outcome != "halt":` at `:396` evaluates **true** (outcome is still default), so `present-complete` runs.
5. `if result.outcome != "halt":` at `:407` evaluates **true**, so `result.outcome = "success"`.
6. CLI exits 0. The HALT step is buried inside `result.step_results[]`; the headline outcome reports success.

**Documented contract** (STRICT = halt pipeline) is violated. The pipeline continues past a STRICT failure, runs the completion step, and reports success. Failure is recorded but operationally ignored — a silent quality regression with no exit-code signal for CI/automation.

Reproducibility: HIGH. Any STRICT-tier failure mode in either gate (e.g., qa report missing verdict per `gates.py:482-484`, or `min_lines<20`) triggers this; no race condition, no environment dependency.

---

## Persona 2 — Refactorer (blast radius)

Surveyed all qa-step call sites in `executor.py`:

| Step | Call site | STRICT propagation? |
|---|---|---|
| `research-qa` | `:644-664` via `_execute_qa_fix_cycle` | YES — `:861-869` checks STRICT and sets `result.outcome = "halt"` |
| `synthesis-qa` | `:668-688` via `_execute_qa_fix_cycle` | YES — same shared helper |
| `assembly` (not a qa step but adjacent gate) | `:674-689` inline | YES — `:684-689` |
| **`structural-qa`** | **`:691-697` inline** | **NO** |
| **`qualitative-qa`** | **`:699-705` inline** | **NO** |

The `_execute_qa_fix_cycle` helper (`:808-892`) correctly implements the STRICT halt at `:861-869`. The two failing call sites are the **only** qa steps that bypass that helper — they invoke `_execute_step` directly. The pattern is therefore not pervasive; it is a localized 2-instance omission introduced when these inline calls were added without the helper's halt logic.

**Blast radius: contained.** Two steps, both in `_execute_stage_b`, both STRICT-declared in gates.py. No silent-pass anti-pattern outside Stage B's tail. Stage A's STRICT propagation loop at `:380-389` covers all Stage A steps generically.

Secondary observation: `present-complete` is `enforcement_tier="LIGHT"` (`gates.py:504`), so its lack of propagation is by design and not part of this finding.

---

## Persona 3 — Architect (severity calibration)

**Calibration against MEDIUM preliminary**:

- **Contract violation**: STRICT declarations in `gates.py` are the formal enforcement contract; bypassing them silently for two of the four STRICT-declared late-stage gates means the contract is honored on writer side (`:534`) but broken on reader side (`:691-705`). This is exactly the "silent failure on a quality gate" class.
- **User impact**: Operators relying on exit code for CI gating get a false-success signal. The QA report is on disk and in `result.step_results`, so it is recoverable post-hoc — but the documented STRICT semantics promise halt + nonzero exit, and that promise is broken.
- **Data integrity**: No corruption — assembled PRD on disk is whatever the assembly step produced; qa steps don't mutate it. The failure mode is missed signal, not bad data.
- **Recovery**: Re-running detects the same failure. No state poisoning.
- **Fix cost**: trivial (see Synthesis).

**Calibration: MEDIUM is correct.** Not HIGH because:
- No data corruption.
- The failure record is preserved in `result.step_results` (auditable post-hoc).
- Only the late-stage QA gates are affected; assembly itself, which produces the actual PRD artifact, halts correctly at `:684-689`.

Not LOW because:
- STRICT is a load-bearing contract; selectively honoring it undermines all downstream trust in tier semantics.
- CI/automation cannot rely on exit code for these two gates → real operational blast on any consumer treating exit 0 as "PRD passed all STRICT gates."

---

## Convergence

**Verdict**: CONFIRMED. Finding is reproducible, correctly localized, accurately traced to a missing STRICT-propagation branch at `executor.py:691-705`. Stage B's inline qa-step calls bypass the propagation logic that the `_execute_qa_fix_cycle` helper (`:861-869`) and the assembly branch (`:684-689`) implement correctly elsewhere.

**Convergence score**: 0.95
All three personas agree. Analyzer confirms user-visible silent success; Refactorer confirms scope is contained to exactly two call sites; Architect confirms MEDIUM calibration is appropriate (contract violation with operational but non-corrupting impact).

**Final severity**: **MEDIUM** (unchanged from preliminary).

**Fix difficulty**: **TRIVIAL** (~6 lines × 2 sites). Pattern is already in-repo; copy the assembly branch's shape:
```python
# After :697
if struct_qa.status.is_failure:
    gate = GATE_CRITERIA.get("structural-qa")
    if gate and gate.enforcement_tier == "STRICT":
        result.outcome = "halt"
        result.halt_step = "structural-qa"
        result.halt_reason = f"STRICT gate failure: {struct_qa.status.value}"
        return
# Same shape after :705 for qual_qa
```
Or — preferably — extract a helper `_propagate_strict_failure(result, step_id, step_result) -> bool` and call it after every `_execute_step` invocation in Stage B. This removes the class of bug (future late-stage steps would inherit the propagation by construction).

**Synthesis**:

The contract is: any step whose gate is `enforcement_tier="STRICT"` MUST halt the pipeline on failure. `gates.py:475-498` declares structural-qa and qualitative-qa STRICT. `_execute_step` correctly stamps `PrdStepStatus.HALT` on STRICT gate failure (`executor.py:534`). But the inline Stage B call sites at `executor.py:691-705` append the result and move on without checking `is_failure`/`enforcement_tier`. The next-door assembly branch at `:684-689` shows the exact missing pattern; the `_execute_qa_fix_cycle` helper at `:861-869` shows it again. Two sites, ~12 lines of duplication of an in-repo pattern, fixes the silent-success regression for STRICT QA gates. Recommend the helper-extraction variant to prevent re-occurrence.

**Recommended remediation pattern** (not part of this read-only adjudication; for downstream task):
1. Introduce `_propagate_strict_failure(result, step_id, step_result) -> bool` returning True if pipeline should halt.
2. Replace the assembly inline check (`:684-689`), the qa_fix_cycle branch (`:861-869`), and add calls after `:697` and `:705`.
3. Stage A's loop at `:380-389` is already generic; leave it.
4. Add regression test: force a `qa_verdict: FAIL` in structural-qa output; assert `result.outcome == "halt"` and `result.halt_step == "structural-qa"`.
