# Returned by reflect-reviewer (read-only); persisted by the orchestrator.
# Orchestrator verification 2026-11-02 (~21:49Z), see artifacts/t1-shell-evidence.txt sections 5-6:
#   R1-1 CONFIRMED: loading scripts/eval_runner.py via spec_from_file_location + exec_module WITHOUT sys.modules registration
#         raises "AttributeError 'NoneType' object has no attribute '__dict__'"; with sys.modules[spec.name] = module it loads OK.
#   R1-2 CONFIRMED: `git worktree remove --force <unregistered mkdtemp dir>` exits 128 and the directory remains.
reviewer: 1
persona: analyzer
model_class: sonnet
findings:
  - id: R1-1
    headline: "Task 2's test loader pattern can crash on import because eval_runner.py uses @dataclass under `from __future__ import annotations`"
    location: ".dev/tasks/to-do/TASK-WF-revisedPlanRefac-20261102-213941/TASK-WF-revisedPlanRefac-20261102-213941.md:67"
    classification: drift
    severity: medium
    evidence: "Plan :67 'It loads the script with `importlib.util.spec_from_file_location` (the pattern at tests/swarm/test_bare_review_golden_regen.py:153)'. tests/swarm/test_bare_review_golden_regen.py:157-158 'module = importlib.util.module_from_spec(spec) / spec.loader.exec_module(module)' (no sys.modules). scripts/eval_runner.py:10 'from __future__ import annotations'; scripts/eval_runner.py:46-47 '@dataclass / class RunResult:'."
    rationale: "A module executed without being put in sys.modules crashes @dataclass processing of string annotations, so the regression test would fail at import for a reason unrelated to the feature (confirmed by the orchestrator)."
    recommendation: "In Task 2's test description add: register the module with `sys.modules[spec.name] = module` before `exec_module`, and remove it in teardown. Verify the pre-change failure comes from the missing `master_checkout` attribute, not an import error."
  - id: R1-2
    headline: "Task 2's cleanup does not cover the failed-creation path, so the mkdtemp directory leaks, and a failing teardown could hide the body's exception"
    location: ".dev/tasks/to-do/TASK-WF-revisedPlanRefac-20261102-213941/TASK-WF-revisedPlanRefac-20261102-213941.md:62"
    classification: drift
    severity: low
    evidence: "Plan :62 'On a non-zero exit it raises an error carrying git's stderr. In `finally` it runs `git worktree remove --force <that directory>` (never `rm -rf`)'. Plan :70 'a repo with no `master` branch makes `master_checkout()` raise with git's stderr'."
    rationale: "If `git worktree add` fails the directory is not a registered worktree, so `git worktree remove` fails (exit 128, confirmed) and the empty temp directory stays; the plan does not say whether a failing teardown may replace the original exception."
    recommendation: "When creation fails, remove the still-empty mkdtemp directory with `os.rmdir` before raising; make teardown failure non-masking; assert in the no-master test that the mkdtemp directory no longer exists."
  - id: R1-3
    headline: "Task 3 bans Orca link flags unconditionally while Task 4 bans them only until the project id changes"
    location: ".dev/tasks/to-do/TASK-WF-revisedPlanRefac-20261102-213941/TASK-WF-revisedPlanRefac-20261102-213941.md:88"
    classification: drift
    severity: low
    evidence: "Plan :88 'Forbid Orca link flags (`--issue`, `--pr`) for this repo, pointing to the fork rule edited in Task 4.' Plan :111 'until `orca worktree current --json` shows the fork's project id, `--issue`, `--pr` and other Orca link flags are never passed for this repo.' Plan :105 'no gh or Orca link flag that resolves to it'."
    rationale: "The same CLAUDE.md would carry three different strengths for one rule; a reader cannot tell when the ban lifts."
    recommendation: "In Task 3 say 'Orca link flags are governed by the fork rule below', or use the same conditional form as plan :111."
  - id: R1-4
    headline: "Two lines of the fork section survive that conflict with the new rules, and the plan names neither"
    location: ".dev/tasks/to-do/TASK-WF-revisedPlanRefac-20261102-213941/TASK-WF-revisedPlanRefac-20261102-213941.md:113"
    classification: drift
    severity: low
    evidence: "Plan :113 'keep ... pre-PR check 2 and the Rationale paragraph, editing them only where they contradict the rules above.' CLAUDE.md:64 '(gh prefers an `upstream` remote over `origin`)'; CLAUDE.md:70 'only this CLAUDE.md rule + explicit `--repo` on every invocation does.'"
    rationale: "CLAUDE.md:70 in the kept Rationale says `--repo` on every invocation, contradicting the positional form for `gh repo view`; plan :118 is a judgment-only check."
    recommendation: "In Task 4 name CLAUDE.md:70 and change it to 'the repo named explicitly on every gh call'; say the check-1 `upstream` parenthetical is dropped."
  - id: R1-5
    headline: "The Task 4 gh-line check greps for `gh ` with a trailing space, which also matches ordinary words"
    location: ".dev/tasks/to-do/TASK-WF-revisedPlanRefac-20261102-213941/TASK-WF-revisedPlanRefac-20261102-213941.md:117"
    classification: drift
    severity: low
    evidence: "Plan :117 'the check is saved as `./artifacts/t4-gh-lines.txt` from `grep -n 'gh ' CLAUDE.md`.'"
    rationale: "`gh ` matches 'through ', 'though ', 'enough '; the whole file is searched although the criterion is about one section."
    recommendation: "Use `grep -n -w 'gh' CLAUDE.md` restricted to the section's line range."
  - id: R1-6
    headline: "The pr-submit scripts' bare `gh repo view` fallback is real but outside the plan's spec scope (partial dispute of T1 F1)"
    location: "src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh:35"
    classification: authorized
    severity: low
    evidence: "poll-ci-checks.sh:34-35 'REPO=\"${REPO:-$(git remote get-url origin ...)}\" / [ -n \"$REPO\" ] || REPO=\"$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || true)\"'. source.md:1 'Also tighten the CLAUDE.md rule: SuperClaude upstream is never pushed to or interacted with.'"
    rationale: "The fallback runs only after the origin lookup returns nothing; the spec scopes the tightening to CLAUDE.md and D-002 names only CLAUDE.md:64 and :66."
    recommendation: "Optional: one sentence in Task 4 saying the guarded fallbacks in sc-pr-submit-protocol scripts are not covered by the allowed-forms list and are unchanged."
