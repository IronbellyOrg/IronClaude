---
title: "sc:reflect Deterministic Runtime-Surface Sweep (FR-DRS)"
version: "0.1.0"
status: draft
feature_id: FR-DRS
parent_feature: sc-reflect-protocol
spec_type: new_feature
complexity_class: HIGH
target_release: TBD
authors: [user, claude]
created: 2026_06_21
supersedes_concern: "FR-RSR structured-output reliability (issue-1-uc2-reachability)"
---

# sc:reflect Deterministic Runtime-Surface Sweep (FR-DRS)

## 0. Why this exists (evidence)

FR-RSR (issue-1) added runtime-surface reachability escalation to `sc-reflect-protocol` as
**SKILL.md prose executed by an LLM**. A controlled 3×-before / 3×-after eval experiment
(2026-06-20, full data in
`.dev/tasks/.../TASK-RF-uc2-reachability-20260620-025931/phase-outputs/reports/before-after-comparison.md`)
proved that a prose-only implementation cannot deliver FR-RSR's **structured-output** guarantee:

- The six `runtime_surface_*` contract fields are emitted with **ad-hoc names** on the
  non-escalating paths (REACHED → `runtime_surface_reachable: true`; DEGRADE →
  `surface_reachability_verdict: DEGRADE`; quiet-UNREACHED → `surface_production_reachable: false`
  / `unreachable_surfaces`), even after the SKILL.md prose was strengthened to forbid exactly those
  names (strengthened skill verified loaded). Full-pass before→after: positive-control 0/3→0/3,
  dynamic-dispatch 0/3→1/3, test-only-ref 0/3→0/3.
- The `runtime-surface-ledger.yaml` is written in only **1 of 9** quiet-path runs, so deriving the
  contract fields from the ledger is also non-viable — the ledger is the missing artifact.
- Root cause: the LLM fully engages the structured machinery (ledger + canonical scalars) only on an
  alarming UNREACHED that escalates (the headline, 3/3 at standard depth). On quiet paths it does a
  lighter reflection — correct verdict in prose, no ledger, improvised scalar names.

**What already works (do NOT rebuild):** the *safety* behavior. Across every run the skill caught
the unwired / registry / test-only surface and never clean-passed it — the original FR-S9-04 blind
spot is closed at the verdict/prose level. FR-DRS is ONLY about making the **structured contract
mirror** (consumed by the §5.3 forbid-STOP pre-filter and the `sprint run` executor) reliable.

## 1. Goal

Produce the runtime-surface structured outputs — `runtime-surface-ledger.yaml` and the six
`runtime_surface_*` contract scalars — **deterministically, on every UC-2 run, independent of LLM
reflection depth or "alarm level."** Remove the LLM from the structured-emission path; keep it only
for narration/verdict in REPORT.md.

## 2. Approach (proposed)

A standalone Python sweep module invoked by the deterministic reflect layer:

- **Module:** `src/superclaude/cli/reflect/runtime_surface.py` (new), pure-Python, no LLM.
- **Inputs:** the diff/patch under audit, the scope/work-tree, and the tasklist (for requirement
  mapping). Reuses the same static surfaces the SKILL prose describes.
- **Algorithm (mirrors `refs/runtime-surface.md`, now in code):**
  1. **Tag** surface symbols from the diff hunks by resolved symbol kind/decorator against the
     allowlist (AST + decorator detection per language; py/rust/ts/js/go, others DEGRADE).
  2. **Find referrers** of each tagged symbol (ripgrep/AST-based, or programmatic LSP/Serena if
     available; fail-open to grep with `degraded_components` on tool loss).
  3. **Partition** referrers into production vs test/comment via the lang→(test-marker,comment)
     table (including inline-test modules).
  4. **Degrade oracle** (categories a–d): decorator routes, `[project.scripts]`/entry-points,
     registry/DI/string-dispatch, reflection/dynamic-import → `DEGRADE`.
  5. **Entrypoint rootwalk** (depth=1): REACHED if reachable from any enumerated root; partial
     enumeration → DEGRADE.
  6. **Reduce** per-edge → per-symbol verdict under `DEGRADE-on-incompleteness > UNREACHED > REACHED`.
  7. **Emit** `runtime-surface-ledger.yaml` (always) + compute the six contract scalars from the
     ledger rows (count invariant holds by construction).
