---
title: "FR-RH1 v1 Requirements Amendment — Authoritative R1–R9 (supersedes stale merged-requirements clauses)"
status: amendment-authoritative
supersedes: merged-requirements.md
canonical_source: /config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/reflect/pre-uc2-reachability-gate-20260620-041729/REPORT.md
created: 2026-06-20
---

# FR-RH1 v1 Requirements Amendment (Authoritative)

## Why this amendment exists (instead of an in-place patch)

`merged-requirements.md` in this folder was authored from the **pre-patch** FR-RH1 design and still contains
clauses that contradict the canonical patched report (`REPORT` =
`/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/reflect/pre-uc2-reachability-gate-20260620-041729/REPORT.md`).
Per the verified spec-delta research
(`/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-uc2-reachability-gate-20260620-043410/research/01-report-and-spec-delta.md:109-111`),
the executor may either patch `merged-requirements.md` in place **or** create an explicit companion amendment.
This amendment is the companion: it is **non-destructive** (the historical brainstorm artifact is left intact
for provenance) and **parallel-session-safe** (no shared brainstorm file is mutated while sibling tasks are being
restructured in this worktree).

**Authority rule:** For FR-RH1 implementation, **this amendment + `REPORT` R1–R9 are the ONLY authoritative
requirements source.** Where any clause in `merged-requirements.md` conflicts with R1–R9 below, the clause in
`merged-requirements.md` is **SUPERSEDED and MUST NOT be implemented**. The §6 override table names each stale
clause by line.

## Authoritative R1–R9 (corrected, implementation-ready)

### R1 — `unreachable`/Regression is real-boot-only
`unreachable` (→ Regression: `reachability_unreachable += 1`, `verification_regressions_detected += 1`,
`regression_present: true`, trips §5.3 rule 3) is set **ONLY** when a real-boot verifier runs and observes the
contracted sink **absent** after exercising the booted entrypoint. Static signals (missing binding, discarded
emitter result, oracle mismatch) are advisory recall signals → at most `unproven`. `REPORT:31-47`.
**No clause may permit "static binding absence AND oracle_mismatch ⇒ unreachable/Regression".** Such a verdict
is `unproven`, never Regression.

### R2 — `--no-reachability` is telemetry-only
Disables Step 5.6; sets ONLY `reachability_gate_ran: false` + `reachability_skip_reason: --no-reachability`,
ledger null, scanned/unreachable/unproven = 0, `reachability_real_boot_ran: false`. MUST NOT create/append
`grounding-gaps.yaml`, MUST NOT set `needs_human_decision`, MUST NOT force `status: partial`. `REPORT:49-68`.

### R3 — spec-and-tasklist-absent is telemetry-only
Neither `--spec` nor `--tasklist` → no blocking gate (no authoritative contracted sink). May emit non-blocking
telemetry on a diff-side discarded-emitter shape, but MUST NOT create a Grounding Gap, set `needs_human_decision`,
set `reachability_unproven`, or change status. Skip reason `spec-and-tasklist-absent`. `REPORT:70-89`.

### R4 — contract version `1.6.0`
Reachability stable fields are additive top-level → ship under `contract_version: "1.6.0"`, **never `1.5.0`**.
Every fixture/report-template/eval/version-test bearing reachability fields uses `1.6.0`. `1.5.0` remains the
D13-only set (`coverage_pct_union`, `coverage_degraded`, `unmapped_requirements_union`). `REPORT:91-101`.

### R5 — wrapper plumbing (`/sc:reflect` ⇄ `superclaude reflect run`)
(1) wrapper config/model field default-enabled; (2) Click `--reachability/--no-reachability`; (3)
`ReflectRunner._build_prompt()` forwards `--no-reachability` when disabled (exactly once), omits by default; (4)
update `docs/guides/reflect-cli-tools-guide.md` + generated command docs; (5) `--help` parity/smoke tests.
`REPORT:103-120`.

### R6 — producer-level eval fixture (mandatory, distinct from consumer tests)
Add an eval fixture forcing Step 5.6 to produce reachability fields + ledger rows from real inputs (tree:
`spec.md` w/ explicit `durable_sink:`, `tasklist.md`, `before/`, `after/`, proxy-oracle `tests/`,
`expected.yaml`). Assertions: `contract_version: "1.6.0"`, `reachability_gate_ran: true`,
`reachability_requirements_scanned: 1`, `reachability_unreachable: 0`, `reachability_unproven: 1`,
`needs_human_decision: true`, `status: partial`; ledger row `verdict: unproven`, `oracle_match: false`,
`gap_kind: oracle-mismatch`. Real-boot-proven Regression producer fixture is a follow-up unless safe under the
§6.1.1 envelope. `REPORT:122-156`.

### R7 — field-presence & consistency
Reachability block MANDATORY for every UC-2 `1.6.0` contract; optional/absent for UC-1. Exact 7 fields:
`reachability_gate_ran`, `reachability_ledger_path`, `reachability_requirements_scanned`,
`reachability_unreachable`, `reachability_unproven`, `reachability_real_boot_ran`, `reachability_skip_reason`.
Invariants: gate-ran (skip null, ledger non-null, scanned ≥1); `--no-reachability`; `no-side-effect-requirements`;
`unreachable>0 ⟹ real_boot_ran ∧ regression_present ∧ verification_regressions_detected ≥ reachability_unreachable`;
`unproven>0 ⟹ grounding_gaps_path non-null ∧ needs_human_decision`. `REPORT:158-209`.

