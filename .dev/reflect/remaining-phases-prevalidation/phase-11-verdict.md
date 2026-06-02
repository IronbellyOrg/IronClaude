---
phase: "Phase 11 — R1.6 Cleanup"
task: TASK-RF-20260531-042405
task_file_lines: 627-668
validator: sc-adversarial-protocol (Mode B, inline)
date: 2026-06-02
driving_authority:
  - "BUILD-REQUEST §R1.6 (L174) + §Contract #4/#5/#6/#7 + §Acceptance Gate #7"
  - "Task objective 10 (L99) — concrete deletion targets (carries STALE framing)"
  - "CORRECTED framing: task L1044 + .dev/reflect/r1-3-uc2-validation/{merged-recommendation.md, option-b-rf-qa.md}"
  - "master §Flaw 1 / §Flaw 3 (master-report.md L474, L498)"
convergence: 0.88
convergence_status: "BLOCKED by 3 HIGH UNADDRESSED invariants until REFACTORs applied"
verdict_tally: { KEEP: 3, REFACTOR: 6, DISCARD: 0 }
adversarial_artifacts: .dev/reflect/remaining-phases-prevalidation/phase-11/adversarial/
---

# Phase 11 (R1.6 Cleanup) — Pre-Execution Verdict

## Headline

**No executable Phase 11 step mandates blanket-deleting the `gate_passed` envelope-None shim
(`cli/pipeline/gates.py:93-98`).** Steps 11.3 / 11.4 / 11.7 correctly target only genuine fail-open stubs
(`_cross_refs_resolve`, `fidelity_checker` `found=True`, the convergence `gate=None`) and do **not** conflate
them with the legitimate CI-only-assertion skip. The feared conflation did NOT reach a deletion step.

**However, the wrong framing survives in three quieter, HIGH-severity forms:** (1) the CORRECTED R1.6
deliverable — splitting `code_assertions` into CI-only vs runtime and replacing the shim with explicit
per-assertion classification — is **absent from every Phase 11 step**; (2) the shim's own code comment
(`gates.py:39, 97`) still instructs "R1.6 deletes this branch"; (3) the PG11.1 QA criterion (d) demands a
`superclaude.contracts.parsers` parser that Step 11.2 explicitly forbids.

## Per-item verdict table