- **Integration:**
  - **Product path:** the reflect CLI wrapper (`src/superclaude/cli/reflect/commands.py`) invokes
    the sweep and writes/overwrites the six `runtime_surface_*` fields + ledger in
    `return-contract.yaml` BEFORE the contract is parsed by consumers. The §5.3 pre-filter and the
    SKILL's escalation read the deterministic values, not LLM-typed ones.
  - **Eval path:** the eval harness/grader invokes the same module so the eval is deterministic and
    free of LLM variance. (Resolves the current eval's reliance on LLM-emitted scalars.)
  - **SKILL.md:** demote the prose §6.1 step 4b/4b' to "the deterministic sweep computes these;
    narrate the verdict in REPORT.md" — the LLM no longer hand-types the scalars.

## 3. Open questions

- OQ-DRS.1 — Referrer source: pure ripgrep/AST vs programmatic Serena/LSP. Determinism + no-MCP
  fallback argue for ripgrep/AST as the floor, LSP as an optional precision upgrade.
- OQ-DRS.2 — Does the sweep run inside `commands.py` (post-skill) or as a Wave-1A tool the skill
  shells out to? Post-skill in `commands.py` is simplest and fully deterministic but only covers the
  `superclaude reflect run` path, not a bare `claude -p /sc:reflect`. Decide whether bare-skill runs
  must also get deterministic fields.
- OQ-DRS.3 — Contract-version handling: FR-RSR shipped 1.6.0 fields; FR-DRS changes the PRODUCER, not
  the field set — likely no version bump (semantics unchanged, reliability improved).

## 4. Acceptance criteria

- [ ] On every UC-2 run, `runtime-surface-ledger.yaml` is written and the six `runtime_surface_*`
      contract scalars are present with their exact canonical names — REACHED, DEGRADE, and UNREACHED
      paths alike — with zero dependence on LLM field emission.
- [ ] The 5 FR-RSR eval cases (ids 37–41) pass deterministically across ≥3 repeated runs (no
      variance): unwired/test-only → UNREACHED + count invariant; positive-control → unreached 0,
      degraded false; dynamic-dispatch (registry) → degraded true, regression 0; degraded-backend →
      Grounding Gap, no STOP, no clean-pass.
- [ ] `len(unreached_surfaces) == runtime_surface_unreached` holds by construction (computed, not
      asserted-on-LLM).
- [ ] The §5.3 forbid-STOP pre-filter and `sprint run` executor read the deterministic scalars.
- [ ] Existing FR-RSR safety behavior (never clean-pass an unwired surface) is preserved.
- [ ] `make verify-sync` clean; UV-only; `ruff format --check` clean for the new module.

## 5. Out of scope

- Re-litigating the REACHED-vs-DEGRADE policy for `[project.scripts]` (keep `refs/runtime-surface.md`
  oracle as-is: traceable dynamic wiring still DEGRADEs).
- The headline fail-pre fixture rewrite (state reachability implicitly) — carry it as a fixture task
  alongside FR-DRS so the eval is a true falsifier.
- Any change to the LLM's narration/verdict role in REPORT.md.

## 6. Dependencies / references

- Driving evidence: `TASK-RF-uc2-reachability-20260620-025931/phase-outputs/reports/before-after-comparison.md`
- Behavior source of truth (to port to code): `src/superclaude/skills/sc-reflect-protocol/refs/runtime-surface.md`
- Contract fields: `SKILL.md` §9.1 (1.6.0 runtime_surface_* block)
- Consumers: `SKILL.md` §5.3 pre-filter; `src/superclaude/cli/.../executor.py` TurnLedger; §9.3 consumer map
