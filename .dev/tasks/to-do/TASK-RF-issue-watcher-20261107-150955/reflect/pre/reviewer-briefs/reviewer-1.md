# Reviewer brief 1 (analyzer, model class sonnet)

## T1 card excerpt

## Coverage (deterministic, artifacts/coverage-matrix.yaml)

- Pass 1 (regex `R-/REQ-/SPEC-/T-`): 13 parsed rows, all of them transition ids T-1..T-13 of design section 7.4 (docs/designs/issue-watcher.md:478-490). 12 matched by exact token in the tasklist. T-2 has no exact token in the tasklist.
- Pass 2 (inference): 157 rows submitted, 155 kept (2 dropped because they overlap a parsed span). 133 matched by the containment rule, 22 unmatched.
- Union: 145 of 168 matched, `coverage_pct_union` 0.8631, parsed-only `coverage_pct` 0.9231, `S_dev_density` 0.1369, `coverage_degraded: parsed-sparse` (155 inferred rows against 13 parsed rows).
- The containment rule is lexical: at least 0.6 of a quote's content words must occur inside one task item. A match is weak evidence of real coverage; an unmatch is weak evidence of a gap.
- Structural signals: S_scope 209 items, S_domains 3 (code, tests, docs) which alone forces escalation under rule 4.

## Leads for the reviewers (each is a lead, not a verdict)

1. Unmapped rows to judge by reading both documents: T-2 (docs/designs/issue-watcher.md:479, failed entry backoff), INF-009 (the poller never assigns, comments or moves Project items, :44), INF-016 (non-goals NG-1..NG-5, :70), INF-051 (exit precedence 2, 6, 7, 5, 3, 4, :166), INF-089 (project id compared in Python, never in argv, :558), INF-101 (never-keys list, :718), INF-139 (every recorded prompt matches the D3 regex over a hostile corpus, :880), INF-147 (shared-input exit mapping, :888), INF-151 (sleeping stub ends with gh_timeout, :892). The full list is in artifacts/coverage-summary.yaml.
2. Gate divergence: design section 13 lists `make test` and `uv run ruff format --check src/ tests/` (docs/designs/issue-watcher.md:798,800). The tasklist instead uses a named affected subset, a pinned `uvx --offline ruff@0.15.20` and an xdist run, citing research/06 (DF-05, DF-60). Check that every deviation from the design is declared in the tasklist's Open Questions or Deviations section and that the substitute gates are at least as strict.
3. Section 11 of the design says `cli.py` holds "six verbs" (docs/designs/issue-watcher.md:759) while section 4.1 lists five verb names with `reset` split into two forms (:112-119). Check that the tasklist builds exactly the verbs of section 4.1 and the exit codes of section 4.3.
4. The design's UNVERIFIED shapes (docs/designs/issue-watcher.md:829-847) may enter the tasklist only as `_assumed_shape` fixtures. Check that no item states an unverified gh or Orca reply shape as fact.
5. The tasklist asks one local checkpoint commit before the POST reflect gate and forbids push and PR. Check that the commit allowlist, the BASE capture and the stop rules are internally consistent across Phase 10.

## Grounding hunks

codegraph run state: index_state=unverified checked_at=2026-11-07T18:46:15Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher  (not verified with the readiness check; use Read, Grep and Glob only)

### .dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:68-152

```markdown
## Task Overview

Issue 331 on IronbellyOrg/IronClaude asks for a watcher that polls GitHub every 5 minutes for issues that are tagged, assigned exactly to the own login, approved by an allow-listed human, unchanged since approval and in the Project Backlog column, and for at most one such issue per cycle starts `/sc:issue --claim <N>` in the owner's workspace through `orca agent launch`. The owner chose option A (a workspace-side poller), claim-only scope and an integer-only prompt (D1 to D3). This task builds the repo-side part that can be tested with mocks. The driving design is `docs/designs/issue-watcher.md`; where the design and the research disagree, `research/06-gap-fill-decisions.md` (decisions DF-01 [... line truncated in brief; Read the file for the rest]

The deliverables are: the `issue_watch` package (eight modules plus an empty `__init__.py`: `runner`, `github`, `predicates`, `record`, `launch`, `audit`, `cycle`, `cli`) behind a Click group with five commands (`once`, `status`, `check-config`, `init-state`, `reset`; six usage forms because `reset` has two); its two-line registration in the CLI registry (`main.py`); the suite under `tests/issue_watch/` (an empty package marker, `conftest.py`, 8 per-module test files, 11 cross-cutting test files and 13 `_assumed_shape` JSON fixtures; stubs for `gh`, `orca`, `orca-ide` and `git` are written at test time into `tmp_path`, nothing executable is committed); and the owner runbook `docs/designs/iss [... line truncated in brief; Read the file for the rest]