### R8 — bounded cost (not zero)
Replace zero-token/zero-turn claims with: `reachability_gate_added_tool_classes: 0`,
`reachability_gate_added_turns_per_side_effect_requirement: "1-3"`,
`reachability_gate_max_side_effect_requirements_scanned: 12`, `reachability_gate_added_turns_cap: 36`,
`reachability_gate_real_boot_invocations_cap: 1`; overflow >12 → `reachability_sampled: true` + non-blocking
coverage warning. **No `reachability_gate_added_tokens: 0` / `..._turns: 0` may remain.** `REPORT:211-227`.

### R9 — semantic fallback advisory-only
v1 blocking trigger = explicit machine-readable `durable_sink:` / `@sink` ONLY. Without it, semantic
classification may record an advisory candidate but MUST NOT set `reachability_unproven`, write a reachability
Grounding Gap, or affect `status`. `REPORT:229-239`.

## Superseded-clause override table (merged-requirements.md → corrected rule)

| `merged-requirements.md` clause (line) | Stale content | Corrected by | Override |
|---|---|---|---|
| `:26-28` | static scan/real-boot "never the gating mechanism" | R1 | Narrow: static signals CAN create a blocking `unproven` Grounding Gap; only real boot gates Regression. |
| `:92` (verdict table) | `unreachable` when "binding unambiguously absent AND oracle_mismatch confirmed" | R1 | SUPERSEDED → that condition is `unproven`, not `unreachable`. |
| `:130-132` (§4.1 step 5.6) | "real-boot observed … OR binding unambiguously absent AND oracle_mismatch confirmed ⇒ unreachable" | R1 | SUPERSEDED → drop the OR branch; real-boot only. |
| `:133-138` (§4.1) | spec/tasklist absent ⇒ `unproven` + §10.6 Grounding Gap | R3 | SUPERSEDED → telemetry-only skip `spec-and-tasklist-absent`. |
| `:93` (§3.3 verdict table) | `unproven` condition includes "or spec absent" ⇒ Grounding Gap + `needs_human_decision: true` | R3 | SUPERSEDED → spec-and-tasklist-absent is telemetry-only; it does NOT set `reachability_unproven`, does NOT create a Grounding Gap, does NOT set `needs_human_decision`. |
| `:236` (§4.12 taxonomy) | `unproven` condition includes "spec absent" ⇒ Grounding Gap, `needs_human_decision: true` | R3 | SUPERSEDED → telemetry-only skip; no `unproven`/Grounding Gap/`needs_human_decision` for the spec-absent branch. |
| `:138` (§4.1) | `--no-reachability` "records the skip in Grounding Gaps" | R2 | SUPERSEDED → telemetry-only; no Grounding Gap. |
| `:191` (§4.7 reflect.md) | flag row "records the skip in Grounding Gaps" | R2 | SUPERSEDED → telemetry-only skip wording. |
| `:235` (§4.12 taxonomy) | non-real-boot `unreachable` Regression condition | R1 | SUPERSEDED → real-boot only. |
| `:257-258` (§4.14 cost) | `reachability_gate_added_tokens: 0` / `..._turns: 0` | R8 | SUPERSEDED → bounded caps. |
| `:67-69` (§3.1 trigger) | semantic classification → `unproven` when sink unresolved | R9 | SUPERSEDED → advisory telemetry only; no `unproven`/gap/status. |
| `:270,:274,:309` (§5 fixtures) | reachability fields under `contract_version: "1.5.0"` | R4 | SUPERSEDED → `1.6.0`. |
| `:151-162` (§4.3 fields) | field list without presence/consistency invariants | R7 | EXTEND with R7 mandatory-block + invariants. |
| (no concrete wrapper section) | wrapper plumbing absent from concrete edits | R5 | ADD wrapper config/Click/`_build_prompt`/docs/parity tasks. |
| `:395-399`,`:418-424` (§5 note, DoD) | consumer fixtures emphasized; producer fixture vague | R6 | ADD mandatory producer eval fixture + assertions. |

## Reusable structure from merged-requirements.md (NOT superseded)
The trigger taxonomy concept (side-effect-bearing requirement; durable_row/db_write/queue_publish/event_emit/
file_persist/external_api_write/process_spawn/prod_route), the two sub-claims (reachability + oracle-admissibility),
the §6.1 step-5.6 placement (UC-2-only, Wave-1A), routing through existing §10.6 Grounding-Gap / §10.4 Regression
fields (no `contract.py` change required for v1), and the 4-category-ledger-purity / no-5th-class decision remain
valid and are carried forward — corrected by R1–R9 above.

## Explicit safety closure
- **No clause in the authoritative requirements (this amendment) permits static binding absence plus oracle
  mismatch to set `regression_present`.** That path is `unproven` only (R1).
- `--no-reachability` and `spec-and-tasklist-absent` are telemetry-only (R2/R3): no Grounding Gap, no
  `needs_human_decision`, no `status: partial`, no `reachability_unproven`.
- Semantic fallback is advisory-only; explicit `durable_sink:` / `@sink` is the sole v1 blocking trigger (R9).
