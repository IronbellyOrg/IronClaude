# Diff Analysis: reflect reviewer-card Comparison

## Metadata
- Generated: 2026-11-02T22:31:00Z
- Variants compared: 3 (variant-1 = reviewer-1 sonnet/analyzer, C 0.84; variant-2 = reviewer-2 haiku-slot glm-5.3/qa, C 0.75; variant-3 = reviewer-3 opus/refactorer, C 0.80)
- Input note: variants are YAML reviewer cards copied as `variant-N-original.md` (non-markdown input; warning logged in audit.log 4.0-prereq)
- Focus: correctness, coverage, deviation-classification
- Analysis performed by the orchestrator (analytical-agent equivalent) from the three cards plus the shared evidence file `artifacts/t1-shell-evidence.txt`
- Total differences found: 26
- Categories: structural (3), content (4), contradictions (5), unique (10), shared assumptions (6 listed; 4 UNSTATED promoted)

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|------|-----------|-----------|-----------|----------|
| S-001 | Deviation-resolution section | `deviations_resolution`: 14 rows, D-001..D-014 each mapped to a plan location, all `resolved: yes` | `missing_requirements: []` plus a span-by-span justification mapping D-001..D-014 to INF rows; reproduces Search A (108/17) and Search B (9/7) | No deviation-resolution or missing-requirements section | Medium |
| S-002 | Finding count and depth | 6 findings (1 medium, 4 low, 1 authorized low) | 3 findings (1 medium, 2 low) | 9 findings (5 medium, 4 low) | Low |
| S-003 | Dispute of the Tier 1 card | Disputes T1 F1 (pr-submit fallback is out of scope) and F3 (#419 decision is authorized) | No disputes | Disputes T1 S1 (Task 2 not executable as written) and S3 (understated) | Low |

## Content Differences

| # | Topic | Variant 1 Approach | Variant 2 Approach | Variant 3 Approach | Severity |
|---|-------|-------------------|-------------------|-------------------|----------|
| C-001 | Task 2 test loader crashes on import (plan:67; eval_runner.py:10, :46-48) | R1-1, medium, drift: register `sys.modules[spec.name]` before `exec_module`; fail-before must fail on missing `master_checkout` | Not raised | R3-F1, medium, "necessary": same fix; fail-before must not fail on `'NoneType' object has no attribute '__dict__'` | Medium |
| C-002 | `master_checkout()` failure path (plan:62, :64; shell section 6) | R1-2, low: `os.rmdir` the empty mkdtemp dir on failed add; teardown must not mask the body's exception | Not raised | R3-F3, medium: dedicated `MasterCheckoutError`; rmdir and raise before any try/finally; try/finally around `yield` only; `main` catches only that error so a pytest timeout (eval_runner.py:70) is not reported as global-setup | Medium |
| C-003 | Global-setup path, `main()` wiring and exit code (plan:64, :67-76; eval_runner.py:313) | Not raised | R2-F2, low: add a test that makes `master_checkout` raise and asserts a `global-setup` RunResult with errors=1; state whether :313's local-only exit code changes | R3-F2, medium: fail-before is vacuous; add a `main()` `--mode global` test and a master-present test; R3-F9, low: global-setup failure exits 0 | Medium |
| C-004 | Task 4 `gh` rules and their check (plan:108-119; CLAUDE.md:50, :64, :70; pr-submit scripts) | R1-4, low: name CLAUDE.md:70 ("explicit `--repo` on every invocation") and the :64 parenthetical; R1-5, low: `grep -n 'gh '` matches "through", use `-w` on the section range; R1-6, authorized low: pr-submit fallback is out of scope, optional note | Not raised | R3-F4, medium: CLAUDE.md:50 `gh pr create --repo <repo>` fails plan:117 while plan:113 keeps it; allowed-forms list contradicts the scripts' bare `gh repo view` fallback; section-scoped `awk ... | grep -n '\bgh '` | Medium |

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Variant 3 Position | Impact |
|---|-------------------|-------------------|-------------------|-------------------|--------|
| X-001 | Do the pr-submit scripts' guarded bare `gh repo view` fallbacks (poll-ci-checks.sh:34-35 etc.) put the plan in conflict? | No: out of the spec's CLAUDE.md scope, `authorized`, low; disputes T1 F1 ("real and guarded ... out-of-scope low") | Silent (accepts T1 card without dispute) | Yes: the plan:110 allowed-forms list "contradicts the mandated tool's scripts"; drift, medium (R3-F4) | Medium |
| X-002 | Is Task 2 executable as written (T1 S1)? | D-001 "resolved: yes"; R1-1 and R1-2 are execution risks to note | Accepts S1; no Task 2 executability finding | Disputes S1: "Task 2 is not executable as written (R3-F1, R3-F2, R3-F3)" | Medium |
| X-003 | Classification of the import-crash finding | `drift` (R1-1) | n/a | `necessary` (R3-F1); calibrator notes this is outside the rubric set | Low |
| X-004 | Severity of the `master_checkout` failure-path finding | low (R1-2) | n/a | medium (R3-F3) | Medium |
| X-005 | Severity of the untested global-setup path | n/a | low (R2-F2) | medium (R3-F2) | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | Variant 1 | R1-3: Task 3 bans Orca link flags unconditionally (plan:88) while Task 4 bans them only until the project id changes (plan:111) | Medium |
| U-002 | Variant 1 | `deviations_resolution` table: every D-001..D-014 mapped to a plan location | Medium |
| U-003 | Variant 2 | R2-F1: Task 8's conditional rerun (plan:176) names no artifact and no way to obtain the full-depth, non-root checkout | High |
| U-004 | Variant 2 | R2-F3: no disposition for a leaked `IronClaude-eval-master` checkout from past runs (premise refuted by orchestrator probe 22:23Z: none exists) | Low |
| U-005 | Variant 2 | Independent reproduction of Search A (108 lines / 17 files, POST-REFLECT-TASK.md 79) and Search B (9 lines / 7 files) | Medium |
| U-006 | Variant 3 | R3-F5: plain `git diff` checks at plan:119, :148, :178 are vacuous once files are staged; use `git diff HEAD` | High |
| U-007 | Variant 3 | R3-F6: Task 8 residual check has no class for files created after Task 1 (the new test file) | Low |
| U-008 | Variant 3 | R3-F7: test fixture needs `git init -b master` and a git identity | Low |
| U-009 | Variant 3 | R3-F8: teardown grep `worktree", "remove"` is formatting-dependent | Low |
| U-010 | Variant 3 | R3-F9 (exit-code half of C-003 stated as its own finding) and the `.venv` deletion note in inferred_claims | Low |

## Shared Assumptions

Agreement points: (AG-1) all three accept that the revised plan resolves D-001..D-014 at plan level; (AG-2) all three accept Task 2's core design (mkdtemp, `git worktree add --detach <dir> master`, `git worktree remove --force` in teardown) and critique only its edges; (AG-3) none challenges the Search A / Search B baselines.

| # | Agreement Source | Assumption | Classification | Promoted |
|---|------------------|------------|----------------|----------|
| A-001 | AG-2 | A local branch named `master` exists and is the intended ref for the eval checkout | UNSTATED | Yes |
| A-002 | AG-2 | `git worktree add --detach` into an existing empty directory succeeds | STATED (V2 inferred_claims; shell section 1 confirms) | No |
| A-003 | AG-2 | `scripts/eval_runner.py` has no import-time side effects, so a test can import it once registered | UNSTATED | Yes |
| A-004 | AG-2 | A new file under `tests/unit/` is collected by `uv run pytest` | UNSTATED | Yes |
| A-005 | AG-1 | The executor stages files before the acceptance checks run | STATED (V3 inferred_claims) | No |
| A-006 | AG-1 | No existing test pins the CLAUDE.md fork-rule or worktree sentences that Tasks 3-4 rewrite | UNSTATED | Yes |

### Promoted [SHARED-ASSUMPTION] diff points

| # | Assumption | Impact | Status |
|---|------------|--------|--------|
| A-001 [SHARED-ASSUMPTION] | Local `master` exists and is the right ref. Orchestrator check: `git rev-parse --verify master` -> d953b983 (committed 2026-11-02T16:39). In an Orca worktree a local `master` can lag `origin/master`; the existing script already uses local `master`, so this is not new behaviour. | Low | Open for debate |
| A-003 [SHARED-ASSUMPTION] | No import-time side effects. Shell section 5: the registered load succeeds without running git or writing files. | Low | Open for debate |
| A-004 [SHARED-ASSUMPTION] | Test collection. pyproject.toml:108 `testpaths = ["tests"]`, :109 `python_files = ["test_*.py"]`; `tests/unit/` exists. | Low | Open for debate |
| A-006 [SHARED-ASSUMPTION] | CLAUDE.md sentences not test-pinned. Grep of `tests/` for `close it immediately|ABSOLUTE RULE: PR Target|Contributing back` returns nothing; `.dev/worktrees` appears only at tests/docs/test_tavily_doc_alignment.py:49 and tests/skills/test_implement_retry_revert.py:613, :1053, which are already in Search A. | Low | Open for debate |

## Summary
- Total structural differences: 3
- Total content differences: 4
- Total contradictions: 5
- Total unique contributions: 10
- Total shared assumptions surfaced: 6 (UNSTATED: 4, STATED: 2, CONTRADICTED: 0)
- Convergence denominator (S + C + X + promoted A): 3 + 4 + 5 + 4 = 16
- Highest-severity items: U-003 (High value), U-006 (High value); Medium: S-001, C-001, C-002, C-003, C-004, X-001, X-002, X-004, X-005
- Similarity check: differences well above 10% of comparable items; debate proceeds.
- Taxonomy pre-tag: L3 (state/guard/boundary/invariant/validation): C-001, C-002, C-003, X-002, X-004, X-005, A-001, A-003; L2 (structure/interface/dependency): S-001, C-004, X-001, A-004, A-006; L1 (wording/style/presentation): S-002, S-003, X-003.
