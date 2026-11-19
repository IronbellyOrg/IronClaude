```yaml
contract_version: 1.8.0
status: partial
mode: pre
tier_reached: 2
confidence_calibrated: 0.82
citations_total: 37                  # counting rule: each distinct cited range (30 file:line, 2 logs, 5 process files)
citations_revalidated: 37
citations_dropped: 0
citations_inferred: 3
citation_budget_policy: full_reread
coverage_degraded: parsed-sparse
```

# Reflect report (pre-execution, Tier 2): make install_core use the cache-safe same_content

**Spec**: `.dev/tasks/done/TASK-WF-makeInstallCoreS-20261119-013812/source.md` | **Tasklist**: `.dev/tasks/done/TASK-WF-makeInstallCoreS-20261119-013812/TASK-WF-makeInstallCoreS-20261119-013812.md`
**Run**: `--mode pre --depth deep`; second opinion on the Tier 1 run in `.dev/reflect/pre-makeInstallCoreS-20261119013914/REPORT.md` (partial, calibrated 0.79).
**Verdict**: accept the plan and its implementation. No blocking finding. One optional readability fix and four MEDIUM leads for follow-up.

## Why partial

- Wave 1D (blind calibration of the Tier 1 card) was not re-run in this run, because `--depth deep` forces Tier 2 regardless; the Tier 1 calibration of 0.79 comes from the first run. A required protocol step was skipped, so the status is partial.
- The calibrated confidence in the header, 0.82, is the mean of the two reviewer-card calibrations (0.88 and 0.75). Each card was scored by an independent calibrator; the merged card itself was not re-calibrated.
- Diversity and identity gaps are listed under Grounding Gaps.

## Tier 2 process

| Step | Result |
|---|---|
| Reviewers | 2: reviewer 1 analyzer (opus-class alias), reviewer 2 qa (haiku-class alias). Three were not possible: this session runs as the sonnet-class alias, which is excluded as the executor class, and no fourth class is available |
| Blind calibration | Reviewer 1: 0.88 (STOP). Reviewer 2: 0.75 (ESCALATE). 32 of 32 reviewer citations checked by the calibrators, 0 failed (`reviewer-cards/reviewer-1-calibration.md`, `reviewer-cards/reviewer-2-calibration.md`) |
| Adversarial merge | `sc-adversarial-protocol` Mode A, `--depth standard`: Round 1, Round 2 and the Round 2.5 invariant probe. Convergence 9 of 9 diff points (threshold 0.80). Base: Variant 1 (combined 0.961 against 0.822; tiebreaker not needed). 10 of 10 planned changes applied, 7 of 7 references resolved, no new contradiction (`adversarial/merge-log.md`) |
| Invariant probe | 14 findings: 8 addressed, 6 unaddressed (0 HIGH, 4 MEDIUM, 2 LOW). No HIGH unaddressed, so convergence was not blocked (`adversarial/invariant-probe.md`) |
| Input drift | None. The five input file hashes match the snapshot (`artifacts/input-snapshot.yaml`) |

## Inferred requirements (Pass 2)

| INF id | Verbatim quote (source.md line 1) | Citation | Match result |
|---|---|---|---|
| INF-001 | "Make install_core._same_content use the fixed install_keep.same_content" | `.dev/tasks/done/TASK-WF-makeInstallCoreS-20261119-013812/source.md:1` | Task 1 |
| INF-002 | "so it no longer answers from filecmp's stale cache" | same | Task 1, Task 2 |
| INF-003 | "a test in tests/cli for install_core" | same | Task 2 |
| INF-004 | "a same-size same-mtime rewrite is reported as different by install_core" | same | Task 2 |
| INF-005 | "existing tests/cli -k install stay green" | same | Task 1 |

Union coverage 5 of 5 = 1.00; parsed coverage null (the spec is one unlabelled prose line), so `coverage_degraded: parsed-sparse` stays set.

## Findings

All findings come from the merged card (`merged-reflection-card.md`); the line numbers below are against today's files, since the plan has been implemented.

