---
adversarial_status: pre-debate
contract_version: "1.0"
created: 2026-05-27T07:48:00Z
domain: code
strategy: systematic
convergence_score_internal: 0.78
upstream_seed_brief: ../seed-brief.md
upstream_troubleshoot_report: ../../../troubleshoot/spec-fidelity-soft-fail-20260527073000/REPORT.md
intended_next_step: /sc:adversarial debate on this spec
---

# Spec — Make `spec-fidelity` Soft-Fail the Default

## 1. Goal

When the roadmap pipeline's `spec-fidelity` step exhausts its 3 convergence runs without driving `active_high_count` to 0, the pipeline MUST log a clearly-marked warning and **continue** to downstream steps (anti-instinct → deviation-analysis → remediate → certify) — not halt with `sys.exit(1)`. This becomes the default behavior, with no opt-in flag or operator switch.

Crashes, timeouts, and any other non-convergence-exhaustion failure modes MUST retain their current hard-FAIL semantics.

## 2. Considered Design Variants

### V1 — Minimal: unconditional promotion at the StepResult mapping seam

Modify the single line at `executor.py:1466` to promote convergence-exhaustion to `StepStatus.PASS` with a warning, gated on `halt_reason.startswith("Convergence not reached after")`. No new types, no new fields, no new enums. **Pro**: smallest diff (~10 LOC production). **Con**: telemetry consumers cannot distinguish degraded passes from clean passes — they have to grep the gate_failure_reason string.

### V2 — Status-promotion with a new `DEGRADED` enum

Introduce `StepStatus.DEGRADED`, have `execute_pipeline` treat it as "continue but record", and downstream telemetry filters on `status in (FAIL, DEGRADED)` vs `status == FAIL`. **Pro**: cleanest signal preservation. **Con**: wider blast radius — every consumer of `StepStatus` (release-gate, retrospective, state save/load, dashboard filters, the StepStatus serializer) needs an audit, and adding a new enum value is a breaking change for anything that does exhaustive `match status:` dispatch.

### V3 — Per-step soft-fail policy table

Add `step.soft_fail_on: list[str] = []` to the `Step` dataclass — a list of `halt_reason` prefixes that demote to PASS-with-warning. `spec-fidelity` step gets `["Convergence not reached after"]`; everything else gets `[]` (no change). **Pro**: most extensible — future steps with their own soft-fail criteria can register declaratively. **Con**: over-engineered for a single-step need (YAGNI); adds a new field to a widely-used dataclass; tests must verify the empty default doesn't change behavior on every other step.

## 3. Chosen Approach — Hybrid V1+observability

Take V1's surgical seam (small, easy to reason about) and augment it with **one new structured field on `StepResult`** to preserve telemetry signal (V2's strongest point) without enum sprawl.

### 3.1 Behavioral contract

| Convergence outcome | `halt_reason` shape | New StepResult | Pipeline action |
|---|---|---|---|
| `passed=True` (active_high_count == 0) | `None` | `status=PASS, degraded=False, gate_failure_reason=None` | Continue (unchanged) |
| `passed=False`, exhaustion | `"Convergence not reached after 3 runs. ..."` | `status=PASS, degraded=True, gate_failure_reason="[SOFT-FAIL WARNING] ..."` | Continue + log WARNING |
| `passed=False`, agent crash / timeout / internal error | any other prefix (e.g., `"Budget exhausted ..."`, `"Run X timed out"`, exception traceback) | `status=FAIL, degraded=False, gate_failure_reason=<original>` | Hard-halt (unchanged) |

The discriminator is **strictly** `halt_reason.startswith("Convergence not reached after")`. Every other `halt_reason` value (or `None` when an exception escaped before halt_reason was set) routes to hard-FAIL.

### 3.2 Spec-patch resume cycle interaction

`_apply_resume_after_spec_patch` (executor.py:3147) currently runs when the FIRST spec-fidelity attempt FAILs. It attempts to auto-patch the spec and re-run the pipeline. After this change:

- The first attempt's convergence-exhaustion now returns `status=PASS, degraded=True` (not FAIL).
- Since the spec-patch resume cycle is gated on `StepStatus.FAIL`, it WILL NO LONGER auto-trigger on convergence-exhaustion. **This is correct**: the soft-fail's whole point is to allow the pipeline to proceed without operator intervention. The spec-patch retry was a strict-mode recovery mechanism that's no longer needed when the default is soft-fail.
- **However**, the spec-patch cycle SHOULD still fire on the actual hard-FAIL cases (crash, timeout). The change at executor.py:3137-3164 to filter `failures` by `r.status == StepStatus.FAIL` (not `degraded=True` PASSes) keeps that path intact.

