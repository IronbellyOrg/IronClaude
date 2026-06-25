# Synthesis 01 — Executive Summary, Problem Statement, Goals & Non-Goals, Success Metrics

**Source TDD:** FR-DRS — sc:reflect Deterministic Runtime-Surface Sweep
**Template:** `src/superclaude/examples/tdd_template.md` (v1.2, sections 1–4)
**Status:** Complete
**Date:** 2026-06-21

These four sections are template-aligned and drawn exclusively from the FR-DRS research files
(`research/00-prd-extraction.md`, `research/01-runtime-surface-algorithm.md`,
`research/02-product-path-integration.md`) and the discovery template-orientation notes. No facts
are invented; every claim traces to a research file.

---

## 1. Executive Summary

FR-DRS exists to **produce the runtime-surface structured outputs — the `runtime-surface-ledger.yaml`
artifact and the six `runtime_surface_*` contract scalars — deterministically on every UC-2 run, by
moving their emission out of LLM reflection prose and into a standalone pure-Python sweep module, so
they no longer depend on LLM field emission or "alarm level."**

FR-RSR (issue-1) added runtime-surface reachability escalation to `sc-reflect-protocol` as SKILL.md
prose executed by an LLM. A controlled 3×-before / 3×-after eval experiment (2026-06-20) proved that
a prose-only implementation cannot deliver FR-RSR's structured-output guarantee: the LLM engaged the
full structured machinery (ledger + canonical scalars) only on an alarming UNREACHED that escalates,
while quiet REACHED/DEGRADE paths got a lighter reflection — correct verdict in prose, but no ledger
(written in only 1 of 9 quiet-path runs) and improvised scalar names (the observed set: `runtime_surface_reachable`,
`surface_reachability_verdict`, `surface_production_reachable`) that persisted even after the prose was
strengthened to forbid improvised names. The fix is a standalone `src/superclaude/cli/reflect/runtime_surface.py` module that runs
a deterministic 7-step sweep (tag → find-referrers → partition → degrade-oracle → rootwalk → reduce →
emit), always writes the ledger, and computes the six scalars from ledger rows by construction. The LLM
retains its role authoring narration/verdict in REPORT.md; only the structured contract mirror moves to
code. The safety behavior (never clean-pass an unwired/registry/test-only surface) already works at the
verdict/prose level and is explicitly **not** rebuilt — FR-DRS is scoped narrowly to making the structured
mirror, consumed today by the §5.3 forbid-STOP pre-filter (and, as a deferred/FR-006a future consumer, the `sprint run` executor — which reads no reflect contract today), reliable.

**Key Deliverables:**

- A new pure-Python, LLM-free sweep module `src/superclaude/cli/reflect/runtime_surface.py` implementing the 7-step algorithm ported from `refs/runtime-surface.md`.
- Deterministic emission of `runtime-surface-ledger.yaml` (one row per evaluated edge) plus the six `runtime_surface_*` contract scalars on every UC-2 path (REACHED, DEGRADE, UNREACHED alike).
- Three integration paths: the product path (reflect CLI wrapper writes/overwrites the fields + ledger into `return-contract.yaml` before consumers parse it), the eval path (harness/grader invokes the same module), and the SKILL.md demotion of prose §6.1 steps 4b/4b' to "the deterministic sweep computes these; narrate the verdict in REPORT.md."

---

## 2. Problem Statement & Context

### 2.1 Background

FR-RSR (issue-1-uc2-reachability) added runtime-surface reachability escalation to `sc-reflect-protocol`
as **SKILL.md prose executed by an LLM**. The intent was that, on a UC-2 audit, the skill tags surface
symbols from the diff, sweeps their referrers, classifies reachability (REACHED / UNREACHED / DEGRADE),
writes a `runtime-surface-ledger.yaml`, and emits six `runtime_surface_*` contract scalars that the
downstream consumer (the §5.3 forbid-STOP pre-filter) reads to gate. *(The original FR-RSR intent also
named the `sprint run` executor as a reader, but that read is **deferred to FR-006a** — `cli/sprint/executor.py`
reads no reflect contract today and is net-new, out of FR-DRS v1 scope.)*