### Minor (optional, non-blocking)

- **The new test fails unreadably without the fix.** With the old behaviour the "NOT updated" section is not printed, so `message.split("NOT updated")[1]` raises `IndexError` instead of an assertion failure. The plan itself prescribes that expression (`.dev/tasks/done/TASK-WF-makeInstallCoreS-20261119-013812/TASK-WF-makeInstallCoreS-20261119-013812.md:36`), the log shows it (`.dev/tasks/done/TASK-WF-makeInstallCoreS-20261119-013812/artifacts/t2-checks.log:8-10`), and the older test uses the same pattern (`tests/cli/test_how_we_work_install.py:113`, new test `:134`). The bug is still detected; only the message is poor.

### Notes

- Bare line numbers in Task 1 drift once edits start (`.dev/tasks/done/TASK-WF-makeInstallCoreS-20261119-013812/TASK-WF-makeInstallCoreS-20261119-013812.md:26`); each comes with a symbol name, so no wrong edit is possible.
- "Different bytes of the same length" is left open (`.dev/tasks/done/TASK-WF-makeInstallCoreS-20261119-013812/TASK-WF-makeInstallCoreS-20261119-013812.md:36`); the test flips the first byte (`tests/cli/test_how_we_work_install.py:128`), which is valid while the shipped `PRINCIPLES.md` is non-empty; nothing guards that.
- The new relative import sits in its own block (`src/superclaude/cli/install_core.py:8-12`); ruff is clean (`.dev/tasks/done/TASK-WF-makeInstallCoreS-20261119-013812/artifacts/t2-checks.log:5-6`).
- `same_content` clears the process-wide cache on every call (`src/superclaude/cli/install_keep.py:20-22`): a speed cost only.
- Switching to the shared function does not change behaviour on unreadable files (`src/superclaude/cli/install_keep.py:23-26`).
- A lead only: `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` calls `filecmp.cmp(..., shallow=False)` without clearing the cache (lines 480, 500, 1682). The advocate check found line 500 follows `shutil.copyfile` (line 499), so no stale hit is expected there. [INFERRED] Whether a caller runs the two functions twice in one process was not checked.

### MEDIUM, carried over from the invariant probe (not raised by either reviewer)

- **INV-001.** `filecmp.cmp` empties its whole cache once it holds more than 100 entries (re-checked against the installed Python source). The second call in the new test compares 8 files that sort before `PRINCIPLES.md` (`src/superclaude/cli/install_core.py:59` the glob, `:71-73` the skip, `:97-99` the compare). In a long process with a full cache, the purge could hide the old bug; the supplied failing run executed only this test (`.dev/tasks/done/TASK-WF-makeInstallCoreS-20261119-013812/artifacts/t2-checks.log:7`).
- **INV-002.** The new test ignores its first call's result (`tests/cli/test_how_we_work_install.py:125`) and never checks that size and mtime still match `before` after the rewrite (`:128-129`); if the setup stops priming the cache, the test passes without testing anything.
- **INV-003.** No shipped CLI path compares the same pair twice in one process (`src/superclaude/cli/main.py:178` once; `update` forces at `:365`, which copies without comparing, `src/superclaude/cli/install_core.py:71-77`). The bug is reachable only in-process; this changes priority, not correctness. [INFERRED] from the call sites read; no other caller outside `src/superclaude/cli` was enumerated.
- **INV-008 (outside this plan).** `src/superclaude/cli/install_keep.py:3-7` says `install --force` and `update` back up a differing file first; `src/superclaude/cli/install_core.py:71-77` copies with `shutil.copy2` and no backup, so `update` overwrites a user-edited core file with no copy kept (re-checked: `src/superclaude/cli/install_commands.py:68` and `src/superclaude/cli/install_user_setup.py:95` do back up; `src/superclaude/cli/install_agents.py:56` and `src/superclaude/cli/install_templates.py:76` do not).

## Deviation classification

No deviation: the plan matches its source (none of Authorized, Necessary, Drift or Regression applies in a pre-execution review).

