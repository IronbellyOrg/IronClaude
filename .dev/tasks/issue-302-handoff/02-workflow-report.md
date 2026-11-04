# Issue #302 handoff: 02 workflow report

- Task: task_dba89f6c9f0a (dispatch ctx_583c4fc886f0, resumed and finished under dispatch ctx_f4fb98ca009d)
- Branch: ironbelly/feat-sc-issue-command
- Scope: checked implementation plan for `/sc:issue` only, produced by `/sc:workflow docs/designs/sc-issue-command.md --depth standard --handoff none`. No file under `src/` or `tests/` is edited by this task.

## 1. Plan path

- Plan: `.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/TASK-WF-scIssueCommand-20261104-064713.md`
- Task: task_dba89f6c9f0a, resumed under dispatch ctx_f4fb98ca009d (the earlier dispatch ctx_583c4fc886f0 was cut off by an API outage from about 09:10 to 12:38 UTC). The plan was not regenerated on resume.
- Package folder: `.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/` holding the plan, `source.md` (byte-identical snapshot of `docs/designs/sc-issue-command.md`, checked with `cmp`) and `return-contract.yaml`. Correction: the earlier version of this line said `return-contract.yaml` was already there; it was not on disk at resume time (12:41 UTC). It is written on resume, after the check, as the workflow skill's Wave 5 requires (section 2).
- Next command (not run by this task): `/sc:implement .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/TASK-WF-scIssueCommand-20261104-064713.md`
- `progress.md` is not in the folder. The workflow skill says it is written by `/sc:implement`, not by `/sc:workflow` (`~/.claude/skills/sc-workflow-protocol/refs/input-parse.md`, "Package contents": "`progress.md`, `artifacts/` | `/sc:implement` | Not created here"). It is an append-only ledger that `/sc:implement` parses on resume (`~/.claude/skills/sc-implement-protocol/refs/ledger.md`), so a hand-written one could be read as a real run record. It appears when `/sc:implement` first runs.

## 2. Advisory check verdict

**Final verdict (check round 2, on plan version 2): PASS with notes. 0 blocking findings, 18 minor. No fix round was needed after round 2.** The check's own status is `partial`, but only because its final citation check dropped 2 items from the report (a misattached citation and a verifier command that could never pass). Neither changes a finding or the verdict.

| Round | Folder | Result | Effect on the plan |
|---|---|---|---|
| 1 (07:09-08:09 UTC) | `.dev/reflect/pre-TASK-WF-scIssueCommand-20261104-064713-20261104070955/` | merged verdict FAIL: 2 blocking (F-01 the full suite sat behind smoke tasks that could block; F-02 the ClickUp token went through the session) plus 16 minor; check status `success` | Fix round 1 (the only fix round used) produced plan version 2 at 08:17 UTC. Round 2's reviewers confirmed both blocking fixes (`round1_fix_check: {F-01: fixed, F-02: fixed}`) |
| 2 (08:17 UTC; interrupted 12:39; resumed and finished 12:41-13:23) | `.dev/reflect/pre-TASK-WF-scIssueCommand-20261104-064713-20261104081732/` | merged verdict PASS with notes: 0 blocking, 18 minor; convergence 1.0 (19 of 19 points); check status `partial` (2 citation drops) | None. The plan was not edited: the workflow skill forbids editing the plan from check findings, and the brief allows a fix round only for blocking gaps |

Round 2 artifacts: report `REPORT.md`, contract `return-contract.yaml` (status partial, tier 2, confidence 0.76), merged verdict `adversarial/merged-verdict.yaml`, debate files under `adversarial/adversarial/`. The plan package's `return-contract.yaml` records `reflect_status: partial` and this report path.

How round 2 was resumed, in that folder: the failed step-2.5 risk probe (an independent agent hunting hidden assumptions) was re-run; it found 1 high-severity flaw in the debate's own fix and no blocking defect in the plan. The step-3 base selection (`base-selection.md`) was regenerated from its sources. The copy written at 12:40:48 is kept unchanged as `base-selection.partial-1240.md`. I did not write it: this session started at 12:41:02 UTC, so it came from the old worker session. The regenerated scores match it exactly, but it was not used. Then the merge plan was drafted and approved by an independent reviewer, the merge was done by a separate merge agent, and the report was written and checked by two citation validators. The 20 input files hashed the same at 12:44 and 13:17 UTC as at the 08:19 snapshot.

