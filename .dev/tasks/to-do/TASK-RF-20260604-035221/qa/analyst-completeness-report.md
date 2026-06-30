# Research Completeness Verification

**Topic:** PR #124 merge-conflict resolution + PASS_RECOVERED correctness fix
**Task:** TASK-RF-20260604-035221
**Date:** 2026-06-04
**Files analyzed:** 3 research files (+ research-notes.md context)
**Depth tier:** Quick (3 researchers, 0 web)
**Analysis type:** completeness-verification (10 spawn-prompt criteria)

---

## Verdict (preliminary — see bottom for final)

Findings appended incrementally below, one criterion at a time.

---

## Files In Scope

| File | Status header | Size | Read |
|---|---|---|---|
| research/01-conflict-hunks-verified.md | Complete | 10.9 KB | YES |
| research/02-pass-recovered-coupling.md | Complete | 21.0 KB | YES |
| research/03-validation-and-test-surface.md | Complete | 25.7 KB | YES |
| research-notes.md (context) | — | 5.8 KB | YES |

All three research files carry `Status: Complete`. None are In Progress.

---

## Criterion-by-Criterion Findings

### Criterion 1 — All 3 conflicted files + every hunk with exact markers/line numbers + verified resolution

**PASS.**

Evidence (file 01):
- **CHANGELOG.md** (1 hunk): markers tabulated — `## [Unreleased]` @5, `<<<<<<< origin/master` @7, `=======` @25, `>>>>>>> ...v435` @55 (01 lines 37-42). Resolution: KEEP BOTH `###` sections, master block first then PR block, preserving the trailing `### sc:cleanup-audit` at line 57 (01 line 51). Both sides characterized as additive/non-overlapping.
- **executor.py** (1 hunk): markers `<<<<<<< origin/master` @354, `=======` @356, `>>>>>>> ...v435` @358 (01 lines 61-63). Conflict body shown both sides (01 lines 67-75). Resolution: TAKE MASTER (01 line 77).
- **commands.py** (2 hunks): hunk-1 decorators @191/211/235, hunk-2 param list @255/259/262 — tabulated (01 lines 97-99). Both resolutions specified (union + insertion; union concat).

All line numbers are sourced from the merge-tree blob `git show $TREE:<path>` with TREE OID `a53db586640dc2bb2753e585862108ed737fd529` (01 lines 16-25), and the file flags the caveat that these are *merged-blob* line numbers (not post-edit), which is the correct frame for marker stripping. Every hunk has a stated, justified resolution. Complete.

### Criterion 2 — commands.py `@click.option(` mid-decorator insertion subtlety documented WITH compile evidence both ways (naive=FAIL, insertion=OK)

**PASS — and this is the strongest single finding in the research set.**

Evidence (file 01 lines 101-145):
- The shared `@click.option(` opener at **line 190** (one line ABOVE the `<<<<<<<` at 191) is explicitly identified, and the mechanism — master's first option (`--handoff/--no-handoff`) consumes the line-190 opener, leaving PR's `"--fresh",` block with NO opener of its own — is spelled out (01 lines 103-121).
- The naive-strip orphan point is pinpointed: closing `)` of `--task-parallelism` immediately followed by `"--fresh",` with no decorator (01 lines 119, 135-139).
- **Compile evidence BOTH ways via `uv run python -m py_compile`:**
  - NAIVE union → `IndentationError: unexpected indent (naive.py, line 210)` → `NAIVE: COMPILE FAILED` (01 lines 130-139).
  - CORRECT union (one inserted `@click.option(` + param-list union) → `CORRECT: COMPILE OK` (01 lines 141-144).
- Resulting decorator order explicitly enumerated (01 line 124): `--handoff/--no-handoff → --resume → --task-parallelism → (inserted opener) → --fresh → --restart → --yes/-y → @click.pass_context`.

This is exactly what the criterion demands: the subtlety is documented and both the failing and passing states are demonstrated with actual compiler output. Complete.

### Criterion 3 — executor.py take-master rationale tied to the auto-merged models.py `is_success={PASS,PASS_RECOVERED}`

**PASS.**

