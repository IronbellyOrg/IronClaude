# PRD Extraction: FR-DRS

**Investigation type:** PRD/Spec Extraction
**Scope:** `.dev/reflect-hardening/issue-3-deterministic-runtime-surface-sweep/spec.md` (full)
**Status:** Complete
**Date:** 2026-06-21

Source of truth: `src/superclaude/skills/sc-reflect-protocol/refs/runtime-surface.md` (behavior), spec.md (this extraction). Every fact below is quoted or closely paraphrased from spec.md with section references.

## 1. Feature Identity

From spec.md frontmatter (lines 1–13):

- **feature_id:** `FR-DRS`
- **title:** "sc:reflect Deterministic Runtime-Surface Sweep (FR-DRS)"
- **type / spec_type:** `new_feature`
- **complexity_class:** `HIGH`
- **parent_feature:** `sc-reflect-protocol`
- **supersedes_concern:** "FR-RSR structured-output reliability (issue-1-uc2-reachability)"
- **version:** `0.1.0`
- **status:** `draft`
- **target_release:** TBD
- **created:** 2026_06_21
- **authors:** [user, claude]

## 2. Goal (spec §1)

Produce the runtime-surface structured outputs **deterministically, on every UC-2 run, independent of LLM reflection depth or "alarm level"** (spec §1, lines 44–48).

The two structured outputs are:

- **`runtime-surface-ledger.yaml`** — the per-symbol/per-edge ledger artifact.
- **The six `runtime_surface_*` contract scalars** — the canonical-named contract fields computed from the ledger rows.

**Core principle — LLM removal from the structured-emission path:** "Remove the LLM from the structured-emission path; keep it only for narration/verdict in REPORT.md" (spec §1, lines 47–48). The goal restates this from §1: produce the outputs deterministically with "zero dependence on LLM field emission."

The deliverables are explicitly distinguished from the LLM's preserved role: the LLM continues to author narration/verdict in REPORT.md; only the structured contract mirror is moved to code.

## 3. Evidence (spec §0 — "Why this exists")

**Origin:** FR-RSR (issue-1) added runtime-surface reachability escalation to `sc-reflect-protocol` as **SKILL.md prose executed by an LLM** (spec §0, lines 19–20).

**The controlled experiment:** A 3×-before / 3×-after eval experiment (dated 2026-06-20), full data at `.dev/tasks/.../TASK-RF-uc2-reachability-20260620-025931/phase-outputs/reports/before-after-comparison.md` (lines 20–22). It proved a prose-only implementation **cannot deliver FR-RSR's structured-output guarantee** (lines 23).

**Ad-hoc field names observed** (lines 25–30) — the six `runtime_surface_*` contract fields were emitted with improvised names on the non-escalating paths, even after SKILL.md prose was strengthened to forbid exactly those names (strengthened skill verified loaded):

- REACHED path → `runtime_surface_reachable: true`
- DEGRADE path → `surface_reachability_verdict: DEGRADE`
- quiet-UNREACHED path → `surface_production_reachable: false` / `unreachable_surfaces`

**Full-pass before→after results** (line 30): positive-control 0/3→0/3, dynamic-dispatch 0/3→1/3, test-only-ref 0/3→0/3.

**Ledger-write rate:** `runtime-surface-ledger.yaml` is written in only **1 of 9** quiet-path runs (lines 31–32), so deriving the contract fields from the ledger is also non-viable — "the ledger is the missing artifact."

**Root cause** (lines 33–35): the LLM fully engages the structured machinery (ledger + canonical scalars) only on an alarming UNREACHED that escalates (the headline, 3/3 at standard depth). On quiet paths it does a lighter reflection — correct verdict in prose, but no ledger and improvised scalar names.

## 4. What Already Works — DO NOT REBUILD (spec §0, lines 37–40)

The **safety behavior** already works and must NOT be rebuilt:

- Across every run the skill **caught the unwired / registry / test-only surface and never clean-passed it** (lines 37–38).
- The original **FR-S9-04 blind spot is closed at the verdict/prose level** (line 39).
- **FR-DRS is ONLY about making the structured contract mirror** — consumed by the §5.3 forbid-STOP pre-filter and the `sprint run` executor — **reliable** (lines 39–40).

In other words: verdict/prose correctness is solved; FR-DRS is scoped narrowly to deterministic structured emission, not to re-deriving the reachability safety logic.

## 5. Approach (spec §2)

A **standalone Python sweep module invoked by the deterministic reflect layer** (spec §2, line 51).

**Module:** `src/superclaude/cli/reflect/runtime_surface.py` (new), pure-Python, no LLM (line 53).

