```yaml
contract_version: 1.8.0
status: partial
mode: pre
tier_reached: 2
confidence_calibrated: 0.81
citations_total: 74
citations_revalidated: 74
citations_dropped: 1
citations_inferred: 1
citation_budget_policy: full_reread
coverage_degraded: parsed-sparse
```

# Reflection report (pre-execution): plan `TASK-WF-design-20261108-041415`

- Spec: `.dev/tasks/to-do/TASK-WF-design-20261108-041415/source.md`
- Tasklist: `.dev/tasks/to-do/TASK-WF-design-20261108-041415/TASK-WF-design-20261108-041415.md`
- Run directory: `.dev/reflect/pre-design-20261108041729/`

## Verdict

The plan covers the design (union coverage 0.9455, 52 of 55 requirement rows matched), but it has one blocking gap: it never updates `tests/skills/test_worker_contract.py`, which will fail when the plan's tasks rewrite and add `gh api` lines. Ten smaller issues are listed below. Nothing in the plan was edited (reflect is advisory).

Tier 2 ran because the spec has no `R-`/`REQ-`/`SPEC-` ids (0 parsed against 55 inferred rows, so the Tier 1 stop is forbidden) and because the plan touches four areas (code, tests, docs, config). The Tier 1 card scored 0.31 under blind calibration (self-reported 0.92). Three reviewers of different model classes were calibrated at 0.81, 0.78 and 0.85, and the adversarial merge converged on all 15 diff points.

## Blocking finding

### M-F1: the plan breaks the exact-line classification table
- **Location:** `tests/skills/test_worker_contract.py:3006-3037`, `:3086-3093`
- **What the plan does:** Tasks 2, 3 and 5 rewrite `refs/create.md:9`, `SKILL.md:73-74` and `agents/issue-worker-t3.md:27`, and add new `gh api` lines.
- **Evidence:** the test keeps each of those lines word for word as a key and fails on any unclassified line and any stale key (`tests/skills/test_worker_contract.py:3129-3138`). A `gh api -X POST` line may not be classified read-only (`tests/skills/test_worker_contract.py:3150-3156`).
- **Why the plan misses it:** Task 12 runs only `tests/skills/test_issue_protocol.py`, and CI runs the whole suite.
- **Confirmed by:** reviewers 1 and 3 independently, all three advocates, and the calibrators.

## Minor findings

| ID | Finding | Evidence |
|---|---|---|
| M-F2 | Plan test runs omit `tests/commands/test_issue_command.py` and `tests/skills/test_issue_worker_agents.py`, which read the edited files | `tests/commands/test_issue_command.py:119-123`, `tests/skills/test_issue_worker_agents.py:93-105` |
| M-F3 | Task 8's new tests check prefixes and names, not exact output formats or the Q7/Q8 pairs; the weakness is inherited from the design | `TASK-WF-design-20261108-041415.md:122`, `source.md:114-116` |
| M-F4 | `complexity-field.json` has no template and is not named in Tasks 1 and 2 or in the command's Outputs row | `SKILL.md:52`, `commands/issue.md:78` |
| M-F5 | Nothing tells the T1/T2 workers (or the orchestrator) who fills the new `Issue type` row in `flags.md` | `templates/flags-decision.md:8-10` |
| M-F6 | Task 10's line list leaves out `docs/designs/sc-issue-command.md` line 331 (the orchestrator write list, no `--type` or POST) and line 330 (the `repos/<R>/` path rule); line 34 (rule B7, "fixed set") is covered only by Task 10's sentence "keep rule B7 true" | `docs/designs/sc-issue-command.md:331` |
| M-F7 | Task 8's `orgs/` scanner has no regex; the spaced spelling defeats `orgs/\S+` and prose mentions would be flagged | `TASK-WF-design-20261108-041415.md:122` |
| M-F8 | `SKILL.md:107` says "Print this block last" and a third block makes that more wrong (the ambiguity pre-dates the plan) | `SKILL.md:107` |
| M-F9 | The Will / Will Not test reads only `SKILL.md`, so Task 7's "keep unchanged" proves no agreement with the command file | `tests/skills/test_issue_protocol.py:527-541` |
| M-F10 | Constraint "writes exactly two things" is false: the plan keeps the mode label and the pushback comment | `TASK-WF-design-20261108-041415.md:23` |
| M-F11 | No new Task 8 test pins what Task 3 adds to `SKILL.md`, so the claim "reverting any of Tasks 1 to 5 turns a test red" fails for Task 3 | `TASK-WF-design-20261108-041415.md:122` |

[INFERRED] The GitHub field POST may need the `X-GitHub-Api-Version: 2026-03-10` header from GitHub's example; the plan does not name it. A wrong version would show up as a `not set` line, which the design treats as the safe failure.

