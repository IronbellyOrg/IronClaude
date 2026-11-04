# Round 1: Variant 1 Advocate (sonnet:analyzer)
<!-- Returned by a read-only advocate agent; persisted verbatim by the orchestrator. -->

## Position summary

Variant 1 is the best calibrated and the only card that checks spec coverage D-001..D-014 and disputes the Tier 1 card against `source.md` scope. Variant 3 beats it on breadth: the unwired `main()` path, error-catch scope, `git diff` vs `git diff HEAD`, and the `CLAUDE.md:50` conflict. I recommend merging V1's classification discipline and coverage table with V3's Task 2 and Task 4 findings and V2's R2-F1.

## Steelman

### Variant 2
Its strongest argument is R2-F1: Task 8's conditional rerun (plan:176) names no artifact and no way to get a full-depth, non-root checkout, so the D-008 rerun can't be checked after the fact. That is a real acceptance-criterion hole. V2 also independently reproduced Search A (108 lines, 17 files) and Search B (9 lines, 7 files), and its `missing_requirements: []` is backed by a span-by-span walk of `source.md`. R2-F2 correctly spots that the plan:64 `global-setup` path has no test.

### Variant 3
Its strongest argument is that Task 2 is not executable as written. R3-F1 is confirmed by shell evidence section 5, and the plan's fail-before check (plan:74) is vacuous for the `main()` wiring. R3-F3 also makes a point I missed: a broad `except` around the whole `with` block would relabel a 120 s pytest timeout (`eval_runner.py:70`) as `global-setup`. R3-F5 is right that plain `git diff` is blind to staged changes. R3-F4 is right that `CLAUDE.md:50` says `gh pr create --repo <repo>`, which fails the literal plan:117 criterion while plan:113 says to keep that sentence.

## Strengths claimed

1. Coverage traceability: `deviations_resolution` maps all 14 deviations to plan locations. V3 has no equivalent, and V2's mapping is only a prose justification (U-002).
2. Confirmed findings: R1-1 (import crash) and R1-2 (`git worktree remove` on an unregistered mkdtemp exits 128, directory stays) are both confirmed by shell evidence sections 5 and 6.
3. Scoped findings on Task 4: R1-4 names `CLAUDE.md:70`, which says "explicit `--repo` on every invocation". I re-read it and it contradicts the positional `gh repo view` form that plan:110 allows. R1-5 is also correct, because `grep -n 'gh '` matches words like "through".
4. Taxonomy discipline: R1-6 and the F3 dispute use `authorized` where `source.md:1` scopes the work to `CLAUDE.md` and tells the plan to decide the `#419` link. The plan's scope is stated at `source.md:1` and the guarded fallback is at `poll-ci-checks.sh:34-35`.
5. U-001 is unique to V1: Task 3 (plan:88) bans Orca link flags unconditionally, while Task 4 (plan:111) lifts the ban once the project id changes. The plan gives two different strengths for one rule.

## Weaknesses identified in other variants

1. V3 R3-F1 is classified `necessary`. That category means a justified departure from spec, and here the plan defect departs from no spec. The diff analysis (X-003) itself notes the label falls outside the rubric. `drift` is closer.
2. V3 R3-F4 overreaches. The pr-submit fallbacks run only after the `origin` lookup returns nothing (evidence section 4; `poll-ci-checks.sh:34-35`), and `source.md:1` scopes the work to `CLAUDE.md`. The `CLAUDE.md:50` placeholder point is valid, but the "contradicts the scripts" part is not a medium finding.
3. V3 severity is inflated: 5 of 9 findings are medium. R3-F7 (`init.defaultBranch`, git identity) and R3-F8 (grep formatting) are conjecture with no failing run, and the `.venv` removal claim is `[INFERRED]` only.
4. V2's R2-F3 rests on a premise the orchestrator refuted: no `IronClaude-eval-master` worktree exists on this host. V2 missed the import crash, and its card has no dispute of any Tier 1 finding, so it checked fewer claims.

## Concessions

- V3 is right on C-003 and X-005. The plan:64 `global-setup` path and the `main()` wiring are untested, and I missed both. I also missed R3-F9, that a global-setup failure still exits 0 (`eval_runner.py:313`).
- I missed U-003 (V2's R2-F1) and U-006 (V3's R3-F5).
- My "resolved: yes" for D-001 sits awkwardly beside R1-1, since the test description cannot run as written.
- R1-2 at low understates the broad-`except` risk that V3 found.

## Per-point positions

| Point | Preferred | Reason |
|---|---|---|
| S-001 | V1 | The 14-row mapping is checkable. V2's independent reproduction of the search baselines complements it. |
| S-002 | V3 | It found more real defects. V1 is better calibrated. |
| S-003 | V1 on F1/F3, V3 on S1 | F1 is out of scope per `source.md:1`. S1 is not executable once R1-1 is confirmed. |
| C-001 | Tie, V1 label | The content is identical. `drift` is closer than `necessary`. |
| C-002 | V3 | A typed error plus a narrow catch fixes the misreport hazard that V1 omits. |
| C-003 | V3 | It tests the unwired `main()` path and the exit code. |
| C-004 | Merge | V1 for `CLAUDE.md:70` and `grep -w`. V3 for the `CLAUDE.md:50` placeholder. Scripts out of scope. |
| X-001 | V1 | The fallbacks are guarded and outside the `CLAUDE.md` scope. Add one clarifying sentence. |
| X-002 | V3 | The text as written would fail at import. The fix is one line. |
| X-003 | V1 | `drift`. |
| X-004 | V3, qualified | Medium holds only because of the catch scope. The temp-dir leak alone is low. |
| X-005 | V3 | An untested behavior that plan:64 explicitly specifies. |

## Shared assumptions

- **A-001: QUALIFY.** Local `master` exists (d953b983) but may lag `origin/master`. The existing script already uses local `master`, and the tests use a throwaway repo, so the impact is low.
- **A-003: ACCEPT.** `eval_runner.py` only sets constants at module level (lines 35-36) and guards `main` at line 317. The registered load succeeds in evidence section 5.
- **A-004: ACCEPT.** I did not re-read it myself. The diff analysis cites `pyproject.toml:108-109` (`testpaths = ["tests"]`, `python_files = ["test_*.py"]`).
- **A-006: QUALIFY.** My grep of `tests/` for `ABSOLUTE RULE: PR Target|close it immediately|Contributing back` found nothing. I did not check the strings in the rewritten worktree section.
