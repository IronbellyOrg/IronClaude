# Round 2: Variant 2 Rebuttal (haiku-slot glm-5.3:qa)
<!-- Returned by a read-only advocate agent; persisted verbatim by the orchestrator. -->

All inputs read: the three original cards, diff analysis, all Round 1 statements, V1's Round 2 rebuttal, the plan, and the shell evidence. I re-read `scripts/eval_runner.py:260-319` and plan lines 170-179 this session to verify the claims below.

## Response to criticisms

**V1/V3: V2 missed C-001 (import crash) and accepted T1 S1 despite it.** Full concession, unchanged from Round 1. My card stayed inside the plan's own text and never executed the cited loader pattern against the cited script; the probe (shell section 5) settled it against me. S1 acceptance was wrong.

**V1: no T1 disputes means fewer claims checked.** Partial rebuttal. I checked different claims and reproduced them: Search A 108/17 and Search B 9/7 (including the tuple-form hit at `tests/cli/reflect/test_isolate_reviewers_cli.py:147`), and `eval_runner.py:313`'s local-only exit filter, verified again this session. Coverage verification and T1 dispute are separate jobs; I did the first and skipped the second. The skip was a real gap, but "fewer claims checked" is not accurate.

**V1/V3: R2-F3 rests on a refuted premise.** Conceded in Round 1; the finding survives only as a plan-completeness note (Task 1 never records `git worktree list` entries outside `/.dev/worktrees/`). Low, unchanged.

**V1 Round 2 new evidence (`eval_runner.py:294-295`).** Verified: line 294 builds `REPO_ROOT.parent / "IronClaude-eval-master"`, line 295 guards the global E2E block with `if worktree_path.exists()`. Partial concession. Plan:64 ("wrap the whole global block ... and the global E2E scripts in one `with master_checkout()`") plus plan:65 ("remove every use of `IronClaude-eval-master`") jointly dictate the outcome: the guard dies because the context manager guarantees existence, and the per-script `script_path.exists()` check at line 298 remains. What the plan omits is naming that rewrite and any test for the E2E block — which is exactly C-003, already conceded to V3. It strengthens V3's position; it does not create a new point.

## Updated assessment

V3 remains the strongest card on Task 2 executability; V1's Round 2 concessions (D-001 cell, C-003 miss, X-004 severity) narrow its lead on calibration but its coverage table and scope disputes still hold. V1's new A-006 evidence (tests read `_CORE / "CLAUDE.md"`, the distributed core file) is useful and moves me off ACCEPT there. No variant disputed R2-F1 in either round; V1 called it "a real acceptance-criterion hole" and V3 "the most valuable finding in the set."

## New evidence

- `scripts/eval_runner.py:294-295` confirmed this session (V1's claim).
- Plan:170 names `t8-internal-checkouts.txt` and records `is-shallow`/`id -u` for the first run only; plan:176's rerun names no artifact. Reconfirmed by fresh Read.
- **R2-F1 is still uncontested, and medium holds — sharpened by shell section 2.** This checkout is already full-depth (`false`) and non-root (`1000`). So if the first run shows any SKIPPED line, those skips are not shallow-or-root-caused, and "repeat in a full-depth, non-root checkout" either means this same checkout (skips recur, branch unpassable) or an unnamed different checkout the plan never says how to obtain — with no artifact either way. The branch is the only pass path once a skip exists, and it is unverifiable post-hoc. Medium, not low: it is an acceptance criterion whose escape hatch cannot be audited.

## Final per-point positions

| Point | Preferred variant | Changed since Round 1? |
|---|---|---|
| S-001 | V1 (merge V2's search reproduction) | no |
| S-002 | V3 | no |
| S-003 | V3 on S1; V1's F1/F3 disputes also valid | no |
| C-001 | V3 content, V1's `drift` label | no |
| C-002 | V3 | no |
| C-003 | V3 (V1's 294-295 note folds in) | no |
| C-004 | V3 base plus V1 R1-4/R1-5 | no |
| X-001 | V1 (one clarifying sentence) | no |
| X-002 | V3 | no |
| X-003 | V1 | no |
| X-004 | V3 (medium) | no |
| X-005 | V3 (medium) | no |

## Shared assumptions

- **A-001: QUALIFY.** Local `master` exists (d953b983) but can lag `origin/master` in an Orca worktree; the existing script already uses local master, so low risk — the plan should say it is deliberate.
- **A-003: ACCEPT.** Shell section 5: registered load succeeds, no git run, no files written; module level is constants only, `main` guarded.
- **A-004: ACCEPT.** Verified in Round 1: `pyproject.toml:108-109` (`testpaths = ["tests"]`, `python_files = ["test_*.py"]`); `tests/unit/` exists.
- **A-006: QUALIFY** (moved from ACCEPT). No test pins the rewritten sentences, but V1's Round 2 finding that `tests/cli/test_issue_body_templates.py:18` and `tests/core/test_claude_md_routing_block.py:16` read `_CORE / "CLAUDE.md"` is unverified by me — I did not resolve `_CORE`. Residual risk low either way; a one-line verification during Task 4 closes it.