### 3.3 Downstream consumers (anti-instinct, deviation-analysis, remediate, certify)

Audit required (Phase 0 of the implementation): grep for `tasklist_ready`, `validation_complete`, and `fidelity_status` consumers under `src/superclaude/cli/roadmap/`. Each consumer needs one of two behaviors:

- **Tolerates degraded**: reads the report, sees `validation_complete: false`, short-circuits or runs in degraded mode cleanly. No code change needed; add a test case.
- **Crashes on degraded**: needs a guard that reads `validation_complete` and either skips or emits its own degraded-output. Code change required.

The audit's results determine Phase 2 scope.

### 3.4 Telemetry / observability hooks

- **`StepResult.degraded: bool = False`** — new field, default False (backward compatible for any external StepResult constructors).
- **`gate_failure_reason` prefix** — `[SOFT-FAIL WARNING]` string marker for log-grep / dashboard filters that don't yet consume the structured field.
- **Convergence-mode report frontmatter** — add `degraded_reason: convergence-exhaustion` (or `degraded_reason: agent-crash`, `degraded_reason: timeout`) to `_write_convergence_report` (executor.py:1481+). Resolves seed-brief Q5.
- **State file (`.roadmap-state.json`)** — `StepResult.to_dict()` (assuming it exists) emits `degraded` field; state restore round-trips correctly. State-schema bump if the consumer is strict about unknown fields.

### 3.5 Tests required

In `tests/roadmap/test_executor.py` (or new sibling):

1. `test_convergence_exhaustion_soft_fails_by_default` — drive convergence to exhaust max_runs, assert StepResult has `status=PASS`, `degraded=True`, `gate_failure_reason` starts with `[SOFT-FAIL WARNING]`.
2. `test_convergence_pass_remains_clean` — drive convergence to active_high_count==0, assert StepResult has `status=PASS`, `degraded=False`, `gate_failure_reason=None`.
3. `test_agent_crash_during_convergence_hard_fails` — simulate agent throwing or timing out, assert StepResult has `status=FAIL`, `degraded=False`, `gate_failure_reason` does NOT start with `[SOFT-FAIL WARNING]`.
4. `test_budget_exhaustion_hard_fails` — simulate `ledger.can_launch()==False` mid-convergence (the `convergence.py:494-508` halt path), assert StepResult has `status=FAIL`, `degraded=False`.
5. `test_pipeline_continues_after_soft_fail` — full pipeline test: spec-fidelity soft-fails, anti-instinct + deviation-analysis + remediate + certify all execute. Assert pipeline does NOT call `sys.exit(1)`.
6. `test_spec_patch_resume_does_NOT_trigger_on_soft_fail` — convergence-exhaustion → degraded PASS, assert `_apply_resume_after_spec_patch` is NOT called.
7. `test_spec_patch_resume_DOES_trigger_on_hard_fail` — agent crash → FAIL, assert `_apply_resume_after_spec_patch` IS called (preserves existing recovery path).

In `tests/roadmap/test_convergence.py`:

8. Update any existing test that asserts `result.passed == False` → `status == StepStatus.FAIL` to now assert against the new mapping. Likely candidates: `test_flatline_halt_emits_structural_verdict` (just added in PR #92) may need its assertion section adjusted depending on whether it inspects StepResult or just ConvergenceResult.

### 3.6 Documentation

- `src/superclaude/skills/sc-roadmap-protocol/SKILL.md` — describe the new default behavior in the "Pipeline halt semantics" section (or create one if absent).
- CLI `superclaude roadmap run --help` text — note that spec-fidelity convergence exhaustion is non-blocking by default.
- `KNOWLEDGE.md` — record the design decision with a one-line entry and a back-link to this spec.
- `CLAUDE.md` if there's a roadmap-pipeline section — same note.

### 3.7 Restrictions held

| # | Restriction | How honored |
|---|---|---|
| R1 | FR-7 binary pass predicate (`active_high_count == 0` at `convergence.py:539`) | **Untouched** — the convergence loop's return contract is unchanged; the StepResult mapping at executor.py:1466 is the only seam modified |
| R2 | `max_runs=3` (`convergence.py:440`) | **Untouched** — soft-fail does not extend the run count |
| R3 | Crashes/timeouts still hard-FAIL | Enforced by the `halt_reason.startswith("Convergence not reached after")` discriminator at the new mapping logic |
| R4 | Soft-fail must be observable | New `StepResult.degraded` field + `[SOFT-FAIL WARNING]` marker in gate_failure_reason + `degraded_reason` in the report frontmatter |
| R5 | Spec-patch resume cycle preserves automatic recovery on real failures | Cycle is gated on `status == StepStatus.FAIL`; degraded PASS does not trigger it; hard-FAIL still does |
| R6 | Existing tests that assert hard-halt must be UPDATED not deleted | Test list above explicitly enumerates the 8 test cases (7 new + 1 updated) |

## 4. Implementation Phases (preliminary; task-builder will refine)

- **Phase 0** (research): Audit `tasklist_ready` / `validation_complete` consumers under `src/superclaude/cli/roadmap/` to inventory which downstream steps tolerate degraded fidelity and which need adaptation. Output: `phase0-downstream-consumer-audit.md`.
- **Phase 1** (production code, minimal): Add `StepResult.degraded` field; modify `roadmap_run_step` at executor.py:1466 to promote convergence-exhaustion to PASS+degraded; update `_write_convergence_report` to include `degraded_reason` in frontmatter.
- **Phase 2** (downstream consumer adaptation, scope per Phase 0 audit): adapt any consumer that crashes on `validation_complete: false`.
- **Phase 3** (tests): 8 cases enumerated in §3.5.
- **Phase 4** (validation): `make lint`, `make format` (in-scope only per Restriction #1 from PR #92), `uv run pytest tests/roadmap/ -v`. All exit 0; no regressions.
- **Phase 5** (docs): SKILL.md, CLI help, KNOWLEDGE.md per §3.6.
- **Phase 6** (restrictions audit): per-restriction verdicts for R1-R6 above + module ownership (changes confined to `executor.py`, `models.py` if StepResult lives there, and `tests/roadmap/`).

## 5. Risks

| Risk | Mitigation |
|---|---|
| Soft-fail masks a release-blocking spec drift | Operator sees `[SOFT-FAIL WARNING]` in stdout; degraded report still records residual HIGH count; release-gate tooling can filter on `StepResult.degraded` |
| Crashes accidentally promoted to PASS due to discriminator-string drift | Discriminator string is centralized: `convergence.py:656` produces it, executor.py reads it; add a single-source constant `CONVERGENCE_NOT_REACHED_PREFIX = "Convergence not reached after"` shared between the two files |
| Downstream consumer crashes on `validation_complete: false` | Phase 0 audit catches this BEFORE production change; Phase 2 adapts as needed |
| State-file schema change breaks `--resume` | New `degraded` field default-False on missing key during state load; bump state-schema version if a stricter validator exists; add a round-trip test |
| Telemetry dashboards continue counting FAILs as proxy for "needs review" and miss degraded passes | §3.4 surfaces a clear marker AND a structured field; dashboard owner update is a separate task (out of scope for this PR; documented as a follow-up) |
| Test 6 (resume-NOT-triggered-on-soft-fail) regresses if a future contributor restores resume-on-soft-fail behavior | Test is a regression-lock; named explicitly to surface intent |

## 6. Out of scope (explicit non-goals)

- A strict-mode environment variable or CLI flag to restore hard-halt behavior. Per user mandate: no opt-in lane. If a strict CI gate is needed later, it can be added with proper discussion at that time.
- Generalizing soft-fail to other pipeline steps (per-step policy table from V3). YAGNI.
- Modifying the convergence loop's internal logic (any change to `convergence.py` beyond adding the shared prefix constant). Restriction-locked.
- Updating dashboards / release-gate tooling that consume StepResult. Surfaced as a follow-up; out of scope for this PR.

## 7. Acceptance Criteria

The implementation is acceptable when:

1. `superclaude roadmap run <spec>` against a TUIBBS-shape spec (51 residual HIGHs after canonicalizer) produces: spec-fidelity step PASS-with-degraded marker, full downstream pipeline runs, exit code 0 (not 1).
2. Same command against a clean spec/roadmap pair: PASS, no warning, exit 0 (unchanged).
3. Same command with an agent crash injected: hard-FAIL, spec-patch resume runs (if applicable), exit 1 if resume also fails (unchanged).
4. All 8 test cases in §3.5 pass.
5. `make lint` exits 0 on in-scope files; `uv run pytest tests/roadmap/ -v` exits 0 with no regressions.
6. 6 restrictions R1-R6 in §3.7 all PASS in a final restrictions audit.
7. Docs updated per §3.6.

## 8. Rollback

The change is contained to a small set of files (`executor.py`, possibly `models.py` for StepResult, `convergence.py` if a shared constant is introduced, `tests/roadmap/`). A revert via `git revert <commit>` restores hard-halt behavior. The new `StepResult.degraded` field defaults to False, so post-revert state files remain readable.