This work is happening now because a controlled experiment (dated 2026-06-20; full data at
`TASK-RF-uc2-reachability-20260620-025931/phase-outputs/reports/before-after-comparison.md`) ran the skill
3× before and 3× after the SKILL.md prose was strengthened to forbid the improvised field names. The
strengthened skill was verified loaded, yet the improvised names persisted and the ledger remained mostly
unwritten — proving the prose-only approach cannot deliver the structured-output guarantee, independent of
how the prose is worded.

As of this investigation, **no runtime-surface implementation exists** in `src/superclaude/cli/reflect/`
(grep-confirmed zero matches for `runtime_surface`, `ledger`, `RuntimeSurfaceLedger`, `rootwalk`,
`unreached_surfaces` across all seven files in that package). `refs/runtime-surface.md` is a forward-looking
SPEC to build, not a description of existing code — so FR-DRS is greenfield product-path work.

### 2.2 Problem Statement

**The core problem:** A prose-only, LLM-executed implementation cannot reliably emit the
`runtime-surface-ledger.yaml` artifact or the six `runtime_surface_*` contract scalars, because the LLM
only engages the structured machinery on an alarming UNREACHED escalation and does a lighter reflection
(no ledger, improvised scalar names) on the quiet REACHED/DEGRADE paths.

| Symptom | Evidence (from the 3×before/3×after experiment) |
|---------|-------------------------------------------------|
| Ad-hoc field names on non-escalating paths | **Observed (emitted by the LLM, research/00 §3 lines 45–49):** REACHED path emitted `runtime_surface_reachable: true`; DEGRADE path emitted `surface_reachability_verdict: DEGRADE`; quiet-UNREACHED emitted `surface_production_reachable: false` / `unreachable_surfaces`. These ad-hoc names persisted even after the SKILL prose was strengthened to forbid improvised names — though note the SKILL's explicit forbid-list (research/03 §1.1: `runtime_surface_reachable`, `reachability_path`, `static_caller_absent_is_expected`) is a *separate* enumeration that overlaps the observed set only on `runtime_surface_reachable`; the persistence is structural, not a matter of which exact names the prose named. |
| Ledger not written on quiet paths | `runtime-surface-ledger.yaml` written in only **1 of 9** quiet-path runs — so deriving the contract fields from the ledger is also non-viable; the ledger is the missing artifact |
| Full-pass before→after results never converged | positive-control 0/3→0/3; dynamic-dispatch 0/3→1/3; test-only-ref 0/3→0/3 |

- **What is broken/inadequate:** the structured contract mirror (ledger + 6 scalars) is unreliable; the consumer that reads it today (§5.3 pre-filter) cannot trust it (the `sprint run` executor is a deferred/FR-006a future consumer that reads no reflect contract today).
- **Who is affected:** the deterministic reflect layer and its downstream consumers — not end users directly, but the reliability of the forbid-STOP gating and `sprint run` execution.
- **Cost of not solving:** the FR-RSR structured-output guarantee remains undeliverable; gating consumers must fall back to unreliable LLM-typed values.
- **Root cause:** the LLM fully engages the structured machinery (ledger + canonical scalars) only on an alarming UNREACHED that escalates (the headline case, 3/3 at standard depth); on quiet paths it does a lighter reflection — correct verdict in prose, but no ledger and improvised scalar names.

### 2.3 Business Context

- **Parent spec reference:** `sc-reflect-protocol`; FR-DRS supersedes "FR-RSR structured-output reliability (issue-1-uc2-reachability)". Driving evidence: `TASK-RF-uc2-reachability-20260620-025931/phase-outputs/reports/before-after-comparison.md`. Behavior source of truth to port: `src/superclaude/skills/sc-reflect-protocol/refs/runtime-surface.md`. Contract field definitions: `SKILL.md` §9.1 (the 1.6.0 `runtime_surface_*` block).
- **Impact:** makes the structured contract mirror — consumed today by the §5.3 forbid-STOP pre-filter (and, as a deferred/FR-006a future consumer, the `sprint run` executor) — reliable, so reachability gating no longer depends on LLM field emission.
- **User impact:** the existing FR-RSR **safety behavior** (caught the unwired / registry / test-only surface and never clean-passed it; FR-S9-04 blind spot closed at the verdict/prose level) already works and must NOT be rebuilt. FR-DRS is ONLY about making the structured mirror reliable, not about re-deriving the reachability safety logic.