deviations_resolution:
  - {deviation: D-001, resolved: yes, plan_location: "Task 2, Task 1, Task 8, Constraints Search B", note: "R1-1/R1-2 are execution risks"}
  - {deviation: D-002, resolved: yes, plan_location: "Task 4", note: "R1-4, R1-5 remain"}
  - {deviation: D-003, resolved: yes, plan_location: "Constraints, Task 1", note: "Search A 108/17, Search B 9/7 confirmed"}
  - {deviation: D-004, resolved: yes, plan_location: "Constraints, Task 4", note: "line-64 parenthetical in R1-4"}
  - {deviation: D-005, resolved: yes, plan_location: "Task 4", note: "narrowed; #419 kept with diff check"}
  - {deviation: D-006, resolved: yes, plan_location: "Task 1", note: "Historical record first; Blocked noted"}
  - {deviation: D-007, resolved: yes, plan_location: "Task 1, Task 5", note: "row label correct"}
  - {deviation: D-008, resolved: yes, plan_location: "Task 8", note: "-rs, zero skips or recorded reason + rerun"}
  - {deviation: D-009, resolved: yes, plan_location: "Task 4", note: "literal reading + authorized Orca bullet"}
  - {deviation: D-010, resolved: yes, plan_location: "Constraints", note: "flags added"}
  - {deviation: D-011, resolved: yes, plan_location: "Task 7", note: "contract test in pytest command"}
  - {deviation: D-012, resolved: yes, plan_location: "Task 3, Task 6", note: "optional read-only, removed after scan"}
  - {deviation: D-013, resolved: yes, plan_location: "Task 3, Task 1, Constraints", note: "stay until merged; not moved"}
  - {deviation: D-014, resolved: yes, plan_location: "Task 1", note: "recorded out of scope; Task 8 checks unchanged"}
t1_findings_disputed:
  - {t1_id: F1, reason: "Real and guarded, but the spec scopes the tightening to CLAUDE.md and D-002 names only :64/:66; out-of-scope low (R1-6), not drift."}
  - {t1_id: F3, reason: "source.md:1 tells the plan to decide CLAUDE.md:251 explicitly; authorized, not necessary."}
self_confidence: 0.78
inferred_claims:
  - "[INFERRED, now CONFIRMED by orchestrator] R1-1 import crash without sys.modules registration."
  - "[INFERRED, now CONFIRMED by orchestrator] R1-2 git worktree remove on an unregistered path exits non-zero and leaves the directory."
  - "[INFERRED] R1-5 the pattern `gh ` matches words such as 'through '."
  - "[INFERRED] git worktree add --detach into an existing empty directory behaves as Task 2 assumes (orchestrator separately confirmed it does; artifacts/t1-shell-evidence.txt section 1)."