## Key Objectives

The following objectives MUST be achieved by this task:

1. **The package:** `src/superclaude/cli/issue_watch/` holds `__init__.py`, `runner.py`, `github.py`, `predicates.py`, `record.py`, `launch.py`, `audit.py`, `cycle.py` and `cli.py`, with the intra-package import rules of design section 5.3, Python 3.10 compatibility, and every decision DF-01 to DF-60 applied.
2. **The registration:** `src/superclaude/cli/main.py` gains exactly the import line and the `main.add_command(issue_watch_group, name="issue-watch")` line after the `reflect` registration (decision DF-29), and `uv run superclaude issue-watch --help` lists exactly the five commands.
3. **The tests:** `tests/issue_watch/` passes under `uv run pytest tests/issue_watch/ -v` and under xdist, adds no pytest marker and no dependency, writes only under `tmp_path`, and covers AC-1 to AC-25 including crash points C1 to C5 with five reruns each.
4. **The runbook:** `docs/designs/issue-watcher-setup.md` documents runbook steps 1 to 10 of the spec for the owner, states no unverified gh or Orca shape as fact, and contains no retired doc path and no model-alias string.
5. **The gates:** every command of research/06 Table 1.2 (G-1 to G-11) passes and is recorded, and all QA gates pass with serialized fixes, within two fix cycles per gate.
6. **The checkpoint and the POST reflect:** exactly one local commit (no push, no PR), a POST reflect run over `<BASE SHA>..HEAD`, and the Done item last, all in P10.

## Prerequisites & Dependencies

### Parent Task & Dependencies

- **Parent Task:** GitHub issue 331 (IronbellyOrg/IronClaude): the automated issue watcher.
- **Blocking Dependencies:** none. The research phase (reports in `qa/`, files in `research/`) is complete; its third review round was closed by a coordinator-approved exception recorded in research/06 under "Round 3 change log" (four small text fixes applied but not re-reviewed).
- **This task blocks:** the PR step (`/sc:pr-submit --monitor 3`, outside this task) and the owner-run follow-ups FU-1 (live test) and FU-2 (cron), which are not part of this task.

### Previous Stage Outputs (MANDATORY INPUTS)

**INFORMATIONAL ONLY - NO CHECKLIST ITEMS HERE**

**Required Previous Stage Outputs:**
- **Design:** `docs/designs/issue-watcher.md` - the binding module, schema, call-contract, test and gate design; read by section range in each item.
- **Spec:** `.dev/brainstorms/20261107-064825-github-issue-watcher/spec-final.md` - FR/NFR text, the closed reason table (lines 330-358) and runbook steps (lines 384-395).
- **Decision register:** `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/research/06-gap-fill-decisions.md` - DF-01 to DF-60, Tables 1.2 to 1.6, phase plan, item-author lookup table.
- **Research:** `research/01-cli-package-conventions.md`, `02-integration-points-and-citation-check.md`, `03-test-and-verification.md`, `04-template-and-examples.md`, `05-work-breakdown.md` and `research-notes.md` in the same folder - background only; superseded by research/06 wherever they conflict.
- **Research QA reports:** `qa/*-r3.md` where present, otherwise `qa/*.md` - minor notes already folded into the items below.

## Execution Context

### References

