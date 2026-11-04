# Refactoring Plan: Merge into Base (Variant 1)

## Overview
- Base: Variant 1 (reviewer-1, sonnet:analyzer), `variant-1-original.md`
- Incorporating strengths from: Variant 3 (reviewer-3, opus:refactorer), Variant 2 (reviewer-2, haiku-slot glm-5.3:qa), and the Round 2.5 invariant probe (invariant-probe.md; MEDIUM UNADDRESSED items are carried as findings)
- Planned changes: 16
- Risk level: Medium overall (several base findings are restructured or re-rated)
- Output: `../merged-findings.md` (one level up, beside this folder), a YAML reviewer card inside a markdown file with provenance comments
- Classification vocabulary for every finding: authorized | necessary | drift | regression (UC-1 meaning: regression = the plan as written would remove existing behaviour)

## Planned Changes

### Change 1: Sharpen R1-1 with V3's failure-string criterion (from Variant 3)
- **Source**: Variant 3, R3-F1 recommendation ("t2-fail-before.txt must fail on the missing `master_checkout`, not on `'NoneType' object has no attribute '__dict__'`")
- **Target**: Base R1-1 recommendation (append)
- **Rationale**: C-001 won by V3 content with V1 label at 95% (debate-transcript.md scoring matrix); X-003 settled `drift` at 100%
- **Integration point**: keep R1-1 id, label `drift`, severity medium; append the failure-string criterion and `monkeypatch.setitem(sys.modules, ...)` as the cleanup form
- **Risk**: Low (additive)

