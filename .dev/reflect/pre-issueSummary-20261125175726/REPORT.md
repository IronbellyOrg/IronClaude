# Reflect Report: pre-execution review of TASK-WF-issueSummary-20261125-175231

```yaml
contract_version: 1.9.0
status: success                    # the review ran and the evidence gate passed; the plan's verdict is FAIL (see Verdict)
mode: pre
tier_reached: 2
confidence_calibrated: 0.76
citations_total: 141               # 100 file:line items and checkable counts, plus the 41 inferred rows
citations_revalidated: 141
citations_dropped: 0
citations_inferred: 3
citation_budget_policy: full_reread   # the validator re-read all 141 although the count would allow sampling
coverage_degraded: parsed-sparse
```

## Verdict

**FAIL.** The plan has 5 blocking defects, 5 medium ones and 3 notes (13 rows). It is not safe to hand to `/sc:implement` as written. The code change itself is sound: one forced `export` between `ccsession:2438` and `ccsession:2440` reaches all six places that start Claude. The blocking defects are all in the checks around it:

- No task runs the full test suite or the project lint gate that the spec requires (row 1).
- Nothing connects the changed launcher to the launcher the live check observes (row 2).
- Task 6's environment check can pass on any terminal launch, not the coordinator's own process (row 3).
- The wrapper test the plan prescribes contradicts the plan's own "capture only one variable" rule (row 4).
- Raw-resume launches, which the spec asks to cover and which are how Orca resumes a coordinator, have no test case (row 5).

Plan under review: `.dev/tasks/to-do/TASK-WF-issueSummary-20261125-175231/TASK-WF-issueSummary-20261125-175231.md` (6 tasks). Spec: the `source.md` beside it (38 lines). The merged review card is `adversarial/merged-review-card.md`.

## How the review ran