- GOAL (verbatim from the build request): Build an MDTM task file (template 02) that implements the GitHub issue watcher exactly as designed in `docs/designs/issue-watcher.md` (IronbellyOrg/IronClaude issue 331; the design was produced by /sc:design from the finalized spec `.dev/brainstorms/20261107-064825-github-issue-watcher/spec-final.md`). Deliverables the task must produce: the `superclaude issue-watch` Click package under `src/superclaude/cli/issue_watch/` (`__init__`, `runner`, `github`, `predicates`, `record`, `launch`, `audit`, `cycle`, `cli`), its two-line registration in `src/superclaude/cli/main.py`, the test suite under `tests/issue_watch/` (per-module unit tests, the cross-cutt [... line truncated in brief; Read the file for the rest]
- WHY (summary): issue 331 asks for an automated watcher that polls GitHub every 5 minutes for approved issues and starts `/sc:issue --claim <N>` in the owner's workspace; the owner decided option A (workspace-side poller), claim-only scope and an integer-only prompt (D1 to D3); this task builds the repo-side part that can be tested with mocks, and research/06 wins wherever the design and the research disagree.
- R-001, the design: `docs/designs/issue-watcher.md`. R-002, the finalized spec: `.dev/brainstorms/20261107-064825-github-issue-watcher/spec-final.md`. R-003, the decision register: `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/research/06-gap-fill-decisions.md`. R-004, the build request in the same folder.
- Legend: "D" is R-001 and "S" is R-002, each followed by line numbers of that document; "DF-nn" is a row of R-003; "G-1" to "G-11" (with a hyphen) are the gate-command rows of R-003 Table 1.2, distinct from the design's GitHub argv ids G1 to G7 (no hyphen); "C1" to "C5" are the crash points of design section 7.6 and "T-1" to "T-13" the transitions of design section 7.4; "AC-n" are the acceptance criteria of design section 17; "M3" is the lens-based QA sequence and "M4" the source-fidelity gate of the MDTM template; "TASK_DIR" in an item means the folder `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/`, which holds this file, `research/`, `qa/` and, after Step 1.2, `phase-outputs/`.

### Source Areas

- The `issue_watch` package inside the CLI package tree (nine files, all created by this task).
- The CLI registry module `main.py` (edited: two registration lines).
- The `tests/issue_watch` suite (all created by this task) and the existing `tests/conftest.py` autouse fixtures it must coexist with.
- The owner runbook under `docs/designs` (created by this task).
- Reused or mirrored existing code, read-only: the swarm `atomic` helper (`write_prepared_bytes`), the `install_user_setup` Orca probe (`_ORCA_CLIS`, `_find_orca`), the `sc-issue-protocol` skill (`origin_repo.py`, `refs/claim.md`, `templates/claim-comment.md`).
- Repository gates: `pyproject.toml`, `Makefile`, `.github/workflows/test.yml`, `.pre-commit-config.yaml`.

### Key Constraints

- UV only for every Python operation (`uv run pytest`, `uv run python`, `uvx --offline ruff@0.15.20`); never `python -m`, bare `pip` or bare `pytest`; no new dependency, no new pytest marker, no `hypothesis`, Python 3.10 floor, tests safe under xdist and writing only under `tmp_path`.
- Every `gh` call names `--repo IronbellyOrg/IronClaude` (or the literal repository inside a GraphQL constant); never `SuperClaude-Org`, never an `{owner}` placeholder; only a validated integer (`type(v) is int`, 1 to 999999999) reaches the launch prompt `/sc:issue --claim <n>`; the poller never writes to GitHub.
- Nothing live: no real `gh`, `orca`, `orca-ide`, `git` or network call in any test, no cron entry, no `gh label create`, no push, no PR; never stage or commit anything under `.claude/` (and never `git add -A` or `--no-verify`); `.dev/tasks` is always staged; the P10 checkpoint commit item HALTs on any commit or hook failure (stop rule) and nothing inside this task retries or works around it.

### Handoff File Convention

This task uses intra-task handoff patterns. Items write intermediate outputs to:
**`.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/phase-outputs/`**

Subdirectories:
- `discovery/` - baselines, tool versions, citation anchors
- `test-results/` - raw pytest, lint and gate command output with structured summaries
- `reviews/` - gate verdicts and reviews
- `plans/` - conditional-action outputs (BASE SHA, gate verdicts, commit allowlist check)
- `reports/` - gate change-set aggregations, the AC trace, the deviation register, post-completion validation

QA agents write to `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/qa/` (subfolders `gate-a/`, `gate-b/`, `gate-c/`, `gate-d/`, `final/`, `m4/`). These files persist across all batches and session rollovers. Later items read them by path.

### Frontmatter Update Protocol

YOU MUST update the frontmatter at these MANDATORY checkpoints:
- **Upon Task Start:** Update `status` to "🟠 Doing" and `start_date` to current date
- **Upon Completion:** Update `status` to "🟢 Done" and `completion_date` to current date
- **If Blocked:** Update `status` to "⚪ Blocked" and populate `blocker_reason`
- **After Each Work Session:** Update `updated_date` to current date

DO NOT modify any other frontmatter fields unless explicitly directed by the user. The POST reflect item records its result into `reflect_post`; the frontmatter carries no `start_commit` and no `executor_model_class` (skill mode).

## Detailed Task Instructions
```

### .dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:838-876

```markdown
### Phase 10: Checkpoint Commit, POST Reflect and Completion

(Plan: research/06 Section 2, row P10 and decision DF-07. This is the final phase, so the completion items live here (anti-orphaning): post-completion validation, one LOCAL checkpoint commit, the task summary, the POST reflect gate as the penultimate item and the Done item last. There is no push item and no PR item: the PR is a separate step run with `/sc:pr-submit --monitor 3` outside this task. No QA gate follows this phase. P10 starts only after the M4 verdict is PASS. STOP RULE: on any commit failure, hook failure or allowlist failure the task HALTs; it does not fix and retry the commit, never uses `--no-verify` or `--no-gpg-sign`, never uses `git add -A`, never stages anything under `.c [... line truncated in brief; Read the file for the rest]

YOU MUST complete EVERY item in this checklist IN ORDER. DO NOT skip ahead. Mark each item as complete before proceeding to the next.

**Step 10.1:** Post-completion validation (template I17 items 1 to 4; items 5 and 6 are the Final and M4 gates already passed)
- [ ] Read `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/phase-outputs/plans/final-gate-verdict.md` and `m4-verdict.md` (both must say PASS) and this task file, then use Grep on this file to count the `- [ ]` items that appear ABOVE this item and use Glob to confirm that every deliverable exists on disk: the nine files `src/superclaude/cli/issue_watch/{__init__,runner,github,predicates,record,launch,audit,cycle,cli}.py`, the registration lines in `src/superclaude/cli/main.py`, `tests/issue_watch/__init__.py` and `conftest.py`, the 19 test files (`test_runner`, `test_github`, `test_predicates`, `test_record`, `test_launch`, `test_audit`, `test_cycle`, `test_cli`, `test_cli_e2e`, `te [... line truncated in brief; Read the file for the rest]

**Step 10.2:** Check the branch and capture BASE immediately before the commit
- [ ] Depends on Open Questions OQ-7 and OQ-35: the authority for a checkpoint commit is inferred from the coordinator brief for this work, not from a repository text, and the owner has not yet confirmed it; proceed with Steps 10.2 to 10.4 unless the owner has withdrawn the commit in this session, and if it was withdrawn skip Steps 10.2 to 10.4, say so in the ### Phase 10 - Commit and POST Reflect Findings section, write the line `commit withdrawn by owner` there and to `phase-outputs/plans/commit-result.md`, and run Step 10.6 over a base the owner names instead of `plans/base-sha.txt` (when the owner names none, the POST reflect runs with the working-tree diff against HEAD as its change set [... line truncated in brief; Read the file for the rest]

**Step 10.3:** Stage the deliverables and run the allowlist check
- [ ] Subject to Open Questions OQ-7 and OQ-35 (inferred commit authority, see Step 10.2: skip this item if the owner withdrew the commit). Use the Bash tool to run `git add src/superclaude/cli/issue_watch src/superclaude/cli/main.py tests/issue_watch docs/designs/issue-watcher.md docs/designs/issue-watcher-setup.md .dev/tasks` from the repository root (explicit paths only; never `git add -A`, never `git add -f`, never any path under `.claude/`; `docs/designs/issue-watcher.md` is untracked today and enters the commit unchanged, decisions DF-07 and DF-31), then run `git diff --cached --name-only` and `git diff --exit-code pyproject.toml Makefile` and `git diff --exit-code -- .github/` (gate G [... line truncated in brief; Read the file for the rest]

**Step 10.4:** Create the single local checkpoint commit (no push, no PR)
- [ ] Subject to Open Questions OQ-7 and OQ-35 (inferred commit authority, see Step 10.2: skip this item if the owner withdrew the commit). Read `phase-outputs/plans/commit-allowlist-check.md` (it must say PASS; if it does not, do nothing and HALT) and read BASE from `phase-outputs/plans/base-sha.txt`, then use the Bash tool to run exactly `git commit -m "feat(cli): add issue-watch poller for issue #331" -m "Co-Authored-By: Claude Code <noreply@anthropic.com>"` from the repository root (no `--no-verify`, no `--no-gpg-sign`, no `--amend`, no push, no `gh` call; no local hook is installed in this checkout, so the hygiene rules were applied by gate G-11), and then `git log -1 --stat`, writing t [... line truncated in brief; Read the file for the rest]

**Step 10.5:** Populate the Task Summary
- [ ] Read `phase-outputs/reports/final-gate-record.md`, `ac-trace.md`, `deviation-register.md`, `post-completion-validation.md`, `phase-outputs/plans/commit-result.md` (which records `commit withdrawn by owner` instead of a SHA when the owner withdrew the commit) and the ### Phase Gate Findings section of the Task Log, then populate the existing ### Task Summary section at the top of the ## Task Log / Notes section of this task file (do not create a second one) using the template there: the completion date; the work completed (the package, the registry edit, the test suite counts read from `p9-g1-summary.md`, the fixtures, the runbook, the six gate verdicts (Gates A to D, Final, M4) with th [... line truncated in brief; Read the file for the rest]

**Step 10.6:** Independent POST reflection gate (a dedicated subagent runs the post-execution reflection end to end; penultimate item)
- [ ] Context: all implementation, test, gate, commit and summary items above are complete; the inline QA gates ran in the executor's own frame and cannot give an executor-independent audit, so a DEDICATED SUBAGENT (not the executor) runs the reflection, which is expected to catch spec-literal-token, invariant-arithmetic and integration blind spots that same-frame QA misses; nested-subagent and Skill-tool-in-subagent capability are expected to hold but are not yet session-validated for this skill-mode path (disclosure carried from the task-builder rules). Action: first read the SHA from `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/phase-outputs/plans/base-sha.txt` and substitute i [... line truncated in brief; Read the file for the rest]

    > You are the post-execution reflection runner for the task at .dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md. Your sole job is to run the `sc-reflect-protocol` skill end-to-end, in full, exactly as specified, and return its verdict and report path. You MUST run the actual skill via the Skill tool; you must NOT hand-roll, paraphrase, simulate, or partially run a reflection of your own.
    >
    > 1. Invoke the skill with the Skill tool, exactly: `Skill(skill: "sc-reflect-protocol", args: "--mode post --remediate --diff <BASE SHA>..HEAD --tasklist .dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md --spec docs/designs/issue-watcher.md --depth deep --output .dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/reflect/post")`. Do NOT pass `--executor-model` or any executor-exclusion flag: the skill-mode POST arm does not capture or forward an executor-class flag on this path (`executor_model_class` is captured in CLI mode only), so there is nothing for you to forward here. Reviewer-panel independence on this path comes from fresh revie [... line truncated in brief; Read the file for the rest]
    > 2. Let the skill run its FULL pipeline for whatever tier its own rubric resolves. Do NOT pin, downgrade, or shortcut the tier yourself. If the skill resolves Tier 2, the run MUST include every structural wave: the heterogeneous reviewer ensemble (Wave 3), per-card blind calibration by `confidence-calibrator` (Wave 3C), the adversarial merge (Wave 4), and the evidence-validator gate on the final report (Wave 5). If the skill legitimately resolves Tier 1 (per its own rubric and the `--depth` floor), the run MUST still include the full Tier-1 path: real-code grounding, the single-agent reflection card, and the blind calibration of that card (Wave 1D).
    > 3. Classify every deviation under the skill's 4-category taxonomy (Authorized / Necessary / Drift / Regression). If the skill surfaces any Regression or any unauthorized Drift, apply the remediations the skill offers under `--remediate`; if any Regression or unauthorized Drift stays unresolved, HALT and escalate to the user with those deviations (never log them to Open Questions and proceed). Only Authorized or Necessary deviations and minor findings may be appended as notes to the `### Open Questions` section of .dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md (never delete existing items).
    > 4. Persist ALL reflect artifacts under .dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/reflect/post (the skill writes them; confirm the directory exists and is populated before you return).
    > 5. Return, as your final message, EXACTLY: the merged verdict (PASS | PASS-with-deviations | FAIL), the reflect `run_id`, the absolute path to the final reflect report, the resolved tier, and a one-line waves-attestation naming which structural waves actually ran (e.g. "Tier 2: ensemble=3 reviewers, calibration=done, merge=done, evidence-gate=PASS" or "Tier 1: grounding=done, reflection-card=done, calibration=done").
    >
    > COMPLETION CONTRACT (read carefully): "a verdict was recorded" does NOT satisfy this job. This job is satisfied ONLY by a full run of `sc-reflect-protocol` executed exactly as stated above, for the tier its own rubric resolves, with every structural wave that tier requires actually executed and its artifacts persisted under .dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/reflect/post. Each of the following is an EXPLICIT NON-satisfaction: a partial run; a reviewer panel you assembled yourself instead of the skill's ensemble; a verdict you synthesized without the skill's merge wave; a skipped blind calibration, adversarial merge, or evidence-validator gate; or a Tier-2-eligible r [... line truncated in brief; Read the file for the rest]

    Output: the subagent returns `{verdict, run_id, report, resolved_tier, waves_attestation}`; record `{verdict, run_id, report}` into this file's frontmatter field `reflect_post`; if reflect surfaced Regression or unauthorized Drift deviations, the remediations were applied or the task HALTed and escalated them to the user, and only Authorized or Necessary deviations and minor findings were logged as notes to `### Open Questions`. Verification: `reflect_post` holds the subagent's `{verdict, run_id, report}` (not empty); the returned `waves_attestation` confirms every structural wave the resolved tier requires actually ran; a `reflect_post` recorded from a partial, hand-rolled or `RUN_INCOM [... line truncated in brief; Read the file for the rest]

**Step 10.7:** Update task status to Done
- [ ] Read this task file to confirm that every prior checklist item is marked complete, that the frontmatter `reflect_post` holds a non-empty `{verdict, run_id, report}` recorded from the subagent's return, that `phase-outputs/plans/commit-result.md` shows exit 0 and one commit (or, only when the owner withdrew the checkpoint commit in this session, that it records `commit withdrawn by owner` instead and the POST reflect ran with the working-tree diff documented as an Open Question), and that the Open Questions section lists no unresolved blocking item (an item marked NEEDS OWNER DECISION or an unresolved Regression keeps the task from Done; the entries OQ-7 and OQ-35 about the inferred com [... line truncated in brief; Read the file for the rest]

```

### docs/designs/issue-watcher.md:747-806

```markdown
## 11. Files to create or change

| Path | Purpose |
|---|---|
| `src/superclaude/cli/issue_watch/__init__.py` | Package marker; exports nothing |
| `.../issue_watch/runner.py` | `Runner` Protocol, `SubprocessRunner` (argv list, `shell=False`, timeout, 500-byte stderr cap) |
| `.../issue_watch/github.py` | `REPO`, argv builders G1 to G7, jq and GraphQL constants, paging, `classify`, `CallBudget` |
| `.../issue_watch/predicates.py` | Pure eligibility checks (approval, owner, unchanged, project, marker window) |
| `.../issue_watch/record.py` | `Store` Protocol, schema, migrations, transitions, lock, atomic save |
| `.../issue_watch/launch.py` | `Launcher` Protocol, `find_orca`, `parse_origin`, `build_claim_prompt`, `launch_argv`, outcome parse, `ORCA_AGENT` |
| `.../issue_watch/audit.py` | `REASONS`, line builders, `AuditLog` append and rotation, stderr fallback |
| `.../issue_watch/cycle.py` | `Clock` Protocol, `Deadline`, `run_cycle`, `slo_numbers` |
| `.../issue_watch/cli.py` | click group `issue_watch_group` and the six verbs; exit-code mapping only |
| `src/superclaude/cli/main.py` | Two lines after line 561, same pattern as `reflect_group` (lines 559 and 561) |
| `tests/issue_watch/__init__.py`, `conftest.py` | Package marker (C14); `FakeRunner`, `FakeClock`, `FakeLauncher`, `tmp_state` fixtures |
| `tests/issue_watch/test_{runner,github,predicates,record,launch,audit,cycle,cli}.py` | One file per module |
| `tests/issue_watch/test_{cli_e2e,security_invariants,crash_injection,concurrency,no_shell,no_text,origin_parity,marker_contract,find_orca_parity,module_boundaries,slo_helper}.py` | Spec-named and design-added cross-cutting tests |
| `tests/issue_watch/fixtures/_assumed_shape/*.json` | Assumed `gh` and Orca replies, replaced by FU-1 |
| `tests/issue_watch/stubs/gh`, `stubs/orca` | Executable PATH stubs for `test_cli_e2e.py` |
| `docs/designs/issue-watcher-setup.md` | Runbook steps 1 to 10 for the owner |

Not changed: `pyproject.toml` (no dependency, no marker, no entry point), `Makefile`, CI, any file under `.claude/`. `docs/designs/issue-watcher-live-test.md` is written by the owner during FU-1. No primitive is added, so the installed-path rule is not engaged.

## 12. Tests

No test runs a real `gh`, `orca`, `git` or network call. Every external effect goes through a fake or a PATH stub.

| Seam | Fake | Rule |
|---|---|---|
| `Runner` | `FakeRunner(script: dict[tuple[str, ...], Reply])` | records every argv; unknown argv returns exit 99 and fails the test at teardown |
| `Clock` | `FakeClock(now, mono)` with `advance(s)` | the only time source; no `sleep` |
| `Launcher` | `FakeLauncher(outcomes)` | records argv and cwd; can raise |
| `Store` | `CrashingStore(real, crash_at="C1".."C5")` | raises `SystemExit` at the named point (section 7.6) |
| PATH | `stubs/gh`, `stubs/orca` (bash; scenario file in, argv log out) | stub dir prepended to `PATH` as in `tests/pr_submit/test_conflict_e2e.py`; a guard asserts `shutil.which("gh")` is the stub |

| Test | Checks |
|---|---|
| `test_crash_injection.py` | per C1 to C5, run, crash, rerun: total fresh launches per issue ≤ 1 (NFR-005) |
| `test_concurrency.py` | two `multiprocessing` processes on one `tmp_path` store: one exits 75 `lock_held`, one launch total |
| `test_cycle.py::test_fifty_cycles` | 50 cycles over a changing fixture: `launches` never exceeds 1 per issue |
| `test_cycle.py::test_acceptance_property` | for N in {1, 2, 6, 7, 50, 99}: at most 1 launch per cycle; after 24 h of cycles exactly min(N, 6) launched and the rest `day_cap`; after +24 h one more per cycle |
| `test_no_shell.py` | AST: no `shell=True`, no `os.system`, no `subprocess` outside `runner.py` |
| `test_no_text.py` | hostile titles, bodies and stderr (`PWNED-TITLE`) never appear in audit, store, prompt or stdout |
| `test_module_boundaries.py` | AST import graph matches section 5.3; no module named `select` |
| `test_marker_contract.py` | `CLAIM_MARKER` occurs in `refs/claim.md` and `templates/claim-comment.md`, read through the dual surface |

## 13. Gates, sync and packaging

| Gate | Source | Note |
|---|---|---|
| `uv run pytest tests/issue_watch/ -v` | spec line 366 | fast loop |
| `make test` | `Makefile:13-15` | CI uses `-n auto` (`test.yml:47`), C11 |
| `make lint` | `Makefile:48-50` | includes `lint-architecture` (C8); ruff 0.15.20, select `E,F,I,N,W,TID`, line length 88, py310 (`pyproject.toml:54,174-184`) |
| `uv run ruff format --check src/ tests/` | `test.yml:106` | no make target (C10) |
| `make verify-deps` | `Makefile:356-358`, `test.yml:123` | passes with no new dependency |
| `make verify-sync` | `Makefile:166`, `test.yml:131` | unaffected: nothing under skills, agents, commands, hooks or templates changes |
| `make sync-dev` | `Makefile:109` | preparation, not a gate |

The Python floor is 3.10 (`pyproject.toml:16`, CI `test.yml:22`): no `tomllib`, no `datetime.UTC` (use `timezone.utc`). Packaging needs nothing: hatchling includes the new package under `src/superclaude/`, and the `superclaude` entry point (`pyproject.toml:71`) reaches it through `main.py`.

```

## Coverage slice

| Requirement | Source | Citation | Match | Matched task items | Ratio | Quote |
|---|---|---|---|---|---|---|
| T-1 | parsed | docs/designs/issue-watcher.md:478 | exact | Step 4.1c, Step 4.4, Step 5.G5, Step 5.G6, Step 9.M1 | - |  |
| T-2 | parsed | docs/designs/issue-watcher.md:479 | none | - | - |  |
| T-3 | parsed | docs/designs/issue-watcher.md:480 | exact | Step 4.4 | - |  |
| T-4 | parsed | docs/designs/issue-watcher.md:481 | exact | Step 4.1a, Step 4.4 | - |  |
| T-5 | parsed | docs/designs/issue-watcher.md:482 | exact | Step 4.4 | - |  |
| T-6 | parsed | docs/designs/issue-watcher.md:483 | exact | Step 4.4 | - |  |
| T-7 | parsed | docs/designs/issue-watcher.md:484 | exact | Step 4.4 | - |  |
| T-8 | parsed | docs/designs/issue-watcher.md:485 | exact | Step 4.4 | - |  |
| T-9 | parsed | docs/designs/issue-watcher.md:486 | exact | Step 4.4 | - |  |
| T-10 | parsed | docs/designs/issue-watcher.md:487 | exact | Step 4.1c, Step 4.4, Step 6.2 | - |  |
| T-11 | parsed | docs/designs/issue-watcher.md:488 | exact | Step 4.1c, Step 4.4, Step 6.2 | - |  |
| T-12 | parsed | docs/designs/issue-watcher.md:489 | exact | Step 4.1c, Step 4.4, Step 6.2 | - |  |
| T-13 | parsed | docs/designs/issue-watcher.md:490 | exact | Step 4.1c, Step 4.4, Step 5.G5, Step 5.G6, Step 9.M1 | - |  |
| T-2 | parsed | docs/designs/issue-watcher.md:479 | none | - | - |  |
| INF-006 | inferred | docs/designs/issue-watcher.md:33-33 | none | - | 0.5 | No cron entry is enabled and `enabled` stays `false` until an owner-run live test (FU-1) shows the prompt running as a slash command, records the session's permission mode, and replaces every `_assume |
| INF-008 | inferred | docs/designs/issue-watcher.md:39-39 | none | - | 0.5 | D1 option A (workspace-side poller, pull); D2 claim-only; D3 only a validated integer issue number reaches a session prompt. |
| INF-009 | inferred | docs/designs/issue-watcher.md:44-44 | none | - | 0.571 | The poller never assigns, comments or moves Project items. |
| INF-016 | inferred | docs/designs/issue-watcher.md:70-70 | none | - | 0.581 | NG-1 push designs B/C/D; NG-2 no GitHub write (REST GET only; GraphQL POST only with a constant query without `mutation`); NG-3 no Project writes; NG-4 no session constraint beyond the deployment gate |
| INF-022 | inferred | docs/designs/issue-watcher.md:90-90 | none | - | 0.548 | The NFR-014 dependency rules need a new AST test, `tests/issue_watch/test_module_boundaries.py`. The package must not rebind `ID_PATTERNS`, `THRESHOLDS` or any other `contracts.__all__` name and must  |
| INF-037 | inferred | docs/designs/issue-watcher.md:133-133 | none | - | 0.556 | `project_id` / string / yes / none / Matches `^PVT_[A-Za-z0-9_-]{1,64}$` [PROPOSAL; Projects v2 node-id prefix is UNVERIFIED, FU-3] |
| INF-042 | inferred | docs/designs/issue-watcher.md:139-139 | none | - | 0.417 | Unknown keys are rejected (exit 2), so a typo such as `enable` cannot silently leave the poller on its default. |
| INF-044 | inferred | docs/designs/issue-watcher.md:158-158 | none | - | 0.538 | 2 / Usage, config, platform, origin, Orca probe / `config_invalid`, `approvers_invalid`, `platform_unsupported`, `worktree_invalid`, `origin_mismatch`, `orca_not_found`, `account_id_mismatch` |
| INF-051 | inferred | docs/designs/issue-watcher.md:166-166 | none | - | 0.5 | When several conditions hold, the cycle exits with the first of 2, 6, 7, 5, 3, 4. |
| INF-055 | inferred | docs/designs/issue-watcher.md:219-219 | none | - | 0.531 | Builds every `gh` argv from module constants (section 8); runs it through the runner with a timeout supplied by the cycle; parses JSON; follows paging; classifies replies into `ok`, `timeout`, `non_js |
| INF-089 | inferred | docs/designs/issue-watcher.md:558-558 | none | - | 0.5 | Project ids are compared in Python (`project.id == config.project_id`); the id never enters an argv, so a hostile config value cannot alter a query. |
| INF-101 | inferred | docs/designs/issue-watcher.md:718-718 | none | - | 0.583 | `rate_remaining`, titles, bodies, label names and stderr text are never keys (NFR-006, T11). |
| INF-108 | inferred | docs/designs/issue-watcher.md:763-763 | none | - | 0.364 | `tests/issue_watch/test_{cli_e2e,security_invariants,crash_injection,concurrency,no_shell,no_text,origin_parity,marker_contract,find_orca_parity,module_boundaries,slo_helper}.py` / Spec-named and desi |
| INF-123 | inferred | docs/designs/issue-watcher.md:798-798 | none | - | 0.5 | `make test` / `Makefile:13-15` / CI uses `-n auto` (`test.yml:47`), C11 |
| INF-124 | inferred | docs/designs/issue-watcher.md:799-799 | none | - | 0.435 | `make lint` / `Makefile:48-50` / includes `lint-architecture` (C8); ruff 0.15.20, select `E,F,I,N,W,TID`, line length 88, py310 (`pyproject.toml:54,174-184`) |
| INF-128 | inferred | docs/designs/issue-watcher.md:812-812 | none | - | 0.333 | `max_launches_per_cycle` / 1 / caps blast radius of a bad cycle |
| INF-129 | inferred | docs/designs/issue-watcher.md:814-814 | none | - | 0.545 | call cap / 35, 3 reserved / worst cycle 37 calls, 8.88% of 5,000 an hour |
| INF-135 | inferred | docs/designs/issue-watcher.md:876-876 | none | - | 0.538 | Approval table: outsider, bot, unlabel, relabel, incomplete history, edit after approval each skip with their reason |
| INF-139 | inferred | docs/designs/issue-watcher.md:880-880 | none | - | 0.545 | Every recorded prompt matches the D3 regex over the hostile corpus; non-int input raises |
| INF-142 | inferred | docs/designs/issue-watcher.md:883-883 | none | - | 0.4 | Budget, day cap and `consumed_log` hold through `reset`; acceptance property passes |
| INF-147 | inferred | docs/designs/issue-watcher.md:888-888 | none | - | 0.5 | Shared-input failures map to exits 2, 3, 5, 6, 7 with the precedence 2, 6, 7, 5, 3, 4 |
| INF-151 | inferred | docs/designs/issue-watcher.md:892-892 | none | - | 0.429 | A sleeping stub ends with `gh_timeout`; no launch starts after 120 s |
