# Refactoring Plan

## Overview
- Base variant: Variant 1 (reviewer-1, sonnet, analyzer) — `variant-1-original.md`
- Incorporated: Variant 3 (R3-F1, R3-F3, R3-F4, R3-F5, A-003 qualification), Variant 2 (coverage section, C-005, X-001 majority, fixture citation), invariant probe (INV-001..INV-014 unaddressed items)
- Planned changes: 14
- Changes not being made: 5
- Overall risk: Medium (adds findings and reclassifies two; no base finding is deleted)
- Output: a merged reviewer card in YAML, same schema as the base, plus `coverage` and `invariants_carried` sections and per-finding `provenance` fields
- Severity scale: high | medium | low; classification: authorized | necessary | drift | regression

## Planned Changes

### Change #1: Add the missed worktree creator as a HIGH finding (M-1)
- Source: Variant 3 R3-F1 + invariant probe INV-005 (HIGH)
- Target: new finding after R1-1
- Approach: insert
- Content: scripts/eval_runner.py:138-147 creates `REPO_ROOT.parent / "IronClaude-eval-master"` with list-argument `["git", "worktree", "add", str(worktree_path), "master"]`, never removes it, ignores the return code. The spec's grep (plan line 19) cannot see it; it fits neither plan class (plan line 57 "creates and removes itself"; plan line 33 "Use exactly these classes"); no task edits it; Task 7 (plan line 134) re-runs only the first grep. Classification: drift (plan scope gap against source.md:1 "every tracked file"). Severity: high. Recommendation: add a task (or extend Task 1 and Task 2) that classifies scripts/eval_runner.py explicitly — either rewrite it to create and remove its own temporary checkout (internal temporary checkout) or route it to an Orca-created worktree — and extend Task 7's residual check with the list-argument search.
- Rationale: X-002 consensus 97% (debate-transcript.md); INV-005 blocks convergence.
- Risk: Low (additive)

### Change #2: Add the other list-argument hits and the count accounting (M-2)
- Source: invariant probe INV-003, INV-004
- Target: new finding after Change #1
- Approach: insert
- Content: list-argument `worktree add` also appears at tests/unit/test_ccsession_tag.py:1858, :1912 and tests/troubleshoot/backtest/test_git_replay_unit.py:34 (outside the 17 files), and on uncounted lines in listed files (src/superclaude/cli/reflect/config.py:202, tests/troubleshoot/backtest/git_replay.py:191, tests/skills/test_implement_retry_revert.py:614, :1054, tests/cli/reflect/test_isolate_reviewers_cli.py:147). Task 1's acceptance (plan line 42) requires counts summing to the live `git grep -c` total. Classification: drift. Severity: medium. Recommendation: Task 1 runs a second search `git grep -n -E '"worktree",\s*"add"|worktree", "add"' -- ':!.dev'` and keeps a separate total for it; each new file gets a class and reason.
- Risk: Low

### Change #3: Extend R1-1 with the recovery gap and the gh-flag gap (M-3)
- Source: invariant probe INV-008, INV-009, INV-007 (addressed); Variant 3 R3-F2 alternative
- Target: base R1-1
- Approach: append to rationale and recommendation
- Content: after check 3 is removed there is no permitted recovery for a PR opened on upstream by mistake — the rewrite must say the agent stops, reports the URL and the user closes it (matches src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:222, which already halts). "--repo on every gh call that accepts it" does not cover `gh repo view` (positional repo) or `gh api repos/{owner}/{repo}` (default repo); tests/pr_submit/test_static_grep.py:616 pins the bare `gh repo view` fallback. Acceptance: name the exact allowed forms.
- Risk: Low

### Change #4: Add the missing-upstream-remote finding (M-4)
- Source: invariant probe INV-001 (verified: `git remote -v` lists only `origin`)
- Target: new finding
- Approach: insert
- Content: CLAUDE.md:41 and plan lines 73 and 76 assume an `upstream` remote that does not exist in this repository; Orca's upstream project id more likely comes from upstream URLs in pyproject.toml:64-67 and package.json; the guard "until `orca worktree current --json` shows the fork's id" (plan line 76) may never lift. Classification: drift. Severity: medium. Recommendation: Task 3 states the rule without depending on a remote named `upstream` (forbid any remote or URL that resolves to SuperClaude-Org/SuperClaude_Framework) and records the observed project-id source as unverified.
- Risk: Low

### Change #5: Strengthen R1-4 with the zero-skip rule and CI depth (M-5)
- Source: Variant 3 / A-003 (92%), invariant probe INV-006, Variant 2 fixture citation
- Target: base R1-4
- Approach: modify recommendation
- Content: run with `-rs`; require zero skips, or record each skip reason and repeat in a full-depth, non-root checkout. Evidence: test_git_replay_integration.py:56-68 skips on shallow clones; .github/workflows/test.yml:17 `actions/checkout@v4` has no `fetch-depth`; test_implement_retry_revert.py:357 skips as root; fixtures are self-contained (test_implement_retry_revert.py:613).
- Risk: Low