---

## 3. Goals & Non-Goals

### 3.1 Goals

What FR-DRS WILL accomplish:

| ID | Goal | Success Criteria |
|----|------|------------------|
| G1 | Emit the structured outputs deterministically on every UC-2 run | On every UC-2 run, `runtime-surface-ledger.yaml` is written AND the six `runtime_surface_*` scalars are present with their exact canonical names — REACHED, DEGRADE, and UNREACHED paths alike — with zero dependence on LLM field emission (AC-1) |
| G2 | Remove the LLM from the structured-emission path | A standalone pure-Python module `src/superclaude/cli/reflect/runtime_surface.py` (no LLM) computes the ledger + scalars via the 7-step sweep; the LLM keeps only narration/verdict in REPORT.md (spec §1, §2) |
| G3 | Compute the six scalars from the ledger rows by construction | The six `runtime_surface_*` scalars are derived from the per-edge ledger rows reduced to per-symbol verdicts; the count invariant holds by construction, not by asserting on LLM output (AC-3) |
| G4 | Wire the deterministic values into the in-scope consumer | The §5.3 forbid-STOP pre-filter reads the deterministic scalars, not LLM-typed ones (AC-4, v1 in-scope portion). *(The `sprint run` executor read is **deferred to FR-006a** — `cli/sprint/executor.py` reads no reflect contract today, so wiring it is net-new and out of v1 scope.)* |
| G5 | Make the eval deterministic | The eval harness/grader invokes the same module so the eval is free of LLM variance; the 5 FR-RSR eval cases (ids 37–41) pass deterministically across ≥3 repeated runs with no variance (AC-2) |
| G6 | Preserve the existing safety behavior | Existing FR-RSR safety behavior (never clean-pass an unwired surface) is preserved (AC-5) |
| G7 | Pass repo hygiene gates | `make verify-sync` clean; UV-only; `ruff format --check` clean for the new module (AC-6) |

### 3.2 Non-Goals

What FR-DRS will NOT do (explicit scope boundaries, inherited from spec §5 Out of Scope):

| ID | Non-Goal | Rationale |
|----|----------|-----------|
| NG1 | Re-litigate the REACHED-vs-DEGRADE policy for `[project.scripts]` | Keep `refs/runtime-surface.md` oracle as-is: traceable dynamic wiring (incl. packaging entrypoints / console-scripts) still DEGRADEs. FR-DRS changes the producer, not the policy (spec §5) |
| NG2 | Rewrite the headline fail-pre fixture | The headline fail-pre fixture rewrite (state reachability implicitly) is carried as a sibling fixture task alongside FR-DRS so the eval is a true falsifier — it is not part of the FR-DRS module itself (spec §5) |
| NG3 | Change the LLM's narration/verdict role in REPORT.md | The LLM continues to author narration/verdict in REPORT.md; only the structured contract mirror moves to code (spec §1, §5) |
| NG4 | Rebuild the reachability safety logic | Verdict/prose correctness is already solved and verified (caught unwired/registry/test-only surfaces, never clean-passed; FR-S9-04 blind spot closed). FR-DRS is scoped narrowly to deterministic structured emission (spec §0) |

### 3.3 Future Considerations

Items deferred / dependent on open-question resolution (spec §3):

| Item | Target Phase | Notes |
|------|--------------|-------|
| Programmatic LSP/Serena referrer precision upgrade (OQ-DRS.1) | Future | ripgrep/AST is the determinism floor + no-MCP fallback; LSP is an optional precision upgrade |
| Deterministic fields on bare `claude -p /sc:reflect` runs (OQ-DRS.2) | Decision needed | Post-skill in `commands.py` covers only `superclaude reflect run`; a Wave-1A skill shell-out is the only option covering the non-CLI path |
| Contract-version handling (OQ-DRS.3) | Decision needed | FR-RSR shipped 1.6.0 fields; FR-DRS changes the PRODUCER, not the field set — likely no version bump (semantics unchanged, reliability improved) |

