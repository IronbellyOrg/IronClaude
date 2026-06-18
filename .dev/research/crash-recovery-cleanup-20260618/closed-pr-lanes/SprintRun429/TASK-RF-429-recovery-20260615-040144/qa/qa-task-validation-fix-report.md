# QA Report — Task-Integrity Consolidated Fix (Serialized)

**Topic:** Sprint Run 429 / Account-Exhaustion Recovery task-file consolidated fix
**Date:** 2026-06-15
**Phase:** task-integrity / fix-cycle (consolidated-fix lens)
**Fix authorization:** true (single serialized fix agent, no team context)
**Task file:** `.dev/tasks/to-do/TASK-RF-429-recovery-20260615-040144/TASK-RF-429-recovery-20260615-040144.md`

---

## Overall Verdict: FIXED (all 4 IMPORTANT)

All four IMPORTANT findings (F1, F2, F3, F4) from `qa-task-validation-consolidated.md` were applied in-place via Edit and re-verified. The MINOR items were left as-is (non-blocking, opportunistic-only; none were trivial-and-zero-risk task-file edits — two are research-artifact cosmetic notes and one is an accepted soft telemetry-test target).

---

## Fixes Applied

### F1 (B2-1) — Split the XL re-spawn-loop items 4.3 and 5.2 — FIXED

The task uses descriptive Step headers (`Step 4.3:`, `Step 4.4:` …) with **unnumbered** `- [ ]` items underneath. Splitting items *within* a Step therefore does NOT shift any Step header number, and there are no per-item numeric identifiers to renumber. The only `- [ ]`-to-Step cross-references in the file point at Step headers (unchanged), so no dependency/"after Step X" reference broke.

**Step 4.3 (per-task loop): 3 items → 5 items.** The single XL loop item (which bundled latch-precheck-under-lock + unlocked spawn + decide-dispatch + 3 action branches + counter) was split into two atomic B2-complete sub-items; the existing ladder item already covered the third F1-named concern (status-ladder branch + `_task_completed_before_overrun` guard):

| Order | Sub-item | Concern |
|-------|----------|---------|
| 4.3-1 | (unchanged) Edit `_run_one_task` signature | add `reset_policy` kwarg + imports |
| 4.3-2 | **NEW** Loop skeleton + attempt counter | `while`/counter wrapper, locked latch-precheck, unlocked spawn; `reset_policy is None` == today |
| 4.3-3 | **NEW** Detector + policy dispatch | `detect_provider_failure` → `decide` → dispatch over the 4 `Action` values (RETRY/HALT/CONTINUE; FAIL_TASK reserved) |
| 4.3-4 | (was the ladder item) Status-ladder branch | provider-failure branch ABOVE `_is_transient_failure`, BELOW `:1003` gate, guarded by `_task_completed_before_overrun` |
| 4.3-5 | (unchanged) `TaskResult` population | 3 new fields from loop-local counters |

**Step 5.2 (single-session loop): 2 items → 3 items.** The XL loop+short-circuit item was split:

| Order | Sub-item | Concern |
|-------|----------|---------|
| 5.2-1 | (was the big loop item, now scoped) Read + loop skeleton + counter | `while`/counter wrapper around `ClaudeProcess` spawn→poll→exit-capture; per-attempt `monitor.reset`/isolation |
| 5.2-2 | **NEW** Detector + dispatch + short-circuit | `detect_provider_failure(config.output_file(phase))` → `decide`; `PROVIDER_EXHAUSTED` short-circuit BEFORE `_determine_phase_status` |
| 5.2-3 | (unchanged) Persistence | set `halt_reason`/`exhausted_model` on `phase_result` |

Each new sub-item is 5-component B2-complete (Context / Action / Output / Verification / Completion gate — i.e., the "ensuring …" verification clause + "log the specific blocker … then mark this item complete" completion gate). Post-split counts: **Phase-4 implementation = 25 checklist items; Phase-5 implementation = 13** (verified by awk count). Item ordering is sequential within each Step.

### F2 (B2-2) — Anchor line-fragile items with symbol names — FIXED

Symbol anchors were baked into the F1 sub-items as they were split, and added to the unsplit call-site items:

