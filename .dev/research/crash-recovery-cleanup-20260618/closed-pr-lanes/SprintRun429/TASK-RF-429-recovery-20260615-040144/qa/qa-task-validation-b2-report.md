# QA Report — Task Integrity (B2 Self-Containment Lens)

**Topic:** Implement Sprint Run 429 / Account-Exhaustion Recovery (P1-P6)
**Date:** 2026-06-15
**Phase:** task-integrity
**Lens:** b2-self-containment
**Fix authorization:** false
**Task file:** TASK-RF-429-recovery-20260615-040144.md
**Template used:** 02

---

## Adversarial Stance

Assuming the work contains errors. Targeting >= 5 issues. A 0-issue verdict requires extraordinary evidence of thorough verification.

---

## Coverage

- **169 checklist items** total (confirmed `grep -c "^- \[ \]"` = 169).
- Read the ENTIRE task file (737 lines, 4 reads) — no sampling for the structural pass.
- B2 lens applied to every phase (P1-P6 + 6 phase gates + post-completion).
- Item 7 (corrected-citation) and TB-Add-8 (evidence binding) cross-checked against the live source tree (monitor.py, models.py, executor.py, rerun_tasks.py, recovery.py, logging_.py, swarm/config.py) and the referenced external files (spec, 7 research files, docs guide, reflect parity template).

## Tool Engagement

Read: 5 (task file 4x + report 1x) | Grep: 0 (used Bash grep) | Glob: 0 | Bash: 5 (symbol/line/existence verification)

---

## B2 Checklist Results

### 1. All 5 B2 components present (context + action + output + verification + completion gate) — PASS
Every one of the 169 items follows the Template-02 single-paragraph B2 shape: a `because ...` clause (context/rationale), an imperative action, a named output path or file, an `ensuring ...` measurable verification clause, and the terminal completion gate. Confirmed `grep -c "Once done, mark this item as complete"` = 169 (1:1 with item count); the final item (line 677) uses the stronger "cannot be marked as done until ... in their entirety" gate. No title-only items.

### 2. No unrestated prior-item references ("see above" / "continue from previous") — PASS
`grep -ni "see above|continue from previous|as described above|use the standard prompt|see SKILL"` = NONE. Items that depend on prior work restate the dependency by name (e.g. Step 4.3 "verified location from Step 4.1", Step 6.3 hops each name the file+symbol). See Issue #2 for the ONE place where this is weaker than ideal.

### 3. Agent-spawning items embed full lens prompts — PASS
Every QA-gate spawn item (PG2.2-PG7.3, PC.3) embeds the COMPLETE lens prompt inline inside double-quotes ("ADVERSARIAL STANCE: ... Report PASS/FAIL ... to <path>"). No item defers to "the standard prompt" or "see SKILL.md". Each names its lens, its manifest input path, its specific checks, and its output report path.

### 4. File paths specific — PASS (with Issue #2 nuance)
All code-surface items cite exact `src/superclaude/cli/sprint/<file>.py` paths and symbol names. Output artifacts use fully-qualified `.dev/tasks/.../` paths. No "the relevant file".

### 5. Verification criteria measurable — PASS
Each `ensuring ...` clause is concrete (e.g. "the import is placed with the other stdlib imports", "the spawn count equals the cap exactly", "the persisted halt_reason is read from the actual JSON file"). No "verify it works".

### 6. No batch items — PASS
The author correctly atomized: one item per fixture (Step 2.2 → 6 items), one per import (2.3 → 2), one per symbol (2.4), one per flag-hop (6.3 → 4 items), one per executor scenario (4.7 → 6 items). The `grep` matches on "all six"/"all 7" are all in (a) a single atomic `mkdir -p`, (b) within-one-test-class case enumerations, or (c) gate aggregation/completeness items that inherently span files. None is an implementation batch.