Minor findings worth applying before `/sc:implement` runs (these are not blocking; the plan as written is executable):
- **F-01 (top priority).** Task 17 runs a live `/sc:issue --claim https://github.com/octocat/Hello-World/issues/1` without asking (plan:26, plan:254). Nothing tests that the guard comparing the URL with origin actually stops it. Fix: use a URL with no digits outside `/issues/<N>`, for example `https://github.com/IronbellyOrg/no-such-repo-sc-issue-probe/issues/999999999`, and add a tested URL check to `origin_repo.py` that Wave 0 calls. The debate's first suggestion, `.../issue302-no-such-repo/...`, must not be used: its `302` is the real issue's number.
- **F-14.** Copying `evidence-validator.md`'s frontmatter (plan:56) would carry `permissionMode: plan` into the workers, and every worker would fail to write its file. Task 3's test should forbid it.
- **F-02, F-06, F-11, F-12.** `/sc:implement` cannot pause to ask the user (`~/.claude/skills/sc-implement-protocol/refs/qa.md` closed interrupt list; no AskUserQuestion tool). So the asks in Tasks 15, 16 and 17 (plan:233, plan:243, plan:254) cannot fire. On a first run the worker smoke spawns, the ClickUp smoke claim and the live acceptance items will be recorded as pending. A short post-restart runbook at the end of Task 17 would keep them from being dropped.
- The other 13 minor findings and their exact fixes are in the round-2 merged verdict (F-03 to F-05, F-07 to F-10, F-13, F-15 to F-18).

## 3. Steps

17 tasks in 6 phases (plan version 2, revised after check round 1 at 08:17 UTC):

| Phase | Tasks |
|---|---|
| 1. Deterministic helper scripts | Task 1 `origin_repo.py` + tests; Task 2 `clickup_claim.py` + tests |
| 2. Tier-pinned worker agents | Task 3 three `issue-worker-t*` agents + tests |
| 3. Skill package | Task 4 fourteen templates; Task 5 five refs; Task 6 `SKILL.md`; Task 7 skill package tests |
| 4. Command file and inventory tests | Task 8 `commands/issue.md` + test; Task 9 replace the no-issue guard test, add `issue` to the refresh inventory |
| 5. Routing registration and documentation | Task 10 HOW-WE-WORK row, plugin copy, `_OTHER_COMMANDS`; Task 11 developer guide; Task 12 user command reference |
| 6. Sync, full suite, smoke checks, acceptance record | Task 13 `make sync-dev`, `make verify-sync`, path grep; Task 14 full `uv run pytest`, `make lint`, `make verify-sync`; Task 15 worker smoke spawns; Task 16 ClickUp smoke claim; Task 17 section 20 acceptance record |

## 4. Coverage of the brief's required items

Checked against the plan text (plan:N = line N of the plan file) and the design (`source.md`, the byte-identical snapshot of `docs/designs/sc-issue-command.md`). The round-2 check's fault-finder repeated this mapping independently and found no missing deliverable (`.dev/reflect/pre-TASK-WF-scIssueCommand-20261104-064713-20261104081732/adversarial/adversarial/.work/r25-probe.md`, "Missed blocking defects").