## Inferred requirements (Pass 2)

55 rows were extracted from the spec (`INF-001` to `INF-055`), each pinned to a verbatim quote and a spec line. Verbatim quotes are in `artifacts/inf-rows.json`; the match for every row is in `artifacts/coverage-matrix.json` (rule: case-folded content-word containment of at least 0.6 against a single task). The table lists the spec line and the match.

| Row | Spec line | Match |
|---|---|---|
| INF-001 | source.md:15 | Task 2 (containment 0.7895) |
| INF-002 | source.md:15 | Task 1 (containment 0.8333) |
| INF-003 | source.md:16 | Task 1 (containment 0.8182) |
| INF-004 | source.md:16 | Task 1 (containment 0.6429) |
| INF-005 | source.md:18 | Task 2 (containment 1.0) |
| INF-006 | source.md:18 | Task 2 (containment 0.7857) |
| INF-007 | source.md:18 | Task 1 (containment 0.7143) |
| INF-008 | source.md:19 | Task 3 (containment 0.7) |
| INF-009 | source.md:19 | Task 1 (containment 0.7) |
| INF-010 | source.md:20 | Task 3 (containment 1.0) |
| INF-011 | source.md:21 | Task 1 (containment 1.0) |
| INF-012 | source.md:22 | Task 1 (containment 0.6667) |
| INF-013 | source.md:23 | Task 2 (containment 0.625) |
| INF-014 | source.md:32 | Task 2 (containment 1.0) |
| INF-015 | source.md:33 | Task 2 (containment 1.0) |
| INF-016 | source.md:34 | Task 1 (containment 1.0) |
| INF-017 | source.md:35 | Task 1 (containment 0.9231) |
| INF-018 | source.md:37 | Task 2 (containment 0.6667) |
| INF-019 | source.md:38 | Task 1 (containment 0.9286) |
| INF-020 | source.md:38 | Task 3 (containment 0.7333) |
| INF-021 | source.md:39 | Task 1 (containment 0.7857) |
| INF-022 | source.md:41 | Task 2 (containment 0.8889) |
| INF-023 | source.md:45 | Task 3 (containment 0.9091) |
| INF-024 | source.md:53 | Task 3 (containment 1.0) |
| INF-025 | source.md:57 | Task 2 (containment 0.9444) |
| INF-026 | source.md:58 | Task 3 (containment 1.0) |
| INF-027 | source.md:59 | Task 3 (containment 0.9091) |
| INF-028 | source.md:60 | Task 1 (containment 0.7857) |
| INF-029 | source.md:60 | Task 1 (containment 0.9167) |
| INF-030 | source.md:66 | Task 2 (containment 0.9286) |
| INF-031 | source.md:79 | none (best Task 1, 0.1667) |
| INF-032 | source.md:81 | none (best Task 2, 0.5714) |
| INF-033 | source.md:77 | Task 1 (containment 0.75) |
| INF-034 | source.md:86 | Task 12 (containment 0.7273) |
| INF-035 | source.md:92 | Task 1 (containment 1.0) |
| INF-036 | source.md:93 | Task 2 (containment 0.7273) |
| INF-037 | source.md:94 | Task 3 (containment 0.6667) |
| INF-038 | source.md:95 | Task 6 (containment 0.8) |
| INF-039 | source.md:96 | Task 5 (containment 0.9) |
| INF-040 | source.md:97 | Task 2 (containment 1.0) |
| INF-041 | source.md:98 | Task 2 (containment 1.0) |
| INF-042 | source.md:99 | Task 4 (containment 0.8) |
| INF-043 | source.md:100 | Task 10 (containment 0.8333) |
| INF-044 | source.md:101 | Task 11 (containment 1.0) |
| INF-045 | source.md:103 | none (best Task 4, 0.5556) |
| INF-046 | source.md:107 | Task 7 (containment 1.0) |
| INF-047 | source.md:111 | Task 1 (containment 0.9231) |
| INF-048 | source.md:112 | Task 8 (containment 1.0) |
| INF-049 | source.md:113 | Task 1 (containment 0.9231) |
| INF-050 | source.md:114 | Task 8 (containment 1.0) |
| INF-051 | source.md:115 | Task 2 (containment 1.0) |
| INF-052 | source.md:116 | Task 1 (containment 0.9167) |
| INF-053 | source.md:117 | Task 8 (containment 1.0) |
| INF-054 | source.md:119 | Task 12 (containment 1.0) |
| INF-055 | source.md:130 | Task 12 (containment 0.875) |