### Change #6: Reframe R1-5 per the X-001 majority and INV-011 (M-6)
- Source: Variant 2 X-001 (62%, contested), Variant 3 R3-F6 dissent, invariant probe INV-011
- Target: base R1-5
- Approach: modify rationale and recommendation
- Content: the literal text of plan line 73 ("no tool call or link") covers the static URL at CLAUDE.md:251; plan line 82 names only Orca `--issue`/`--pr` linking (dissent). 22 lines in 10 tracked files hold the upstream URL, including deliberate negative test fixtures (test_pre_pr_checks.py:37, :82; test_crash_recovery.py:179), so the literal reading cannot be satisfied without weakening tests. Recommendation: narrow plan line 73 to "no tool call, and no gh or Orca link flag" and state that static references in docs and test fixtures are out of scope.
- Risk: Low

### Change #7: Reclassify R1-6 for fetch/pull (M-7)
- Source: Variant 2 C-005 (95%); Variant 1 Round 2 concession
- Target: base R1-6
- Approach: modify
- Content: fetch/pull ban is a literal reading of source.md:1 (not a deviation); only the dated Orca project-id bullet (plan line 76) is an authorized expansion.
- Risk: Low

### Change #8: Soften R1-2 per blind calibration (M-8)
- Source: reviewer-1-calibration.yaml (R1-2 weak); POST-REFLECT-TASK.md:576
- Target: base R1-2
- Approach: modify rationale
- Content: plan line 37 never calls the file finished; POST-REFLECT-TASK.md:576 records the substantive work as validated with only a manual reflect gate outstanding. Keep the necessary-deviation class and the request to surface the third class to the user.
- Risk: Low

### Change #9: Add the Orca-flag confirmation gap (M-9)
- Source: Variant 3 R3-F3
- Target: new finding
- Content: plan line 23's confirmed list lacks `--json`, `--issue`, `--pr`, used at plan lines 54, 56, 76. Mitigation noted: plan line 76 records `orca worktree current --json` as run. Classification: drift. Severity: low. Recommendation: list those flags in the Constraint or add a `--help` check, saving output under ./artifacts/.
- Risk: Low

### Change #10: Add the unrun contract test (M-10)
- Source: Variant 3 R3-F4
- Target: new finding
- Content: tests/skills/test_sc_recommend_routing_contract.py:27, :29, :130 reads all three Task 5 files; plan line 116 does not run it. Classification: drift (coverage gap). Severity: low. Recommendation: add it to Task 6's pytest command.
- Risk: Low

### Change #11: Add the post-release exception mismatch (M-11)
- Source: Variant 3 R3-F5
- Target: new finding
- Content: src/superclaude/skills/sc-post-release-protocol/SKILL.md:91 offers `git worktree add` with no location and no removal; plan line 57 defines the exception as create-and-remove. Classification: drift. Severity: low. Recommendation: Task 2's exception text describes it as an optional read-only tag checkout removed after the scan, or Task 1 reclassifies it.
- Risk: Low

### Change #12: Add the two remaining low invariant items (M-12)
- Source: invariant probe INV-002, INV-014
- Target: new findings
- Content: a live checkout exists at the retired location (/home/coder/workspaces/IronClaude/.dev/worktrees/issue-body-templates; `git worktree list`), and docs/swarm/runbook.md:34 cites a `.claude/worktrees/BareReview` path outside both greps. Severity: low each. Recommendation: Task 2 says what happens to existing retired-location checkouts; Task 1 notes the runbook line or states it out of scope.
- Risk: Low

### Change #13: Add the coverage section (M-13)
- Source: Variant 2 structure (S-001 winner)
- Target: new top-level `coverage` section
- Content: 11 inferred requirements (INF-001..INF-011); missing in plan substance: INF-003 "every tracked file" is not fully covered (Changes #1, #2); all others covered.
- Risk: Low

### Change #14: Carry inferred-only items and remaining invariant warnings (M-14)
- Source: invariant probe INV-010; Variant 1 U-007 (Round 2: guarded)
- Target: `inferred_claims` and `invariants_carried`
- Content: INV-010 bare gh calls in sc-auggie-review-protocol and sc-troubleshoot-protocol (resolution behaviour [INFERRED]); U-007 sc-pr-submit fallback guarded (informational).
- Risk: Low

## Changes NOT Being Made
| Diff point | Non-base approach | Rationale |
|---|---|---|
| C-001 | Variant 3 fix check 1 with `gh repo set-default --view` only | Leaves CLAUDE.md:66; Variants 2 and 3 conceded (97%) |
| U-006 / R2-F4 | Rewrite the `.claude/` staging constraint | Withdrawn by its advocate; misquotes .gitignore:129; plan copies CLAUDE.md's absolute rule. Recorded as informational: `.claude/cache/sc-recommend-lookup.yaml` is tracked |
| S-002 | Variant 3 all-drift labels | Conceded by Variant 3 |
| Variant 2 `missing_requirements: []` | Empty missing list | Disproved by scripts/eval_runner.py:143 |
| U-007 as a finding | Raise sc-pr-submit SKILL.md:267 as drift | Round 2 showed the fallback is guarded; kept informational |

## Risk Summary
| Change | Risk | Impact | Rollback |
|---|---|---|---|
| #1-#2, #4, #9-#12 | Low | Adds findings | Remove the inserted finding |
| #3, #5-#8 | Low | Modifies base wording | Restore from variant-1-original.md |
| #13-#14 | Low | Adds sections | Remove the section |

## Review Status
Auto-approved (non-interactive), 2026-11-02T18:45:00Z