| Brief item | Where the plan covers it |
|---|---|
| Every file in design section 15 (13 create rows) | `origin_repo.py` Task 1; `clickup_claim.py` Task 2; three agents Task 3; 14 templates Task 4; 5 refs Task 5; `SKILL.md` Task 6; `commands/issue.md` Task 8 |
| Every file in design section 15 (7 change rows) | `HOW-WE-WORK.md`, plugin copy, `tests/core/test_how_we_work_routing_table.py` Task 10; developer guide Task 11; `docs/user-guide/commands.md` Task 12; `tests/cli/test_issue_body_templates.py` and `tests/recommend/test_routing_refresh.py` Task 9. The "Not changed" list is honoured in the Constraints (plan:25) |
| Every test in design section 16 (8 rows) | new: `test_issue_repo_resolution.py` Task 1, `test_clickup_claim.py` Task 2, `test_issue_worker_agents.py` Task 3, `test_issue_protocol.py` Task 7, `test_issue_command.py` Task 8; changed: `test_issue_body_templates.py` and `test_routing_refresh.py` Task 9, `test_how_we_work_routing_table.py` Task 10 |
| `make sync-dev` and `make verify-sync` | Task 13 (and again in Task 14 and after any Task 16 code change) |
| Routing registration and docs (section 17) | item 1 edit scope: Constraints plan:20; item 2 sync: Task 13; item 3 byte copy plus `uv run pytest tests/core tests/commands`: Task 10; item 4 `src/superclaude` path grep: Task 13; item 5 PR via `/sc:pr-submit --monitor 3`: deliberately deferred, with the exact command, in the Constraints (plan:25), because this plan does not open the PR |
| Replacement of `test_no_issue_skill_or_command_added` | Task 9 (becomes `test_issue_command_and_skill_are_the_only_issue_primitives`) |
| Implementation-time smoke checks the design schedules | one smoke spawn per worker: Task 15 (source.md D19, section 20 item 7); one manual ClickUp claim against a test task: Task 16 (source.md section 12) |
| Final step running the FULL suite with every failure fixed or explained | Task 14: `uv run pytest`, `make lint`, `make verify-sync`, every failure fixed or recorded in `./artifacts/t14-failures.md` with master evidence. Caveat: Task 14 is the last code-verification task but not the last task; it runs before the three live-check tasks 15-17, an order that check round 1 required (its blocking finding F-01: the full suite must not sit behind smoke checks that may end pending). Task 16 re-runs `test_clickup_claim.py`, `make sync-dev`, `make verify-sync` and `make lint` (not the full `uv run pytest`) if it has to change the script or fixtures |

## 5. Staging and what is left

- Staged with `git add .dev/tasks` (staging only; nothing committed or pushed): the plan package `.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/` (plan, `source.md`, `return-contract.yaml`) and `.dev/tasks/issue-302-handoff/` (design report and this report).
- Not staged: the two check folders under `.dev/reflect/` and `docs/designs/sc-issue-command.md`. The always-staged rule covers `.dev/tasks/` only, and this task did not stage them.
- Files written by this resumed dispatch: the plan package's `return-contract.yaml`; this report; inside the round-2 check folder: `REPORT.md`, `return-contract.yaml`, appended `audit.log` rows (rows reconstructed from file times are marked as such), `adversarial/merged-verdict.yaml`, `adversarial/return-contract.yaml`, and under `adversarial/adversarial/`: `debate-transcript.md`, `invariant-probe.md`, `base-selection.md` (regenerated), `refactor-plan.md`, `merge-log.md`, appended `.work/pipeline.log` lines. Also `.work/r25-probe.md`, `.work/quant_score.py` and `quant-score.out`, `.work/refactor-plan-review.md`, `artifacts/render_report.py` and the two `artifacts/evidence-validator-*.md` files. One file was renamed: `base-selection.md` to `base-selection.partial-1240.md`, as the coordinator asked. Nothing was deleted. Nothing under `src/` or `tests/` was edited.
- Brief acceptance items not met as literally written: `progress.md` is not in the plan folder. `/sc:implement` creates it on its first run (section 1); writing it by hand could be misread as a run record.
- Left (not in this task):
  1. Optional, the coordinator's call: apply the F-01, F-14 and F-02/F-06/F-11/F-12 minors to the plan before execution (section 2). The workflow skill does not let the check edit the plan, so this would be a deliberate plan revision.
  2. Run `/sc:implement .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/TASK-WF-scIssueCommand-20261104-064713.md`.
  3. After that, in a new session: the live checks that will be pending on the first run (worker smoke spawns, ClickUp smoke claim with the variables exported beforehand, Task 17 item 4).
