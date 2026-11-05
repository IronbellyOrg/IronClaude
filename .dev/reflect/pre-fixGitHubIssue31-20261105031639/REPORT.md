# Reflection report (UC-1, pre-execution): issue 315 workflow plan

```yaml
contract_version: 1.8.0
status: success   # verdict ready-with-notes; evidence validator ran and dropped nothing (zero-drop-flag: true, audit-logged, not treated as proof of quality)
mode: pre
tier_reached: 2
confidence_calibrated: 0.76   # mean of the three reviewer-card calibrations (0.75, 0.78, 0.74); Tier-1 card was 0.50
citations_total: 42   # validator count: 25 file:line citation instances + 17 inferred quotes (the draft said 37)
citations_revalidated: 42
citations_dropped: 0
citations_inferred: 2
citation_budget_policy: full_reread
coverage_degraded: parsed-sparse
```

Spec: .dev/tasks/to-do/TASK-WF-fixGitHubIssue31-20261105-031410/source.md. Plan: .dev/tasks/to-do/TASK-WF-fixGitHubIssue31-20261105-031410/TASK-WF-fixGitHubIssue31-20261105-031410.md (11 tasks, 5 phases). Output folder: .dev/reflect/pre-fixGitHubIssue31-20261105031639/.

## Verdict

The plan is implementable and covers every requirement in the source (no spec span is taskless). It is ready with notes: one point blocks until a criterion is added (an invalid name must still start Claude), and eleven further required notes plus six executor notes come from the debate. The plan package itself is not edited (workflow rule); the notes in adversarial/merged-verdict.yaml are handed to the /sc:implement run.

How it was reached: Tier 1 card (calibrated 0.50, so it escalated; the parse-density guard also forced Tier 2 because the source has no numbered requirements), three reviewer cards (sonnet, haiku, opus classes), blind calibration of each card, adversarial debate at standard depth (convergence 0.8889, threshold 0.80), invariant probe (0 unaddressed HIGH), hybrid scoring (base: reviewer 1), merge.

## Inferred requirements (Pass 2)

17 inferred rows INF-001 to INF-017, each a verbatim quote of source.md:1; the matcher result is in artifacts/coverage-matrix.md. coverage_pct (parsed-only) is null (0 parsed IDs); coverage_pct_union 0.7059 by deterministic containment; the five misses (INF-007, INF-008, INF-014, INF-015, INF-016) are planned in Tasks 2, 4 and 7 and the plan Constraints, which the matcher does not read. No inferred row was dropped.

## Findings that matter (each [Grounded] with a re-Read citation unless marked)

### Deviation D-001: an invalid name makes ccsession exit before Claude starts (blocking until a criterion exists)
- **Location:** src/superclaude/skills/ccsession-tag/ccsession:1649-1650
- **Mapped tasklist item:** Task 3, Task 4
- **Spec section:** source.md:1 (CCSESSION_NAME; Ctrl+C and timer rules)
- **Evidence:** `TOPIC=$(validate_label "$NAME_ARG") || exit 2` (ccsession:1649-1650) under `set -e` (src/superclaude/skills/ccsession-tag/ccsession-orca:34 and src/superclaude/skills/ccsession-tag/ccsession:98); the header promises Claude never "ends up at a dead prompt" (src/superclaude/skills/ccsession-tag/ccsession-orca:20-24). Tasks 3 and 4 (plan lines 57 to 76) have no invalid-name case.
- **Classification:** regression (would break an existing guarantee)
- **Classification rationale:** a new path (CCSESSION_NAME, lifted --name, failing --auto-name) can end with no Claude start; all three advocates converged on blocking until the criterion exists.
- **Default remediation:** add RN-1 (fall back: drop the bad name with a warning, then auto-name, then untagged start) to Tasks 3 and 4 with the listed tests.

### Deviation D-002: --auto-name placed after the argument loop swallows option-shaped task text
- **Location:** src/superclaude/skills/ccsession-tag/ccsession:648-723 (loop) versus the early dispatch at ccsession:597-628
- **Mapped tasklist item:** Task 1
- **Classification:** drift; **Default remediation:** RN-3, dispatch in the early fast path; tests for `--model`, `--claude-args`, `--shim`, `--tier=x`.

### Deviation D-003: Task 5 contradicts itself and misses three tests
- **Location:** tests/unit/test_ccsession_tag.py:1801-1804 and tests/unit/test_ccsession_tag.py:1859-1863 (Enter reopen tests), tests/unit/test_ccsession_tag.py:1592-1610 (invalid-name test), tests/unit/test_ccsession_tag.py:1536-1559 (Ctrl+C test launches with "the prompt"), tests/unit/test_ccsession_tag.py:1494-1509 (saved-name test expects the question)
- **Mapped tasklist item:** Task 5 (plan line 84 says to keep the reopen tests "as they are")
- **Classification:** drift; **Default remediation:** RN-4.

