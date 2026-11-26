# Round 2 findings: issue #807 (C26) Build process for the coordinator pull requests and the local end-to-end gate

Checked 2026-11-24 on master `f2894fc44` (HEAD of this worktree). Issue state: OPEN, label enhancement, no comments. Parent: umbrella #716. `<P>` = `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify`. `<R>` = `/home/coder/workspaces/worktrees/IronClaude/Coordinator/.dev/releases/backlog/issue-watcher-zero-setup/requirements.md`. Analyze check: `.dev/issuecleanup/b/8/analyze/807/analyze-report.md` (target `.github/workflows`).

## Alignment with architectural decisions

- **R38** (`<R>:64`, owner 2026-11-21): the merged watcher is the design; no element of Clay's 655 design is adopted; the "Clay strengths adopted" rows of the unification spec are void. **Partly aligned.** C26 is a process item and R38 does not touch process. But C26's tests "T1 to T13" are Clay's G1 test plan (`<P>/spec/SPEC.md:467` "G1 tests T1-T13 ... ADOPT+CHANGE"; `DECISIONS.md:591`), and the design text that defined them was removed by PR 700 (`SPEC.md` Appendix B). Whether T1-T13 survive R38 is UNVERIFIED; only T13 (`tests/coordinator/test_merge_path.py`, `SPEC.md:498`) is pinned by the plan.
- **Owner workflow rule** (global CLAUDE.md "How to choose a workflow", level 3; project CLAUDE.md "`.dev/tasks/` Is Always Staged"; PR #288 merged 2026-10-23): S12-F4 is **aligned** and already practice. The item says so itself ("a reminder, not a new design").
- **WORKER-CONTRACT WC-9** (`~/.claude/WORKER-CONTRACT.md:41-45`): a worker never runs `git add` (not even `.dev/tasks`); the coordinator stages it. **Partly aligned**: "the ledger is staged under `.dev/tasks/`" must say the coordinator or a person stages it. WC-9 also makes every outward action off for a worker, so creating throwaway repos or issues (S14-F3) is not worker work (same file `:41`).
- **WC-13** (`~/.claude/WORKER-CONTRACT.md:63`): a worker never creates worktrees or Tasks. **Aligned**; no conflict with C26.
- **S17 live tests** (`<P>/spec/SPEC.md:501`) and "Nothing below has run" (`SPEC.md:700`, section 13.2 at `:698`): S14-F1 is **aligned** with the plan's own live-test table. The stage list it hangs on (S13 to S15) extends "PR 686 adapted", and PR 686 is CLOSED unmerged (R38, `<R>:64`; design-comparison-655.md:53). So the stage names need a re-check: **UNVERIFIED** which stages still stand.
- **OA-19** (`<P>/spec/SPEC.md:582`): "at most one throwaway repo after the shadow run, cap 1". S14-F3 asks for one repo in each org. **In conflict (partly)**: the cap is about switching a repo on for the poll, not test repos, but the two should be reconciled before repos are made. UNVERIFIED which orgs "the work covers".
- **SEC-14** (`<P>/spec/SPEC.md:303`): approvals go through chat, an agent records them. **Aligned**: creating throwaway repos needs the owner's go given in chat.
- **Contract 3 workflow** (`.github/workflows/contract3-generator-constraint-lint.yml`): S12-F20 is **already enforced** (paths gates.py, structural_checkers.py, `*_validator.py`; heading `## Generator-Constraint Considered`).
- **CI** (`.github/workflows/test.yml:102,106,123,131,135`): S12-F18 is **already enforced** (`ruff check`, `ruff format --check src/ tests/`, `make verify-deps`, plus `verify-sync`, `lint-architecture`). PR #280 (merged 2026-10-22) kept these on every PR to master or integration. This resolves the item's "UNVERIFIED whether CI already runs these".
- Searched `DECISIONS.md`, `SPEC.md` and the 27 `debates/*/VERDICT.md` for: throwaway, T13, ledger, verify-deps, Generator-Constraint, OA-19, S17. No decision forbids the item.

## Complementary issues

- **#716** (umbrella): its review says "C26 applies to every pull request"; C26 is the rule for building all other C items (#782 C1 to #805 C24, #808 C27). No code interface; the interface is the PR body (ledger link, three-command pass, e2e paste).
- **#782** (C1, skill layout and file-table test): C26's gate checks each stage PR; C1's tests are one of the things the gate runs. C26 completes the process around it; no dependency either way.
- **#442** (live observations OB-H1..H3 of the launch-level guard on disposable PRs): the same style of throwaway evidence that S14-F1/F3 want for T1-T13. Reuse its disposable-issue approach and its runbook; do not duplicate the repos.
- **#733** (unattended `/sc:implement`): when built, the ledger C26 asks for can come from a worker run; C26's "ledger shows QA passed" depends on `/sc:implement` ledgers, which exist today.
- **#723** (protect master with rules, parked): its throwaway test (FR-77, `SPEC.md:341`) would share the throwaway repo set of S14-F3.
- **#618** (ruff version follows the Coder image): affects S12-F18, because `uv run ruff format --check` gives a different answer under ruff 0.17.3 than under the pinned 0.15.20 when the dev extra is missing. Order: fix or note #618 before relying on the local check.

## Closest overlap

**#442**, "[TEST GAP] Run the live observations OB-H1, OB-H2, OB-H3 and OB-CTX for the launch-level guard" (open). Shared: running real checks on disposable issues and PRs and recording the result next to the test (what S14-F1 and S14-F3 ask for the coordinator PRs). I estimate it covers about 10 to 15 percent of C26's done-when (only the throwaway-evidence part of S14-F1/F3); the ledger link, the three-command record and the Contract 3 check, which are the stated done-when lines, are covered 0 percent by any open issue. Next two closest: **#723** (shares the throwaway repo and the FR-77 test, about 5 percent) and **#777** (map the whole watcher and coordinator chain and decide what to automate; overlaps only in "what to automate in the build chain", about 5 percent; also #761).

## Standalone or merge

**Verdict: stand alone, narrowed.** Tested against #442:
- Owner: C26 belongs to whoever builds the coordinator PRs (#716 build); #442 belongs to the launch-level guard work (#394, #432). Different.
- Acceptance test: C26 = every stage PR body links a ledger with all tasks QA passed and shows a pass for three commands; #442 = twelve skipped observation tests run in a real session. Different.
- Files touched: C26 = `.github/PULL_REQUEST_TEMPLATE.md` plus docs for throwaway repos; #442 = `tests/hooks/test_launch_level_observations.py` and fixtures. No overlap.
- Build phase: C26 applies at every stage PR (S13 and later; #716 review: "applies to every pull request"); #442 is a pre-condition for governed launches. Different.
- Risk if merged: merging C26 into #442 would tie a general PR rule to one guard test run and block it on a person at a real terminal; merging into #716 would hide a cross-cutting rule inside a 27-item umbrella. Not merged.
Plainly: **merging into #716 would be right** if the owner drops S14-F3 (the throwaway repo set). Then only one XS PR-template line remains and it is no longer worth its own issue.

## Closed issues and merged PRs checked

- **#450** (closed COMPLETED 2026-11-24): the watcher rollout; live operation reported and automatic first-run checks substituted for older manual gates. Contradicts the premise that live e2e gates must precede enabling; supports a smaller S14-F1.
- **PR #280** (merged 2026-10-22): kept lint, format, deps, sync and architecture lint on every PR. Delivers S12-F18 in CI.
- **PR #288** (merged 2026-10-23): `.dev/tasks` always staged. Delivers the staging half of S12-F4.
- **PR #285** (merged 2026-10-23): `/sc:pr-submit --monitor 3` is the PR route. The ledger link and e2e paste would ride in the body that command writes; no change to the command is needed.
- **PR #707** (merged 2026-11-20): the watcher with its own `/sc:implement` ledger (`TASK-WF-requirements-20261119-143917-2`, ends `T28: complete`, `FINAL: pass`, per `<R>` rows). Shows the practice works.
- **PR #729** (merged 2026-11-23): records R38.
- **PR #686** (CLOSED unmerged 2026-11-23): the stage list C26 builds on is partly gone.
- **#796 (C15), #809 (W1), #813 (W5)** closed NOT_PLANNED 2026-11-24 by the owner: the owner is already pruning Clay-derived items; C26's T1-T13 are Clay-derived.

## Updated recommendation

**Keep open with changes**, priority **P3**, complexity **medium**, size **S** (round 1: M). Changes: (1) drop S12-F18 and S12-F20 (already enforced by `test.yml` and the Contract 3 workflow; cite them); (2) keep S12-F4 as one PR-template line asking for the ledger link and say the coordinator or a person stages `.dev/tasks` (WC-9); (3) mark S14-F1 and S14-F3 "when the first coordinator PR is planned", need the owner's go in chat, reconcile with OA-19, and name which of T1-T13 survive R38; (4) re-check stage names after PR 686 closed. Changed from round 1 only in size (two of five lines drop, so M to S); priority, action and complexity unchanged.

## Scan record

Read in full: open-issues.tsv (133 rows), closed-issues.tsv (156 rows), merged-prs.tsv (507 rows), titles only (numbers and titles). Search terms: ledger, throwaway, e2e, lint, ruff, format, verify, CI, workflow, unattended, implement, build process, template, test gate, stage, PR submit, protect, staging, .dev/tasks. Opened in full: open #716 (body and 3 comments), #782, #442, #733, #618, #695, #723, #761, #777, #794, #802; closed #450, #796, #809, #813, #651; PRs #280, #288, #285, #707, #729, #661, #686. Plan files: `SPEC.md`, `DECISIONS.md`, `FOLLOW-UPS.md`, 27 `VERDICT.md` greps; `<R>` rows R30 to R38. Master checks: `.github/workflows/test.yml`, `contract3-generator-constraint-lint.yml`, `.github/PULL_REQUEST_TEMPLATE.md` (no ledger, implement or e2e line, by grep). UNVERIFIED: which orgs "the work covers"; which of T1-T13 survive R38; whether PR 693 and others change the stage names; #695, #618 read as skims only.
