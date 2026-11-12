# Tier-2 reviewer 2 (qa, haiku): UC-1 audit of TASK-WF-enforceTheOwnerP-20261108-031809

<!-- Returned by reflect-reviewer (read-only), persisted by orchestrator on receipt 2026-11-08T03:48Z. Self-reported confidence 0.91. Paths below abbreviate the repo root /home/coder/workspaces/worktrees/IronClaude/fix-flaky-parallel-thread-test and the plan package .dev/tasks/to-do/TASK-WF-enforceTheOwnerP-20261108-031809/ (plan = <pkg>/TASK-WF-enforceTheOwnerP-20261108-031809.md). -->

**Persona:** QA, testability and acceptance. **Mode:** UC-1 pre-execution. **Diff scope:** plan vs source; no implementation diff.

**best_practice_grade: 2/5.** Good task structure and substantial test coverage, but the plan can pass while missing ownership requirements, retaining contradictory `none` instructions, or implementing unsafe terminal cleanup. Source-relative departures: 2. QA findings: 9 (prospective plan defects, not shipped regressions).

## Per-task acceptance review

"Would fail" = the specified checks reject a wrong implementation.

| Task | Observable / would fail on wrong work? | Existing tests affected, named? |
|---|---|---|
| 1 New hook | Partly. Exit codes and listed commands observable; no per-command flag isolation, wrapper handling, all fail-open branches, or full stderr message. A scanner that carries `--agent` into the next command escapes the listed cases. | None must break if sibling unchanged; Python-hook tests named as model. |
| 2 Registration/install | Mostly. Count, matcher, timeout, exec bits, mirror bytes, installed settings concrete. Interaction check can be satisfied with prose. | Exact Bash-hook-set test will fail until updated (named). Fake installer inventory named. Unit inventory named but presence checks only. |
| 3 First-tab cleanup | No, not safely. No safe handling of opaque/timed-out create replies; no repository validation before close. Happy-path fixture returns invalid JSON, so the five-call assertion conflicts with conservative cleanup. | FO-18 call-list test will break (named). FO-11 opaque-create test needs an expectation change (not named individually). Timeout tests included by file, cleanup expectations unspecified. |
| 4 `none` skips worktree | Partly. Wave 7 skip pin catches one sentence; contradictions elsewhere and `none` return values not pinned; grep checks one old wording. | No existing test requires old semantics. ST-9 already skips launch for `none`; ST-10 pins keys not values. Plan overstates need to rewrite old pins. |
| 5 Design documents | Partly. Text-inspectable; preserves D2/FO-18 contrary to source without demonstrated authorization; user-facing docs omitted. | None established. |
| 6 Project instructions | Partly. Example and agent phrase testable; omitting creator ownership/coordinator rule passes every assertion; negative grep passes if old example deleted. | None necessarily breaks; new test required. Orca-only rule, link restriction, temp-checkout exception not pinned. |
| 7 Installed instructions | Mostly. Two added phrases and twelve pins observable; ownership wording, paragraph equality not proven. Existing paragraphs not byte-identical, so comparing only the appended paragraph is right. | Twelve-phrase test named, stays green. Routing-block tests named, unaffected. |
| 8 Delivery | Mostly. Logs and steps observable; pending live checks identified; inherits earlier gaps; omits verify-sync test module. | None established. |

Evidence for test impact: tests/hooks/test_freshness_subagent_start_policy.py:105-114; tests/cli/test_install_hooks.py:763-819; tests/unit/test_cli_install.py:891-901; tests/skills/test_issue_orca_worktree.py:794-820, :552-618; tests/skills/test_issue_protocol.py:431-447, :487-515; tests/core/test_orca_session_launch_guidance.py:13-31; src/superclaude/cli/install_core.py:70-75; src/superclaude/cli/main.py:365.

## Findings