### Deviation D-004: the typed-line safety net has shell-mechanics gaps
- **Location:** src/superclaude/skills/ccsession-tag/ccsession:1482 (`read -r` without IFS= trims a leading or trailing tab), src/superclaude/skills/ccsession-tag/ccsession:1426 (bash 3.2 has no `read -t 0`; a drain needs python3)
- **Mapped tasklist item:** Task 2, Task 4
- **Classification:** drift; **Default remediation:** RN-5 (IFS= read, raw control-character and 245-byte test, `--` before text starting with `-`) and EN-1 to EN-3.

### Deviation D-005: the timer default is not pinned by any criterion
- **Location:** src/superclaude/skills/ccsession-tag/ccsession:1471 (default 0) versus plan line 46 (criterion says both "no CCSESSION_ASK_TIMEOUT set" and "the test sets the limit to 1 second")
- **Mapped tasklist item:** Task 2, Task 6; **Classification:** drift; **Default remediation:** RN-8.

### Deviation D-006: README and classification drift for --session-id and the = forms
- **Location:** src/superclaude/skills/ccsession-tag/README.md:266 groups --session-id with the resume choices; src/superclaude/skills/ccsession-tag/ccsession-orca:75-76 already lists the `=` forms that Task 3 omits (`--prefill=*`, `--session-id=*`, `--from-pr=*`; Task 3 already has `--name=*`)
- **Mapped tasklist item:** Task 3, Task 9; **Classification:** drift; **Default remediation:** RN-7 and RN-12.

### Deviation D-007: a name equal to a saved label resumes that conversation
- **Location:** src/superclaude/skills/ccsession-tag/ccsession:1681-1706
- **Mapped tasklist item:** Task 3 (the --name lift); **Classification:** drift; **Default remediation:** RN-2 (do not lift Claude --name by default) and the RN-1 saved-label test.

### Reachability (invariant probe highlight)
- INV-001 (HIGH, addressed only as a documented condition): nothing in the repo makes an orchestrator pass a task or name, and a task typed after the question appears is read as a name (src/superclaude/skills/ccsession-tag/ccsession:1482-1489). Owner decision (a) accepts it; Tasks 9 and 11 must state it.

## Grounding Gaps

None written. [INFERRED] notes: (1) F3 of reviewer 1 (paste-timing race) and F8/F9 are inferred, not grounded; kept as executor notes only. (2) The hook-recording claim (A-002) rests on the advocates' reading of hooks/session-name.sh and is not re-run live.

## Degradations and limits (honest list)
- calibrator_diversity: degraded (all three model classes were reviewers; the calibrator for each card used a different class from its reviewer, not a class outside the reviewer set).
- Tier-1 card (Wave 1C) was written by the orchestrator, not by a root-cause or requirements agent.
- Executor class unresolved (executor_class_source: unknown); the anti-self-confirmation guarantee is weakened.
- The haiku alias resolves to glm-5.3 here (a non-Claude vendor), so t2_vendor_diversity is multi; its reviewer took about 24 minutes.
- Scoring counts came from agents, not a script; per-criterion re-evaluation of the two scoring passes was not run.
- Only the first-pass quantitative claims were spot-checked by the calibrators, not recomputed.
- The wave count of the debate is standard depth: Round 1, Round 2 (sequential), invariant probe; no Round 3.

## Inferred-claim audit
- `citations_inferred: 2`; inferred fraction 2 / 42 = 0.05. No WARN.

## Recommendations

### Recommendation R-001: add the invalid-name fallback to Tasks 3 and 4
- **File:** src/superclaude/skills/ccsession-tag/ccsession-orca (and Task 3/4 acceptance criteria)
- **Change:** an invalid CCSESSION_NAME, empty or failing --auto-name, or unexpected --ask status drops the name with a stderr warning and still starts Claude with status other than 2
- **Verifier:** tests in tests/unit/test_ccsession_tag.py with a leading-dot folder, a tab name, a 300-character CCSESSION_NAME, a name equal to a saved label: each reaches the fake Claude record
- **Linked deviation(s):** D-001, D-007
- **Priority:** P0

### Recommendation R-002: dispatch --auto-name early and fix the Task 5 test list
- **File:** src/superclaude/skills/ccsession-tag/ccsession (early case at 597-628); tests/unit/test_ccsession_tag.py
- **Change:** RN-3 and RN-4 of adversarial/merged-verdict.yaml
- **Verifier:** `uv run pytest tests/unit/test_ccsession_tag.py -k orca -v` passes; `ccsession --auto-name --model` prints a valid label
- **Linked deviation(s):** D-002, D-003
- **Priority:** P0

### Recommendation R-003: apply the remaining required notes RN-5 to RN-12
- **File:** src/superclaude/skills/ccsession-tag/ccsession, ccsession-orca, README.md, CHANGELOG.md
- **Change:** as listed in adversarial/merged-verdict.yaml
- **Verifier:** each note's acceptance_check in that file; `make lint`; the named pytest selectors
- **Linked deviation(s):** D-004, D-005, D-006
- **Priority:** P1

## Owner questions to carry into the pull request description
- OQ-1: print mode and CCSESSION_AUTOSTART=0 stay untagged (plan-author decision).
- OQ-2: the Claude --name lift is dropped (RN-2), reversing the plan Constraint.
- OQ-3: the dependency on orchestrators passing a task or name is documented, not enforced (INV-001).