Unmapped by the rule: INF-031 (POST error codes), INF-032 (`gh issue create` failure stays a STOP) and INF-045 ("Not changed" list). Reviewers 1 and 3 confirmed they are covered by Tasks 1 to 3 and the plan Constraints, so they are matcher limits, not dropped requirements. Per-row task ids are word matches, not proof of coverage.

## Grounding Gaps (dropped citations)

This section lists citations the evidence-validator did not accept. It is not a hunk gap, so no `grounding-gaps.yaml` was created and `needs_human_decision` stays false.

- **Dropped:** `tests/skills/test_worker_contract.py:3133-3138`, cited in M-F1 for "fails on any unclassified line and any stale key". That range holds only the stale-key test. The unclassified-line test is at `:3129-3130` (checker at `:2005-2012`). The report text was corrected to `:3129-3138`, and the drop is still counted in `citations_dropped`, which forces `status: partial`.
- **Weak support, kept:** `tests/commands/test_issue_command.py:119-123` (the test reads the command file, but the rows Task 6 edits are at `:105-117`), `templates/flags-decision.md:8-10` (shows where the row goes, not who fills it), and `docs/designs/sc-issue-command.md:331`.

## Calibration and ensemble

| Item | Value |
|---|---|
| Tier 1 card, blind calibration | 0.31 (self-reported 0.92); recommendation: escalate |
| Reviewer 1 (sonnet, analyzer) | 0.81 |
| Reviewer 2 (haiku, qa) | 0.78 |
| Reviewer 3 (opus, refactorer) | 0.85 |
| Calibrator | opus; `calibrator_diversity: degraded` (all three classes were reviewers) |
| Vendor diversity | `single` (Anthropic only) |
| Base after the debate | variant 3, combined score 0.847 (variant 1 0.804, variant 2 0.639) |
| Convergence | 1.00 on 15 points, depth quick (one round) |

## Recommendations

### Recommendation R-001: add a task that updates the exact-line classification table
- **File:** `tests/skills/test_worker_contract.py`
- **Change:** rebuild the four changed keys and add a key for every new `gh api` line from the post-edit text; classify GET lookups read-only and POST lines never-worker.
- **Verifier:** `uv run pytest tests/skills/test_worker_contract.py -k "classified or stale or read_only" -v` passes.
- **Linked deviation(s):** M-F1
- **Priority:** P0

### Recommendation R-002: run the neighbouring test files in Task 6 and Task 12
- **File:** the plan, Tasks 6 and 12
- **Change:** run `uv run pytest tests/skills/ tests/commands/test_issue_command.py -v` (or `make test`) and state that only the Meaning column of the `--mode` and `--type` rows changes.
- **Verifier:** the same command passes after the edits.
- **Linked deviation(s):** M-F2
- **Priority:** P1

### Recommendation R-003: tighten Task 8
- **File:** the plan, Task 8
- **Change:** assert the full output formats and the Q7/Q8 pairs, fix the `orgs/` regex with a prose-guard self-check, and add one test for the wording Task 3 adds.
- **Verifier:** changing a separator, swapping Simple and Complex, or reverting Task 3's wording turns a new test red.
- **Linked deviation(s):** M-F3, M-F7, M-F11
- **Priority:** P1

### Recommendation R-004: name and place `complexity-field.json`
- **File:** the plan, Tasks 1, 2, 3 and 6
- **Change:** name `.dev/issues/<N>/complexity-field.json`, extend the template exception at `SKILL.md:52`, add the file to the Outputs row at `commands/issue.md:78`.
- **Verifier:** grep for `complexity-field` finds it in the four edited files.
- **Linked deviation(s):** M-F4
- **Priority:** P1

### Recommendation R-005: fix the remaining wording gaps
- **File:** the plan, Constraints and Tasks 2, 7 and 10
- **Change:** scope the "two writes" constraint to classification writes; say who fills the `Issue type` row; add the two doc lines; add assertions that read the command file; reword `SKILL.md:107`.
- **Verifier:** the plan's Constraints and Task 2 describe the same allowed writes; `grep "fixed set"` in `docs/designs/sc-issue-command.md` returns nothing.
- **Linked deviation(s):** M-F5, M-F6, M-F8, M-F9, M-F10
- **Priority:** P2

## Inferred-claim audit

- `citations_inferred: 1`
- Inferred-fraction: 1 / 74 = 0.01

## Not done in this run

- Codegraph was not used (index state not checked); the Grep/Read floor was used.
- The position-bias second pass of the adversarial scoring was not run independently.
- The executor class was not resolved (`executor_class_resolved: false`), so the executor-versus-reviewer separation is not guaranteed.
- No GitHub behaviour was tested; the design's API claims remain UNVERIFIED.