| ID | Sev | Task | Claim | Evidence | Recommended plan change | vs T1 |
|---|---|---|---|---|---|---|
| R2-1 | MEDIUM | 1 | Scanner reuse needs argument-state tests: sibling stops on ordinary args after the command word and exits on a forbidden executable; new hook must defer its verdict until it knows that command's flags and isolate nested/chained commands. | src/superclaude/hooks/scripts/block-bare-python.sh:97-106, :130-134; plan :31-34 | Require per-command argument state and finalization; add wrappers, backticks, comments/newlines, direct shell heredocs, both command orders (allowed then bare; bare then allowed/help); nested-substitution cases so an outer `--agent` cannot exempt an inner bare create; document ceilings. | Agrees F1 |
| R2-2 | LOW | 1 | Untested contract branches and incomplete blocking message: wrong status on missing/erroring awk, or omitted ownership/worker instructions, still pass. | plan :31-35; tests/hooks/test_block_bare_python.py:224-247 | Tests for missing command, empty stdin, missing jq, missing awk, scanner failure, `-h`; assert full command form, ownership instruction, worker-start instruction, one stderr message. | New |
| R2-3 | MEDIUM | 2 | Interaction criterion permits "no test needed". The identity hook wraps the original command as a quoted argument and says rewrite ordering is unverified. | src/superclaude/hooks/scripts/launch-job-identity.sh:475-481; plan :42-47 | Require a governed-session regression test with a bare create expecting exit 2; record live ordering as unverified. | Agrees F11 |
| R2-4 | MEDIUM | 3, 5 | Plan contradicts source: new worktrees stay bare creates, `agent launch` stays the new-worktree path, D2/FO-18 unchanged. "Stated to the owner" is not evidence of approval; copy-before-launch explains the current design but does not show agent-on-create infeasible. | <pkg>/source.md:1; plan :20, :53, :75 | Obtain and record explicit authorization, or restore agent-on-create and adjust ordering/tests. | New |
| R2-5 | HIGH | 3 | No conservative unknown-reply branch; `created_scene()` returns `"opaque, not json"` and FO-11 asserts no warning, yet Task 3 requires that happy path to list and close. Closing after an unreadable/timed-out reply cannot establish absence of setup/default tabs. | tests/skills/test_issue_orca_worktree.py:365-387, :552-561, :607-618; orca_worktree.py:611-614; plan :53-57 | Define create/list envelopes, validate types; unknown/malformed/unsuccessful/timed-out → no close + non-fatal warning; valid-reply fixture for cleanup happy path; keep an opaque-create test (copies/records, warns, closes nothing); list failure/malformed/zero-terminal tests. | Agrees F5 + fixture conflict |
| R2-6 | HIGH | 3 | Closure can run before the repository-identity guard: the new-row branch checks row-id difference, name pattern, directory existence; git-common-dir check is inside `finish()` just before copy. "Not failed" not yet established at the proposed pre-copy point. | src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:618-645, :504-513; plan :53 | Require git-common-dir validation before any close; test a new row whose path belongs to another repo → failed/stale, zero close calls; zero cleanup for ambiguous/missing/reused rows. | New |
| R2-7 | MEDIUM | 4 | `none` change incomplete: unconditional Wave 7/Will instructions and Final output "open <wt>" not named. | src/superclaude/skills/sc-issue-protocol/SKILL.md:90-92, :124-136, :170; refs/claim.md:131-136; tests/skills/test_issue_protocol.py:503-514 | Update all claim entry/summary/final-output instructions; `worktree_path`, `worktree_branch`, `worktree_match_key`, `worktree_warning` null for `none`; keep ten keys; pin no-worktree output and main-checkout next-steps for `none`. | Agrees F3; refutes F3's line-range error (105-134 includes the return fields) |
| R2-8 | MEDIUM | 4, 5 | Public `none` behavior changes without updating the user guide or installed routing row. | docs/user-guide/commands.md:367, :379, :394; src/superclaude/core/HOW-WE-WORK.md:329; plan :64-80 | Add those to the update list (with HOW-WE-WORK's plugin mirror); add a `none` consistency assertion. | New |
| R2-9 | MEDIUM | 6, 7 | Ownership policy unprotected: new pins cover agent wording and "never own use" only; can pass while omitting creator-becomes-orchestrator/coordinator-and-owns-agents. | plan :88-103; tests/core/test_orca_session_launch_guidance.py:17-31; <pkg>/source.md:1 | Assert creator ownership and both orchestrator/coordinator roles in the project rule and both installed copies; compare the appended paragraph between copies. | New |

## Other T1 findings checked

- **F2 not confirmed as a defect.** Keeping Orca mandatory for `none` is consistent with the binding P1 dependency decision at docs/designs/sc-issue-claim-pipeline-flag.md:39. Record the decision explicitly and test whichever behavior is authorized.
- **F8 confirmed.** Command tests check flags, defaults, outputs, examples, not the old sentence; tests/commands/test_issue_command.py:169-179 stays valid.
- **F9 partly confirmed.** tests/cli/test_verify_sync_hooks.py:101-111 parses the script list dynamically; adding a script does not inherently break it. Including the suite is reasonable; it mutates in place, so do not run it concurrently with other source-changing work. verify-sync already in Task 7.

## Deviations from the source

| # | Category | Location | What diverged | Evidence | Severity |
|---|---|---|---|---|---|
| 1 | Drift | Tasks 3, 5 | Replaces agent-on-create with bare create + first-tab cleanup; keeps D2/FO-18 the source says to change. Necessity and owner approval not demonstrated. | <pkg>/source.md:1 vs plan :20, :53, :75 | MEDIUM |
| 2 | Authorized expansion | Tasks 4, 5 | `--pipeline none` skips worktree creation; recorded as an owner decision. | plan :19, :60-80 | LOW |

Necessary deviation: none demonstrated. Regression: none observed (plan audit); HIGH findings are destructive-operation risks to prevent.

## Adherence summary (8 tasks)

Fully adherent at intended scope: 5 (Tasks 1, 2, 6, 7, 8). Authorized expansion: 1 (Task 4). Necessary deviation: 0. Drift: 2 (Tasks 3, 5; one shared departure). Regression: 0. Scope-adherent is not execution-ready.

## Confidence and limits

Self-reported confidence: 0.91. Not verified: owner approval of the Task 3 replacement beyond the plan's statement; installed Orca create/list schemas and close behavior; live PreToolUse rewrite ordering; no tests/lint/sync run.

Recommended action (reviewer): return the plan for revision; resolve R2-4 first; if cleanup stays, require R2-5 and R2-6 guards and tests before execution.