- Tier 2. The spec has no labelled requirement ids (Pass 1 found 0), so the sparse-labelling guard forbade a Tier 1 stop, and three domains (code, tests, docs) also trigger Tier 2 (`artifacts/tier_decision.yaml`, rule 4).
- First pass: an inline card (`t1-card.md`), blind-calibrated at C 0.76.
- Two read-only reviewers on different model classes: analyzer on the haiku-alias model, qa on the opus-alias model. The sonnet class, which wrote the plan, was excluded from the reviewer pool and used as the calibrator (the three-way separation is therefore only partly met). Reviewer 1's self-report names an OpenAI model, so that alias is a non-Anthropic model even though the alias-name check said "single vendor". Calibrated C: 0.76 and 0.77.
- Adversarial merge (`/sc:adversarial`, standard depth): 2 debate rounds, an invariant probe, base selection (reviewer 2's card won, 0.82 against 0.70), a refactor plan and a merge by a separate agent. Convergence 16 of 18 points (0.8889). The probe found no HIGH unaddressed invariant. One dispute (the grade of the help-notice defect, row 6) was settled by a judge ruling at Medium.
- The first spawn of the reviewers used the `name` field, which made them mailbox teammates that never ran; they were stopped and respawned as plain background agents with identical prompts (`audit.log`).

## Coverage

- 41 requirement rows were inferred from the spec by an independent agent (`artifacts/inferred-requirements.json`); all 41 quotes were checked as exact substrings of their cited spec lines.
- The deterministic word-overlap matcher placed 19 of 41 rows on a task (`coverage_pct_union` 0.4634, `S_dev_density` 0.5366). It under-counts: most unmatched rows are covered in meaning by the plan's Constraints (for example the Part 2 exclusion, the base branch, no role inference), and 7 rows are effort estimates that place no requirement on the plan.
- Rows with a real gap: INF-041 (broader gates, row 1), INF-002, INF-004 and INF-009 (live coordinator proof, fresh and resumed verification, rows 2 and 3), INF-023 (raw-resume coverage, row 5), and `source.md:25` (capture only the named switch, row 4). Of 35 requirement-bearing units, 29 are adherent and 6 are not.
- Full matrix: `artifacts/coverage-matrix.yaml`.

## Deviations

All 13 are Drift (a plan statement that omits or contradicts a spec requirement or the plan's own constraint, with no inline rationale). Grades follow the consequence, not the Severity label. Fix sentences are in `adversarial/merged-review-card.md`. `PLAN` is `.dev/tasks/to-do/TASK-WF-issueSummary-20261125-175231/TASK-WF-issueSummary-20261125-175231.md`; `SPEC` is `source.md` in the same folder.

### Deviation D-001: the full test suite and the project lint gate are never run (Blocking (Missing))

- **Location:** `PLAN:76-77`, `PLAN:89`
- **Mapped tasklist item:** Task 4, Task 5
- **Spec section:** `SPEC:32`
- **Evidence:** "Run the three targeted test files, the required broader regression/lint/format gates and sync checks" (`SPEC:32`). `uv run pytest` is the `test:` target (`Makefile:15`); `lint: lint-architecture` (`Makefile:48`) adds the architecture check. `tests/core/test_orca_session_launch_guidance.py:15-16` reads the README section starting `### Orca session launches`, and `:52` requires the paragraph after `commands' internal Agent-tool subagents.` to start with "Every Orca worktree gets an agent".
- **Classification:** Drift
- **Classification rationale:** a required step named by the spec is absent in substance. The plan runs three test files (`PLAN:76`), repo-wide Ruff (`PLAN:77`) and `make verify-sync` (`PLAN:89`). 21 test files mention ccsession (case-sensitive count; 24 case-insensitive), so most run nowhere. The README break is conditional. The test reads the README from line 409 (`### Orca session launches`) to the next `## ` heading (line 613), requires the paragraph after line 418 (`commands' internal Agent-tool subagents.`) to be the one at lines 420-426, and forbids the phrase "coordinator under another orchestrator" anywhere in that span. A sentence inserted between lines 418 and 420, or new text in that span that uses the forbidden phrase, would pass every plan check and fail the suite; lines 392-408 lie before the span and are safe. (The evidence validator pointed out that only lines 418-426 are pinned that tightly; the earlier "409-426" wording was wider than the test.)
- **Default remediation:** add `uv run pytest`, `make lint` and `uv run ruff format --check .` to Task 5's acceptance criteria, each compared with a baseline run before Task 2.

### Deviation D-002: nothing connects the changed launcher to the launcher the live check observes (Blocking (Missing))

- **Location:** `PLAN:98`, `PLAN:101`, `PLAN:22`
- **Mapped tasklist item:** Task 6 (and Constraint `PLAN:22`)
- **Spec section:** `SPEC:31`
- **Evidence:** `ccsession-orca:54` sets `CCSESSION="$(cd "$(dirname "$_self")" && pwd)/ccsession"`, the launcher next to the wrapper's own resolved path. `install_ccsession.py:71` links with `link.symlink_to(script)`. `install_skills.py:102` skips an existing skill with `if skill_target.exists() and not force:`. Constraint `PLAN:22` says "`wire_ccsession` copies the launcher unchanged".
- **Classification:** Drift
- **Classification rationale:** the check at `PLAN:101` rests on a prerequisite no task establishes. `wire_ccsession` links; it does not copy the launcher. A plain `superclaude install` leaves an existing installed skill as it is; only `superclaude update` (`main.py:402`), `install --force`, `update.sh` or the skill's own `install.sh` replace it, host-wide.
- **Default remediation:** before Task 6 collects evidence, record which launcher the process runs and show it holds the export, by launching the checkout's launcher by absolute path or after an owner-authorised refresh the plan names; correct `PLAN:22`.
- **[INFERRED] notes:** [INFERRED] the installed launcher on this host may still lack the export; its contents were not read.

### Deviation D-003: Task 6's environment check does not require the coordinator's own process (Blocking (Decision))

- **Location:** `PLAN:98`, `PLAN:101-102`
- **Mapped tasklist item:** Task 6
- **Spec section:** `SPEC:7`, `SPEC:31`
- **Evidence:** "the new coordinator process starts with the switch set" (`SPEC:7`). `PLAN:98` allows "in an existing terminal or the owner's relaunched coordinator". `PLAN:101` asks only for "the single matching environment line" for the fresh and the resumed launch. `PLAN:102` gives the message check, not this check, a "not run" outcome.
- **Classification:** Drift
- **Classification rationale:** the acceptance check can pass while the real coordinator, for example one whose Orca command is plain `claude`, lacks the switch, which contradicts the Goal at `PLAN:15`. The `grep -x '...=1'` line also appears when the parent shell already held `=1`, and a coordinator started before the change shows no line, which is neither "unavailable" nor a failure.
- **Default remediation:** require the line from the coordinator's own PID after fresh and resumed launches that started after the change, with PID, start time and launch route recorded, a `0` set in the launching shell for one launch, and the "not run, partial" outcome for this check too.

### Deviation D-004: the prescribed wrapper test fake contradicts the plan's own capture rule (Blocking (Decision))

- **Location:** `PLAN:60`, `PLAN:66`, `PLAN:26`
- **Mapped tasklist item:** Task 3
- **Spec section:** `SPEC:25`
- **Evidence:** the `_orca_env` fake already records `'env_names': sorted(os.environ),` (`tests/unit/test_ccsession_tag.py:1838`). `PLAN:66` says "only the one named variable is captured".
- **Classification:** Drift
- **Classification rationale:** following Task 3 as written makes its own criterion false. Names only, no secret values, so it is not a Safety finding.
- **Default remediation:** give the new wrapper tests their own fake Claude that writes `FAKE_CLAUDE_RECORD` with the arguments and the one switch, passed as `CLAUDE_BIN` through `_orca_env`'s extra arguments.

### Deviation D-005: raw-resume launches have no test case (Blocking (Missing))

- **Location:** `PLAN:60`, `PLAN:63`
- **Mapped tasklist item:** Task 3
- **Spec section:** `SPEC:21`
- **Evidence:** "Cover untagged/raw-resume, labeled resume and new-label launches, both with and without an explicit model." (`SPEC:21`). `tests/unit/test_ccsession_tag.py:1489` asserts `assert ("--resume" in launched) == transcript` over `_LAUNCH_CASES`. `ccsession-orca:90` sets `resume_like=1` for `--resume`.
- **Classification:** Drift
- **Classification rationale:** the plan's 20-case check can pass without a raw `--resume <id>` input, which is how Orca resumes a coordinator. The export position is not in doubt; the missing item is the coverage the spec names. Appending raw-resume cases to `_LAUNCH_CASES` would break the assertion at line 1489, and `PLAN:63` is an exact count that must be restated.
- **Default remediation:** add a separate raw-resume case list (`--resume <id>` with and without `--profile claude`, across the three starting states), make the wrapper's untagged case `--resume <id>` with no carried name, and restate the total.

### Deviation D-006: the `--help` header line is placed where `--help` never prints (Medium)

- **Location:** `PLAN:46`, `PLAN:51-52`
- **Mapped tasklist item:** Task 2
- **Spec section:** n/a (the spec does not mention help output)
- **Evidence:** `PLAN:46` says the line is added "so `ccsession --help` readers see it". `show_help` runs `awk 'NR >= 2 { if ($0 ~ /^# The wrapper always runs/) exit; sub(/^# ?/, ""); print }' "$0"` (`ccsession:2271`), and `# The wrapper always runs claude with --allowedTools=Grep and, unless` is line 143 (`ccsession:143`).
- **Classification:** Drift
- **Classification rationale:** the stated reason is false, but nothing the plan or spec rests on reads the help line, so it is a defect without a consumer. The two reviewers split between Blocking (Decision) and Medium; the judge ruled Medium.
- **Default remediation:** place the line above line 143, add "the `--help` output contains it" to the criteria and carve it out of `PLAN:52`; or drop the claim.

### Deviation D-007: the route trace leaves out the tab-reopen execs (Medium)

- **Location:** `PLAN:33`
- **Mapped tasklist item:** Task 1
- **Spec section:** `SPEC:23`
- **Evidence:** `exec "$CCSESSION" --name "$name" --shim --claude-args "$@"` is at `ccsession-orca:186` and `exec "$CCSESSION" --shim --claude-args "$@" --resume "$session"` at `ccsession-orca:189`; the plan names lines 261 and 263 only.
- **Classification:** Drift
- **Classification rationale:** both execs still reach ccsession, so protection holds; the scope record is incomplete.
- **Default remediation:** add both execs to Task 1's trace.

### Deviation D-008: Task 1's cited line numbers go stale after Task 2 (Medium)

- **Location:** `PLAN:33`, `PLAN:38`, `PLAN:46`
- **Mapped tasklist item:** Task 1, Task 2
- **Spec section:** n/a
- **Evidence:** `PLAN:38` requires every cited line to match "the live file"; Task 2 inserts lines at `ccsession:2438-2440` (`PLAN:46`), which moves the six exec lines the artifact lists.
- **Classification:** Drift
- **Classification rationale:** the criterion is true only at the moment Task 1 finishes.
- **Default remediation:** cite commit `a6fec24` or anchor each line by its text.

### Deviation D-009: `make verify-sync` has tool dependencies outside the baseline (Medium)

- **Location:** `PLAN:89`
- **Mapped tasklist item:** Task 5
- **Spec section:** `SPEC:32`
- **Evidence:** `Makefile:309` runs `uv run python -c "from superclaude.cli.install_hooks import _FRESHNESS_SCRIPTS; ...`, and `Makefile:329` runs `jq -r '.hooks.PostToolUse[].matcher // empty'`.
- **Classification:** Drift
- **Classification rationale:** if either tool is missing the target reports drift regardless of this change.
- **Default remediation:** run `make sync-dev` and `make verify-sync` once before Task 2 and record the result as the baseline.

### Deviation D-010: the Ruff criterion names two files but the commands cover the project (Medium)

- **Location:** `PLAN:77`
- **Mapped tasklist item:** Task 4
- **Spec section:** `SPEC:32`
- **Evidence:** `PLAN:77` says the two Ruff commands "report nothing for the two changed test files" and gives no path argument; `pyproject.toml:177-182` holds the exclusions (`docs/`, `.dev/`).
- **Classification:** Drift
- **Classification rationale:** a pre-existing finding elsewhere would fail the check for a reason unrelated to this change.
- **Default remediation:** scope both commands to the two files, or keep them repo-wide and compare with the baseline.

### Deviation D-011: the `git status` check cannot show ignored mirror changes (Note)

- **Location:** `PLAN:89`
- **Mapped tasklist item:** Task 5
- **Spec section:** n/a
- **Evidence:** `.gitignore:127` is `.claude/*` and `.gitignore:128` is `!.claude/settings.json`; `PLAN:89` says `git status --short` "shows no path under `.claude/` other than the already tracked `.claude/settings.json`".
- **Classification:** Drift
- **Classification rationale:** ignored files never appear in `git status`; the real guard is `make verify-sync` in the same criterion.
- **Default remediation:** describe the status check as covering only files git does not ignore.

### Deviation D-012: the spec's relative links do not resolve in the package (Note)

- **Location:** `SPEC:37-38`
- **Mapped tasklist item:** n/a
- **Spec section:** `SPEC:37`
- **Evidence:** `SPEC:37` links `analysis/analyze-ccsession.md`; the package holds no `analysis/` folder (the original is `.dev/issues/765/analysis/analyze-ccsession.md`).
- **Classification:** Drift
- **Classification rationale:** form only; no task depends on the link.
- **Default remediation:** copy the analysis into the package or use paths that resolve from it.

### Deviation D-013: a count in one reviewer card was wrong (Note)

- **Location:** `reviewer-cards/reviewer-2-card.md:11`
- **Mapped tasklist item:** n/a
- **Spec section:** n/a
- **Evidence:** the card says "16 test files mention ccsession and only 3 are run"; the orchestrator's count is 21 (case-sensitive) and 24 (case-insensitive).
- **Classification:** Drift
- **Classification rationale:** a wrong number on a true statement; it supports D-001 and is not an acceptance number.
- **Default remediation:** state the counting rule or drop the number.

## Inferred requirements (Pass 2)

Pass 1 (id regex) found 0 labelled requirements. Pass 2 (the requirements-analyst agent) enumerated 41 rows from `source.md`; every quote below is an exact substring of its cited line (checked by script, then by the evidence validator). "Match result" is the deterministic word-overlap result first, then the orchestrator's note on who owns the row in substance. `PLAN:19-27` are the plan's Constraints.

| INF id | Verbatim quote | Citation | Match result |
|---|---|---|---|
| INF-001 | Effort estimate: 8 hours | `source.md:6` | none by word overlap; an estimate, not a plan requirement |
| INF-002 | the new coordinator process starts with the switch set | `source.md:7` | Task 5 by word overlap; owned in substance by Task 6, gap in D-003 |
| INF-003 | launch tests cover the chosen scope | `source.md:7` | Task 2 by word overlap; owned in substance by Tasks 3 and 4 |
| INF-004 | live proof verifies the environment and message delivery | `source.md:7` | Task 5 by word overlap; owned in substance by Task 6, gap in D-002 and D-003 |
| INF-005 | start every coordinator's Claude process with `CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1` in its initial environment, so Claude Code's low-memory background-command cleanup cannot kill its message watch. | `source.md:11` | Task 5 by word overlap; owned in substance by Task 2 (the export) |
| INF-006 | Change the ccsession launcher | `source.md:11` | Task 1 by word overlap; owned in substance by Task 2 |
| INF-007 | record whether protection covers coordinators only or all ccsession launches | `source.md:11` | none by word overlap; Task 1 and Task 5 |
| INF-008 | document the session-wide effect and the need to launch a new process | `source.md:11` | Task 5 |
| INF-009 | verify fresh and resumed launches | `source.md:11` | none by word overlap; Tasks 3 and 6, gaps in D-003 and D-005 |
| INF-010 | Part 2 is dropped entirely, including research, guard, sampler, browser stops and the eight plan problems; none belongs in this plan or estimate. | `source.md:11` | none by word overlap; `PLAN:19` |
| INF-011 | Use `origin/integration`, not the old body's `master` | `source.md:11` | none by word overlap; `PLAN:20` |
| INF-012 | Recommend all ccsession launches because there is no verified coordinator-role signal in the launcher | `source.md:13` | Task 1 |
| INF-013 | The plan must record its decision | `source.md:13` | Task 1 |
| INF-014 | ensure a conflicting inherited or env-file value cannot leave a protected coordinator without `=1` | `source.md:13` | none by word overlap; `PLAN:24`, Task 2 and Task 3 criteria |
| INF-015 | do not treat earlier suggestions to respect overrides as owner approval to weaken the final requirement | `source.md:13` | none by word overlap; `PLAN:24` |
| INF-016 | Direct `ic` and bare Claude launches bypass ccsession, so verify the actual coordinator launch route rather than claiming universal coverage. | `source.md:13` | Task 1 |
| INF-017 | 2 hours to trace the real route and record scope/override policy | `source.md:15` | Task 1; an estimate, not a plan requirement |
| INF-018 | 1 hour for the shared export and README | `source.md:15` | none; an estimate, not a plan requirement |
| INF-019 | 2 hours for branch/configuration regression tests | `source.md:15` | none; an estimate, not a plan requirement |
| INF-020 | 1 hour for checks and synchronization | `source.md:15` | none; an estimate, not a plan requirement |
| INF-021 | 2 hours for live launch/message evidence and recording limitations | `source.md:15` | none; an estimate, not a plan requirement |
| INF-022 | The earlier 32-hour complex estimate included the now-dropped research and no longer applies | `source.md:15` | none; an estimate, not a plan requirement |
| INF-023 | Cover untagged/raw-resume, labeled resume and new-label launches, both with and without an explicit model. | `source.md:21` | none; gap D-005 |
| INF-024 | the shared pre-exec location after 2438 and before 2440 reaches all six Claude exec sites | `source.md:21` | Task 2 |
| INF-025 | do not infer roles from labels | `source.md:22` | none by word overlap; `PLAN:23` |
| INF-026 | Verify the coordinator's actual configuration during live proof. | `source.md:23` | Task 5 by word overlap; owned in substance by Task 6, gap in D-002 and D-003 |
| INF-027 | Add scope, session-wide effect, override behavior, bypasses and treatment of existing sessions. | `source.md:24` | none by word overlap; Task 5 |
| INF-028 | Add coverage for unset/conflicting shell and env-file values, new/resumed and tagged/untagged launches, and the chosen scope. | `source.md:25` | Task 3 |
| INF-029 | Extend targeted capture to prove tier/model/profile selection does not remove protection. | `source.md:26` | none by word overlap; Task 4 |
| INF-030 | Keep tests isolated from developer environment values. | `source.md:26` | Task 3 |
| INF-031 | Run alongside the two launch-test files | `source.md:27` | Task 4 |
| INF-032 | installer changes are not required by the recommended launch-only approach | `source.md:27` | none by word overlap; `PLAN:22` (its wording about `wire_ccsession` is wrong, D-002) |
| INF-033 | no settings change is planned | `source.md:28` | Task 6 by word overlap; owned in substance by `PLAN:22` |
| INF-034 | Document this boundary | `source.md:29` | none by word overlap; Task 5 |
| INF-035 | do not expand this issue into unrelated launcher work without a scope decision | `source.md:29` | none by word overlap; `PLAN:25` |
| INF-036 | Preserve the contract; the fix is launch-time environment, not automatic watch restart. | `source.md:30` | none by word overlap; `PLAN:22` |
| INF-037 | Check only the exact switch in `/proc/<pid>/environ`, never the full environment | `source.md:31` | Task 6 |
| INF-038 | verify receipt and watch renewal across at least two five-minute cycles | `source.md:31` | Task 6 |
| INF-039 | Do not force memory pressure on the shared host. | `source.md:31` | Task 6 |
| INF-040 | Implement in `src/`, not generated `.claude/` mirrors. | `source.md:32` | none by word overlap; `PLAN:21` |
| INF-041 | Run the three targeted test files, the required broader regression/lint/format gates and sync checks | `source.md:32` | none; gap D-001 |

## Inferred-claim audit

- `citations_inferred: 3` (the three `[INFERRED]` notes: D-002's installed-launcher note and the two inheritance and runtime-switch lines under Not verified).
- Inferred fraction: `3 / 141` = 0.02. The WARN threshold (more than 20 citations and more than half inferred) is not reached.
- Zero-drop flag: the evidence validator dropped nothing (`zero-drop-flag: true` in `audit.log`). It re-read every citation itself, including a second pass over the merged card's 79 citations, and its notes record the one wording point corrected in D-001. A zero-drop pass on a report of this size is a flag for later spot-checks, not proof of perfection.

## Recommendations

Ordered P0 first. Each names the file, the change and the check that confirms it. The plan author revises the plan (Wave 4R of `/sc:workflow` does this for blocking findings); nothing here edits product code.

### Recommendation R-001: add the full suite and the lint gate to Task 5

- **File:** `.dev/tasks/to-do/TASK-WF-issueSummary-20261125-175231/TASK-WF-issueSummary-20261125-175231.md` (Task 5 acceptance criteria, after `PLAN:89`)
- **Change:** add `uv run pytest`, `make lint` and `uv run ruff format --check .` (not `make format`) as "no new failure compared with a baseline run before Task 2 at the recorded commit", and keep the README cross-reference in README lines 392-408.
- **Verifier:** `grep -n "uv run pytest" <plan>` finds the new criterion; `uv run pytest tests/core/test_orca_session_launch_guidance.py` passes after the README edit.
- **Linked deviation(s):** D-001, D-009, D-010
- **Priority:** P0

### Recommendation R-002: make Task 6 name and prove the launcher it observes

- **File:** same plan (Task 6, `PLAN:98`; Constraints, `PLAN:22`)
- **Change:** require the executor to record which launcher the process runs and show it contains the export, by launching the checkout's launcher by absolute path or after an owner-authorised refresh the plan names; correct `PLAN:22` to say `wire_ccsession` links the installed launcher.
- **Verifier:** Task 6's artifact `./artifacts/live-proof.md` lists the launcher path and a grep of that file for `CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1`; re-read `PLAN:22`.
- **Linked deviation(s):** D-002
- **Priority:** P0

### Recommendation R-003: tie the environment check to the coordinator's own process

- **File:** same plan (Task 6 criterion `PLAN:101`, and `PLAN:102`)
- **Change:** require the exact switch line from the coordinator's own Claude PID after a fresh and a resumed launch that started after the change, with PID, start time and launch route recorded, a `0` set in the launching shell for one launch, terminal launches as supporting evidence only, and the "not run, partial" outcome for this check too.
- **Verifier:** the revised criterion text names the coordinator's PID; the live-proof file has a PID and a start time later than the change.
- **Linked deviation(s):** D-003
- **Priority:** P0

### Recommendation R-004: give the wrapper tests their own switch-only fake

- **File:** same plan (Task 3, `PLAN:60`, `PLAN:66`); `tests/unit/test_ccsession_tag.py`
- **Change:** the new wrapper tests use their own fake Claude that writes `FAKE_CLAUDE_RECORD` with the arguments and the one switch, passed as `CLAUDE_BIN` through `_orca_env`'s extra arguments; the shared record at lines 1833-1839 stays as it is.
- **Verifier:** `uv run pytest tests/unit/test_ccsession_tag.py -k reap -v` passes, and no new test reads `env_names`.
- **Linked deviation(s):** D-004
- **Priority:** P0

### Recommendation R-005: add raw-resume cases and restate the count

- **File:** same plan (Task 3, `PLAN:60`, `PLAN:63`); `tests/unit/test_ccsession_tag.py`
- **Change:** add a separate raw-resume case list (`--resume <id>` with and without `--profile claude`, across the three starting states), make the wrapper's untagged case `--resume <id>` with no carried name and assert no `--name`, and write the new total in `PLAN:63`.
- **Verifier:** the case count in `-k reap -v` output equals the number written in `PLAN:63`; `test_every_launch_restores_grep_and_glob` still passes.
- **Linked deviation(s):** D-005
- **Priority:** P0

### Recommendation R-006: fix or drop the `--help` header line

- **File:** same plan (Task 2, `PLAN:46`, `PLAN:52`); `src/superclaude/skills/ccsession-tag/ccsession`
- **Change:** place the line above line 143, add "the `--help` output contains it" to the criteria and carve it out of `PLAN:52`; or drop the claim.
- **Verifier:** `ccsession --help | grep CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP` finds the line, or `PLAN:46` no longer mentions help readers.
- **Linked deviation(s):** D-006
- **Priority:** P1

### Recommendation R-007: complete the route trace and make its line numbers durable

- **File:** same plan (Task 1, `PLAN:33`, `PLAN:38`)
- **Change:** add the tab-reopen execs at `ccsession-orca:186` and `:189`, and cite commit `a6fec24` or anchor each line by its text.
- **Verifier:** `./artifacts/scope-decision.md` names both execs and states the commit.
- **Linked deviation(s):** D-007, D-008
- **Priority:** P1

### Recommendation R-008: baseline `verify-sync` and scope the Ruff criterion

- **File:** same plan (Task 4 `PLAN:77`, Task 5 `PLAN:89`)
- **Change:** run `make sync-dev` and `make verify-sync` once before Task 2 and record the result; scope the two Ruff commands to the two changed files or compare repo-wide results with the baseline; describe the `git status` check as covering only files git does not ignore.
- **Verifier:** the plan has a before-Task-2 baseline step and the Ruff criterion names its scope.
- **Linked deviation(s):** D-009, D-010, D-011
- **Priority:** P2

### Recommendation R-009: repair the spec links

- **File:** the package folder `.dev/tasks/to-do/TASK-WF-issueSummary-20261125-175231/` (its `source.md` stays a byte-exact snapshot of the issue summary and is not edited)
- **Change:** copy `analysis/analyze-ccsession.md` and `accuracy-check.md` from `.dev/issues/765/` into the package at the paths `source.md:37-38` link to.
- **Verifier:** the two links open from inside the package folder.
- **Linked deviation(s):** D-012
- **Priority:** P2

## Not verified

- [INFERRED] Whether Claude Code passes `CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP` on to the processes a protected session starts (inheritance). Nobody checked it against Claude Code; it is not a table row.
- [INFERRED] That the real Claude Code runtime honours the switch as the spec describes. Not re-proved by this review.
- The installed launcher's current contents, the coordinator's Orca configuration and live access: not read.
- Whether any `.claude/` file besides `settings.json` is tracked by git: no git access in the review.
- The review made no verification run (tests, lint, build): UC-1 reviews a plan, not code, so the verification step does not apply.
- Reviewer 1's identity: its header says haiku class, its self-report says an OpenAI model; the self-report is not proof of model diversity.