Evidence (file 01 lines 77-88):
- Resolution = TAKE MASTER: `report.tasks_passed = sum(1 for r in task_results if r.status.is_success)`.
- Rationale tied directly to the auto-merged `models.py` blob: `git show $TREE:.../models.py` keeps `PASS = "pass"` (49), `PASS_RECOVERED = "pass_recovered"` (50), and `is_success` returning `self in (TaskStatus.PASS, TaskStatus.PASS_RECOVERED)` (57-58) — quoted verbatim (01 lines 81-86).
- Causal chain stated: PR's strict `== TaskStatus.PASS` would **drop every PASS_RECOVERED task** from the passed-count; PR side is stale (predates #126's PASS_RECOVERED landing). (01 line 88).

Cross-validated against file 02 §1 (lines 20-32) and file 02 §7 (line 228), which independently confirm the executor.py `==PASS` line is the merge-conflict-surfaced one and resolver MUST keep master's `is_success`. Consistent across files. Complete.

### Criterion 4 — All 6 resume/ PASS_RECOVERED sites enumerated (file:line) with precise None-safe replacements

**PASS.**

Evidence (file 02 §6 lines 202-214, consolidated table) — all 6 sites enumerated with file:line, role, current predicate, and proposed None-safe replacement:

| # | File:line | Role | Proposed (None-safe) |
|---|---|---|---|
| 1 | planner.py:163 | rerun_task_ids ("not done") | `is None or not .is_success` |
| 2 | planner.py:318 | last_completed ("done") | `is not None and .is_success` |
| 3 | planner.py:324 | next_unfinished ("not done") | `is None or not .is_success` |
| 4 | integrity.py:123 | signal_a_pass ("done") | `is not None and .is_success` |
| 5 | integrity.py:129 | signal_b_pass ("done", derived) | `is not None and .is_success` |
| 6 | drift.py:93 | recorded_completed ("done") | `is not None and .is_success` |

Each site is also documented individually with its source code, the `is`/`is not` polarity, and the failure-mode effect (02 §3 planner ×3, §4 integrity ×2, §5 drift ×1). The two canonical predicates ("done" vs "not done") are stated separately (02 lines 204-205) so polarity isn't conflated — a subtle correctness point handled correctly (the "not done" sites use `is None OR not is_success`; the "done" sites use `is not None AND is_success`).

The None-safety rationale is grounded: `persisted_status` is `TaskStatus | None` because `_coerce_task_status` returns `None` on unparseable strings (02 line 101; 03 lines 75-83), and the `is None` guard preserves the original junk-handling behavior (02 line 147). The synthetic-boundary literal `BoundaryTask(persisted_status=TaskStatus.PASS, ...)` at planner.py:215-220 is explicitly noted as an assignment, NOT a comparison → correctly excluded from the edit set (02 line 137). The phase-level `_is_pass_family` path (planner.py:380-385) is explicitly marked DO-NOT-CHANGE because it already routes through `PhaseStatus.is_success` (02 line 135). Complete and precise.

### Criterion 5 — Persisted-status data path traced (executor assigns PASS_RECOVERED → phase-N-result.json → planner reads back) with evidence

**PASS.**

Evidence (file 02 §2 lines 63-94) — full round-trip traced with line citations:
1. **Assignment:** master `executor.py:1004-1015` — `status = TaskStatus.PASS_RECOVERED` at :1011 when `detect_error_max_turns(...) and _task_completed_before_overrun(...)` (02 lines 67-79).
2. **Serialization:** `TaskResult.to_dict` master `models.py:207` → `"status": self.status.value` → `"pass_recovered"` (02 lines 81-84).
3. **Persistence to disk:** master `executor.py:2638-2658` `_write_phase_result_json` → `payload["task_results"] = [tr.to_dict() ...]` (:2652) → `config.phase_result_json(phase)` (:2655) → `tmp.write_text(json.dumps(...))` (:2658) (02 lines 87-92).
4. **Read-back:** `from_dict` master `models.py:231` → `status=TaskStatus(data["status"])` reconstructs `TaskStatus.PASS_RECOVERED` (02 line 85), which the resume planner then compares by identity (02 line 94).

File 03 §0.4/§0.3 independently corroborates the read-back via `_coerce_task_status(TaskStatus(value))` and shows the pre-rebase vs post-rebase divergence (03 lines 85-89). The data path is end-to-end traced with file:line evidence at every hop. Complete.

### Criterion 6 — integrity.py:129 Signal B deeper-problem nuance captured (transcript re-derivation never emits PASS_RECOVERED → design decision, not a swap)

