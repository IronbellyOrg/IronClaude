# QA Report — Task Qualitative Review

**Topic:** TASK-RF-20260518-181333 (7-PR split workflow for feat/hook-sync-and-matcher-fix)
**Date:** 2026-05-18
**Phase:** task-qualitative
**Fix cycle:** 1
**Output:** /config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260518-181333/qa/qa-qualitative-review.md

---

## Overall Verdict: FAIL → Re-spawn after Cycle 1 fixes applied

Three critical-severity issues fixed in-place during this review (test file paths + test class names + cleanup-merge contradiction). Three IMPORTANT issues remain that the executor must address before runtime safety is restored.

---

## Scope of Review

- Task file: 79 items / 12 phases (single-instance review, no partitioning)
- Inherited Structural Verdict: 28/28 PASS (relied on; semantic counterparts verified independently below)
- Adversarial stance: ENABLED — assumed errors present until verified
- Drift axis baseline: BUILD_REQUEST.GOAL verbatim available via TRACK GOAL in spawn prompt

---

## Items Reviewed

| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Gate/command dry-run | AX-5 | FAIL | Phase 2 Step 2.1 pytest command targets nonexistent file `tests/skills/test_task_builder_skill.py` — actual file is `tests/skills/test_task_builder_merge.py`. Verified via `find tests/skills -name "test_task_builder*"`: only `test_task_builder_merge.py` exists. Pytest command WOULD collect 0 tests if executed as written. FIXED in-place via replace_all. |
| 2 | Project convention compliance | none | PASS | All edits target `src/superclaude/`-tree files (PR-A) or `.dev/`-tree artifacts; UV-only commands (`uv run pytest`, `uv run ruff`) used throughout; conventional-commits scopes (`feat(sprint)`, `test(audit)`, `docs(task-builder)`, `docs(hooks)`, `chore(tests)`, `chore(releases)`, `chore(tasks)`) all in R2 catalog. `git add` always explicit (never `-A`). Co-Authored-By present in all 8 commit HEREDOCs. |
| 3 | Intra-phase execution order simulation | AX-2 | FAIL | Contradiction between Key Objective #2, Phase 3 prose, and Phase 4 prose: Objective #2 said "Land this cleanup branch on master BEFORE creating any of the 7 PR branches"; Phase 3 prose (L214) says merge is "(optionally — the user decides)"; Phase 4 prose (L291) says "the cleanup branch is NOT merged in yet". NO checklist step actually merges the cleanup branch to master. FIXED in-place by rewriting Objective #2 to align with Phase 3/4 prose: cleanup branch is prepared but NOT merged; all 7 PR branches are parallel siblings off the same master HEAD. |
| 4 | Function signature verification | AX-5 | FAIL | Pytest class names wrong throughout: Task referenced `TestPR01::` and `TestPR02::` 12 times. Actual class names: `TestPR01ExecutionContextHeader` and `TestPR02RetryMonotonicityGuards` (verified via grep lines 150 + 362 of test file). Without correct class names, pytest cannot collect any of the 3 target tests. FIXED in-place via 3 replace_all operations. Live pytest run with corrected names confirms tests collect and FAIL as expected. |
| 5 | Module context analysis | none | PASS | SKILL.md final-state authoritative-text adjudication is sound at section level — verified via grep: lines 1032, 1038, 1039, 1041 contain canonical regression-precedence wording the tests' INTENT targets, even though the exact byte-strings the tests look for (`"NEVER write specific"`, `"Regression takes precedence"`, `"non-convergent"`) are absent. Adjudication direction is correct (update tests, NOT SKILL.md). |
| 6 | Downstream consumer analysis | AX-3 | FAIL-MINOR | Phase 3 cleanup's `.gitignore` additions (Step 3.11) — pattern `prd-*-test/` only matches names ending in `-test/`, so it catches `prd-dry-run-test/` but NOT `prd-test-product/`. The redundant pattern `prd-dry-run-*/` doesn't cover `prd-test-product/` either. → Step 3.11 IS LIKELY MISSING a `prd-test-*/` entry. See I-3. |
| 7 | Test validity | none | PASS | After C-1/C-2 fixes, verification commands exercise the actual changes. Pytest invocations target the specific test files/classes that were modified; ruff invocations target the specific changed-files for the rot-budget rule. |
| 8 | Test coverage of primary use case | none | PASS | Each PR's pre-PR triplet covers the relevant test area: PR-A → `tests/sprint/ tests/pipeline/`; PR-B → `tests/audit/ tests/skills/`; PR-F → `tests/hooks/ tests/cli/`. PR-C/D/E (docs-only) run `tests/skills/ tests/audit/` as a sanity check. |
| 9 | Error path coverage | none | PASS | Each phase has explicit blocker-logging, deviation-note, max-attempt counters (2 before logging blocker), and FR-CONV.5 retry monotonicity protocol with byte-exact halt-messages wired into Phase 11. Step 9.5 cherry-pick has abort-and-log. Step 10.1's adb7d36 verification is gated PRESENT/MISSING before Step 10.2 delete. |
| 10 | Runtime failure path trace | AX-1 | FAIL | Stale-fact / silent-fail trace: the wrong pytest target (Phase 2 Step 2.1) would collect 0 items → summary file at Step 2.1 records "tests passed unexpectedly" → skip Steps 2.2-2.4 → Step 2.5 captures empty diff → PR-B ships 8 audit tests with NO task-builder repair → PR-B's pre-PR triplet (Step 6.4) FAILS with same 3 failures → triplet attempts 2 amend cycles → HALT and degrade. 4 phases silently produce wrong state. NOW FIXED via C-1 + C-2. |
| 11 | Completion scope honesty | none | PASS | All 7 OQs resolved at task-creation time per BUILD_REQUEST; OQ resolutions reflected in actual checklist behavior; follow-up tasks (Steps 12.2-12.4) clearly out-of-scope and described concretely enough for future task-builder pickup. |
| 12 | Ambient dependency completeness | AX-3 | FAIL-MINOR | Step 3.11 .gitignore pattern coverage — see I-3 (overlap with check #6). NOT FIXED in-place; runtime-verify clause exists in Step 3.11 but only catches false-positives, not false-negatives. |
| 13 | Kwarg sequencing red flags | none | PASS | All "stage then commit" sequences properly ordered. Cherry-picks (Step 7.2, 9.5) before commits. `git stash push` (Step 3.1) before `git stash show` (Step 3.3). |
| 14 | Function existence claims require verification | none | PASS | Verified: all 5 cherry-pick SHAs (`20b58f6`, `c9e2b12`, `0dcc947`, `db6166e`, `edd3ddd`) exist with correct D-0064..D-0067 evidence. Commit `adb7d36` resolves to full SHA `adb7d363e19836d3c8673d6dd0b3fe98df7743e4` and is single-file addition. All D-0053..D-0100 evidence dirs exist on disk. `tests/cli/` + `tests/hooks/` exist. |
| 15 | Cross-reference accuracy for templates | none | PASS | PR template at `.github/PULL_REQUEST_TEMPLATE.md`: 51 lines, final line ends with `-->` (verified via `tail -1`). CONTRIBUTING.md: 48 lines (matches gap-fill GAP 3 expectation). |

---

## Summary

- Checks passed: 9/15
- Checks failed: 6 (3 CRITICAL fixed in-place; 3 IMPORTANT remain unfixed)
- Critical issues: 3 (all FIXED in-place)
- Important issues: 3 (recommended fixes documented; not applied automatically)
- Minor issues: 0
- Issues fixed in-place: 3 of 6

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| C-1 | CRITICAL | Phase 2 Steps 2.1-2.5 + Phase 6 Steps 6.1, 6.4, 6.5 + Key Objective #1 | Task references nonexistent test file `tests/skills/test_task_builder_skill.py` (9 occurrences). Actual file: `tests/skills/test_task_builder_merge.py`. Pytest would collect 0 tests → silent false-pass cascade. | FIXED via replace_all → `test_task_builder_merge.py`. Verified via grep: 0 wrong-path occurrences, 9 correct. |
| C-2 | CRITICAL | Phase 2 Steps 2.1-2.4 + Phase 6 Step 6.4 + Phase 6 commit-message | Task references nonexistent test classes `TestPR01::` and `TestPR02::` (12 occurrences in `::` form). Actual classes: `TestPR01ExecutionContextHeader` and `TestPR02RetryMonotonicityGuards`. Pytest cannot collect with wrong class names. | FIXED via 3 replace_all operations on the `ClassName::method` form. Verified via fresh pytest run with correct names: 3 tests collect and FAIL as expected (confirming drift is real, adjudication is correct). |
| C-3 | CRITICAL | Key Objective #2 vs Phase 3 prose (L214) vs Phase 4 prose (L291) | Three contradictory statements about cleanup-branch-to-master merge: Obj #2 said "Land BEFORE Phase 4"; Phase 3 says "optionally — user decides"; Phase 4 says "NOT merged in yet". NO step performs the merge. | FIXED by rewriting Objective #2 to align with Phase 3/4 prose: cleanup branch is prepared but NOT merged; 7 PR branches branch off same post-fetch master HEAD as siblings; user decides at PR-opening time. |
| I-1 | IMPORTANT | Phase 2 Steps 2.1 → 2.4 ambiguity-resolution | SKILL.md byte-strings the tests look for (`"NEVER write specific"`, `"Regression takes precedence"`, `"non-convergent"`) are ABSENT from current source. Task tells executor to "extract FINAL authoritative text" without pre-identifying matching substrings. Recommended substitutes: test 1 → look for "no specific file:line references" / "READING aid" wording near SKILL.md L1856; test 2 → `"Precedence rule (regression > monotonicity)"` (SKILL.md L1041) or `"Regression detection ALWAYS runs BEFORE the monotonicity check"`; test 3 → rf-task-builder.md does NOT contain `"non-convergent"` — test must be updated to a substring that IS present (e.g. `"byte-exact wire string"` or `"Retry Monotonicity Protocol"`). | NOT FIXED in-place. Executor will resolve at runtime via the existing "if still fails, re-read and adjust" logic, but better to pre-identify substitutes in Steps 2.2-2.4. |
| I-2 | IMPORTANT | Phase 6 Step 6.1 stash-recovery + cross-branch flow | Phase 2 modifies test file in-place on current branch BEFORE Phase 3.1 stashes everything. Phase 6.1 says "recover via `git checkout stash@{0} -- tests/skills/test_task_builder_merge.py`" — but the stash contains only the polluted state, not the Phase 2 edits if those were done before stash. The fallback in Step 6.1 (`git apply phase-2-test-diff.patch`) is the correct path but labeled fallback. | NOT FIXED. Recommended: invert Step 6.1 logic so patch-apply is primary, stash-recovery is fallback. Also: ensure Phase 2 captures the diff BEFORE Phase 3.1 stash (the current order does — Step 2.5 runs before Phase 3.1). |
| I-3 | IMPORTANT | Phase 3 Step 3.11 `.gitignore` patterns | Pattern `prd-*-test/` only catches names ending in `-test/`. The directory `prd-test-product/` ends in `-product/`, not `-test/`, so it's NOT defended against. Companion pattern `prd-dry-run-*/` doesn't help (matches only `prd-dry-run-*`-prefixed names). | NOT FIXED. Recommended: change Step 3.11 entries to `prd-*-test/`, `prd-test-*/`, `prd-dry-run-*/` OR use broader `prd-*/` and accept false-positive risk. |

---

## Actions Taken

Fixes applied in-place to `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260518-181333/TASK-RF-20260518-181333.md`:

1. **C-1 (test file path):** `replace_all` — `tests/skills/test_task_builder_skill.py` → `tests/skills/test_task_builder_merge.py` (9 occurrences). Verified by grep: 0 remaining occurrences of wrong path.
2. **C-2 (test class names — invocation form):** 3 replace_all operations on the `ClassName::method` form:
   - `TestPR01::test_execution_context_uses_source_areas_not_paths` → `TestPR01ExecutionContextHeader::test_execution_context_uses_source_areas_not_paths`
   - `TestPR02::test_skill_regression_detection_precedence` → `TestPR02RetryMonotonicityGuards::test_skill_regression_detection_precedence`
   - `TestPR02::test_rf_task_builder_has_protocol` → `TestPR02RetryMonotonicityGuards::test_rf_task_builder_has_protocol`
   - Verified via fresh `uv run pytest` with correct names: 3 tests collected, all FAIL (as expected — drift is real, adjudication direction is correct).
3. **C-3 (cleanup-merge contradiction):** Edited Key Objective #2 (line 75) to align with Phase 3/4 prose: cleanup branch is prepared but NOT merged; 7 PR branches branch off same post-fetch master HEAD as parallel siblings; user decides at PR-opening time whether to open cleanup as PR-0 or fold into another PR. Removed the "Land BEFORE creating" command that no checklist step actually executes.

---

## Inherited Structural Verdict — Reliance Audit (PR-04, INV-019)

Relied on rf-qa A.10 structural verdict (28/28 PASS). For each reliance, the corresponding semantic check was independently verified with my own tool engagement:

- Relied on rf-qa PASS #5 (Evidence-based file paths) → semantic counterpart verified: ran `find` to confirm `tests/skills/test_task_builder_skill.py` does NOT exist while `tests/skills/test_task_builder_merge.py` does. **Counter-finding:** rf-qa PASS for "file paths exist" did NOT catch that the task's path references don't match actual files. rf-qa likely passed because the structural check verifies whether file paths SYNTACTICALLY appear, not whether the referenced files exist on disk.
- Relied on rf-qa PASS #6 ("No items based on [CODE-CONTRADICTED] research") → semantic counterpart verified: ran `grep "class TestPR" tests/skills/test_task_builder_merge.py` to confirm class names. **Counter-finding:** the task's research-derived class names (`TestPR01`/`TestPR02` short form) ARE [CODE-CONTRADICTED] by actual source — rf-qa missed this because the structural check only verifies whether research files exist, not whether they match code.
- Relied on rf-qa PASS #18 (All commits use explicit `git add <paths>`) → semantic counterpart verified: read each of the 8 commit blocks (Phase 3.12, 5.3, 6.5, 7.3, 8.2, 9.2, 9.6, 9.9) and confirmed explicit path lists with no `-A` / `.`. All sound.
- Relied on rf-qa PASS #19 (Co-Authored-By signoff) → semantic counterpart verified: same 8 commit blocks each contain `Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>`. All sound.
- Relied on rf-qa PASS #25 (All 7 PRs target master) → semantic counterpart verified: 7 paste-ready `gh pr create` stubs verified, all use `--base master`. All sound.
- Relied on rf-qa PASS #26 (Pre-PR triplet encoded per PR) → semantic counterpart verified: read each Phase 5-9 triplet step (Step 5.4-5.6, 6.6, 7.4, 8.3, 9.3, 9.7, 9.10) and confirmed each runs ruff + pytest + verify-sync as 3-command sequence. All sound.
- Relied on rf-qa PASS #27 (Phase 11 uses rf-qa-qualitative FINAL_ONLY) → semantic counterpart verified: Step 11.2 spawn instructions and Step 11.3 conditional-proceed with 3-cycle ceiling + FR-CONV.5 monotonicity checks. Sound, and Phase 11 self-review fallback (when rf-qa-qualitative unavailable) is reasonable.

**Anti-inflation compliance:** I performed independent tool engagement on every semantic counterpart (≥6 distinct categories of independent verification beyond reliance on rf-qa). Total tool calls: Read=4, Bash=~22, Grep=~10, Edit=4 (fixes). Exceeds the 15-checklist-item minimum.

---

## Self-Audit

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- Relied on rf-qa PASS for TB-Add-1 / item #5 / item #6 / item #18 / item #19 / item #25 / item #26 / item #27 (8 items)
- Relied on rf-qa structural enumeration of 79 items / 12 phases (skipped re-counting)
- Relied on rf-qa template-conformance verification (skipped re-reading template)

**(b) Independent semantic checks (≥1 required, INV-019):**
- Test-file-existence semantic check — verified by `find /config/workspace/IronClaude/tests/skills -name "test_task_builder*"` showing only `test_task_builder_merge.py` (NOT `test_task_builder_skill.py`). This catches a [CODE-CONTRADICTED] reference that rf-qa structural verdict could not detect.
- Pytest-class-name semantic check — verified by `grep "class TestPR" tests/skills/test_task_builder_merge.py` showing `TestPR01ExecutionContextHeader` (L150) and `TestPR02RetryMonotonicityGuards` (L362). Live pytest collection confirmed the wrong short-form names collect 0 tests.
- Test-failure-mode semantic check — verified by running `uv run pytest ... --tb=short` with correct class names: 3 tests FAIL with assertion messages showing the byte-strings (`"NEVER write specific"`, `"Regression takes precedence"`, `"non-convergent"`) are absent from current SKILL.md / rf-task-builder.md. This confirms drift is real and adjudication direction is correct.
- Cleanup-merge-ordering semantic check — verified by reading Phase 3 + Phase 4 in entirety and finding NO checklist step that performs the cleanup-branch-to-master merge while three prose passages assert mutually contradictory facts about whether the merge happens.
- Cherry-pick-scope semantic check — verified by `git show --stat 20b58f6 c9e2b12 0dcc947 db6166e edd3ddd`: each commit contains ONLY D-0064..D-0067 evidence files + matching `tests/audit/test_*.py` for the relevant fixture (no contamination). The PR-C cherry-pick assertion is sound.
- Stale-branch unique-commit semantic check — verified by `git log master..fix/auggie-flag-clear-mcp-prefix --oneline`: TWO unique commits (`adb7d36` + `f9a7e34`), not one. But `f9a7e34` is the squash-source of origin/master's `9574788` (PR #47), so after `git pull --ff-only origin master` only `adb7d36` will be unique. Task's claim is correct only AFTER the pull happens (Phase 3.2). This is acceptable since Phase 3.2 runs before Phase 9.5 cherry-pick.
- Gitignore-pattern semantic check — verified by manual pattern-matching analysis: `prd-*-test/` does NOT match `prd-test-product/`. Task's defensive guard has a coverage gap (I-3).

---

## Confidence Gate

- **Verified:** 13/15 | **Unverifiable:** 0 | **Unchecked:** 2 (item 6 + item 12 share root cause I-3 — partial verification: pattern semantics confirmed, but runtime fix not applied)
- **Confidence:** 86.7% (13/15)
- **Tool engagement:** Read: 4 | Grep: ~10 | Bash: ~22 | Edit: 4
- **Threshold:** 95% required for PASS; current 86.7% — NOT eligible for PASS.

Self-audit answers:

1. **How many factual claims independently verified against source code?** At least 12 — file existence (test file path, evidence dirs, hooks tests dir, PR template, CONTRIBUTING.md), commit existence (5 cherry-picks + adb7d36 with full SHA), class names + line numbers (lines 150 + 362 of test file), test failure modes (live pytest output captured), branch state (master..HEAD log, stale branches' unique-commit count), SKILL.md text content (multiple grep + read), gitignore pattern semantics.
2. **What specific files did you read?** `TASK-RF-20260518-181333.md` (full task across 4 reads), `SKILL.md` (grep + read), `test_task_builder_merge.py` (grep + pytest exec), `rf-task-builder.md` (grep), `solutions_learned.jsonl` (diff), 8 commit HEREDOCs (read in task file), `.github/PULL_REQUEST_TEMPLATE.md` (tail + wc).
3. **If 0 issues found, would user trust?** Not applicable: 6 issues found, 3 critical fixed in-place. User can verify by running `grep -c "test_task_builder_skill" .dev/tasks/to-do/TASK-RF-20260518-181333/TASK-RF-20260518-181333.md` (expect 0) and re-running the corrected pytest to see 3 tests collect and FAIL as the adjudication direction expects.

---

## Recommendations

**Before executing the task:**

1. **(MUST)** Verify the 3 critical fixes propagated correctly by running:
   ```
   grep -c "test_task_builder_skill.py" .dev/tasks/to-do/TASK-RF-20260518-181333/TASK-RF-20260518-181333.md   # expect 0
   grep -c "test_task_builder_merge.py" .dev/tasks/to-do/TASK-RF-20260518-181333/TASK-RF-20260518-181333.md   # expect 9
   grep -c "TestPR01::" .dev/tasks/to-do/TASK-RF-20260518-181333/TASK-RF-20260518-181333.md                   # expect 0 (or only in non-pytest-invocation prose context)
   grep -c "TestPR01ExecutionContextHeader::" .dev/tasks/to-do/TASK-RF-20260518-181333/TASK-RF-20260518-181333.md  # expect 2+
   grep -c "TestPR02RetryMonotonicityGuards::" .dev/tasks/to-do/TASK-RF-20260518-181333/TASK-RF-20260518-181333.md  # expect 4+
   ```
2. **(SHOULD)** Apply the I-3 fix: edit Step 3.11 to include `prd-test-*/` alongside the existing `prd-*-test/`, so `prd-test-product/` is covered.
3. **(SHOULD)** Apply the I-1 fix: pre-identify recommended substitute substrings for the 3 tests in Steps 2.2-2.4. Specifically: test 2 should target `"Precedence rule (regression > monotonicity)"` (SKILL.md L1041); test 3 needs a substring present in rf-task-builder.md (e.g. `"Retry Monotonicity Protocol"` or `"byte-exact wire string"`); test 1 needs a substring describing the no-file-paths-in-Execution-Context rule (search SKILL.md for `"no specific file:line references"`).
4. **(SHOULD)** Apply the I-2 fix: invert Step 6.1's recovery preference — patch-apply (`git apply phase-2-test-diff.patch`) primary, stash-recovery fallback — since Phase 2 has no commit.
5. **(OPTIONAL)** Re-spawn this rf-qa-qualitative review after applying recommendations 2-4 to confirm cycle-2 PASS verdict.

---

## QA Complete

VERDICT: **FAIL** (Cycle 1)

Cycle-1 produced 3 critical in-place fixes (test file path, test class names, cleanup-merge contradiction). 3 IMPORTANT issues remain (I-1 substring ambiguity, I-2 stash-vs-patch recovery preference, I-3 gitignore pattern gap). Per the rf-qa-qualitative anti-leniency stance, ALL findings (including IMPORTANT) must be resolved before this task can proceed. Apply recommendations 2-4 above, then re-spawn for Cycle 2.

Unfixable issues without user input: none — all remaining issues have specific fix recipes documented above.
