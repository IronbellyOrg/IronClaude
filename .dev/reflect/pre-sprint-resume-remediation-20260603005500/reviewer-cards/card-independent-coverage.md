# Independent UC-1 Coverage Audit — Sprint Resume Remediation

## Scope and method

Reviewed the corrective MDTM tasklist against the driving reflection report's Tier-3 remediation recommendation, which enumerates four items: F-3, F-2, F-4, and CG-4 (`/config/workspace/IronClaude/.claude/worktrees/SprintReRun/.dev/reflect/post-sprint-auto-resume-20260603003009/REPORT.md:101-117`). I also checked the supporting design/requirements and current source code for the planned fix surfaces.

## Coverage matrix

| Remediation item | Task-file coverage | Status | Notes |
|---|---|---:|---|
| F-3 — make Tier-1 conservative on Tier-0 hash miss with unchanged IDs; add CG-2 | Overview item 2 (`TASK...md:65`), objective 2 (`TASK...md:76`), Step 2.1 CG-2 RED (`TASK...md:174-176`), Step 2.2 persisted WS hash + test-helper co-edit (`TASK...md:178-180`), Step 2.3 drift branch fix (`TASK...md:182-184`), Step 2.5 GREEN/non-regression (`TASK...md:190-192`), PG.2 QA (`TASK...md:198-200`) | COVERED | The planned fix addresses same-ID material edits via a deterministic whitespace-normalized hash gate rather than a literal checkpoint/deliverable structural diff. This is conservative and directly closes the root defect, but see Gap G-2 for method variance against design §5. |
| F-2 — carry partial-work paths to operator; add CG-1 | Overview item 3 (`TASK...md:66`), objective 3 (`TASK...md:77`), Step 3.1 CG-1 RED (`TASK...md:206-208`), Step 3.3 model field (`TASK...md:214-216`), Step 3.4 integrity assignment independent of cleanup (`TASK...md:218-220`), Step 3.5 printer (`TASK...md:222-224`), Step 3.6 `--yes`/CI residual scoped out (`TASK...md:226-228`), Step 3.7 GREEN/non-regression (`TASK...md:230-232`), PG.3 QA (`TASK...md:238-240`) | COVERED | Option A is coherent: source currently drops `_detect_partial()` paths after surface/quarantine (`integrity.py:63-67`), and `BoundaryReport` currently lacks a partial path field (`models.py:84-101`). The task adds a report field and prints it. |
| F-4 — PHASE hard-crash prior-tail double-validation; add CG-3 | Overview item 4 (`TASK...md:67`), objective 4 (`TASK...md:78`), Phase 4 preface (`TASK...md:242-244`), Step 4.1 CG-3 RED + negative companion (`TASK...md:246-248`), Step 4.2 `BoundaryTask.phase` (`TASK...md:250-252`), Step 4.3 planner prior-tail emit, write-free (`TASK...md:254-256`), Step 4.4 integrity phase-correct transcript + deliverable lookup (`TASK...md:258-260`), Step 4.5 GREEN/no-writes (`TASK...md:262-264`), PG.4 QA (`TASK...md:274-276`) | COVERED | The task explicitly recognizes the multi-file co-dependency and the current vacuous path: planner emits no boundary task on PHASE/no-derived hard crash (`planner.py:158-169`) and integrity returns true when no last-completed task exists (`integrity.py:97-101`). |
| CG-4 — authoritative human ruling on §7 vs §4(c)/FR-2.4, gating F-1 | Overview item 1 (`TASK...md:64`), objective 1 (`TASK...md:75`), Step 1.3 decision record with both options and blank ruling (`TASK...md:154-156`), Step 1.4 ruling handoff/default (`TASK...md:158-160`), Step 1.5 conditional spec amendment and no unconditional F-1 code change (`TASK...md:162-164`), Open Questions (`TASK...md:334-342`) | PARTIAL | The task correctly avoids unconditional F-1 code changes, but Step 1.4 allows unattended auto-application of the recommended default if the operator leaves the ruling blank (`TASK...md:158-160`). The driving item requires an authoritative ruling, not an executor default (`REPORT.md:115-117`). |

## Per-item correctness and best-practice check

### F-3 — drift same-ID material edit

Current root cause is real: the drift assessor compares task IDs and, when recorded/current IDs match, returns `confidence=0.9` and `cosmetic_only=True` (`/config/workspace/IronClaude/.claude/worktrees/SprintReRun/src/superclaude/cli/sprint/resume/drift.py:177-187`) after only ID-removal/addition checks (`drift.py:142-175`). Tier 0 can miss because only exact normalized hash equality returns 1.0 (`drift.py:41-60`), and current `_recorded_sha()` reads only `tasklist_sha256` (`drift.py:267-281`). Existing AC-4/AC-5 tests cover trailing whitespace and completed-ID removal, not same-ID material content (`/config/workspace/IronClaude/.claude/worktrees/SprintReRun/tests/sprint/test_resume.py:239-275`).