**PASS — handled with notable rigor.**

Evidence (file 02 §4 lines 161-176):
- Signal B = `signal_b_pass = derived is TaskStatus.PASS` where `derived = _classify_transcript(transcript)` (02 lines 162-165).
- The nuance is explicitly captured: `_classify_transcript` (master `rerun_tasks.py:547-593`) is typed `-> TaskStatus` (non-Optional) and **never returns `PASS_RECOVERED`** — it only emits `PASS / INCOMPLETE / FAIL_RECOVERABLE / FAIL_TERMINAL`. So widening to `.is_success` is **behavior-neutral for PASS_RECOVERED** (the value can't appear) (02 line 167).
- The DEEPER problem is surfaced: a recovered task exited non-zero, so `_classify_transcript` classifies its transcript as FAIL_TERMINAL/FAIL_RECOVERABLE → Signal B independently returns False for a genuinely-recovered task EVEN AFTER Signal A is fixed (02 line 167).
- Explicitly tagged: **"Signal-B-vs-recovered = needs design decision, not a one-line swap"** (02 line 167), and the §6 table row 5 repeats the cross-reference to the §4 nuance (02 line 213).

This is exactly the "design decision, not a swap" framing the criterion requires, and it is propagated to file 03's test guidance (03 line 223 marks `validated_last is True` for the exact combination as Unverified pending the implementer running it, precisely because of the Signal-B caveat). The research correctly recommends the minimal `is_success` widening as merge-safe/future-proof while flagging that it does NOT by itself make the integrity gate accept a recovered seam. Complete.

### Criterion 7 — Test insertion point concrete (named anchor test to mirror, fixtures) + pre-existing baseline failure documented

**PASS.**

Insertion point + mirror anchor (file 03 §1):
- Named anchor test to mirror: **`TestResumePlanner.test_resume_task_level_recoverable`** (03 lines 124-162, full source quoted) — asserts all three planner behaviors the new test needs.
- Companion gate anchor: **`TestInvariants.test_gate_hard_stops_on_last_completed_overclaim`** (03 line 164) via `_build_gate_fixture`.
- Concrete insertion location: inside `TestResumePlanner` after `test_resume_task_level_recoverable` (~line 140) for planner assertions, companion in `TestInvariants` after the overclaim test (~line 634), OR a single combined method (03 lines 166-167).
- Fixtures enumerated: `_write_index` (51-55), `_complete_phase` (58-66), `_write_log` (69-72), `_task_block` (75-79), `_build_task_interrupted` (242-289), `_build_gate_fixture` (569-608), `PASS_TRANSCRIPT` constant (34-37), autouse `_stub_invoke_sonnet` (40-43) — all with line refs (03 §1.1-§1.2).
- Proposed new-test name + full source draft: `test_resume_pass_recovered_counts_as_completed` with RED-pre-fix / GREEN-post-fix assertions (a)(b)(c) (03 lines 169-220). Naming convention (snake_case + spec-ref docstring) is matched (03 line 122).

Baseline failure (file 03 §2):
- Documented: `tests/sprint/test_e2e_success.py::test_jsonl_events_for_each_phase` (stale event count after #116 added `checkpoint_manifest`), confirmed to exist at line 117 (03 lines 228-238).
- Honestly hedged: marked **Unverified by execution** whether it currently passes/fails post-rebase, with an explicit baseline rule — "the ONLY acceptable failing test ... IF independently confirmed failing on the rebased base without the fix; any other failure is the task's responsibility" (03 lines 236-238).

One honest residual flag worth surfacing (not a gap, a noted limitation): assertion (c) `validated_last is True` for the exact recovered-seam combination is explicitly marked **Unverified** until the implementer runs it (03 line 223), because of the Signal-B nuance from Criterion 6. The research correctly identifies the planner-half assertions (a)+(b) as the load-bearing RED→GREEN signal. This is appropriate flagging, not a deficiency. Complete.

### Criterion 8 — Validation commands correct (pytest; py_compile; ruff check AND ruff format --check separately; verify-sync NOT relevant)

**PASS.**

Evidence (file 03 §3 lines 242-270):
- **pytest:** `uv run pytest tests/sprint/ -q`; isolatable new test via `-k pass_recovered`; explicit RED→GREEN protocol (run before fix = RED, after = GREEN) (03 §3.1).
- **py_compile:** `uv run python -m py_compile <each edited file>` with examples for planner.py + test_resume.py (03 §3.2).
- **ruff check AND ruff format --check SEPARATELY:** correctly grounded against the Makefile + CI workflows — `make lint`/Makefile `lint:` runs ONLY `ruff check .`; CI runs both `ruff check src/ tests/` AND `ruff format --check src/ tests/` separately (quick-check.yml:37/41, test.yml:96/100). Explicitly states `make lint` (green) ≠ CI format gate (green), matching memory `reference_make_lint_vs_ci_ruff_format.md`. Both commands mandated, plus the `ruff format src/ tests/` remediation step if the check fails (03 lines 255-267).
- **verify-sync NOT relevant:** correctly justified — `make verify-sync` only checks `src/superclaude/{skills,agents,commands,hooks,templates}` against the `.claude/` mirror; the fix edits `cli/sprint/resume/planner.py` + tests, which are CLI source + tests, NOT a synced component type (Makefile sync-dev at line 109 syncs only component dirs; `cli/` not among them) (03 §3.4 lines 269-270).

All four validation requirements are present, correct, and evidence-grounded. Complete.

### Criterion 9 — rebase-required + git-worktree (dirty master untouched) + PR-fork-target discipline captured

**PASS.**

Evidence (file 03 §4 + §5):
- **Rebase REQUIRED:** master is 8+ commits ahead of the branch base (merge-base `86c46321`), including #120 (added `TaskStatus.PASS_RECOVERED`) and #126; rebase is required both to satisfy gh ("No commits between...") AND because the fix DEPENDS on master's `TaskStatus`/`is_success` (03 §5.1 lines 297-300). CLAUDE.md line 55 prescription (rebase onto `origin/master`) cited verbatim (03 lines 286, 321).
- **Git-worktree / dirty-master protection:** explicit working-tree caution — current master tree has UNCOMMITTED unrelated changes (`init_lite.py`, `sc-init-lite-protocol/SKILL.md`, plus session-start sprint/executor.py, handoff.py, test files, untracked `.dev/`) that MUST NOT be staged/stashed-lost/committed; recommends `git worktree add ../IronClaude-pr124 ...` to operate in isolation; "never `git checkout` over them" (03 §5.3 lines 309-314). Cites memory `feedback_no_multiline_paste.md` for single-line commands.
- **PR-fork-target discipline:** the entire CLAUDE.md "PR Target = Fork" block is quoted verbatim with line refs — `origin = IronbellyOrg/IronClaude`, never push `upstream`, mandatory `gh pr create --repo IronbellyOrg/IronClaude --base master ...` shape, the 3 pre-PR checks, and verify-URL-points-at-fork (03 §4 lines 274-291). Also notes PR #124 is already OPEN on the fork so no new `gh pr create` is needed; force-with-lease after rebase (03 §5.3 step 6-7).
- `.claude/` staging prohibition also captured (03 line 289).

Complete and well-grounded in both CLAUDE.md and the live repo state.

### Criterion 10 — Genuine ambiguities flagged (not silently assumed)

**PASS.**

Evidence — ambiguities are surfaced, not buried:
- **Signal B design decision** (02 §4 line 167; §6 table row 5 line 213; 03 line 223) — explicitly tagged "needs design decision, not a one-line swap"; downstream test assertion (c) marked Unverified.
- **Out-of-scope same-class couplings as follow-ups:** `handoff.py:34` (`is_validated_success`, master-only, compares `.value` string) and `rerun_tasks.py:1192/1231` (`last_pass` tracking) — both enumerated in the §7 codebase-wide sweep table with explicit OUT-OF-SCOPE verdicts and "same bug class, flag as follow-up" notes (02 §7 lines 230, 233, 235; §summary line 262).
- **Deliverable B scope boundary:** research-notes.md AMBIGUITIES_FOR_USER (lines 102-108) flags that the PASS_RECOVERED widening is technically beyond "resolve the conflicts" and touches non-conflicted files — operator already chose to bundle A+B, but builder must surface it.
- **preflight.py / executor.py:1286 sweep:** explicitly classified out-of-scope with reasons (preflight never assigns PASS_RECOVERED; executor:1286 auto-resolves to master's form) (02 §7 lines 229, 231-232).
- **Line-number volatility caveat:** research-notes.md (lines 56-58) flags that resume/*.py line numbers were from `git show` and may shift after conflict-resolution edits — appropriately hedged.
- **test_resume_* on master:** 03 §5.2 line 306 marks as **Unverified** whether master already has a partial resume surface that the PR branch's `resume/` package must reconcile with — a genuine open item flagged rather than assumed.

No silent assumptions detected. Genuine ambiguities are consistently flagged with Unverified tags or explicit out-of-scope/follow-up classification. Complete.

---

## Cross-Cutting Checklist

### Evidence Quality

| Research File | Evidence character | Unsupported claims | Rating |
|---|---|---|---|
| 01-conflict-hunks-verified.md | Every hunk cites TREE OID `a53db586`, `git show $TREE:<path>` line numbers, and `py_compile` output (both naive-FAIL and correct-OK) | 0 | Strong |
| 02-pass-recovered-coupling.md | Every site cites `git show <ref>:<path>` file:line + quoted source; full data-path trace with line refs; codebase-wide sweep table | 0 | Strong |
| 03-validation-and-test-surface.md | Cites Makefile/CI workflow line numbers, test file line numbers, CLAUDE.md verbatim quotes; honestly marks `validated_last` + e2e-baseline as Unverified-by-execution | 0 (Unverified items are explicitly tagged, not asserted) | Strong |

All claims are traceable to a git command or a quoted file:line. No vague architecture descriptions. The research correctly distinguishes *verified-by-execution* (py_compile, merge-tree) from *Unverified-pending-implementer-run* (e2e baseline pass/fail, gate `validated_last`).

### Documentation Staleness

No doc-sourced architectural claims drive the resolutions — every claim is code-traced (git blobs, source line refs) or CLI/CI-config-traced. The one "documentation" source is PR #124's body (quoted verbatim in 03 §2 for the baseline-failure claim), and it is explicitly cross-checked against the actual test file + master blob and tagged Unverified-by-execution where it could not be confirmed read-only. No untagged doc-sourced claims. No `[CODE-CONTRADICTED]` claims presented as fact.

### Completeness

| Research File | Status | Summary | Gaps/Caveats | Key Takeaways | Rating |
|---|---|---|---|---|---|
| 01 | Complete | Y (lines 203-218) | Y (caveats inline + auto-merge table) | Y | Complete |
| 02 | Complete | Y (lines 249-262) | Y (§4 nuance, §7 sweep, §8 coverage gap, out-of-scope) | Y | Complete |
| 03 | Complete | Y (lines 325-333) | Y (§2 baseline, §5 rebase risks, Unverified tags) | Y | Complete |

All three are Status: Complete with Summary + caveats/gaps + takeaways. None In Progress.

### Contradictions Found

**None.** The three files are mutually consistent and cross-reinforcing on every shared fact:
- The executor.py take-master resolution (01 §FILE 3) agrees with 02 §7's "merge-conflicts here, keep master's is_success" classification.
- The `models.py` auto-merge keeping `is_success={PASS,PASS_RECOVERED}` is identically reported in 01 (lines 81-86), 02 (lines 20-32), and 03 (lines 36-47).
- The planner predicate fix shape (`is not None and .is_success`) is identical across 02 §3/§6 and 03 §0.3.
- The 6-site count is consistent (02 enumerates exactly 6; research-notes lists planner ×3, integrity ×2, drift ×1 = 6).

One *line-number presentation* nuance (not a contradiction): file 03 §0.3 cites planner sites as "~160-163 / ~316-329" (approximate) while file 02 §3 cites exact lines 163/318/324. These are consistent (03 uses range-approx, 02 is precise); both source from `git show origin/feat/...`. The research-notes line-volatility caveat (must reconfirm against checked-out branch HEAD after rebase) covers this. Not a contradiction.

### Compiled Gaps

#### Critical Gaps (block synthesis)
- **None.** All 10 spawn criteria PASS with evidence. The research is sufficient to build the MDTM task file.

#### Important Gaps (affect quality — must be carried into the task file, NOT re-researched)
These are *flagged limitations the research deliberately deferred to implementer-run-time*, correctly handled as Unverified rather than guessed — they are task-file inputs, not research deficiencies:
- **G1 — Signal-B design decision (integrity.py:129).** The minimal `is_success` widening keeps signals consistent but does NOT make the integrity gate accept a recovered seam (Signal B re-derives FAIL_* from a non-zero-exit transcript). The task file must (a) apply the minimal widening AND (b) surface that integrity validation of a `PASS_RECOVERED` last_completed may still STOP via Signal B unless integrity logic is taught to treat a recovered persisted status as authoritative. Test assertion (c) `validated_last is True` is consequently Unverified — the task must treat (a)+(b) planner assertions as the load-bearing RED→GREEN signal, and run (c) to confirm or adjust. (Source: 02 §4 line 167; 03 line 223.)
- **G2 — Post-rebase line-number reconfirmation.** All resume/*.py line numbers are from `git show origin/feat/...`; they may shift after conflict-resolution + rebase edits. The task must re-locate the 6 sites by predicate text (not by raw line number) on the checked-out, rebased branch. (Source: research-notes lines 56-58.)
- **G3 — master `test_resume_*` reconciliation.** Unverified whether master already carries a partial resume surface that the PR branch's `resume/` package must reconcile with during rebase (03 §5.2 line 306). The task's rebase step must inspect `test_resume_backward_compat.py / test_resume_contract.py / test_resume_semantics.py` on the rebased tree.
- **G4 — e2e baseline pass/fail is execution-Unverified.** `test_jsonl_events_for_each_phase` may now pass on the rebased tree (master may have updated the expected count). The task must run the suite once and apply the documented baseline rule (only this test may fail, and only if independently confirmed failing without the fix). (Source: 03 §2.)

#### Minor Gaps (must still be noted)
- **G5 — Out-of-scope same-class follow-ups.** `handoff.py:34` (`is_validated_success`, compares `.value`) and `rerun_tasks.py:1192/1231` (`last_pass`) share the bug class but are pre-existing master couplings, explicitly OUT OF SCOPE for this PR. The task file should record them as follow-up notes (already recommended by 02 §7 + summary). Not action items for this merge.

### Depth Assessment

**Expected depth:** Quick tier (small, well-bounded scope; 3 researchers, 0 web).
**Actual depth achieved:** Exceeds Quick-tier expectations. The research delivers data-flow tracing (persisted-status round-trip), executable verification (py_compile both ways, merge-tree), a full codebase-wide identity-check sweep with in/out-of-scope classification, and a complete RED→GREEN test draft. This is Standard-to-Deep-tier rigor on a Quick-tier scope — appropriate given the correctness-critical merge.
**Missing depth elements:** None. The only Unverified items (gate `validated_last`, e2e baseline, post-rebase line numbers, master test_resume_* surface) are genuinely execution-dependent and correctly deferred to implementer run-time rather than guessed.

### Recommendations (for the task-builder, not re-research)

1. Build the task file as-is from research-notes SUGGESTED_PHASES (6 phases) — research is complete and sufficient.
2. Carry G1 (Signal-B design decision) into the task as an explicit decision point / note, NOT a silent one-line swap. Keep test assertion (c) but mark it adjustable pending the implementer's run.
3. Instruct the executor to re-locate the 6 resume sites by predicate text after rebase (G2), and to inspect master's `test_resume_*` files during conflict resolution (G3).
4. Encode the baseline rule for `test_jsonl_events_for_each_phase` verbatim (G4): run once, attribute only this to baseline if independently confirmed, own all other failures.
5. Record G5 (handoff.py:34, rerun_tasks.py:1192) as out-of-scope follow-up notes in the task file.
6. Encode the worktree + rebase + fork-PR discipline (Criterion 9) into the branch-setup phase exactly as 03 §4-§5 specify.

---

## VERDICT: PASS

All 10 spawn-prompt criteria PASS with cited evidence. Zero critical gaps. The three research files are mutually consistent (no contradictions), uniformly Strong on evidence quality, all Status: Complete, and exceed the Quick-tier depth expectation. The four "Important" items (G1-G4) are not research deficiencies — they are correctly-flagged, execution-dependent inputs that the task file must carry forward (Signal-B design decision, post-rebase line reconfirmation, master test_resume_* reconciliation, e2e baseline confirmation). G5 is an out-of-scope follow-up note. The research is sufficient and ready for task-file assembly.

**Gate recommendation:** PROCEED to task-file build, carrying G1-G5 forward as task-file content per the Recommendations above.