| Step ID | Verdict | Rationale (with citations) | Proposed replacement (REFACTOR) / Discard justification |
|---|---|---|---|
| **11.1** | REFACTOR | Read-only inventory with `Classification (FRAGILITY/EARLY-EXIT/VALID-HEURISTIC)` column — the safety mechanism that prevents blind deletion (good). Enumerates A2/A4 targets. BUT omits the CORRECTED CI-vs-runtime `code_assertion` split (A3/L1044) and the `spec_id_registry.json` deletion TODO (`envelope.py:148-150`). | Add inventory item (f): classify `code_assertions.py` predicates CI-only (`assert_step_reachable`, src-tree, fail-closed `code_assertions.py:77-80`) vs runtime (`assert_envelope_artifacts_present` `:126-184`); record shim `gates.py:93-98` is PRESERVED-not-deleted. Add (g): `spec_id_registry.json` dual-write deletion. |
| **11.2** | REFACTOR | Remediated direction is CORRECT (envelope-module owns single extractor; delete BOTH `gates.py:_parse_frontmatter` + `_check_frontmatter`), rightly overriding stale L99 ("canonicalize on `_check_frontmatter`") per §MVR §1 substrate inversion. BUT the consumer-migration mechanism targets `envelope.frontmatter` — a field that **does not exist** (`envelope.py:128-175` exposes `counts/findings/spec_ids/artifacts`; grep `.frontmatter`=0). | Replace "`envelope.frontmatter`" with the real typed fields, OR add a `frontmatter: dict` field to `PipelineEnvelope`+post-extractors as an explicit sub-step first. Note L99 is superseded by this remediation. Keep canonicalization direction. |
| **11.3** | KEEP | (a) `_cross_refs_resolve` (`gates.py:58-101`) VERIFIED genuine stub — returns True at both L98 and L101 even on unresolved refs, comment admits "to avoid blocking pipeline"; deleting it + `MERGE_GATE` registration = Contract #5. (b)-(d) per-site classify, **honor VALID-HEURISTIC** — exactly A3's required distinction. **Does NOT touch the shim** — no conflation. | — (optional hardening: add an explicit "do NOT touch `cli/pipeline/gates.py:93-98` shim" guard, but deletions are already scoped to named sites). |
| **11.4** | REFACTOR | Deletes VERIFIED genuine fidelity fail-opens (`fidelity_checker.py:302` `found=True,# fail-open`; `:320` partial-match) → fail-closed `ambiguous=True` (correct, A1/A3). Deletes convergence `gate=None` → new convergence-aware gate (correct). Does NOT touch shim. Defects: line drift (item says `executor.py:2167`, actual is **2579**); new `SPEC_FIDELITY_GATE_CONVERGENCE_AWARE` doesn't exist yet (creation is in-scope, OK). | Fix 2167→2579. ADD: rewrite the wrong-framing comment at `gates.py:39,97`; implement the CI-vs-runtime classification + fire only runtime-safe assertions in the live path (A3/L1044). Cross-ref Phase-10 sequencing prereq (L603). |
| **11.5** | REFACTOR | `test_no_fragility_stubs` (Contract #5 regex over `cli/`) is sound AND correctly will NOT flag the shim (its comment lacks `fragile/too hard/for now`) — a positive. The mutation check (restore `_cross_refs_resolve`) is good. BUT `test_gate_empty_target` is shim-blind: a code-assertion-only gate (CERTIFY/VERIFY_IMPLEMENTATION) called via `gate_passed(file, GATE)` with no envelope hits the shim (`gates.py:93-98`) and returns PASS. | Make `test_gate_empty_target` shim-aware: pass `envelope`+`repo_root` for code_assertion gates, OR scope the NOT-PASS assertion to file/min-lines/semantic tiers and document code_assertions are covered by dedicated tests. Keep `test_no_fragility_stubs` as-is. |
| **11.6** | KEEP | Contract #7 retry-mutates-input invariant per master §Flaw 4; framing-independent; sound enumeration of retry sites. | — (minor cross-phase note: ensure `retry_loop_no_terminal_case.*` vs Phase-13-created `disagreeing_parsers_case.md` fixture ownership is consistent; not a Phase-11 blocker). |
| **11.7** | REFACTOR | Lint/format/sync/tests/arch-lint aggregation is necessary. The `return True` fragility grep is fine. BUT "full-codebase grep for `gate=None` (must be 0)" is **unsatisfiable**: a legitimate `gate=None` exists at `sprint/executor.py:85`. | Scope the grep to the roadmap `_build_steps` convergence-bypass pattern `gate=None if config.convergence_enabled` (must be 0), not whole-codebase `gate=None`. |
| **PG11.1** | REFACTOR | **Carries WRONG framing.** Item (d) "exactly ONE canonical frontmatter parser exported from `superclaude.contracts.parsers`" CONTRADICTS Step 11.2 ("no `superclaude.contracts.parsers` submodule; parser owned by envelope module") — a THIRD stale framing that would make rf-qa reject a correct impl or demand a forbidden submodule. (e) inherits it. NO check for the CORRECTED CI-vs-runtime split. | Rewrite (d): single extractor owned by `cli/roadmap/envelope.py`; no `contracts.parsers`; both legacy parsers deleted. Fix (e) consumer-count target. ADD (j) code_assertions classified CI-vs-runtime + only runtime fires live; (k) shim PRESERVED with corrected comment (verify NOT deleted); (l) no source-tree assertion fires at runtime. Flag systemic `contracts.parsers` contradiction (also Phase-13 Step 13.3 + final-acceptance file list L747). |
| **PG11.2** | KEEP | Standard halt-precedence act-on-verdict loop, edits scoped to `src/superclaude/`. Correct once PG11.1's checklist is refactored. | — (conditional: inherits PG11.1 — apply PG11.1 refactor first). |

## Items that carried the WRONG shim/envelope framing (explicit call-out)

1. **PG11.1 item (d)/(e)** — `superclaude.contracts.parsers` canonical parser. CORRECTED: frontmatter is
   owned by `cli/roadmap/envelope.py`; no `contracts.parsers` submodule exists or should be created
   (per Step 11.2 remediation + `envelope.py` docstring "Contract #6 forbids new parsers"). This stale model
   recurs in Phase 13 Step 13.3 and the final-acceptance file list (L747) — **systemic**, referred to Phase 13.

2. **Step 11.2** — "read from `envelope.frontmatter`". CORRECTED: no `frontmatter` field exists on
   `PipelineEnvelope` (`envelope.py:128-175`); migrate to real typed fields or add the field explicitly.

3. **In-code (not a task step, but a Phase-11 cleanup surface)** — `cli/pipeline/gates.py:39, 97` comments
   "R1.6 cleanup deletes this skip-path / R1.6 deletes this branch." CORRECTED: the envelope-None branch is
   the correct behavior for CI-only/source-tree code_assertions (A3 INV-001) and must be PRESERVED + its
   comment rewritten; deleting it would spuriously FAIL certify on every pipx-installed production run
   (no `src/` tree). Step 11.4's REFACTOR now owns this correction.

## What Phase 11 gets RIGHT (do not "fix")

- 11.3 / 11.4 correctly distinguish genuine fail-open stubs (`_cross_refs_resolve`,
  `fidelity_checker` `found=True`, convergence `gate=None`) from the legitimate CI-only-assertion skip.
- `test_no_fragility_stubs` (11.5) will not false-positive on the legitimate shim.
- 11.2's canonicalization *direction* (envelope owns the parser; both legacy parsers deleted) is the
  correct §MVR §1 substrate inversion — only the named field is wrong.

## Missing-from-Phase-11 (must be added, per A3/L1044)

The High-priority CORRECTED R1.6 deliverable — **split `code_assertions` into CI-only vs runtime, replace
the envelope-None shim with explicit per-assertion classification, fire only runtime-safe assertions in the
live gate path** — appears in NO Phase 11 step. Recommended home: extend Step 11.4 (and verify in PG11.1).
Without it, Phase 11 closes without performing the work the r1-3 audit re-scoped it to.
