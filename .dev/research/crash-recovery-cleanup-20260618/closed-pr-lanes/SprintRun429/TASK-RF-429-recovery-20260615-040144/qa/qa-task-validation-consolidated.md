# Consolidated Task-File Validation Findings (A.10 + A.10.25)

**Task file:** TASK-RF-429-recovery-20260615-040144.md
**Date:** 2026-06-15
**Source reports:** qa-task-validation-b2-report.md (FAIL), qa-task-validation-structure-report.md (FAIL), qa-task-research-alignment-report.md (PASS)

## Verdicts
- B2 self-containment (rf-qa): FAIL — 3 IMPORTANT + 3 MINOR
- Phase structure (rf-qa): FAIL — 1 IMPORTANT + 4 MINOR
- Research-alignment (rf-analyst): PASS — 0 gaps, 2 minor advisories

## Fixes to apply (IMPORTANT — all task-file edits, no re-research)

### F1 (B2-1) — Split XL re-spawn-loop items 4.3 and 5.2
Step 4.3 (per-task re-spawn loop) and Step 5.2 (single-session re-spawn loop) each bundle the entire loop (latch-check-under-lock, unlocked spawn, decide-dispatch, 3 action branches, attempt counter, None-passthrough) into one item — the two highest-risk edits. Split EACH into 2-3 atomic sub-items, e.g.:
- 4.3a: insert the bounded re-spawn loop skeleton + attempt counter around the spawn at executor.py:986-993 (the unlocked spawn stays unlocked).
- 4.3b: wire `detect_provider_failure(task_output_path)` + `SessionResetPolicy.decide(signal, attempt)` dispatch over the 4 Action values (RETRY_NEW_SESSION re-spawns; HALT_MODEL_SWITCH trips latch + breaks; FAIL_TASK/CONTINUE fall through).
- 4.3c: insert the provider-failure status branch in the ladder ABOVE `_is_transient_failure` (executor.py:1012) and BELOW the `:1003` completion gate, guarded by `_task_completed_before_overrun` (the (A) directive).
- Mirror the same 2-3 split for Step 5.2 (single-session loop around the ClaudeProcess spawn at executor.py:1815).
Keep each sub-item 5-component B2-complete.

### F2 (B2-2) — Anchor line-fragile items with symbol names
Items 4.3/4.4/4.5/5.2 defer location to "verified from Step 4.1". Reinforce each Context with the anchoring SYMBOL name (not just a line number) so they survive discovery-file drift: e.g. "the spawn call inside `_run_one_task` (executor.py ~:986-993, anchor: the `subprocess_factory`/`_run_task_subprocess` call)", "the two `_run_one_task(...)` call sites (anchor: `lock=lock` K>1 ~:1134-1145 and `lock=None` K=1 ~:1337-1348)", "the single-session `ClaudeProcess(config, phase, env_vars=…)` spawn (anchor: `_determine_phase_status` precedes at ~:1993)". Line numbers stay as ~approximate; the symbol is the durable anchor.

### F3 (B2-3) — Step 5.3: assert the is_terminal default, demote the is_failure fork to a note
Step 5.3 embeds an "if implementer chose is_failure" fork that is NOT a genuine human-decision (unlike OQ-1/OQ-2). The (G-1) resolution is definite: `PhaseStatus.PROVIDER_EXHAUSTED` goes in the `is_terminal` tuple (models.py:411-423) and NOT in `is_failure`. Rewrite 5.3 to ASSERT that default as the Action, and move the "OR guard executor.py:2103-2132 to exclude PROVIDER_EXHAUSTED" alternative into a parenthetical NOTE (the fallback only if some other consumer forces is_failure membership) — not a branch the executor must decide. The no-diagnostic-bundle regression test (Step 5.4) stays.

### F4 (Struct-1, TB-Add-7) — Strip file:line from the Execution Context block
The `## Execution Context` block carries literal `:2103` / `executor.py:2103` citations in two bullets (Source Areas "sprint executor control flow" ~L114; Key Constraints "infra not product-bug" ~L126). TB-Add-7 forbids file:line in the EC block. Strip the `:2103`/`executor.py:2103` tokens from both bullets (keep the prose: "the single-session diagnostic-bundle path" / "infra not product-bug"). The citation already lives correctly in item 5.3's Context (lines 2103-2132).

## MINOR (non-blocking — optional, fix opportunistically)
- B2-MINOR: logging_.py event methods (Step 7.4) lack a dedicated unit test (soft "any … if present" target) — acceptable for a telemetry event.
- Struct-MINOR: Phase 5 header understates the recovery_policy.py dependency on Phase 4 (physical ordering still correct); `config.max_session_resets` forward ref bridged by a "default 8 until P5 lands" note.
- Advisory: cosmetic stale `Status: In Progress` header in research/02-patterns-conventions.md line 2 (research artifact, not the task file).
