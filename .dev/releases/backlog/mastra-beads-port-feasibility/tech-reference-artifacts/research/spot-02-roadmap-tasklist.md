# Spot-Check 02: Roadmap/Tasklist Pipeline Claims

- **Investigation type:** Code Tracer
- **Status:** Complete
- **Date:** 2026-06-03
- **HEAD:** 9e864860
- **Source research file:** `.dev/tasks/to-do/TASK-RESEARCH-20260602-211124/research/02-roadmap-tasklist-pipelines.md`

## Targets

1. `_build_steps()` step ordering (roadmap/executor.py)
2. CERTIFY_GATE defined in gates.py but NOT wired into `_build_steps()`
3. `wiring-verification` gate: TRAILING mode declared but grace_period=0 forces blocking
4. TASKLIST_FIDELITY_GATE presence and role

## Findings

### Target (a) — `_build_steps()` step ordering — CONFIRMED

Research file claims (file-02 line 89) the wired order: extract → [generate-A, generate-B] (parallel) → diff → debate → score → merge → anti-instinct → test-strategy → spec-fidelity → wiring-verification → deviation-analysis → remediate.

Verified at HEAD against `src/superclaude/cli/roadmap/executor.py` `_build_steps()`:

| Step | Gate | path:line |
|---|---|---|
| extract | EXTRACT_TDD_GATE / EXTRACT_GATE | executor.py:2003-2027 |
| [generate-{a}, generate-{b}] parallel | GENERATE_A_GATE / GENERATE_B_GATE | executor.py:2029-2066 |
| diff | DIFF_GATE | executor.py:2068-2076 |
| debate | DEBATE_GATE | executor.py:2078-2086 |
| score | SCORE_GATE | executor.py:2088-2105 |
| merge | MERGE_GATE | executor.py:2107-2128 |
| anti-instinct | ANTI_INSTINCT_GATE | executor.py:2130-2138 |
| test-strategy | TEST_STRATEGY_GATE | executor.py:2140-2156 |
| spec-fidelity | None (convergence) / SPEC_FIDELITY_GATE | executor.py:2158-2173 |
| wiring-verification | WIRING_GATE, gate_mode=TRAILING | executor.py:2175-2184 |
| deviation-analysis | DEVIATION_ANALYSIS_GATE | executor.py:2186-2194 |
| remediate | REMEDIATE_GATE | executor.py:2196-2204 |

**CONFIRMED** — ordering matches exactly, including the parallel generate group at index 2 and the line anchors cited in file-02. `_build_steps` docstring (executor.py:1948) still says "9-step pipeline" which is itself stale vs the 12 wired list elements, but the list contents are as research claimed. Inline comments label spec-fidelity and test-strategy both as "Step 8" (executor.py:2140, 2157) — a cosmetic mislabel, not an ordering error. The list terminates at `remediate` with the comment "Step 12 (certify) constructed dynamically by roadmap_run_step after remediate" (executor.py:2205).

### Target (b) — CERTIFY_GATE defined but NOT wired — CONFIRMED

- **Definition present:** `CERTIFY_GATE = GateCriteria(...)` at `src/superclaude/cli/roadmap/gates.py:1324-1351` (STRICT tier; 5 required frontmatter fields incl. `certified`, `certification_date`; 3 semantic checks).
- **Listed in reference inventory:** `ALL_GATES` includes `("certify", CERTIFY_GATE)` at `gates.py:1440` — but `ALL_GATES` is a reference list, not the wired pipeline.
- **Absent from wired steps:** `_build_steps()` (executor.py:1947-2208) constructs only through `remediate`; no `certify` Step is appended. Comment at executor.py:2205 claims dynamic construction by `roadmap_run_step` after remediate.
- **No production callsite:** `grep -rn "build_certify_step|check_certify_resume"` (excluding the `def` definitions) across `src/superclaude/cli/roadmap/` returned **zero** matches. The "constructed dynamically" comment is not backed by any production invocation in the read paths.

**CONFIRMED** — CERTIFY_GATE is defined-only / not wired into the production `_build_steps()` pipeline at HEAD. Matches file-02 findings (lines 146-149, 287). Per roadmap instruction: preserve this finding, do not normalize.

### Target (c) — wiring-verification: TRAILING declared but grace_period=0 forces BLOCKING — CONFIRMED