## Grounding Gaps

- Executor class: `EXECUTOR_MODEL_CLASS` and `--executor-model` were unset; the executor was taken from the session's own model (sonnet-class alias), so `executor_class_source` is unknown/heuristic and the anti-self-confirmation guarantee is weakened. The calibrators also ran on the sonnet-class alias, so executor and calibrator are not disjoint.
- Vendor diversity: all three aliases are `claude-gw-*` (`t2_vendor_diversity: single`, warn-only). Reviewer 2's alias reported itself as "GPT-5" in its self-report, which does not match the pinned alias, so reviewer identity could not be verified (`identity_mismatch_suspected: true`). The recorded class is the pin, not the self-report.
- Only two reviewers could be fielded (the usual three were not possible), so `panel_shortfall` does not apply but ensemble width is the minimum.
- Convergence caveat: the second advocate reversed three positions in one round; the fault-finder judged one (C-003) mild deference on a low-stakes ranking. Both advocates shared the frame of the diff analysis, which is why the four MEDIUM items above came from the probe and not the debate.
- Nothing was executed by this run: the test pass counts and the failing negative control are supplied evidence (`.dev/tasks/done/TASK-WF-makeInstallCoreS-20261119-013812/artifacts/t1-checks.log`, `.dev/tasks/done/TASK-WF-makeInstallCoreS-20261119-013812/artifacts/t2-checks.log`); the throwaway plugin was not saved. The one skipped test is unidentified.
- The input tree hash is a text hash over the five file hashes, not the canonical JSON serialization the protocol names; drift was checked file by file.
- Memory persist (Wave 5, `docs/memory/reflect/deviation-patterns-IronClaude.md`) was not run, to avoid adding a change to a tracked file on this branch.

## Inferred-claim audit

- `citations_inferred: 3`
- Inferred-fraction: 3 / 37 = 0.08

## Recommendations

### Recommendation R-001: Make the new test fail readably (optional)

- **File:** `tests/cli/test_how_we_work_install.py`
- **Change:** add `assert "NOT updated" in message, message` before line 134 (minimum), and before line 113 for consistency.
- **Verifier:** `uv run pytest tests/cli/test_how_we_work_install.py -q` passes; with `filecmp.clear_cache` disabled the new test fails with the assertion message, not an `IndexError`.
- **Linked deviation(s):** none (proactive)
- **Priority:** P2

### Recommendation R-002: Check that the new test can fail in a long run (optional)

- **File:** `tests/cli/test_how_we_work_install.py`
- **Change:** have the test assert the first call listed no stale file and that size and mtime match `before` after the rewrite (INV-002); separately try the test late in a full run with the fix reverted (INV-001).
- **Verifier:** the test still passes with the fix and fails with `filecmp.clear_cache` disabled, in both a single-test run and a full `tests/cli` run.
- **Linked deviation(s):** none (proactive)
- **Priority:** P2

### Recommendation R-003: Decide whether the core installer should back up edited files (separate issue)

- **File:** `src/superclaude/cli/install_core.py`
- **Change:** decide whether `install_core_files(force=True)` should call `backup_if_differs` like `install_commands.py` and `install_user_setup.py` (INV-008); out of scope for this plan.
- **Verifier:** a test that overwrites a user-edited core file with `force=True` and finds a `.bak.<stamp>` copy next to it.
- **Linked deviation(s):** none (proactive)
- **Priority:** P2

## Validator notes

- Evidence validator (agent): 37 citations, 37 verified, 0 dropped (`evidence-validation.md`). A zero-drop pass is an audit flag, not a clean signal; two places a reviewer could still push back: the claim that behaviour on unreadable files is unchanged (the old function was deleted by the implementation; it is quoted in `.dev/tasks/done/TASK-WF-makeInstallCoreS-20261119-013812/artifacts/retries/T1/prompt-1-1.md:30-34`), and the process figures taken from the merge log and probe, which the validator did not re-read.
- The report stays `partial` for the protocol reasons under "Why partial" and "Grounding Gaps", not because of citations.