**Inputs** (lines 54–55): the diff/patch under audit, the scope/work-tree, and the tasklist (for requirement mapping). Reuses the same static surfaces the SKILL prose describes.

**Algorithm — mirrors `refs/runtime-surface.md`, now in code** (lines 56–69). The 7 steps (tag → find-referrers → partition → degrade-oracle → rootwalk → reduce → emit):

1. **Tag** surface symbols from the diff hunks by resolved symbol kind/decorator against the allowlist (AST + decorator detection per language; py/rust/ts/js/go, others DEGRADE).
2. **Find referrers** of each tagged symbol (ripgrep/AST-based, or programmatic LSP/Serena if available; fail-open to grep with `degraded_components` on tool loss).
3. **Partition** referrers into production vs test/comment via the lang→(test-marker, comment) table (including inline-test modules).
4. **Degrade oracle** (categories a–d): decorator routes, `[project.scripts]`/entry-points, registry/DI/string-dispatch, reflection/dynamic-import → `DEGRADE`.
5. **Entrypoint rootwalk** (depth=1): REACHED if reachable from any enumerated root; partial enumeration → DEGRADE.
6. **Reduce** per-edge → per-symbol verdict under `DEGRADE-on-incompleteness > UNREACHED > REACHED`.
7. **Emit** `runtime-surface-ledger.yaml` (always) + compute the six contract scalars from the ledger rows (count invariant holds by construction).

**Three integration paths** (lines 70–78):

- **Product path:** the reflect CLI wrapper (`src/superclaude/cli/reflect/commands.py`) invokes the sweep and writes/overwrites the six `runtime_surface_*` fields + ledger in `return-contract.yaml` **BEFORE** the contract is parsed by consumers. The §5.3 pre-filter and the SKILL's escalation read the deterministic values, not LLM-typed ones (lines 71–74).
- **Eval path:** the eval harness/grader invokes the same module so the eval is deterministic and free of LLM variance — resolves the current eval's reliance on LLM-emitted scalars (lines 75–76).
- **SKILL.md:** demote the prose §6.1 step 4b/4b' to "the deterministic sweep computes these; narrate the verdict in REPORT.md" — the LLM no longer hand-types the scalars (lines 77–78).

## 6. Acceptance Criteria (spec §4, lines 93–104)

Enumerated verbatim from spec §4:

- **AC-1:** On every UC-2 run, `runtime-surface-ledger.yaml` is written and the six `runtime_surface_*` contract scalars are present with their exact canonical names — REACHED, DEGRADE, and UNREACHED paths alike — with zero dependence on LLM field emission.
- **AC-2:** The 5 FR-RSR eval cases (ids 37–41) pass deterministically across ≥3 repeated runs (no variance): unwired/test-only → UNREACHED + count invariant; positive-control → unreached 0, degraded false; dynamic-dispatch (registry) → degraded true, regression 0; degraded-backend → Grounding Gap, no STOP, no clean-pass.
- **AC-3:** `len(unreached_surfaces) == runtime_surface_unreached` holds by construction (computed, not asserted-on-LLM).
- **AC-4:** The §5.3 forbid-STOP pre-filter and `sprint run` executor read the deterministic scalars.
- **AC-5:** Existing FR-RSR safety behavior (never clean-pass an unwired surface) is preserved.
- **AC-6:** `make verify-sync` clean; UV-only; `ruff format --check` clean for the new module.

## 7. Out of Scope (spec §5, lines 107–112)

- Re-litigating the REACHED-vs-DEGRADE policy for `[project.scripts]` (keep `refs/runtime-surface.md` oracle as-is: traceable dynamic wiring still DEGRADEs).
- The headline fail-pre fixture rewrite (state reachability implicitly) — carry it as a fixture task alongside FR-DRS so the eval is a true falsifier.
- Any change to the LLM's narration/verdict role in REPORT.md.

## 8. Open Questions (spec §3, lines 82–89)

- **OQ-DRS.1 — Referrer engine:** Referrer source: pure ripgrep/AST vs programmatic Serena/LSP. Determinism + no-MCP fallback argue for ripgrep/AST as the floor, LSP as an optional precision upgrade.
- **OQ-DRS.2 — Invocation site:** Does the sweep run inside `commands.py` (post-skill) or as a Wave-1A tool the skill shells out to? Post-skill in `commands.py` is simplest and fully deterministic but only covers the `superclaude reflect run` path, not a bare `claude -p /sc:reflect`. Decide whether bare-skill runs must also get deterministic fields.
- **OQ-DRS.3 — Contract version:** Contract-version handling — FR-RSR shipped 1.6.0 fields; FR-DRS changes the PRODUCER, not the field set — likely no version bump (semantics unchanged, reliability improved).

