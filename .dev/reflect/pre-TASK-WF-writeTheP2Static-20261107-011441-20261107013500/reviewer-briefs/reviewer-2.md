# Reviewer 2 brief (persona: qa; model slot: haiku)

Mode: UC-1 (pre-execution plan review). You review a PROPOSED plan against its driving brief. Read-only: never edit, write or run anything; return findings only. Grounding root: /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P2 (all relative paths below are under it).

Inputs:
- Plan under review: `.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/TASK-WF-writeTheP2Static-20261107-011441.md` (read it whole).
- Driving brief: the spec body below (also on disk at `.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/source.md`).
- Spec section 7.3 rows P2 (AC-2.1 to AC-2.9) and section 7.1 (AC-C1 to AC-C6) in `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`.
- The test file the plan extends: `tests/skills/test_worker_contract.py`.

Persona focus (qa): Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding. Then check each task's acceptance criteria: are they observable (a command, a grep, a test), would each one FAIL on the pre-change text, and do they actually catch the defect the task targets (a test that passes before the edit is a P2 finding)? Check that the tests the plan adds or changes in `tests/skills/test_worker_contract.py` are consistent with the existing helpers (`_check_p1_set`, `_unattended_section`, `_check_unattended_section`, `_artifacts_clause`, `test_only_brainstorm_lists_nested_commands`, `test_nested_check_fails_on_nested_text_without_a_nested_list`, the `_AC14_CASES` table, `WRITE_VERB_CLASSIFICATION`) and that the pytest commands in each AC name test files that exist.

Output: a YAML card with `findings:` (each: id R2-Fn, severity P1 | P2 | P3 as defined: P1 = the plan would produce wrong behaviour or violate a stated rule; P2 = a task is incomplete or an AC cannot catch its defect; P3 = wording/minor), claim, evidence as file:line list you actually read, deviation_class, suggested_fix), plus `self_confidence` (0-1) and a `self_audit` paragraph. Every claim must cite file:line you read; tag anything else [INFERRED].

## T1 card excerpt

```yaml
  - id: T1-F1
    severity: P2
    claim: "F1 (source.md:7) asks every P2 command's artifacts clause to say 'left out (WC-4)'. The plan states it once in the section skeleton (plan:25) and pins it with a test phrase only for cleanup, improve, research (Tasks 2-4); Tasks 6-12 and 15-16 do not name it, and no task carries the 'one short local sentence' rule for a report that names where ignored files went."
  - id: T1-F2
    severity: P3
    claim: "Task 1 tells the executor to 'drop only the case that relied on equality' in test_p1_set_check_fails_on_a_missing_extra_or_repeated_command, but under the new subset rule every existing case still fails, so the instruction has no target."
  - id: T1-F3
    severity: P3
    claim: "Task 14 pins the single token '/task' as a phrase; P1 lesson (source.md:14) asks for exact phrases, not single tokens."
```

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-07T01:31:09Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P2 projectPath=/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P2

### .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/source.md:1-19 (spec body, whole file)

```markdown
Write the P2 STATIC plan for the Orca worker contract, per .dev/orca-command-refactor/specs/orca-worker-contract-spec.md section 6 (row P2), section 7.1 and 7.3 (the P2 checks) and the section 3 rows of the P2 commands (section 3.1 for reflect, release-split, tdd and troubleshoot; section 3.2 for the others), applying .dev/orca-command-refactor/decisions/APPROVED.md. Static plan only: the edits and the checks that need no live Orca run. The live plan is written later.

Context. Program: refactor IronClaude commands so Orca workers can run them (Orca on top, commands stay the units of work). Spec: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md (approved). P0 is done (PR #368, #383). P1 is done and merged: PR #411 (cb8f2f81, 16 commands gained `## Unattended mode` and `--unattended`) and PR #413 (74613822, follow-ups). The P1 static plan is the model for this plan's structure and conventions: .dev/tasks/done/TASK-WF-writeTheP1Static-20261105-033458/TASK-WF-writeTheP1Static-20261105-033458.md (section skeleton, UNATTENDED_EXPECT test data, Check SCAN, Check ADDITIVE, Check WRITEVERB, the mirror rule, test-command rules, baselines). The P1 live report and the owner's answers are in .dev/tasks/done/TASK-WF-p1LivePlanBrief-20261105-164506/artifacts/ (p1-phase-report.md, p1-owner-decisions-20261105.md).

