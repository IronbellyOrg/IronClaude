# Round 1: Variant 3 Advocate (opus:refactorer)
<!-- Returned by a read-only advocate agent; persisted verbatim by the orchestrator (trailing DONE/NEXT table omitted). -->

## Position summary
Variant 3 is the only card that shows Task 2 cannot be carried out as written. Its regression test crashes on import, three of its four "fail-before" tests fail only because `master_checkout` does not exist yet, and its failure path can send errors to the wrong place. Two of those three problems are confirmed by the orchestrator's probes (shell evidence sections 5 and 6). Variant 3 is weak on deviation coverage and on a few low-value findings, and I concede those.

## Steelman

### Variant 1 (sonnet/analyzer)
Its strongest argument is scope discipline combined with precise checks. R1-6 is right that source.md:1 limits the tightening to CLAUDE.md, so the pr-submit scripts (poll-ci-checks.sh:34-35) are not plan defects. R1-3 finds a real inconsistency between tasks: plan:88 bans Orca link flags unconditionally, while plan:111 bans them only until the project id changes. R1-4 names CLAUDE.md:70 ("explicit `--repo` on every invocation"), a kept sentence that contradicts the positional `gh repo view` form. Variant 1 also uses the rubric's own labels correctly and maps every deviation, D-001 to D-014, to a plan location.

### Variant 2 (haiku-slot/qa)
Its strongest argument is that evidence must be checkable after the fact. R2-F1 is the most valuable finding in the set: the D-008 rerun at plan:176 produces no artifact, and plan:170 records `is-shallow`/`id -u` for only one checkout, so an executor could claim a clean rerun with no proof. Variant 2 also reproduced both search baselines independently (108 lines in 17 files; 9 lines in 7 files) and justified "no missing requirements" span by span.

## Strengths claimed
1. **Executability (R3-F1, R3-F2, R3-F3).** R3-F1 is confirmed by section 5. R3-F2 shows the fail-before check proves nothing: three of the four tests at plan:68-71 target `master_checkout()` or grep the source, so they fail before the change only because the function is missing. The global-setup path at plan:64, the `run_global(run_id, checkout)` signature and the E2E block (eval_runner.py:294-300) are never exercised.
2. **Failure-path design (R3-F3).** `subprocess.run(..., timeout=120)` at eval_runner.py:70 raises `TimeoutExpired` from inside the `with` body. Because plan:64 names no exception type, a broad `except` would report a pytest timeout as a "global-setup" failure. Variant 3 is the only card that names this mis-reporting. Its fix (a dedicated `MasterCheckoutError`, and `try/finally` around the `yield` only) is a specification the executor can follow directly.
3. **Self-contradiction in the CLAUDE.md check (R3-F4).** CLAUDE.md:50 contains `gh pr create --repo <repo>`, a placeholder rather than `IronbellyOrg/IronClaude`. That line fails plan:117's criterion, while plan:113 says to keep it.
4. **Vacuous diff checks (R3-F5, U-006 High).** Plain `git diff`, used at plan:119, :148 and :178, compares the working tree with the index. Once files are staged (plan:29, :179), the diff is empty, so these checks pass whatever was changed.

## Weaknesses identified in other variants
1. Variant 1 marks D-001 "resolved: yes" while its own R1-1 shows Task 2's test cannot load. Those two positions contradict each other. It also misses C-003 entirely.
2. Variant 1's R1-2 rates the failure path low, but it covers only the leaked empty directory. It misses the body-exception mis-reporting described in strength 2.
3. Variant 2 misses C-001, which blocks every Task 2 test and was later confirmed by the probe. It accepts T1 S1 without dispute despite that.
4. R2-F3's premise was refuted: the 22:23Z probe found no leaked `IronClaude-eval-master` checkout.

## Concessions
- **R3-F1's label.** "Necessary" is outside the rubric; it should be **drift**, as Variant 1 has it.
- **R3-F6, R3-F7, R3-F8 are weak.** R3-F6 rests on an inferred file match. R3-F7 assumes the executor ignores "a commit on `master`" (plan:67). R3-F8's grep would probably pass, since ruff keeps a short list literal on one line.
- **R3-F9** largely restates R2-F2's exit-code half.
- **Missing coverage section.** Variant 3 has no deviation-resolution or missing-requirements section. That is a real coverage gap; Variants 1 and 2 cover it.
- **Severity of R3-F4.** On the scripts half I concede the scope point. The fix is to word the CLAUDE.md "allowed forms" list so it covers only commands the agent types itself, not to edit the scripts.
- **Merge recommendation.** Variant 1's R1-4 and R1-5 should be merged into C-004.

## Per-point positions

| Point | Preferred | Reason |
|---|---|---|
| S-001 | V2 | Independent count reproduction plus span-by-span mapping is the strongest coverage evidence; Variant 3 has none. |
| S-002 | V3 | More confirmed, executable findings, although R3-F6 to R3-F8 dilute them. |
| S-003 | V3 | Its dispute of S1 rests on two confirmed probes; Variant 1's dispute of F1 is also valid. |
| C-001 | V3 (with V1's label) | It names the exact wrong failure string the fail-before run must not show. |
| C-002 | V3 | Only Variant 3 catches the timeout being mis-reported as global-setup (eval_runner.py:70). |
| C-003 | V3 | It covers vacuous fail-before tests, the `main()` wiring and the exit code; Variant 2's version is a subset. |
| C-004 | V3, merged with V1 R1-4 and R1-5 | CLAUDE.md:50 mechanically fails plan:117; Variant 1 adds the :70 conflict and a better grep. |
| X-001 | V1 on scope, V3 on CLAUDE.md:50 | The scripts are out of scope; the contradiction inside CLAUDE.md is in scope. |
| X-002 | V3 | Task 2 is not executable as written (sections 5 and 6). |
| X-003 | V1 | "Drift" is a rubric label; "necessary" is not. |
| X-004 | V3 (medium) | Mis-reporting body errors produces false results, which is more than a leaked directory. |
| X-005 | V3 (medium) | Plan:64's "do not fail silently" has no test, and the fail-before check is vacuous. |

## Shared assumptions
- **A-001: QUALIFY.** Local `master` exists (d953b983), but in an Orca worktree it can lag `origin/master`. The plan should say that using local `master` deliberately keeps the script's existing behaviour.
- **A-003: ACCEPT.** Section 5 shows the registered load succeeds without running git or writing files.
- **A-004: ACCEPT.** pyproject.toml:108-109 (`testpaths = ["tests"]`, `test_*.py`) collects `tests/unit/`.
- **A-006: QUALIFY.** No test pins the fork-rule sentences (`tests/pr_submit/` does not mention CLAUDE.md). The `.dev/worktrees` mentions in tests are Search A hits that Task 8 must classify, so they are tracked rather than pinned.