The task's planned fix is technically sound for the root cause: it writes a new whitespace-normalized `tasklist_sha256_ws` in the real writer and test fixture (`TASK...md:178-180`), then only keeps 0.9/cosmetic when recorded/current WS hashes match; otherwise it returns `<0.8` (`TASK...md:182-184`). This avoids regressing AC-4 because Step 2.2 explicitly co-edits `_build_task_interrupted()` so the synthetic AC-4 fixture records the WS baseline (`TASK...md:178-180`), and Step 2.5 requires the full drift class including AC-4/AC-5 (`TASK...md:190-192`). It keeps the gate deterministic: the source's git tier is currently additive and never changes confidence (`drift.py:219-265`), and Step 2.3 explicitly forbids putting the decision in `_annotate_git` (`TASK...md:182-184`).

Caveat: design §5 calls for structural diff over task IDs + checkpoint paths + deliverable paths (`/config/workspace/IronClaude/.claude/worktrees/SprintReRun/.dev/brainstorms/20260602-sprint-auto-resume-default/design.md:212-218`). The task chooses a stricter WS-hash proof instead of literally composing `extract_checkpoint_paths`/deliverable diffs. This is safe but not an exact implementation of the driving wording.

### F-2 — partial-work paths to operator

Current code computes paths, then drops them on the default report-only path: `_detect_partial()` returns `list[Path]` (`integrity.py:134-173`), `run()` receives `partial_paths` and only surfaces a `BoundaryTask` or quarantines under opt-in (`integrity.py:63-67`), and `BoundaryReport` has no field for report-only paths (`models.py:84-101`). The printer currently prints suspects, coherence warnings, quarantine mappings, and blocking reasons, but no partial paths (`/config/workspace/IronClaude/.claude/worktrees/SprintReRun/src/superclaude/cli/sprint/commands.py:520-536`).

The task's chosen Option A is coherent and reaches the operator on report-only printed paths: add `BoundaryReport.partial_paths` (`TASK...md:214-216`), assign it inside `if partial_paths:` independently of `cleanup_opted_in` (`TASK...md:218-220`), and print it in `_print_resume_decision()` next to quarantine output (`TASK...md:222-224`). The dry-run path calls `_print_resume_decision()` (`commands.py:292-294`), and the interactive-confirm path also calls it before prompting (`commands.py:436-447`). The task correctly scopes out the `--yes`/CI path: current `assume_yes` returns `proceed` without printer output (`commands.py:436-471`), and Step 3.6 documents that residual as F-1/CG-4 rather than silently expanding scope (`TASK...md:226-228`).

### F-4 — PHASE hard-crash prior-tail validation

Current source matches the reflected defect. In planner hard-crash/pre-v4.3.0 with no derived transcript failures, `derived == []`, granularity stays PHASE, and boundary remains empty (`planner.py:158-169`). In integrity, no `last_completed` means `_validate_last_completed()` returns `(True, [], None)` (`integrity.py:97-101`), so the prior completed phase's tail is never checked. Current tests lock the old behavior by asserting `plan.boundary_tasks == []` on hard crash (`test_resume.py:139-156`) and only test no-writes separately (`test_resume.py:158-172`).

The task correctly treats F-4 as multi-file, not planner-only: add `BoundaryTask.phase` (`TASK...md:250-252`), emit one prior-tail `BoundaryTask` in the planner while threading/accessing `phases` without writes (`TASK...md:254-256`), and update integrity transcript and deliverable lookup to use the task's phase rather than `plan.interrupted_phase` (`TASK...md:258-260`). This is necessary because current transcript lookup uses `plan.interrupted_phase` (`integrity.py:112-114`) and declared-deliverable lookup uses the interrupted phase file (`integrity.py:120-124`). The task also adds a negative companion test proving validation can STOP (`TASK...md:246-248`), which is stronger than a positive-only test.

### CG-4 — human decision and F-1 conditionality

The task is correct that the spec conflict exists: design §4(c) requires `passed = validated_last and (no unresolved suspects) and (partial work quarantined or accepted)` (`design.md:184-187`), while design §7's happy path reports half-written outputs and still says `passed=True` (`design.md:292-296`). Merged FR-2.4 says resume must not proceed until half-finished work is cleaned or explicitly assessed-and-accepted and last completed is double-validated (`/config/workspace/IronClaude/.claude/worktrees/SprintReRun/.dev/brainstorms/20260602-sprint-auto-resume-default/merged-requirements.md:85-87`). Current source implements the §7-style verdict: `return accept_suspect or report.validated_last` (`integrity.py:306-314`).

The task correctly holds F-1 conditional: objective 1 says F-1 remediation is conditional and there is no unconditional gate change (`TASK...md:75`); Step 1.5 explicitly says do not implement `--accept-partial` unless directed (`TASK...md:162-164`); Step 3.6 documents the `--yes` residual instead of changing it (`TASK...md:226-228`); Open Questions repeat that F-1 has no unconditional code-fix item (`TASK...md:340-341`).