- **4.3 sub-items (2 & 3):** anchored to the `subprocess_factory`/`_run_task_subprocess` spawn call ("locate by the symbol, not the line, since discovery may have drifted"). Line numbers kept as `~986-993` approximate.
- **4.3-4 (ladder):** already symbol-anchored (`_is_transient_failure`, `_task_completed_before_overrun`, the `:1003` completion gate) — confirmed durable, no change needed.
- **4.4 K>1 call site:** re-anchored to "the `_run_one_task(...)` call site whose kwargs include `lock=lock` … locate by the `lock=lock` kwarg, not the line number." Line `~1134-1145` kept approximate.
- **4.4 K=1 call site:** re-anchored to the `lock=None` kwarg on the `_run_one_task` call. Line `~1337-1348` approximate.
- **4.5 items:** already symbol-anchored (`PhaseResult`, `_write_phase_result_json`, `aggregate_task_results`) — confirmed durable.
- **5.2-1:** re-anchored to the `ClaudeProcess(...).start()` spawn and the `_determine_phase_status` symbol the short-circuit must precede. Lines `~1815-1816` / `~1993-2001` approximate.
- **5.2-2:** anchored to "after the exit-code capture and BEFORE the `_determine_phase_status` call."

### F3 (B2-3) — Step 5.3: assert the is_terminal default, demote the is_failure fork to a NOTE — FIXED

Step 5.3 was rewritten so the **Action ASSERTS the (G-1) default** as a fixed design fact (not a runtime branch the executor decides): because `PhaseStatus.PROVIDER_EXHAUSTED` is in the `is_terminal` tuple (`models.py:411-423`, verified by Read) and deliberately NOT in `is_failure`, the `if status.is_failure:` diagnostic-bundle block at lines 2103-2132 is structurally never entered for an exhaustion halt. The Action is to add the explicit `PROVIDER_EXHAUSTED` halt branch (HALTED + halt_phase + break, no bundle). The former "if implementer chose is_failure" fork was demoted to a **parenthetical NOTE** explicitly framed as a fallback contingency ("IF a *different* downstream consumer is later found to require … THEN and only then guard …; this is a documented contingency, not a branch to choose between at build time — the default above ships as-is"). The Context retains the `lines 2103-2132` file:line citation (TB-Add-8 per-item evidence binding), and the Step 5.4 no-diagnostic-bundle regression test reference is preserved ("verified by the Step 5.4 no-diagnostic-bundle regression test"). G-1 source: `research/07-gap-fill.md` §G-1.

### F4 (Struct-1, TB-Add-7) — Strip file:line from the Execution Context block — FIXED

Both `## Execution Context` bullets carrying `:2103` tokens were stripped, prose preserved:

- **Source Areas — "sprint executor control flow"** (L114): `… + `:2103` bundle guard)` → `… + single-session diagnostic-bundle guard)`.
- **Key Constraints — "infra not product-bug"** (L126): `… (so `executor.py:2103` skips the bundle) …` → `… (so the single-session diagnostic-bundle path skips the bundle) …`.

Verified: zero `2103` tokens remain in the EC block (L100-135). The citation still lives correctly in item 5.3's Context (lines 2103-2132). The `:2103` mentions in the Overview/Objectives prose (L75, L82) and in item Contexts (5.1-negative-check, 5.3, gate-agent prompts) are outside the EC block and out of F4 scope — correctly left intact.

---

## Constraints Honored

| Constraint | Status |
|------------|--------|
| Frontmatter `start_commit` / `executor_model_class` / `spec_path` / `reflect_post` room comment unchanged | VERIFIED (grep) |
| POST-reflect penultimate item (PC.5) unchanged | VERIFIED (Read) |
| status→Done final item (PC.6) unchanged — anti-orphaning intact | VERIFIED (Read) |
| QA gates not weakened — 6 agents/gate | VERIFIED (36 spawn items = 6 gates × 6) |
| Load-bearing directives A/C/D/E/G-1/G-2/G-3 preserved | VERIFIED (referenced in split sub-items + 5.3) |
| Two OQ PENDING-fallback items (6.1 OQ-1, 7.2 OQ-2) preserved | VERIFIED (grep: OQ-1 ×10, OQ-2 ×8, PENDING ×26) |
| Sub-items 5-component B2-complete | VERIFIED (Read of all new sub-items) |
| Item numbering sequential within each phase | VERIFIED (no per-item numbers; Step headers unchanged) |

## MINOR items (not applied — non-blocking, by spec)

- B2-MINOR (logging_.py event methods soft test target): accepted as-is for a telemetry event; not a task-file structural defect.
- Struct-MINOR (Phase 5 header understates recovery_policy.py dependency; `config.max_session_resets` forward-ref): physical ordering already correct and the "default 8 until P5 lands" bridge note is already present in 4.4 — no edit needed.
- Advisory (stale `Status: In Progress` in `research/02-patterns-conventions.md`): research artifact, not the task file — out of scope for a task-file fix.

## Tool engagement
Read: 4 | Grep: 3 | Glob: 0 | Bash: 5 | Edit: 6

## VERDICT: FIXED (all 4)
