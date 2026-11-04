# Tier 1 reflection card (UC-1, pre-execution)

hypothesis_source: inline-orchestrator
spec: .dev/tasks/to-do/TASK-WF-refactorIronClau-20261102-162730/source.md
tasklist: .dev/tasks/to-do/TASK-WF-refactorIronClau-20261102-162730/TASK-WF-refactorIronClau-20261102-162730.md

## Coverage section (qa lens)

- Pass 1 parsed IDs: 0 (source.md has no R-/REQ-/SPEC-/T- labels). Pass 2 inferred rows: 11 (artifacts/pass2-inferred.yaml). coverage_degraded: parsed-sparse (Step 1B.2b), so a Tier 1 stop is forbidden.
- Containment match (artifacts/coverage-matrix.json): 10 of 11 matched, coverage_pct_union 0.9091, coverage_pct null (no parsed rows), S_dev_density 0.0909.
- INF-001 overall goal -> Task 1 (0.857); INF-002 replace CLAUDE.md rule -> Task 2 (1.0); INF-003 every tracked file -> Task 1 (0.75); INF-004 the git grep hit set -> Task 1 (1.0); INF-005 classify each hit into two classes -> Task 1 (0.842); INF-006 project worktree to Orca -> Task 2 (0.889); INF-007 internal checkout keeps working -> Task 1 (0.889); INF-008 tighten upstream rule -> Task 3 (0.9); INF-009 source of truth src/superclaude -> Task 5 (1.0); INF-010 run make sync-dev -> Task 6 (1.0).
- INF-011 "never stage .claude mirrors" is lexically unmatched (best Task 3, ratio 0.5). Content-level disposition: COVERED. The plan Constraints (line 20) forbid staging any `.claude/` path except `.claude/settings.json`, and Task 6 and Task 7 acceptance criteria require `git diff --cached --name-only` to list no other `.claude/` path (plan lines 116-122, 134-137). The word "mirrors" is missing, not the obligation.
- Content-level check of the matched rows: INF-005 is matched lexically, but the plan answers it with THREE classes, not the two the source names (see F1). INF-007 is covered by "unchanged" assertions, not by a test run (see S2).

## Root-cause / deviation section (analyzer lens)

- F1 (deviation, needs user decision): the plan adds a third class, "Historical record, keep unchanged", for POST-REFLECT-TASK.md (plan line 37). The source names only two classes: project worktree (move to Orca) and internal temporary checkout (keep working without Orca) (source.md:1). POST-REFLECT-TASK.md holds 79 of the 108 hits, so 73% of the hit lines stay as they are. Class: refinement beyond the source; the rationale is recorded in Task 1 but the user did not authorize it.
- F2 (deviation, minor): Task 1 classifies per FILE (one row per file with a hit count, plan lines 33-45), while the source says "Classify each hit" (source.md:1). For a mixed file (CLAUDE.md after Task 2 holds both a retired-location prohibition and an internal-exception line) a per-file class is coarser than per-hit.
- F3 (interpretation, low): Task 3 reads "never pushed to or interacted with" as also forbidding fetch or pull from the upstream remote (plan lines 73 and 82). This is a literal reading of "interacted with", not stated explicitly in the source.
- F4 (residual by design, aligned): Task 4 keeps the `.dev/worktrees/` ignore entry (plan line 89), so a hit remains in .gitignore; Task 7's residual rule (plan line 134) allows it. Aligned with "replace the rule" because the comment is rewritten to say retired.
- F5 (gap, low): CLAUDE.md keeps a markdown link to an upstream SuperClaude-Org issue (#419) in its Slash Commands note. Task 3's new wording "no tool call or link (gh, git or Orca) that resolves to it" (plan line 73) may read as contradicting that existing link. [INFERRED] Whether a static doc link counts as "interaction" is a reading question the plan does not address.

## Structural / tech-debt section (refactorer lens)

- S1: Mirror discipline is correct. Task 6 copies src to plugins and runs `make sync-dev` before `make verify-sync` and the parity tests (plan line 116). tests/commands/test_routing_plugin_parity.py:29-47 enforces byte parity for the sc-recommend skill tree and for commands/recommend.md, so the plan's Constraint (plan line 21) is grounded and its test choice is correct.
- S2: Internal temporary checkouts are protected only by "unchanged" assertions (Task 7, plan line 135). No task runs their tests (tests/skills/test_implement_retry_revert.py, tests/cli/reflect/test_isolate_reviewers_cli.py, tests/troubleshoot/backtest/). Because those files are not edited the risk is low, but "keep working without Orca" is asserted by non-change, not by an observed run.
- S3: Line-number drift avoided: tasks anchor edits by section heading and quoted text, not line numbers (Tasks 2, 4, 5). That avoids the recurring defect "bare line citations drift once earlier tasks edit the same file" (docs/memory/reflect/deviation-patterns-IronClaude.md:12).
- S4: The Orca command surface is pinned to verified help output (plan line 23), and the unverified `orca worktree rm` selector syntax is deferred to a `--help` check inside Task 2 (plan line 58).
- S5: Tasks 2 and 3 both edit CLAUDE.md; Task 3 depends on Task 2, so there are no concurrent edits to one file.

## Self-reported confidence (NOT used by the rubric; calibrator re-grades)

self_reported: 0.86 (plan covers every source obligation; one unauthorized third class F1 and one coarse-granularity choice F2 lower it). Structural signals: S_scope 7 tasks, S_domains 3 (docs, config, tests), S_dev_density 0.0909.