### Change 2: Replace R1-2 with the merged failure-path finding (from Variant 3 + invariant probe)
- **Source**: Variant 3 R3-F3; invariant-probe INV-003 (rmdir may hit an already-deleted dir) and INV-004 (teardown failure handling; model at tests/troubleshoot/backtest/git_replay.py:199-205)
- **Target**: Base R1-2 (restructure; keep id R1-2)
- **Rationale**: C-002 won by V3 at 95%; X-004 settled medium at 90% (V1 conceded in round2-v1.md); INV-004 MEDIUM UNADDRESSED
- **Integration point**: severity low -> medium; headline covers leak, masking, and mis-reporting body errors (eval_runner.py:70 timeout) as global-setup; recommendation: dedicated `MasterCheckoutError`; on failed add remove the mkdtemp dir tolerating its absence (`shutil.rmtree(..., ignore_errors=True)` or `contextlib.suppress(FileNotFoundError)`) and raise before any try/finally; try/finally around `yield` only; teardown failures logged, never raised over the body's exception; `main` catches only `MasterCheckoutError`
- **Risk**: Medium (modifies an existing finding's severity and recommendation)

### Change 3: New finding M-1, `main()` wiring and the global-setup path are untested (from Variants 3 and 2 + V1 Round 2 + probe)
- **Source**: V3 R3-F2 and R3-F9; V2 R2-F2; round2-v1.md new evidence eval_runner.py:294-295; INV-005 (argv parse, eval_runner.py:267-269), INV-006 (plan:74 fail-before rule vs characterization tests), INV-014 (gate chain); A-001 caveat (local `master` may lag origin/master)
- **Target**: Base, new finding after R1-2 (insert)
- **Rationale**: C-003 won by V3 at 95%; X-005 medium at 90%; INV-006 and INV-014 MEDIUM UNADDRESSED
- **Integration point**: id M-1, `drift`, medium; recommendation: add a `main()` `--mode global` test with `sys.argv` patched, asserting a `global-setup` RunResult with errors=1 and git's stderr; decide and state the exit-code rule at eval_runner.py:313; name the replacement for the `if worktree_path.exists()` guard (eval_runner.py:294-295); restate plan:74 so every new test must fail before the change or be named as a characterization test; say the eval checkout deliberately uses local `master`
- **Risk**: Low (additive)

### Change 4: New finding M-2, tests are not isolated from the real checkout (from probe + Variant 3)
- **Source**: INV-001 (RESULTS_DIR fixed at import, eval_runner.py:35-43, :307-309; not ignored), INV-010 (fixture lacks EVAL_FILES/E2E_SCRIPTS, so `run_global` returns early at :150-156 and the E2E loop skips at :297-298), INV-015 (strip `GIT_*`, `GIT_CONFIG_GLOBAL=/dev/null`, per tests/skills/test_implement_retry_revert.py:31-36); V3 R3-F7 (`git init -b master`, identity)
- **Target**: Base, new finding (insert)
- **Rationale**: INV-001 and INV-010 MEDIUM UNADDRESSED; R3-F7 low (weak per calibration, kept as hygiene)
- **Integration point**: id M-2, `drift`, medium; recommendation: patch `RESULTS_DIR` to `tmp_path`; seed the fixture with at least one EVAL_FILES entry and one E2E script stub, or test the `with` body separately; build the fixture with `git init -b master`, a local identity, `GIT_*` removed and `GIT_CONFIG_GLOBAL=/dev/null`; assert nothing new appears under the real repo (`git status --porcelain` unchanged)
- **Risk**: Low (additive)

### Change 5: New finding M-3, removing the temporary checkout deletes the global E2E outputs (from probe)
- **Source**: INV-013 (eval_runner.py:300 runs E2E with the checkout as cwd; scripts/eval_1.py:456-459 default output `eval-results/...` relative to cwd; `RunResult` keeps only `stderr[-500:]`, eval_runner.py:118)
- **Target**: Base, new finding (insert)
- **Rationale**: INV-013 MEDIUM UNADDRESSED; the old persistent checkout kept these outputs
- **Integration point**: id M-3, `regression`, medium; recommendation: Task 2 passes `--output-dir` (or copies `eval-results/`) to a location under the real `RESULTS_DIR` before teardown, or states explicitly that global E2E outputs are discarded; the eval_1.py default spec path note stays `[INFERRED]`
- **Risk**: Low (additive)

### Change 6: Merge R1-4 with V3's CLAUDE.md:50 conflict (from Variant 3)
- **Source**: V3 R3-F4 first half (CLAUDE.md:50 `gh pr create --repo <repo>` fails plan:117 while plan:113 keeps it); scripts half dropped (X-001 to V1, conceded in round2-v3.md)
- **Target**: Base R1-4 (restructure)
- **Rationale**: C-004 merge at 95%
- **Integration point**: severity low -> medium; location adds CLAUDE.md:50; recommendation adds: say how line 50 is rewritten (repo resolved from origin and must be IronbellyOrg/IronClaude; halts on a wrong-owner URL); drop the CLAUDE.md:64 half (calibration: plan :108 already rewrites check 1)
- **Risk**: Medium (modifies severity and scope)

### Change 7: Mark R1-5 as required (from Variant 3 Round 2)
- **Source**: round2-v3.md ("makes V1's R1-5 required, not optional"); V3 R3-F4 section-scoped awk command
- **Target**: Base R1-5 (modify)
- **Rationale**: C-004 merge
- **Integration point**: keep low; recommendation names the section-scoped form `awk '/^## ABSOLUTE RULE: PR Target/,/^## ABSOLUTE RULE: Never Hardcode/' CLAUDE.md | grep -n -w 'gh'`
- **Risk**: Low

### Change 8: Merge R1-3 with the Orca-vs-fork-rule conflict (from probe)
- **Source**: INV-012 (plan:86 requires `orca worktree create`; plan:105 bans any Orca tool call "that resolves to" upstream; plan:111 Orca project id `github:superclaude-org/superclaude_framework`)
- **Target**: Base R1-3 (restructure)
- **Rationale**: INV-012 MEDIUM UNADDRESSED; same rule, same tasks as R1-3
- **Integration point**: severity low -> medium; headline: Tasks 3 and 4 state the Orca rule at different strengths, and plan:105 read literally forbids the local Orca calls plan:86 requires; recommendation: qualify plan:105 so only link flags and network-reaching calls count, and use one wording in both tasks
- **Risk**: Medium

### Change 9: Add R2-F1, Task 8 rerun leaves no artifact (from Variant 2)
- **Source**: Variant 2 R2-F1; round2-v2.md (medium holds; this checkout is full-depth and uid 1000, so any skip has another cause); INV-011 (no deselection)
- **Target**: Base, new finding (append)
- **Rationale**: U-003 High value; uncontested in both rounds
- **Integration point**: keep id R2-F1, `drift`, medium, recommendation verbatim
- **Risk**: Low

### Change 10: Add R3-F5 as low hardening (from Variant 3)
- **Source**: Variant 3 R3-F5; round2-v3.md downgrade citing sc-implement-protocol SKILL.md:111, :125 (orchestrator-verified; plan:29, :160, :179 stage only `.dev/tasks/`)
- **Target**: Base, new finding (append)
- **Rationale**: U-006; severity settled low in Round 2
- **Integration point**: id R3-F5, `drift`, low; rationale states the checks are vacuous only if source files are staged by hand
- **Risk**: Low

### Change 11: Add R3-F6 merged with INV-007 (from Variant 3 + probe)
- **Source**: V3 R3-F6; INV-007
- **Target**: Base, new finding (append)
- **Integration point**: id R3-F6, `drift`, low; drop the untracked memory-note example (calibration: untracked, invisible to git grep)
- **Risk**: Low

### Change 12: Add R3-F8 (from Variant 3)
- **Source**: V3 R3-F8
- **Target**: Base, new finding (append)
- **Integration point**: id R3-F8, `drift`, low; recommendation: prefer the behavioural `git worktree list` assertion over a source grep
- **Risk**: Low

### Change 13: New finding M-4, the two retired-location checkouts no longer exist (from probe)
- **Source**: INV-009 (orchestrator-confirmed 22:40Z)
- **Target**: Base, new finding (append)
- **Integration point**: id M-4, `drift`, low; location plan:27, :44, :51, :90; recommendation: Task 1 records the live `git worktree list`; the plan:27 constraint and the plan:90 rule are reworded to "any checkout found at the retired location", not the two named paths
- **Risk**: Low

### Change 14: Add R2-F3 as a low completeness note (from Variant 2)
- **Source**: Variant 2 R2-F3 with the orchestrator annotation (premise not present on this host)
- **Target**: Base, new finding (append)
- **Integration point**: keep `drift`, low; evidence notes no `IronClaude-eval-master` checkout exists today
- **Risk**: Low

### Change 15: Amend `deviations_resolution` (from debate concessions)
- **Source**: round2-v1.md (D-001 "resolved with required fix"); round2-v2.md; INV-009
- **Target**: Base `deviations_resolution` (modify rows D-001, D-002, D-008, D-013)
- **Integration point**: D-001 resolved at plan level, Task 2 needs R1-1, R1-2, M-1, M-2, M-3; D-002 note R1-4 (now incl. CLAUDE.md:50), R1-5; D-008 note R2-F1; D-013 note M-4 (checkouts gone)
- **Risk**: Low

### Change 16: Extend `t1_findings_disputed` and `inferred_claims` (from Variants 3 and 2)
- **Source**: V3 dispute of T1 S1 (Task 2 not executable as written, confirmed by shell section 5); V3 S3 dispute narrowed to CLAUDE.md:50 (round2-v3.md); V2 search reproduction (U-005) and INV-008 live rerun
- **Target**: Base `t1_findings_disputed` (append S1, S3) and `inferred_claims` (append)
- **Risk**: Low

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|------------|-------------------|---------------------------|
| X-001 | V3: the allowed-forms list contradicts the pr-submit scripts (drift, medium) | Conceded by V3 in Round 2: every fallback runs only after an empty origin lookup (poll-ci-checks.sh:34-35 etc.); source.md scopes the work to CLAUDE.md. R1-6 kept as `authorized`, low. |
| X-003 | V3: `necessary` for the import crash | Conceded by V3; `drift` at 100%. |
| U-006 severity | Diff analysis rated R3-F5 High value; V3 card had medium | Downgraded to low in round2-v3.md on verified sc-implement-protocol evidence. |
| R3-F7 standalone | Separate low finding | Folded into M-2 (isolation), avoiding a duplicate. |
| R3-F9 standalone | Separate low finding | Folded into M-1 (it restates R2-F2's exit-code half, conceded in round1-v3.md). |
| `.venv` deletion claim | V3 inferred_claims | Withdrawn by V3 in round2-v3.md. |
| R1-4 CLAUDE.md:64 half | V1 card | Calibration found it wrong: plan :108 already rewrites check 1. |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|----------|------|------------------|----------|
| 2, 6, 8 | Medium | A re-rated finding misstates the debate outcome | Revert to the base wording in variant-1-original.md |
| 1, 3-5, 7, 9-16 | Low | Additive; no conflict with base content | Remove the inserted item |

## Review Status
- Approved by: auto (non-interactive)
- Approval timestamp: 2026-11-02T22:45:00Z