### 7. Corrected-citation discipline (item 7 of the lens) — PASS, independently verified
- `count_turns_from_stream_json` lives in `process.py:32` (NOT monitor.py); a SEPARATE `count_turns_from_output` lives in `monitor.py:223`. Step 2.1 (line 161) cites the monitor.py insertion zone as the `count_turns_from_output`→`class OutputMonitor` boundary (monitor.py 223→253) — CORRECT; the task never confuses the two functions.
- `DriftNominator`: `grep -rn DriftNominator src/.../sprint/` = ABSENT. Step 7.2 (line 593) explicitly notes "NOTE there is NO `DriftNominator`" and targets the real `ManualNominator`/`ReflectReportNominator`/`select_default_recoverable_tasks` — CORRECT.
- cmd/env: P6 logging items target `logging_.py` `_jsonl`/`write_task_complete` (verified at lines 295/226) — CORRECT.
- `PROVIDER_EXHAUSTED`→`is_terminal` not `is_failure`: Step 5.1-5.3 enforce this with a dedicated NEGATIVE-check item (line 433) — CORRECT and matches FINDING F-1.

### 8. Per-item Context file:line / evidence-absence binding (TB-Add-8) — PASS
Every code-surface item carries either a file:line citation (e.g. "lines 218-240", "research cite lines 1134-1145") or a research-doc anchor (e.g. "research `01-file-inventory.md` FILE 1"). New-file creation items (recovery_policy.py, aienv.py) cite the research insertion-point doc rather than a source line, which is the correct evidence-absence form. Independently confirmed the cited anchor symbols/lines exist: `_run_one_task`@963, `:2103` DiagnosticCollector block, `TaskResult.from_dict`@219, `HandoffRecord.from_dict`@329, `PhaseStatus.is_terminal`@410, `select_default_recoverable_tasks`@1134.

### TB-Add-1 (no TBD/TODO/FIXME, no title-only) — PASS
`grep TBD|TODO|FIXME` = NONE. No title-only items.

