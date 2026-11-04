# Round 1: Variant 2 Advocate (haiku-slot glm-5.3:qa)
<!-- Returned by a read-only advocate agent; persisted verbatim by the orchestrator. -->

## Position summary

I am Variant 2 (qa persona, haiku-slot). My card's value is coverage discipline: the only card that both walks every source obligation span-by-span (D-001..D-014 → INF-015..INF-040) and independently reproduces the Search A (108/17) and Search B (9/7) baselines, plus the one finding the diff analysis rated sole High value on my side (R2-F1, unverifiable Task 8 rerun). Variant 3 outperforms me on Task 2 implementation risk; I concede those points rather than defend them.

## Steelman

**Variant 1.** Its `deviations_resolution` table is the most auditable artifact any card produced: 14 rows, each D-mapped to a plan location with a note. Its disputes of T1 F1 and F3 are scope-correct — source.md:1 does scope the fork tightening to CLAUDE.md, and D-002 names only CLAUDE.md:64/:66, so R1-6's "authorized, out of scope" is the right call, and it was the only card to see that. R1-5's `gh ` grep false-positive ("through ") is a genuine check-correctness catch I missed entirely.

**Variant 3.** It is the only card that asked "does Task 2 actually run?" — and the orchestrator probe answered no (t1-shell-evidence.txt section 5: unregistered load fails with `AttributeError 'NoneType'`). Its R3-F5 (plain `git diff` vacuous once staged) is the second High-value finding in the diff analysis and attacks the plan's evidence machinery itself, which is exactly a QA concern I should have owned. R3-F7 (`git init -b master`, git identity) and R3-F8 (formatting-dependent grep) are the kind of host-dependence edge cases my persona exists to catch.

## Strengths claimed

1. **R2-F1 (U-003, rated High):** plan:176 requires a rerun "in a full-depth, non-root checkout with no SKIPPED line" but names no artifact for it, while plan:170 saves `git rev-parse --is-shallow-repository` and `id -u` only beside the *first* run. The plan demonstrably knows how to name artifacts (plan:74 names `t2-fail-before.txt`/`t2-pass-after.txt`), so this is an omission, not a style choice. Post-hoc, D-008 compliance is unverifiable — the criterion can pass on an unrecorded assertion.
2. **R2-F2 named the exit-code hole with a line citation:** `scripts/eval_runner.py:313` filters `r.name.startswith("local")`, so a `global-setup` RunResult with `errors=1` (plan:64) still exits 0. I verified the line this session. "Do not fail silently" is contradicted by the exit code one function below it.
3. **Independent reproduction of both search baselines (U-005):** including POST-REFLECT-TASK.md at 79 hits and the Search B tuple-form catch at tests/cli/reflect/test_isolate_reviewers_cli.py:147 — confirming the plan's Constraints (plan:20) numbers rather than trusting them.
4. **Coverage closure:** `missing_requirements: []` backed by a span-by-span justification, not an assertion.

## Weaknesses identified in other variants

1. **V3 has no deviation-resolution section at all** (S-001): nine findings, zero mapping of D-001..D-014 to plan locations. Its dispute of T1 S3 ("understated") is asserted without the coverage walk that would show whether the plan still resolves every deviation.
2. **V1's R1-2 rates the `master_checkout` failure path low** (X-004): it sees the leak and masking but misses that `main`'s `with` block plus an unnamed exception type can convert body errors (e.g. the 120 s timeout at eval_runner.py:70) into a false `global-setup` result — that is a wrong-result scenario, not cosmetic. Probe section 6 (remove on unregistered dir exits 128, dir remains) confirms the mechanism.
3. **V3's classification `necessary` for R3-F1 is outside the 4-category taxonomy** (X-003, calibrator-noted): the finding is right, the class is unusable in a deviation ledger.

## Concessions

R2-F3's premise was refuted by the 22:23Z probe — no leaked IronClaude-eval-master checkout exists; it survives only as a plan-completeness note. I accepted T1's S1 and stayed silent on the import crash (C-001) and the CLAUDE.md:50/plan:117 conflict (C-004); V3 disputed S1 and was confirmed. Three findings was too few for a plan this size.

## Per-point positions

| Point | Preferred | Reason |
|---|---|---|
| S-001 | V1 | Structured 14-row table beats prose; merge my search reproduction |
| S-002 | V3 | Breadth won: 5 medium findings, two probe/high-confirmed |
| S-003 | V3 | Its S1/S3 disputes were validated by the probe |
| C-001 | V1 | Same fix as V3 with the taxonomy-correct `drift` class |
| C-002 | V3 | Exception-masking analysis is the real failure scenario |
| C-003 | V3 | R3-F2 is broader; fold my eval_runner.py:313 citation in |
| C-004 | V3 | CLAUDE.md:50 (verified: `gh pr create --repo <repo>`) fails plan:117 while plan:113 keeps it |
| X-001 | V1 | Spec scope is CLAUDE.md; add V3's one-sentence clarifying note |
| X-002 | V3 | Probe section 5 confirms Task 2 is not executable as written |
| X-003 | V1 | `drift` is inside the rubric set |
| X-004 | V3 | False global-setup results are medium |
| X-005 | V3 | Vacuous fail-before weakens the criterion, not just a gap |

## Shared assumptions

- **A-001: QUALIFY** — local master exists (d953b983) but can lag origin/master in a worktree; not new behaviour, so low risk, not zero.
- **A-003: ACCEPT** — probe section 5 shows the registered load succeeds without running git or writing files.
- **A-004: ACCEPT** — verified this session: pyproject.toml:108 `testpaths = ["tests"]`, :109 `python_files = ["test_*.py"]`, and tests/unit/ exists.
- **A-006: ACCEPT** — the diff analysis grep of tests/ for the rewritten CLAUDE.md sentences returns nothing, and the two `.dev/worktrees` test hits are already Search A rows.
