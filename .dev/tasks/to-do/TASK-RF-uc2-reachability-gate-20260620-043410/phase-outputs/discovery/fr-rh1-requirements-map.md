# FR-RH1 Requirements Map (R1–R9) — Implementation Anchor

Phase 1, item C-004. Canonical source: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/reflect/pre-uc2-reachability-gate-20260620-041729/REPORT.md` (abbrev `REPORT`). Delta map: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-uc2-reachability-gate-20260620-043410/research/01-report-and-spec-delta.md` (abbrev `R01`). Every requirement below is derived ONLY from the patched REPORT R1–R9; no `runtime_surface_*` / UNREACHED / degrade semantics and no stale `merged-requirements.md` clause is carried as a requirement.

## R1 — Real-boot proof bar
- `unreachable` / Regression is set ONLY when a real-boot verifier runs and observes the contracted sink **absent** after exercising the booted entrypoint. `REPORT:31-37`.
- Static signals (missing binding, discarded emitter result, oracle mismatch) are advisory recall signals → at most `unproven`; they can create a blocking `unproven` Grounding Gap but never `regression_present`. `REPORT:36`, `REPORT:41-46`, `R01:14`.
- Corrected verdict mapping (`reachable` / `unreachable` / `unproven`) with class, field set, tier effect. `REPORT:41-46`. `unreachable` → `reachability_unreachable += 1`, `verification_regressions_detected += 1`, `regression_present: true`, trips §5.3 rule 3. `REPORT:44`.

## R2 — `--no-reachability` is telemetry-only
- Disables Step 5.6; records only `reachability_gate_ran: false` + `reachability_skip_reason: --no-reachability`. MUST NOT create/append `grounding-gaps.yaml`, MUST NOT set `needs_human_decision`, MUST NOT force `status: partial`. Operator rollback path. `REPORT:49-55`.
- Invariant: ledger null, scanned/unreachable/unproven = 0, `reachability_real_boot_ran: false`, no reachability-created Grounding Gap. `REPORT:59-68`, `R01:15`.

## R3 — Spec-and-tasklist-absent is telemetry-only (not fail-closed)
- Neither `--spec` nor `--tasklist` → no blocking gate (no authoritative contracted sink). May emit non-blocking telemetry on a diff-side discarded-emitter shape, but MUST NOT create a Grounding Gap, set `needs_human_decision`, or change status. Skip reason `spec-and-tasklist-absent`. `REPORT:70-76`.
- Invariant: gate_ran false, ledger null, scanned/unreachable/unproven = 0. `REPORT:80-87`, `R01:16`.

## R4 — Contract version `1.6.0`
- Reachability stable fields are additive top-level → ship as `contract_version: "1.6.0"`, NOT `1.5.0`. `REPORT:91-99`.
- Update every fixture/report-template ref/eval assertion/version-stability test that includes new reachability fields. `1.5.0` continues to mean ONLY the D13 additive set (`coverage_pct_union`, `coverage_degraded`, `unmapped_requirements_union`). `REPORT:101`, `R01:17`.

## R5 — Wrapper plumbing (`/sc:reflect` and `superclaude reflect run` must agree)
- (1) wrapper config/model field defaulting enabled; (2) Click option `--reachability/--no-reachability`; (3) `ReflectRunner._build_prompt()` forwards `--no-reachability` into the child `/sc:reflect` prompt when disabled; (4) update `docs/guides/reflect-cli-tools-guide.md` + generated command docs; (5) parity/smoke tests (`--help` shows flag; `_build_prompt()` forwards exactly once when disabled, omits by default). `REPORT:103-120`.
- Acceptance checks block. `REPORT:115-120`.