- **TRAILING declaration:** the `wiring-verification` Step is constructed with `gate_mode=GateMode.TRAILING` at `src/superclaude/cli/roadmap/executor.py:2183` (Step spans 2175-2184). Comment at executor.py:2174 calls it "shadow mode trailing gate". Gate is `WIRING_GATE`, imported from `audit/wiring_gate` (gates.py:24; defined as a `GateCriteria` at `src/superclaude/cli/audit/wiring_gate.py:1024`).
- **grace_period default = 0:** `PipelineConfig.grace_period: int = 0` at `src/superclaude/cli/pipeline/models.py:232`.
- **Coercion logic:** `_execute_single_step` sets `effective_mode = step.gate_mode`, then `if config.grace_period == 0: effective_mode = GateMode.BLOCKING` at `src/superclaude/cli/pipeline/executor.py:211-214`. The docstring states it outright: "grace_period == 0 forces BLOCKING regardless of gate_mode" (executor.py:206). The TRAILING branch (submit to trailing_runner, return PASS immediately) at executor.py:251-262 only fires when `effective_mode == GateMode.TRAILING and trailing_runner is not None`.
- **No CLI override:** no grace-period flag found in roadmap `commands.py` (file-02 line 159); `RoadmapConfig`/`TasklistValidateConfig` do not redefine `grace_period`, so the default 0 stands.

**CONFIRMED** — the Step declares TRAILING (executor.py:2183) but the default `grace_period=0` (models.py:232) is coerced to BLOCKING by executor.py:213-214, so wiring-verification runs synchronously/blocking in production despite the "shadow mode trailing" intent. Matches file-02 (lines 159, 288).

### Target (d) — TASKLIST_FIDELITY_GATE presence and role — CONFIRMED

- **Definition:** `TASKLIST_FIDELITY_GATE = GateCriteria(...)` at `src/superclaude/cli/tasklist/gates.py:23-46`. STRICT tier; 6 required frontmatter fields (`high_severity_count`, `medium_severity_count`, `low_severity_count`, `total_deviations`, `validation_complete`, `tasklist_ready`); min_lines=20; 2 semantic checks (`high_severity_count_zero`, `tasklist_ready_consistent`).
- **Reuses roadmap checks:** imports `_high_severity_count_zero` and `_tasklist_ready_consistent` from `superclaude.cli.roadmap.gates` (tasklist/gates.py:18-21) — unidirectional dependency, gates are pure data (NFR-005 comment, tasklist/gates.py:4-5).
- **Role — single wired gate of the validation-only pipeline:** `_build_steps()` in `src/superclaude/cli/tasklist/executor.py:191-218` builds exactly one Step `tasklist-fidelity` over `[roadmap.md] + tasklist_files (+ optional TDD/PRD)`, gated by `TASKLIST_FIDELITY_GATE` (executor.py:212), retry_limit=1, timeout 600s.
- **Pilot-port candidate `tasklist_run_step()`:** defined at `src/superclaude/cli/tasklist/executor.py:92-188` — a `ClaudeProcess` subprocess runner (inline input embedding, cancellation polling, timeout=124 → TIMEOUT, non-zero exit → FAIL, `_sanitize_output` preamble strip, returns PASS StepResult). File is 277 lines, matching the ~276 estimate.
- **CLI pass/fail is independent of the gate:** `execute_tasklist_validate` (executor.py:251-276) runs the shared pipeline then separately calls `_has_high_severity` (executor.py:221-248) parsing `high_severity_count` from frontmatter; returns `not _has_high_severity(...)`. Missing/unparseable report → treated as failure (executor.py:227, 248).

**CONFIRMED** — TASKLIST_FIDELITY_GATE is the sole gate of the single-step tasklist validation pipeline; tasklist CLI is validation-only (no `generate` subcommand). Matches file-02 (lines 152-154, 259).

## Summary

**Status: Complete.** All four target findings CONFIRMED at HEAD 9e864860; no DRIFTED or NOT-FOUND verdicts. Line anchors in research file 02 are accurate (no drift detected on the verified ranges).

| # | Target | Verdict | Primary path:line |
|---|---|---|---|
| a | `_build_steps()` step ordering (extract → parallel generate → diff → debate → score → merge → anti-instinct → test-strategy → spec-fidelity → wiring-verification → deviation-analysis → remediate) | **CONFIRMED** | executor.py:1947-2208 |
| b | CERTIFY_GATE defined but NOT wired into production `_build_steps()` | **CONFIRMED** | def gates.py:1324-1351; absent executor.py:1947-2208; no callsite of build_certify_step |
| c | wiring-verification declares TRAILING but grace_period=0 forces BLOCKING | **CONFIRMED** | TRAILING executor.py:2183; default models.py:232; coercion executor.py:213-214 |
| d | TASKLIST_FIDELITY_GATE present, sole gate of validation-only pipeline | **CONFIRMED** | def tasklist/gates.py:23-46; wired tasklist/executor.py:202-218 |

Secondary observations (not in the four targets, surface in Section 14 if useful): `_build_steps` docstring still says "9-step pipeline" (executor.py:1948) and two steps share the "Step 8" comment label (executor.py:2140, 2157) — cosmetic staleness, ordering unaffected. The "Step 12 (certify) constructed dynamically" comment (executor.py:2205) is unbacked by any production callsite, reinforcing finding (b).
