# QA Report — task-qualitative (Partition: Phases 1-4)

**Topic:** TASK-RF-20260603-180207 — 5 post-R1 roadmap-pipeline brittleness follow-ups
**Date:** 2026-06-03
**Phase:** task-qualitative
**Fix cycle:** N/A (initial)
**Assigned scope:** Phase 1 (Prep), Phase 2 (Area A) + Gate, Phase 3 (Area B) + Gate, Phase 4 (Area C) + Gate

---

## Overall Verdict: PASS (3 issues found — 2 fixed in-place, 1 MINOR documented)

[PARTITION NOTE: Cross-phase trace limited to assigned subset (Phases 1-4). Phases 5-7 (Areas D/E + final acceptance) are out of scope for this instance; cross-phase checks (items 6, 10) noted where relevant.]

## Items Reviewed
| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Gate/command dry-run (UV commands, git rm, pytest, collect-only) | none | PASS | Reproduced the baseline collection error live: `uv run pytest tests/integration/test_wiring_pipeline.py --collect-only -q` → `ImportError: cannot import name 'WIRING_GATE' from ...roadmap.gates` at L28, exactly the sole error Step 1.4/2.4 expect. `git rm` precondition (zero importers) verified: `grep -rln test_wiring_pipeline tests/ src/` returns nothing. |
| 2 | Project convention compliance (no sync-dev; src+tests only) | none | PASS | All edits target `src/superclaude/cli/roadmap/`, `cli/audit/`, `tests/` — none under `.claude/`. Confirmed `make sync-dev` mirrors only skills/agents, so absence of sync items is correct, not a gap. |
| 3 | Intra-phase execution-order simulation | none | PASS | P2: 2.1 re-home → 2.2 verify-green → 2.3 delete (gated on 2.2 PASS) → 2.4 collect. 2.3 reads the 2.2 summary as precondition. P3: 3.1 add param → 3.2 consume param → 3.3 test → 3.4 run → 3.5 collect. P4: comment → follow-up → verify. No item reads an artifact a later item creates. |
| 4 | Function signature verification (Area B core) | none | PASS | `render_step_tool_write_with_id_check(step_id, json_text, output_path, spec_ids, accepted_deviations=None)` confirmed at tool_writer.py:455-461; the `if spec_ids:` skip at L487; `validate_id_subset` at L344. Adding `require_spec_ids: bool=False` kwarg is additive/back-compat. `SpecIdRegistry.union_of_known()` confirmed id_registry.py:94 returns `frozenset[str]`; `accepted_deviation_ids` field at L90. |
| 5 | Module context analysis | none | PASS | gates.py:1033-1045 reconstructs `SpecIdRegistry` from the JSON payload — the exact construction Step 3.2 says to mirror/reuse (Contract #8). Executor render-dispatch (L1257-1296) already has `config.output_dir` in scope (reads `config.output_dir / "extraction.json"` at L1282), so the source-swap to `spec_id_registry.json` is wireable. `_save_id_registry` (executor.py:611) writes `<output_dir>/spec_id_registry.json` ALWAYS — confirms registry-always-written premise. |
| 6 | Downstream consumer analysis (merge-gate preserved) | none | PASS | gates.py `_roadmap_ids_within_spec` (L996-1059) is the merge-gate catch; it reads the sidecar independently and is untouched by the Area B plan. Step 3.2 explicitly preserves it as defense-in-depth. The render-dispatch is the upstream (generation) gate; both coexist. [PARTITION NOTE: Area E (Phase 6) also consumes this reader — out of my assigned scope.] |
| 7 | Test validity (real artifact, no stubs) | AX-4 | FAIL→FIXED | 3.3(b)/(c) are EXECUTOR-integration tests but the render-dispatch sits in `_roadmap_run_step_impl` (L1236-1310) AFTER a live `ClaudeProcess` (L1194). Without patching ClaudeProcess the test cannot reach the branch deterministically — the item claimed "pure file-I/O, no LLM" without naming the mandatory mock. FIXED in-place: added the house `patch(...ClaudeProcess)` idiom (cited test_file_passing.py:58-67) to 3.3(b) and (c). |
| 8 | Test coverage of primary use case | none | PASS | 3.3 covers renderer-level (a,d) + executor-level (b,c) + the missing gap-(a) regression (b) + fail-shut (c). The merge-gate catch test (`test_merge_rejects_phantom_id`) is kept green by 3.4. Primary use case (phantom FR-99 rejected at generation) is exercised end-to-end via (b). |
| 9 | Error path coverage | none | PASS | Fail-shut for missing/unreadable registry (3.2 returns StepResult FAIL mirroring gates.py:1013 posture) + `require_spec_ids=True` empty-universe hard error (3.1/3.3d). Bad-input paths covered. |
| 10 | Runtime failure-path trace | none | PASS | Data flow: registry JSON → reconstruct SpecIdRegistry → union_of_known() → spec_ids set → validate_id_subset → FAIL on phantom, no artifact. No downstream gate breaks: merge-gate still reads its own sidecar. Default markdown path (flags False) bypasses the whole branch (L1257 getattr default False). |
| 11 | Completion scope honesty | none | PASS | 3 Open Questions (D/E cutover-gated, Area C latency) are correctly deferred, not silently resolved. Area C Step 4.2 records the latency follow-up rather than implementing across the PRESERVE boundary. |
| 12 | Ambient dependency completeness | none | PASS | New `require_spec_ids` kwarg is local to one renderer; no `__init__` export / CLI parser / registry-dispatch touchpoint needed (internal helper). New test file needs no marker registration unless a marker is added (3.3 forbids unregistered markers; `--strict-markers` ON). |
| 13 | Kwarg sequencing red flags | none | PASS | Step 3.1 (add `require_spec_ids` param) is ordered BEFORE Step 3.2 (pass `require_spec_ids=True`). Correct producer-before-consumer ordering — no "pass kwarg before signature" defect. |
| 14 | Function existence claims verified | AX-5 | PASS | All "exists at" claims grep-verified: `union_of_known` (id_registry.py:94), `render_step_tool_write_with_id_check` (tool_writer.py:455), `validate_id_subset` (L344), `_roadmap_ids_within_spec` (gates.py:996), `SPEC_FIDELITY_GATE_CONVERGENCE_AWARE` (gates.py:1363, wired L1578), `_save_id_registry` (executor.py:611), convergence short-circuit (executor.py:1068-1073), `_run_convergence_spec_fidelity` (L1533), spec-fidelity Step `gate=`/`timeout_seconds=600` (L2675/L2676). No invented artifact. |
| 15 | Cross-reference accuracy (Area A target + Findings headings) | AX-2 | FAIL→1 FIXED, 1 MINOR | (a) CRITICAL: Step 2.1 said "ADD a `TestNFR007Compliance` class" but that class ALREADY exists at test_wiring_gate.py:946 — a second same-named class silently drops the 2 existing methods. FIXED: rewrote 2.1 to add the method INTO the existing class. (b) MINOR: items cite `### Phase N Findings` but actual headings are `### Phase N - <Area> Findings` (L390-417) — cross-ref string mismatch, documented (not mass-edited). |

## Summary
- Checks passed (after fixes): 15 / 15
- Checks failed (pre-fix): 2 (items 7 and 15)
- Critical issues found: 1 (Area A duplicate-class — FIXED)
- Important issues found: 1 (Area B executor-test determinism omission — FIXED)
- Minor issues found: 1 (Findings-heading cross-ref string mismatch — documented, NOT fixed: low value, high churn)
- Issues fixed in-place: 2 (items 7, 15a)
- Tool engagement: Read: 8 | Grep/Bash-grep: 9 | Glob: 0 | Bash(other): 2

## Issues Found
| # | Severity | Location | Issue | Required Fix | Status |
|---|----------|----------|-------|--------------|--------|
| 1 | CRITICAL | Step 2.1 / tests/audit/test_wiring_gate.py:946 | Item instructs "ADD a `TestNFR007Compliance` class" but that class name ALREADY exists in the target with 2 methods (`test_no_pipeline_logic_imports_in_wiring_gate`, `test_no_pipeline_imports_in_wiring_analyzer`). A second `class TestNFR007Compliance:` → Python last-def-wins silently DROPS the 2 existing methods from collection (a coverage regression masquerading as a re-home). | Add the re-homed method INSIDE the existing class, not as a new class. | FIXED in-place |
| 2 | IMPORTANT | Step 3.3(b),(c) | The executor-integration tests must reach the render-dispatch in `_roadmap_run_step_impl` (L1236-1310), which runs AFTER a live `ClaudeProcess` subprocess (L1194). The item claimed "pure file-I/O, no LLM" but omitted the mandatory `ClaudeProcess` mock — an executor would either write a non-deterministic test that spawns a real subprocess, or get stuck on "unclear executor entry points" (the item's own blocker escape). | Name the house idiom `patch("...executor.ClaudeProcess")` + `roadmap_run_step(...)` (template: test_file_passing.py:58-67). | FIXED in-place |
| 3 | MINOR | Steps 1.x–PG4.x (many) | Items reference `### Phase N Findings` but the actual task-file headings are `### Phase N - <Area> Findings` (L390-417). A literal section lookup by an executor would miss the heading. | Either rename headings to short form or update item refs. Documented only — mass-editing ~30 refs is higher-risk than the navigational cost; a competent executor resolves the longer heading. | DOCUMENTED (not fixed) |

## Actions Taken
- Fixed Step 2.1 (Area A) in the task file: replaced "ADD a `TestNFR007Compliance` class" with explicit instruction to add the re-homed `test_no_pipeline_imports_in_wiring_gate` method INTO the pre-existing `class TestNFR007Compliance:` at ~L946, with a CRITICAL duplicate-class-hazard note and the clarification that the invariant is already partially covered (additive strengthening, not unique-coverage rescue). Verified by Edit success.
- Fixed Step 3.3(b) (Area B): added the mandatory `patch("superclaude.cli.roadmap.executor.ClaudeProcess")` determinism idiom with the exact template reference (test_file_passing.py:58-67) and the assert-no-write nuance. Verified by Edit success.
- Fixed Step 3.3(c) (Area B): annotated that the fail-shut executor test inherits the same ClaudeProcess-mock requirement; clarified (d) is renderer-level and needs no mock. Verified by Edit success.

## Adversarial-Axis Notes
- AX-1 (drift): drift-axis-inactive is NOT declared — BUILD_REQUEST.GOAL was available (TRACK GOAL in spawn prompt + task description). Drift check applied: cited line numbers (tool_writer.py:455/344, gates.py:996/1363, executor.py:611/1068/1533/2675-2676) all VERIFIED still in sync with current source — no stale-citation drift found.
- AX-2 (contradictions): fired on item 15 (Area A duplicate class; Area C comment-vs-existing-comment reviewed and cleared — the existing L2666-2674 comment documents the DELETED gate form, which Step 4.1 correctly forbids the NEW comment from reintroducing; not a contradiction).
- AX-3 (omissions): the ClaudeProcess-mock omission surfaced under item 7 (classified AX-4 as the load-bearing axis: weakened/unobservable test) — also an omission of a required step; recorded under item 7.
- AX-4 (weakened criteria): fired on item 7.
- AX-5 (invented content): NO invented artifacts — every named file/function/constant cross-checked against source and present.

## Self-Audit

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- Relied on rf-qa PASS for #3 (checklist items self-contained), #4 (no batch items), #5 (cited file paths real), #10 (TB-Add-1 no TBD/title-only), #15 (TB-Add-6 uniform Verify/Acceptance form), #16 (TB-Add-7 Exec Context), #17 (TB-Add-8 per-item Context), M2 (gates ADVERSARIAL+fix_auth), M5 (no sync-dev items), M6 (UV-only).
- Relied on rf-qa PASS for #8 (phase deps logical — Area A FIRST) at the STRUCTURAL DAG level only.

**(b) Independent semantic checks (≥1 required, INV-019) — where rf-qa PASS was INSUFFICIENT and my own tool work was required:**
- rf-qa #5 verified "cited file paths real" (path existence). INSUFFICIENT for SEMANTICS: I independently verified the cited *symbols/line-targets* are real and SEMANTICALLY match what the items assume — e.g. that `union_of_known()` returns a `frozenset[str]` usable as `set(...)` (id_registry.py:94, Read), that the executor render-dispatch actually has `config.output_dir` in scope (executor.py:1282, Read), and that `_save_id_registry` writes the registry filename the items assume (executor.py:611, Bash-grep). Path-real ≠ symbol-real ≠ semantically-wireable.
- rf-qa #5 path-existence did NOT catch the Area A duplicate-class hazard: `tests/audit/test_wiring_gate.py` is a real path (rf-qa PASS), but it ALREADY contains `class TestNFR007Compliance` (Bash-grep L946) that the item's "ADD a class" instruction would collide with. This required reading the target file's class layout, not just confirming it exists. (CRITICAL finding, item 15a.)
- rf-qa #3 verified items are self-contained as prose. INSUFFICIENT: I traced the actual executor control flow (`_roadmap_run_step_impl` order: ClaudeProcess L1194 → render-dispatch L1236) and the existing test idioms (Bash-grep across tests/roadmap/) to discover that 3.3(b)/(c)'s "no-LLM" claim is only achievable WITH a ClaudeProcess mock the item never names — a semantic/operational gap invisible to self-containment checking. (IMPORTANT finding, item 7.)

## Recommendations
- Apply the 3 in-place fixes (already applied) before execution.
- The MINOR Findings-heading mismatch (item 3) is left for the task author's discretion; if desired, rename the 7 `### Phase N - <Area> Findings` headings to `### Phase N Findings` to match the ~30 item references, OR accept the longer headings (executor can resolve).
- [PARTITION NOTE] Phases 5-7 (Areas D/E HALT scaffolding + final terminal gate) were NOT in my assigned scope. The cross-phase consumer of `gates.py:_roadmap_ids_within_spec` (Area E e1) overlaps the Area B merge-gate-preserve check (item 6) — a merging instance should confirm the Area B "preserve the reader" and Area E "do not delete the writer that feeds the reader" findings are jointly consistent.

## QA Complete

---

## VERDICT: PASS

All 15 task-qualitative checks PASS after the 2 in-place fixes (1 CRITICAL Area A duplicate-class, 1 IMPORTANT Area B executor-test determinism). The 1 remaining MINOR (Findings-heading cross-ref string mismatch) is documented and left to author discretion — it does not block execution (a competent executor resolves the longer heading; it is a navigability nit, not a correctness defect). No unfixable issues remain in the assigned scope (Phases 1-4).