## R6 — Producer-level eval fixture (mandatory, distinct from consumer tests)
- Deterministic `derive_verdict` fixtures prove only consumer wiring; add a producer eval fixture forcing Step 5.6 to produce fields from real inputs. `REPORT:122-124`.
- Fixture tree shape (`spec.md` w/ explicit `durable_sink:`, `tasklist.md`, `before/`, `after/`, proxy-oracle `tests/`, `expected.yaml`). `REPORT:128-136`.
- Required assertions: `contract_version: "1.6.0"`, `reachability_gate_ran: true`, `reachability_requirements_scanned: 1`, `reachability_unreachable: 0`, `reachability_unproven: 1`, `needs_human_decision: true`, `status: partial`; ledger row `verdict: unproven`, `oracle_match: false`, `gap_kind: oracle-mismatch`. `REPORT:140-154`, `R01:74`.
- Real-boot-proven Regression producer fixture only if a safe boot runs under the Step 5.5 envelope; else keep as integration/eval-hardening follow-up. `REPORT:156`.

## R7 — Field-presence and consistency rules
- Reachability block is MANDATORY for every UC-2 return contract at `contract_version: "1.6.0"`; optional/absent for UC-1. `REPORT:158-160`.
- Stable fields (exact 7): `reachability_gate_ran`, `reachability_ledger_path`, `reachability_requirements_scanned`, `reachability_unreachable`, `reachability_unproven`, `reachability_real_boot_ran`, `reachability_skip_reason`. `REPORT:164-172`.
- Consistency invariants: gate-ran (skip_reason null, ledger non-null, scanned ≥1); `no-side-effect-requirements`; `--no-reachability`; `unreachable>0 ⟹ real_boot_ran ∧ regression_present ∧ verification_regressions_detected ≥ reachability_unreachable`; `unproven>0 ⟹ grounding_gaps_path non-null ∧ needs_human_decision`. `REPORT:176-209`.

## R8 — Bounded cost (not zero)
- Replace `reachability_gate_added_tokens: 0` / `..._turns: 0` with: `reachability_gate_added_tool_classes: 0`, `..._added_turns_per_side_effect_requirement: "1-3"`, `..._max_side_effect_requirements_scanned: 12`, `..._added_turns_cap: 36`, `..._real_boot_invocations_cap: 1`. `REPORT:211-221`, `R01:87`.
- No new tool class (reuses Step 4 symbol refs, Step 6 re-Read, Step 5.5 verification); overflow >12 sets `reachability_sampled: true` + non-blocking coverage warning unless a high-stakes `durable_sink:` is present. `REPORT:223-227`.

## R9 — Semantic fallback advisory-only
- v1 blocking trigger = explicit machine-readable `durable_sink:` / `@sink` ONLY. Without it, semantic classification may record an advisory candidate but MUST NOT set `reachability_unproven`, write a reachability Grounding Gap, or affect `status`. `REPORT:229-237`.

## FR-RSR non-goals (MUST NOT copy — structural precedent only)
- Do NOT copy `runtime_surface_*` fields, FR-RSR version-bump rationale, `refs/runtime-surface.md`, the symbol-anchored runtime-surface tagger / production-caller sweep, the STOP pre-filter `runtime_surface_unreached ≥ 1` / `surface_unreached` / degrade-only non-escalation, the §10.9 UNREACHED finding-modifier and counter hygiene, reviewer-spec ledger routing for `runtime-surface-ledger.yaml`, or FR-RSR eval names/ids (`uc2-unwired-surface-passes`, `uc2-surface-*`, ids 37-41). Research 05 §"MUST NOT be copied": `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-uc2-reachability-gate-20260620-043410/research/05-template-and-prior-art.md:110-134`.
- FR-RH1 independently requires its own `contract_version: "1.6.0"` and `reachability_*` schema from the patched REPORT, NOT FR-RSR's runtime-surface schema. `R01` §2.4, `REPORT:91-101`.

## Patch-before-implement note (feeds Phase 2)
- `merged-requirements.md` still contains superseded clauses contradicting R1–R9 (non-real-boot Regression, skips writing Grounding Gaps, spec-absent blocking, reachability fields under `1.5.0`, zero-cost claims, semantic fallback as blocking trigger). These must be patched/amended BEFORE any source implementation. `R01:26-107`, `REPORT:245-253`.
