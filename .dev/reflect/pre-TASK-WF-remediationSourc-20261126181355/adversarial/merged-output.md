<!-- Provenance: merged by the orchestrator from reviewer-cards/reviewer-1-card.md and reviewer-2-card.md after a quick-depth adversarial round (Round 1 only). Base: Variant 2 (reviewer 2, qa) for the prior-blocker and coverage sections; Variant 1 (reviewer 1, analyzer) for the Medium findings. Merge date: 2026-11-26 -->
# Merged review card (second review of the regenerated Run ledger plan)

Plan: /home/coder/workspaces/worktrees/IronClaude/run-ledger/.dev/tasks/to-do/TASK-WF-remediationSourc-20261126-181052/TASK-WF-remediationSourc-20261126-181052.md
Spec: /home/coder/workspaces/worktrees/IronClaude/run-ledger/.dev/tasks/to-do/TASK-WF-remediationSourc-20261126-181052/source.md

## Verdict

PASS with notes. No Blocking finding survives the debate: reviewer 1's one Blocking finding (F1) was reduced to Medium by its own advocate, and the opposing advocate agreed on Medium. Counts: 0 Blocking, 0 HIGH-labelled, 2 Medium, 6 Note.

## Prior blockers

- B-1 resolved: the Constraints allow exactly `RUN_ID_RE` and `parse_time` from `probes` (plan line 21), Task 3 imports `RUN_ID_RE` (plan line 50), and Task 2 names an enforcing test (plan line 43). The weakness of that test is M-2.
- B-2 resolved: the Task 10 check covers `superclaude` commands and flags only (plan line 128).
- B-3 resolved: Task 11 ends with `git add .dev/tasks` and uses the package's own `./artifacts/` (plan lines 136 and 140).
- B-4 resolved: Task 6 names both exact-text cases and requires their expected text to carry the hint (plan line 82); the real cases are tests/sweep/test_cli_contract.py lines 375-387 and 478-490.
- B-5 resolved: Task 9 adds the script name to the install test seed list (plan line 112); the real list is tests/cli/test_install_hooks.py lines 89-107.
- B-6 resolved at the rule level: Task 1 requires parsed UTC datetimes through `parse_time` for every time comparison and names a mixed-form test (plan lines 30 and 33). The gap that remains is M-1.

## Findings

| id | grade | claim | citations | consequence and fix | provenance |
|---|---|---|---|---|---|
| M-1 | Medium: | The `parse_time` rule and the mixed-form test sit in Task 1's paragraph about `decide`. Task 3's `added_at >= generated_at` merge, Task 2's guard 4 ("created or updated within 24 h") and Task 6's 90-minute stale test never mention `parse_time`, and no test feeds both forms to them. The spec lists `added_at >= generated_at` among the rules (source.md line 168). | plan lines 30, 33, 40, 50, 53, 82; source.md lines 67 (guard 4) and 168; src/superclaude/cli/sweep/probes.py lines 413-437 | An implementer can compare raw strings in those three places and still pass every named test. Fix: one clause in each of Tasks 2, 3 and 6 requiring `parse_time`, one mixed-form test for the merge and for guard 4, and a sentence saying what happens when `parse_time` returns None. | V1 F1 (graded Blocking by V1, Medium by both advocates) |
| M-2 | Medium: | `test_ledger_imports_only_allowed_probes_names` is described against the absolute module name `superclaude.cli.sweep.probes`; the sweep package uses relative imports (`from . import probes`), so a check written for the absolute form can pass without testing the allowlist. | plan line 43; src/superclaude/cli/sweep/commands.py line 22 | The exact-allowlist rule of the Constraints (plan line 21) is not really enforced. Fix: the test handles `from .probes import X`, `from . import probes` and attribute access. | V1 F2 |
| N-1 | Note: | The hint suffix is pinned by plan line 82 and the prefixes by probes.py lines 403-407; only a cosmetic join (no separator) is left to the implementer. | plan line 82; src/superclaude/cli/sweep/probes.py lines 403-407 | Wording only. | V1 F3 downgraded |
| N-2 | Note: | Task 4 does not say how the fake runner reaches `ledger_command` through `CliRunner`. | plan line 60 | Wording only. | V1 F4 |
| N-3 | Note: | Task 11 runs `sweep run`, which writes a report under `.dev/sweeps/`; that file is not in the `artifacts:` list. | plan line 136; src/superclaude/cli/sweep/commands.py lines 240 and 275 | Wording only. | V1 F5 |
| N-4 | Note: | `ledger.py` imports `fcntl` at module top level and `main.py` loads `sweep_group` at import; Linux and macOS only, and the plan already records a Windows shortcut. | plan line 54 (the Windows shortcut comment); src/superclaude/cli/main.py line 585 (the `sweep_group` import). That `ledger.py` will import `fcntl` at module top level is the reviewer's inference, not stated in the plan. | None. | V1 F6 |
| N-5 | Note: | The 69-row coverage matrix is an index, not an exhaustive inventory (no rows for the schema's list totals, objective length, restricted reasons and source values). | source.md lines 34-42 (the matrix itself is in the review folder: artifacts/coverage-matrix.json) | Do not describe it as exhaustive. | V2 N-1 |
| N-6 | Note: | `parse_time` returns None for an unparseable value and the plan says nothing about the call sites. | src/superclaude/cli/sweep/probes.py lines 413-437 | Covered by the M-1 fix sentence. | advocates (both) |

## Coverage check

All 69 inferred rows are covered by a task or by the Constraints (the nine rows the string matcher left unmatched are word-choice misses: INF-006, INF-008, INF-016, INF-027, INF-032, INF-053, INF-054, INF-055, INF-061). INF-061 (time comparison) is covered at the rule level with the M-1 gap. Reviewer 2's grouped table shows 69 of 69 adherent at plan-text level.

## Debate record

- Depth: quick (circuit breaker; Round 1 only). Convergence on diff points: 11 of 11 (100%). No invariant probe at quick depth.
- Final counts: blocking 0, label_high 0, medium 2, note 6.
- Calibration (blind, sonnet): card 1 0.85, card 2 0.82.

## Self-reported confidence

0.78 (reviewer 1) and 0.87 (reviewer 2); calibrated 0.85 and 0.82.