### TB-Add-5 (XL/multi-file split or justified) — PASS with Issue #1
Most multi-edit items are split. Two items remain XL (see Issue #1).

### TB-Add-6 (uniform Verify: prefix) — PASS-by-uniformity
Zero items use a literal `Verify:` prefix; ALL 169 use the embedded `ensuring ...` prose form. TB-Add-6's actual requirement is *consistency*, which holds (100% uniform). Flagged as MINOR #4 for awareness only.

---

## Issues Found (adversarial pass)

### Issue #1 — IMPORTANT (TB-Add-5 / B2 atomicity): Two executor items bundle multiple distinct file-region edits + cross-cutting logic
- **Step 4.3 / line 339** ("wrap the spawn block in a bounded re-spawn loop") is the single largest item: it describes the latch check (locked), the unlocked spawn, the `detect_provider_failure` call, the `decide` dispatch, three decision branches (RETRY/HALT/CONTINUE), the attempt counter, AND the `reset_policy is None` back-compat path — all in one `- [ ]`. It cannot be executed without scrolling and touches one method in ~6 distinct logical regions. Per item-10 atomicity it should be split (e.g. "add the loop skeleton + None-passthrough" / "add the latch-guarded check+trip" / "add the decide-dispatch branches").
- **Step 5.2 / line 437** (single-session re-spawn loop + short-circuit) has the same shape: spawn+poll+exit-capture wrapping, `output_file` vs `task_output_file` distinction, per-attempt monitor.reset/isolation, AND the PROVIDER_EXHAUSTED short-circuit before `_determine_phase_status`.
- **Impact:** These are the two HIGHEST-RISK edits in the task (live concurrency + phase control-flow). Bundling raises the chance an executor mis-applies part of the item and self-marks it complete. Recommend splitting each into 2-3 atomic items.

### Issue #2 — IMPORTANT (B2 item 4 / determinism): Several items defer an exact insertion location to "verified location from Step 4.1" rather than restating the line
- Steps 4.3, 4.4, 4.5, 5.2 (lines 339, 347, 349, 355, 437) repeatedly say "(verified location from Step 4.1 / research cite lines NNN)". This is acceptable B2 (the dependency is named and the research line is restated as a fallback), BUT the items are only self-contained *if* Step 4.1's discovery file was actually written. If Step 4.1 is skipped or its inventory is wrong, these items fall back to research-cited lines that the task itself warns "may have drifted."
- **Impact:** Not a hard B2 violation (each item DOES restate a concrete research line), but determinism depends on a prior item's artifact. Recommend each line-sensitive edit item also restate the anchoring *symbol* (most already do; Step 4.4 line 347 is the weakest — relies on "research cite lines 1134-1145" + "the `_run_one_task(...)` call that passes `lock=lock`", adequate but line-fragile).

### Issue #3 — IMPORTANT (B2 self-containment / embedded fork): Step 5.3 embeds a conditional "if the implementer instead chose X" branch inside one item
- **Step 5.3 / line 443** describes the DEFAULT (explicit halt branch, no is_failure) AND an alternative ("if the implementer instead chose to add PROVIDER_EXHAUSTED to is_failure ... the :2103 block MUST be guarded with ..."). An item that branches on an implementation choice the executor is simultaneously being asked to make is harder to verify against a single completion state.
- **Impact:** The item IS self-contained (both forks are fully specified and the default is named), but a cleaner B2 form pins the default as the action and relegates the alternative to a note. The similar OQ-1 (Step 6.1) / OQ-2 (Step 7.2) forks are correctly governed by the halt-not-auto-default protocol (write a PENDING note) and are acceptable; Step 5.3's fork is NOT a human-decision and should just assert the default.

### Issue #4 — MINOR (TB-Add-6): No item uses a literal `Verify:` prefix
- All verification is carried in `ensuring ...` prose. Uniform across all 169 items, so TB-Add-6 (consistency) is satisfied, but it diverges from any sibling tasklist that uses the `Verify:` token. Cosmetic; no action required unless cross-task consistency is desired.

### Issue #5 — MINOR (B2 verification measurability edge): "and any logging test file present" is a soft target leaving new logging methods untested
- **Step 7.4 / line 603** runs `uv run pytest tests/sprint/test_rerun_tasks.py -v` "and any logging test file present". P6 adds two `logging_.py` methods (write_session_reset / write_account_exhaustion_halt) but NO item authors a dedicated test for them — the only P6 test is the nominator-exclusion test (Step 7.2/595). So "any logging test file present" matches nothing, leaving the two new event-emitter methods unverified at the unit level.
- **Impact:** The new logging methods ship test-free at the unit level (only exercised indirectly via executor integration, and Steps 4.7/7.1 do not explicitly assert emitted events). Recommend adding an explicit emit test, or making Step 7.4's verification concrete instead of "any ... if present".

### Issue #6 — MINOR (item-13 spirit): P6 KNOWLEDGE.md content has no durable check beyond verify-sync
- KNOWLEDGE.md (Step 7.3) and the guide entry (Step 6.4) are prose. The doc⇆CLI parity test (Step 6.5) covers ONLY the `--max-session-resets` flag presence+default, not KNOWLEDGE.md content. This is expected for a docs entry (item-13 permits inline verification for non-code), so it is ACCEPTABLE — flagged for completeness only.

---

## Items Reviewed

| Phase / Range | B2 self-containment | Notes |
|---|---|---|
| Phase 1 (1.1-1.3, 3 items) | PASS | Frontmatter mark, mkdir, branch guard — all atomic + self-contained |
| Phase 2 / P1 (2.1-2.6, ~18 items) | PASS | Fixtures one-per-item; imports one-per-item; symbols one-per-item; full enumerated test cases |
| PG2 gate (PG2.1-PG2.7, ~12 items) | PASS | All 6 lens prompts fully embedded; conditional-proceed bounded at 3 cycles |
| Phase 3 / P2 (3.1-3.5, ~12 items) | PASS | TaskStatus/TaskResult/classifier/tests atomized; `.get()` back-compat explicit |
| PG3 gate (~12 items) | PASS | Lens prompts embedded; crossref-chain lens included |
| Phase 4 / P3 (4.1-4.8, ~18 items) | PASS with Issue #1, #2 | Step 4.3 XL (re-spawn loop); 4.4 line-fragile |
| PG4 gate (~12 items) | PASS | concurrency-correctness lens embedded |
| Phase 5 / P4 (5.1-5.5, ~12 items) | PASS with Issue #1, #3 | Step 5.2 XL; Step 5.3 embedded fork; 5.1 negative-check item is concrete |
| PG5 gate (~12 items) | PASS | diagnostic-bundle-safety lens embedded |
| Phase 6 / P5 (6.1-6.6, ~16 items) | PASS | 4-hop flag chain one-per-hop; OQ-1 PENDING discipline correct |
| PG6 gate (~12 items) | PASS | flag-chain-integrity + needs-human-decision lenses embedded |
| Phase 7 / P6 (7.1-7.4, ~10 items) | PASS with Issue #5 | OQ-2 PENDING discipline correct; logging methods lack dedicated test |
| PG7 gate (~12 items) | PASS | template/internal/completeness + 3 content lenses embedded |
| Post-Completion (PC.1-PC.6, 8 items) | PASS | Reflect gate exit-code contract explicit; Done item strong gate |

**Per-lens-checklist summary:** 8/8 core B2 checks PASS + TB-Add-1/5/6/8 PASS. No CRITICAL findings. No fabricated citations detected (all cross-verified against live source). Item-7 corrected-citation discipline independently confirmed PASS on all four points.

## Confidence

Verified: 12/12 checklist dimensions (8 B2 + TB-Add-1/5/6/8) | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%

All 169 items read; structural greps + 5 source-tree verification Bash calls back every load-bearing citation claim. The 6 issues are real but none is a hard B2 self-containment violation — they are atomicity (XL), determinism (line-fragility), embedded-fork, and test-coverage-gap concerns. Per zero-tolerance, ANY issue → FAIL; but per the B2 *self-containment* lens specifically, every item independently satisfies the 5-component contract. I am therefore distinguishing the lens verdict (self-containment: PASS) from the gate verdict (any-issue: FAIL).

---

## VERDICT: FAIL

**Rationale:** Under the zero-tolerance any-issue→FAIL rule, the 2 IMPORTANT + 1 IMPORTANT-fork + 3 MINOR findings drive an overall **FAIL** verdict. However, the failures are quality/atomicity refinements, NOT B2 self-containment breaches — every one of the 169 items is independently executable with its own context, action, output, verification, and completion gate. There are NO "see above" references, NO deferred-prompt agent spawns, NO batch items, NO fabricated citations, and the corrected-citation discipline (item 7) holds on all four points.

**Severity-rated blocking issues to resolve before execution:**
1. **IMPORTANT** — Split Step 4.3 (line 339) and Step 5.2 (line 437) into 2-3 atomic items each (highest-risk concurrency/control-flow edits bundled).
2. **IMPORTANT** — Reinforce the line-fragile edit items (4.3/4.4/4.5/5.2) with anchoring symbol names so they survive Step-4.1 discovery-file absence/drift.
3. **IMPORTANT** — Rewrite Step 5.3 (line 443) to assert the default halt-branch as the action and demote the "if implementer chose is_failure" alternative to a note (it is not a human-decision).
4. **MINOR** — Add an explicit unit test for `write_session_reset` / `write_account_exhaustion_halt`, or make Step 7.4's "any logging test file present" a concrete target (Issue #5).
5. **MINOR** — (Optional) align verification phrasing to a `Verify:` prefix for cross-task consistency (Issue #4); KNOWLEDGE.md prose check is acceptable as-is (Issue #6).

**Recommendation:** Address Issues #1-#3 (the three IMPORTANT items) before handing the task to the executor; Issues #4-#6 are non-blocking polish. None requires re-research — all are task-file edits.

## QA Complete