## 9. Dependencies / References (spec §6, lines 116–119)

- **Driving evidence:** `TASK-RF-uc2-reachability-20260620-025931/phase-outputs/reports/before-after-comparison.md`
- **Behavior source of truth (to port to code):** `src/superclaude/skills/sc-reflect-protocol/refs/runtime-surface.md`
- **Contract fields:** `SKILL.md` §9.1 (1.6.0 runtime_surface_* block)
- **Consumers:** `SKILL.md` §5.3 pre-filter; `src/superclaude/cli/.../executor.py` TurnLedger; §9.3 consumer map

## Gaps and Questions

- **Six scalar field names not enumerated in spec.md.** The spec repeatedly references "the six `runtime_surface_*` contract scalars" and gives examples by inference (e.g. `runtime_surface_unreached` in AC-3, line 95), but does NOT list all six canonical names. The authoritative list lives in `SKILL.md` §9.1 (the "1.6.0 runtime_surface_* block"), which is a referenced dependency (line 118), not reproduced in this spec. Implementation must read SKILL.md §9.1 for the exact six names.
- **`refs/runtime-surface.md` is the load-bearing behavior spec, not reproduced here.** The 7-step algorithm in §2 is described as "mirrors `refs/runtime-surface.md`, now in code" (line 56). The precise allowlist, lang→(test-marker, comment) table, degrade-oracle categories a–d, and root enumeration semantics must be read from that ref file before coding — spec.md only summarizes them.
- **Three open questions (OQ-DRS.1/.2/.3) are unresolved by design** (spec §3) and require a decision before or during implementation: referrer engine (ripgrep/AST floor vs LSP), invocation site (`commands.py` post-skill vs Wave-1A tool; and whether bare `claude -p /sc:reflect` must get deterministic fields), and whether the contract version bumps.
- **Eval ids 37–41 referenced in AC-2** but the evals file is not in scope of this extraction; the five FR-RSR eval cases live in the eval workspace (`.dev/eval-workspaces/sc-reflect/`). Their current pass/fail baseline is the 3×before/3×after data, not re-verified here.
- **Fixture rewrite is carried as a sibling task** (spec §5, line 110–111: "carry it as a fixture task alongside FR-DRS"), so the headline fail-pre fixture work is in-scope-adjacent but not part of the FR-DRS module itself.

## Stale Documentation Found

No stale documentation was identified within spec.md itself — it is a freshly-created draft (created 2026_06_21, status: draft, version 0.1.0). The spec explicitly notes that it SUPERSEDES the prose-only FR-RSR structured-output approach (supersedes_concern frontmatter; §0). Cross-file staleness (e.g. whether SKILL.md §6.1 step 4b/4b' prose, §5.3 pre-filter, or `refs/runtime-surface.md` already reflect FR-DRS) was NOT verified — those files were out of scope for this PRD/spec extraction and the spec itself flags them as targets to be modified (§2 integration paths), implying they currently still encode the LLM-emits-scalars behavior.

## Summary

Extracted the full FR-DRS spec into **9 structured content sections** plus the 3 required closing sections (Gaps and Questions, Stale Documentation Found, Summary).

**Core finding:** FR-DRS is a HIGH-complexity new feature under `sc-reflect-protocol` that supersedes FR-RSR's prose-only structured-output approach. A 3×before/3×after experiment proved an LLM executing SKILL.md prose cannot reliably emit the six `runtime_surface_*` contract scalars (improvised ad-hoc names persisted even after the prose was strengthened to forbid them) nor reliably write `runtime-surface-ledger.yaml` (1/9 quiet-path runs). Root cause: the LLM only engages the structured machinery on alarming UNREACHED escalations; quiet paths get lighter reflection. The fix: a standalone pure-Python module `src/superclaude/cli/reflect/runtime_surface.py` runs a deterministic 7-step sweep (tag → find-referrers → partition → degrade-oracle → rootwalk → reduce → emit), always writes the ledger, and computes the six scalars from ledger rows by construction. It integrates via three paths (product `commands.py`, eval harness/grader, demoted SKILL.md prose). The LLM keeps only narration/verdict in REPORT.md. The safety behavior (never clean-pass an unwired surface) already works and must NOT be rebuilt. Six acceptance criteria (AC-1..AC-6), three out-of-scope items, and three open questions (OQ-DRS.1 referrer engine, OQ-DRS.2 invocation site, OQ-DRS.3 contract version) govern delivery.

**Status:** Complete