---

## 4. Success Metrics

How we will measure success. All targets trace to the FR-DRS acceptance criteria (spec §4, AC-1..AC-6).

### 4.1 Technical Metrics

| Metric | Current State | Target | Measurement Method |
|--------|---------------|--------|--------------------|
| Ledger written per UC-2 run | 1 of 9 quiet-path runs (prose-only) | **`runtime-surface-ledger.yaml` written on every UC-2 run** — REACHED, DEGRADE, UNREACHED paths alike (AC-1) | Assert ledger file present at `<output>/artifacts/runtime-surface-ledger.yaml` after each UC-2 run |
| Six `runtime_surface_*` scalars emitted per UC-2 run | Improvised ad-hoc names on quiet paths | **All six scalars present with exact canonical names on every UC-2 run**, with zero dependence on LLM field emission (AC-1) | Parse `return-contract.yaml`; assert the six canonical keys present on REACHED/DEGRADE/UNREACHED paths |
| Eval determinism across repeats | LLM variance; full-pass never converged (e.g. dynamic-dispatch 0/3→1/3) | **5 uc2 eval cases (ids 37–41) pass deterministically across ≥3 repeated runs with zero variance** (AC-2) | Run each of the 5 cases ≥3× via the harness/grader that invokes the same module; assert identical pass result each run |
| Count invariant | Asserted on LLM output (unreliable) | **`len(unreached_surfaces) == runtime_surface_unreached` holds by construction** — computed, not asserted-on-LLM (AC-3) | Computed in the emitter from the per-symbol UNREACHED set; unit/integration assertion as a checkable post-condition |
| Consumer wiring | §5.3 pre-filter reads LLM-typed values | **§5.3 forbid-STOP pre-filter reads the deterministic scalars** (AC-4, v1 in-scope portion; the `sprint run` executor read is **deferred to FR-006a** — net-new, `cli/sprint/executor.py` reads no reflect contract today) | Trace the §5.3 pre-filter read against deterministically-written `runtime_surface_*` fields |
| Safety behavior preserved | Already works (verdict/prose level) | **Never clean-pass an unwired surface — existing FR-RSR safety behavior preserved** (AC-5) | Eval cases (unwired/test-only → UNREACHED + count invariant; degraded-backend → Grounding Gap, no STOP, no clean-pass) |
| Repo hygiene | n/a (new module) | **`make verify-sync` clean; UV-only; `ruff format --check` clean for the new module** (AC-6) | CI / `make verify-sync` + `uv run ruff format --check` |

**Per-case deterministic expectations (AC-2, the 5 FR-RSR eval cases ids 37–41 — five distinct fixtures):**

| Id | Case | Expected deterministic verdict |
|----|------|--------------------------------|
| 37 | `uc2-unwired-surface-passes` | FAIL-pre / PASS-post; `runtime_surface_unreached ≥ 1` + regression 1; never clean-pass the unwired surface |
| 38 | `uc2-surface-positive-control` | reachable; `unreached` 0, `degraded` false; no UNREACHED/STOP escalation |
| 39 | `uc2-surface-dynamic-dispatch` | `[project.scripts]` registry dispatch → `degraded` true, regression 0; DEGRADE, never UNREACHED |
| 40 | `uc2-surface-degraded-backend` | `backend: none` → Grounding Gap + `degraded` true; no hard-STOP, no clean-pass |
| 41 | `uc2-surface-test-only-ref` | test/comment-only → UNREACHED; hosts the `len(unreached_surfaces) == runtime_surface_unreached` count-invariant assertion |

### 4.2 Business Metrics

Not applicable in the conventional product-KPI sense — FR-DRS is an internal reliability hardening of the
reflect contract pipeline. The closest "business" proxy is **structured-emission reliability**: the
fraction of UC-2 runs that emit the complete ledger + six canonical scalars, with a target of 100% (every
UC-2 run) by construction, versus the prose-only baseline of 1/9 ledger writes and improvised scalar names.

---

**Status:** Complete — §1 Executive Summary, §2 Problem Statement & Context, §3 Goals & Non-Goals, §4 Success Metrics produced.
