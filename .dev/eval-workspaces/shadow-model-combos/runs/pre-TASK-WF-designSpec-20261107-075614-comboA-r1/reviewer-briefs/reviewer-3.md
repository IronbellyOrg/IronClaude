# Reviewer 3 brief — persona: refactorer (structural / consistency lens)

Audit target: UC-1 pre-execution. Spec = `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md` (design spec v3, issue #375, pr-submit merge guard). Plan = `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md` (13 tasks, 5 phases).

ATTRIBUTION NOTE (binding): this is a PRE-execution audit of the frozen spec↔plan pair. The spec's facts F1-F13 are pinned at base commit e8db2fe6 (2026-11-07). HEAD has since evolved (the feature landed as commit 0b8a5801d); do NOT file findings that rest on HEAD source text — audit the plan's structure against the frozen spec only.

Your lens: phase/task decomposition coherence, dependency graph correctness, consistency of conventions across tasks (sync cadence, classification-last, test placement), drift between plan text and spec tables, duplication or missing steps.

## T1 card excerpt

Verbatim excerpt from t1-card.md (structure-relevant slice):

> - **H1 (wording tension, MINOR candidate).** The Wave 0 SKILL.md bullet must itself carry the L3/`--merge-guard off` print clause ("at L3 with `--merge-guard off` the line 'Remediation is unprotected...' is printed once", source.md:241) while Task 9's AC says the bullet "contains no `L3 only` or `draft` gate wording" (tasklist:137,140). The AC's "gate wording" qualifier makes it implementable (the load-clause carries no gate; the print-clause names L3), but a test author reading only the AC could ban the token `L3` outright and write an unpassable test. Family: pass-gate wording (shadow06/08/10 recurrence class).
> - **H2 (superset dependency, MINOR candidate).** Task 13 (docs/user-guide) declares "Depends on: Task 2" (tasklist:190); nothing in Task 13 consumes the enum change. Harmless over-sequencing, not a coverage gap. [INFERRED]
> - **H3 (verified conformance).** Dependency completeness per source.md:363: every consumer declares its producers (T5←T3,T4; T8←T1,T4,T7; T9←T6,T8; T10←T9; T11←T3,T4,T5,T7; T12←T6,T8; T13←T2,T10,T11,T12). Every file in the spec's files-to-change table (source.md:283-301) has an owning task. The 12 minimum tests of source.md:307-322 all appear by name in Task 11 (tasklist:169). The classification-last discipline (source.md:255, 373) appears in Tasks 7, 8, 9, 10, 12.
> - **H4 (constraint without explicit AC, MINOR candidate).** source.md:208 "A corrupt line still raises, as it does today" — no task AC names corrupt-line fold behavior explicitly (implicitly held by existing RunLog tests; Task 5's legacy-log AC is adjacent but not the same). Family: constraint without matching AC (shadow06/10 recurrence).

End your card with a ## Findings block holding one fenced findings-v2 block: JSON lines, one object per line, never a table. Fields: id (F1, F2, ...), severity (CRITICAL, MAJOR or MINOR), blocking (true or false; a MINOR finding is never blocking), category (one of contradiction, data-loss, missing-requirement, other, safety, unpassable-check), lens "reflect-pre", claim (one line, at most 300 characters), refs (requirement ids, may be empty) and citations (1 to 8 objects, each with role plan or spec, a repo-relative path, line_start, line_end and an optional quote). Example line: {"id":"F1","severity":"MAJOR","blocking":false,"category":"contradiction","lens":"reflect-pre","claim":"Task 3 says X but task 5 says Y.","refs":["R-1"],"citations":[{"role":"plan","path":"plan.md","line_start":10,"line_end":12}]}. After the block add a reviewer_model_self_report line stating the model you are running as in one line.

Cite with repo-relative paths: spec = `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md`, plan = `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md`. Quote ≤200 chars.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-13T03:03:29Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### TASK-WF-designSpec-20261107-075614.md:17-50 (Constraints + Phase 1 / Tasks 1-2)

```text
## Constraints
- Edit canonical files under `src/superclaude/` only, then run `make sync-dev`; do not stage `.claude/` mirror files. Use UV for every Python command.
- The new pure module `merge_guard.py` and every CORE_PURE_FILES file must contain no whole word `gh` or `git`... The module must not import `recovery` (an import cycle through `run_log`).
- Protocol and command text must not contain the string `src/superclaude`; `SKILL.md` must keep exactly one python code fence; edits additive, after never inside pinned sentences; no `evidence-validator` / `conflict-intent.md` words...
- Every new line under skills/, commands/ or agents/ with `gh pr`, `gh api` or a git write verb needs one WRITE_VERB_CLASSIFICATION entry, added last in the task that writes the file...
- Cite tests and constants by symbol name, never by line number...
- No test or task may call GitHub. Script tests use a fake `gh`. G1 live part, G2 live part, G4, G5, G6 recorded OPEN, release gate, never claimed verified.
- Scope limits: no labels/commit statuses/rulesets; ordinals 0-2 change only by one report line; conflict-merge cycles never engaged; guard not held through re-review or CI; second concurrent run unsupported.
- Owner decisions fixed: draft not label; engage end of Wave 3; default on at monitor 3; release on confirmed push before replies and re-trigger; unreadable/unpublished keeps draft; build now no GitHub calls, release gate G4/G5.
- Run `make sync-dev` at the end of every task that edits skills/ or commands/.
## Task 1 [pre-build record] Depends on: (none)
## Task 2 [enum] Depends on: Task 1
```

### TASK-WF-designSpec-20261107-075614.md:52-115 (Tasks 3-7 with Depends-on lines)

```text
Task 3 [merge_guard.py core] Depends on: Task 2
Task 4 [decisions] Depends on: Task 3
Task 5 [run-log fold + exports] Depends on: Task 3 / Depends on: Task 4
## Phase 2: Flag and script
Task 6 [--merge-guard flag] Depends on: Task 1
Task 7 [set-draft-state.sh] Depends on: Task 1
## Phase 3: Protocol text
Task 8 [refs/merge-guard.md] Depends on: Task 1 / Task 4 / Task 7
Task 9 [SKILL.md Wave 0 + rows] Depends on: Task 6 / Task 8
Task 10 [SKILL.md Waves 3/6/8 + state-machine overlay] Depends on: Task 9
## Phase 4: Scenario tests
Task 11 [scenario tests] Depends on: Task 3 / Task 4 / Task 5 / Task 7
## Phase 5: Command and user docs
Task 12 [pr-submit.md] Depends on: Task 6 / Task 8
Task 13 [user guides + final checks] Depends on: Task 2 / Task 10 / Task 11 / Task 12
```

### source.md:283-301 (files-to-change table the plan must fully own)

```text
| `src/superclaude/pr_submit/merge_guard.py` | new | section 4.1 |
| `src/superclaude/pr_submit/models.py` | edit | 2 members, docstring and count |
| `src/superclaude/pr_submit/run_log.py` | edit | rebuild_state key, append docstring count |
| `src/superclaude/pr_submit/fsm.py` | edit | flag, SkillArgs, parse_args |
| `src/superclaude/pr_submit/__init__.py` | edit | export the public guard names |
| `scripts/set-draft-state.sh` | new | section 4.4 |
| `refs/merge-guard.md` | new | section 4.5 |
| `SKILL.md`, `refs/state-machine.md`, `refs/loop-guard.md` | edit | additive only (loop-guard: 43→45) |
| `src/superclaude/commands/pr-submit.md` | edit | flag and section |
| `docs/user-guide/commands.md`, `docs/user-guide/flags.md` | edit | flag and paragraph |
| `tests/pr_submit/test_merge_guard.py`, `test_set_draft_state.py` | new | section 7 |
| `tests/skills/test_worker_contract.py` | edit | one WRITE_VERB_CLASSIFICATION entry per new hit line |
| `tests/pr_submit/test_run_log.py`, `test_codex_reviews.py`, `test_static_grep.py`, `test_skill_parse.py` | edit | count 43→45, draft_guard key, CORE_PURE_FILES, script lists, flag test |
```

### source.md:358-378 (section 10 plan-authoring constraints)

```text
- Cite tests and constants by symbol name ... never by bare line number: earlier tasks edit the same files and line numbers drift.
- Declare dependencies completely, one Depends on: line per dependency ...
- The protocol wiring covers the Wave 0 resume and off hook as well as Waves 3, 6 and 8 (section 4.5), with a test for each bullet.
- Run make sync-dev at the end of each task that edits skills/ or commands/, and run the sync-hook tests named in section 6 in the final task.
- The fold, guard_status, resume-reason and per-cycle applied_edits rules ... each get an acceptance criterion that a wrong implementation would fail.
- The pre-build record task states the release-gate decision of section 8 and records the base-commit lint result.
- Update the 43-member enumeration in refs/loop-guard.md in the event-enum task.
- Protocol prose written by the plan never carries file:NNN pointers ...
Added in v3: [classification entries added last per task; L2 line into SKILL.md output table with literal-line test; resume passes published + recovery branch strings, crash tests derive branches from a real RunLog; fold not_applied rules; test hygiene (no imported test_* functions, RunLog.read_events() assertions, string-constant byte compares, repo-pin via fake-gh log + static scan); Wave 3 and Wave 0 bullet ACs assert wording and position, not headings]
```

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|--------------------|---------|--------|-----------|
| INF-011 symbol citations + complete Depends-on | Constraints + Tasks | covered | source.md:362-363 |
| INF-012 files-to-change ownership complete | Tasks 2,3,5,6,7,8,9,10,11,12,13 | covered | source.md:283-301 |
| Structure: 5 phases, 13 tasks, dependency graph acyclic and consumer-declares-producer | — | open | plan:52-115 |
| Convention consistency: sync-dev cadence, classification-last, test placement per task | — | open | plan passim |