Owner decisions since P1 that this plan must apply (they are being recorded in decisions/APPROVED.md by PR #417, which may not be merged when this plan is written, so they are stated here in full):
- P1 verdict PASS (lc09 and lc10 reclassified PASS by the owner on 2026-11-05). P2 may start.
- F1 (PR #413): WC-4 in src/superclaude/core/WORKER-CONTRACT.md states once that `artifacts` leaves out paths git ignores and paths outside the repository, because WC-9 stages every listed path and git refuses them, for every command's list. Each P2 command's `artifacts` clause lists only files the run wrote, names the ignored files it leaves out and points at WC-4 for the reason ("left out (WC-4)"); it never restates the reason and never contains the literal `git add`. A command whose report names where those files went says so in one short local sentence.
- Open for the owner, not decided (P1-C5): 11 P1 workers carried out the command by reading its file in their top-level session, with no `Skill` call. Spec 7.2 step 5 condition 2 was recorded PASS for them. Whether that satisfies WC-7 decides how the P2 live plan judges condition 2. This static plan does not depend on it; list it as an open owner question in the plan.

Phase P2 scope (spec section 6, row P2; AC-2.1 in section 7.3): each default-on gate resolves per its section 3 row under `--unattended`; WC-10 wait splitting for cli-eval (eval waits of at most 240 s). Commands gaining `--unattended` and a `## Unattended mode` section in P2 (15): auggie-review, cleanup, improve, cli-eval, cli-portify, recommend, research, review-translation, spec-panel, task, tasklist, reflect, release-split, tdd, troubleshoot. Also `## Unattended mode` section edits for two P1 commands: workflow (its reflect step passes `--unattended` and a nested report directory `<report-dir>/nested/reflect-<n>/`) and brainstorm (its automatic research enrichment passes `--unattended` and a nested report directory instead of being off). Where a command has an outward default (auggie-review posting, task's `commit`/`push` and committed TFEP report), P2 only turns it off under `--unattended` (WC-9). P2 touches no safety rule and adds no outward capability. AC-2.1's deletions check on src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md must print nothing (SA-6).

Open conflict the plan must resolve or put to the owner: brainstorm's research enrichment has two arms (src/superclaude/skills/sc-brainstorm-protocol/SKILL.md, the enrichment table around line 190): research-light and research-deep, and research-deep invokes `Skill tech-research`, which is not one of the spec's 39 commands and has no Unattended mode. The P1 brainstorm-fix plan recorded this as an open conflict for the P2 author (.dev/tasks/done/TASK-WF-brainstormFixBri-20261106-113538/source.md, "Out of scope, open conflict"). Decide, with the spec's nested-propagation rule (section 2.1), what each arm does under `--unattended` (for example: research-light passes `--unattended` and `<report-dir>/nested/research-<n>/` to `/sc:research`; research-deep is skipped and recorded), and record it as a plan decision for owner approval.

Lessons from P1 to apply in every task: pin each rule with an exact phrase, never a single token that a clause can contain while saying the opposite; a "phrase present" check that replaces old wording also asserts the old wording is absent, scoped to the line that carries the rule; when a test reads a clause with `_artifacts_clause`, the text the test needs sits after the first backticked `artifacts` on that line; each check must fail on the pre-change text.

The plan must have, per task: the exact files to edit (installed-path rules apply: never hardcode src/superclaude/ paths inside installed primitives; edit the src/superclaude/ sources, byte-copy the pinned plugin mirrors, run make sync-dev), acceptance criteria that are observable (a command, a grep, a test), and the tests to add or extend (tests/skills/test_worker_contract.py: extend UNATTENDED_EXPECT and the commands-with-a-section list to the P2 commands, plus one assertion per gate as AC-2.1 lists, and the nested-invocation assertions for workflow and brainstorm). Include the static checks of section 7.1 and 7.3 that apply to P2 (AC-2.1, AC-C1 to AC-C6), make lint, the ruff format check with the pinned ruff (`uv run --extra dev ruff`), make verify-sync, the pre-existing tests that read the edited files, and a static report that states each result and the exact list of paths for the owner-approved commit.

Do not execute the plan: no /sc:implement, no commit, no push, no superclaude install, no live Orca run. Stage nothing under .claude/.
```

### tests/skills/test_worker_contract.py:898-903

```python
def _check_p1_set(commands, expect) -> None:
    assert len(commands) == 16, f"P1 lists {len(commands)} commands, not 16"
    assert len(set(commands)) == 16, "P1_COMMANDS has a duplicate"
    assert set(expect) == set(commands), (
        f"UNATTENDED_EXPECT and P1_COMMANDS differ: {sorted(set(expect) ^ set(commands))}"
    )
```

### tests/skills/test_worker_contract.py:770-775

```python
def _artifacts_clause(text: str) -> str:
    """The rest of the line after the first `artifacts` key (backticked or YAML)."""
    line = next(
        ln for ln in text.splitlines() if re.search(r"`artifacts`|^artifacts:", ln)
    )
    return re.split(r"`artifacts`|^artifacts:", line, maxsplit=1)[1]
```

## Coverage slice

The full matrix is at `.dev/reflect/pre-TASK-WF-writeTheP2Static-20261107-011441-20261107013500/artifacts/coverage-matrix.yaml` (28 inferred rows INF-001..INF-028, parsed 0). Your rows: all 28 (recall backstop), with special attention to:

| Requirement | Plan location | Status |
|---|---|---|
| INF-006 F1 artifacts clause in every P2 command (source.md:7) | plan:25 skeleton; Tasks 2,3,4,13,14 | partial (T1-F1) |
| INF-017/INF-018 P1 lessons (source.md:14) | plan:27 | covered (verify per task) |
| INF-022 one assertion per gate (source.md:16) | Task 20 | covered (verify) |
| INF-023 nested assertions workflow and brainstorm (source.md:16) | Tasks 17, 18, 20 | covered |
| INF-024..INF-027 checks and static report (source.md:16) | Task 21 | covered |