However, CG-4 is not fully handled as a human decision. Step 1.3 creates a decision record with a blank operator ruling (`TASK...md:154-156`), but Step 1.4 allows unattended execution to auto-apply the recommended default if the ruling is blank (`TASK...md:158-160`). That is not an authoritative human ruling, and it can drive spec amendments in Step 1.5 (`TASK...md:162-164`). This undercuts the driving requirement to “get an authoritative ruling” (`REPORT.md:115-117`).

## Best-practice compliance grade

**Grade: 4.0 / 5.0.**

Strengths:

- RED-then-GREEN discipline is explicit for CG-2 (`TASK...md:174-176`, `TASK...md:190-192`), CG-1 (`TASK...md:206-208`, `TASK...md:230-232`), and CG-3 including a negative companion (`TASK...md:246-248`, `TASK...md:262-264`).
- Per-phase QA gates exist for F-3/F-2/F-4 with adversarial stance and `fix_authorization: true` (`TASK...md:198-200`, `TASK...md:238-240`, `TASK...md:274-276`).
- Granularity is strong: each fix has separate test, code, spec amendment, lint, and QA items (`TASK...md:170-200`, `TASK...md:202-240`, `TASK...md:242-276`).
- Dependency ordering is correct: CG-4 first (`TASK...md:142-168`), then F-3, F-2, F-4; F-4 adds model phase field before planner/integrity (`TASK...md:250-260`).
- UV-only and sync discipline are explicit: source is pure Python, no `make sync-dev`, UV pytest and `make lint`, final `make verify-sync` (`TASK...md:138`, `TASK...md:282-288`).

Deductions:

- CG-4's unattended default is not an authoritative human decision (`TASK...md:158-160` vs `REPORT.md:115-117`).
- F-3 does not literally implement the design §5 checkpoint/deliverable structural composition (`design.md:212-218`), instead choosing a stricter WS-hash proof (`TASK...md:182-188`). This is safe but should be acknowledged as an approved design amendment, not just a code tactic.
- QA gates can be logged and marked complete if the agent cannot be spawned (`TASK...md:198-200`, `TASK...md:238-240`, `TASK...md:274-276`), which weakens “per-phase gate” strictness. [INFERRED] This may be a pragmatic task-runner fallback, but it should be explicit whether such a fallback blocks promotion.

## Gap registry

| ID | Severity | Item | Gap | Fix before execution |
|---|---:|---|---|---|
| G-1 | CRITICAL | CG-4 | Step 1.4 lets the executor auto-apply the recommended YES default when the operator ruling is blank (`TASK...md:158-160`). The driving report requires an authoritative ruling on CG-4 (`REPORT.md:115-117`), and the task can otherwise amend specs based on a non-human default (`TASK...md:162-164`). | Change Step 1.4 to STOP/BLOCK when `RULING:` is blank, with a required operator-filled YES/NO ruling before Step 1.5. If a default is desired, require explicit same-session/user authorization or label it non-authoritative and do not proceed to spec/code amendments. |
| G-2 | MINOR | F-3 | The task's algorithm is conservative and likely correct, but it does not literally “compose `extract_checkpoint_paths` + deliverable-path diff” as the report/design wording says (`REPORT.md:106-109`; `design.md:212-218`). It amends design toward WS-hash behavior instead (`TASK...md:186-188`). | In Step 2.4 and PG.2, explicitly record this as an intentional conservative design amendment/ruling: same-ID content changes are allowed only if WS-hash proves whitespace-only; checkpoint/deliverable structural diff remains optional/future. Alternatively add an explicit checkpoint/deliverable extraction comparison if the spec owner requires exact §5 behavior. |
| G-3 | IMPORTANT | QA/process | Per-phase rf-qa gate items allow “unable to spawn agent” to be logged and the item marked complete (`TASK...md:198-200`, `TASK...md:238-240`, `TASK...md:274-276`). For a corrective remediation driven by missed in-band gates, silently proceeding without the independent gate weakens the safety bar. | Amend PG.2/PG.3/PG.4 so inability to run the QA gate marks the phase/task blocked unless an explicit operator waiver is recorded. |
| G-4 | MINOR | F-4/tests | Step 4.1 adds tests that necessarily conflict with the existing reference test asserting `boundary_tasks == []` (`test_resume.py:139-156`). Step 4.5 permits reconciling that reference test (`TASK...md:262-264`), so this is covered but should be watched. | Ensure Step 4.5 requires updating the old assertion to the new expected prior-tail boundary task, not merely noting it, if the new behavior lands. |

## Verdict

**FAIL.** The tasklist is technically strong for F-3, F-2, and F-4, but it should not execute until CG-4 is changed from “auto-apply recommended default if blank” to a real authoritative human ruling/blocking gate. Otherwise the task can resolve the central spec contradiction without the decision the driving report explicitly requires.

**Confidence: 0.89.** High confidence on source-grounded fix surfaces and the CG-4 process gap; modest uncertainty only on whether the project convention intentionally permits unattended defaults to count as “operator” rulings.
