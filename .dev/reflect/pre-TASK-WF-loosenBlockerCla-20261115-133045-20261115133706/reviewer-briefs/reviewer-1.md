# Reviewer brief 1 (persona: analyzer; model class: haiku)

## T1 card excerpt

## Deviation and risk observations

- Drift risk: Phases 4 and 5 can only be started on the owner's go (spec section 12 entry conditions) but the plan carries no machine-checkable gate; an executor that runs the whole plan in one pass would edit `pragmatic.md` (the output style injected into every subagent) without the shadow-stage evidence.
- Internal-consistency risk: Task 24 adds a test that fails if `src/superclaude/output-styles/pragmatic.md` line 225 changes before Task 26. Task 26 changes that line, and neither Task 26 nor Task 31 says to retire or re-pin that test, so it would fail from Task 26 onward.
- Ordering risk: Task 27 and Task 28 depend on Task 26 and Task 1 but the registry rows for `rf-qa.md` and `rf-qa-qualitative.md` are only set to `v2` inside those tasks, while Task 19's strict T2 scan is switched on in Task 39; between Tasks 26 and 39 the T1 digest-equality test must tolerate mixed `legacy` and `v2` rows (the plan says legacy rows are accepted, so this holds).
- Size risk: Tasks 27 and 36 name many line numbers taken from the spec; Task 1 freezes the live list first, which covers staleness for `rf-qa.md` only.
- Evidence risk: the spec's own claims about line numbers and counts were checked for a subset only (the pragmatic.md anchors, the task skill anchors, WORKER-CONTRACT lines 33 and 39, the 13 merge lines). The classifier results the plan cites come from PF `08-test/results.md`, produced by a stand-in judge.

## Recommendations

- Add to Task 26 or Task 31 an explicit instruction to retire or re-pin the Task 24 line-225 test (file `tests/skills/test_review_brief_rests_on.py`).
- State in `## Constraints` that Phase 4 begins with a recorded owner go, and consider splitting Phases 4 and 5 into a second package so no executor can run them in the same pass.
- Keep every classifier task on the Constraints rule that M, C and E run only with code-supplied inputs.

Persona instructions (analyzer): look for deviations and internal contradictions between tasks, and for acceptance criteria that cannot pass as written (the defect class that dominated the blocker study: a check that needs a file or state nothing in that phase produces). Walk the dependency edges (`Depends on:`), check that every file a task says it edits exists or is created by an earlier task, and that no test added by one task is broken by a later task.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-15T13:30:53Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### .dev/tasks/to-do/TASK-WF-loosenBlockerCla-20261115-133045/TASK-WF-loosenBlockerCla-20261115-133045.md:1-36
```markdown
1: ---
2: schema: workflow-plan/1.2
3: source: ./source.md
4: strategy: systematic
5: depth: standard
6: slug: TASK-WF-loosenBlockerCla-20261115-133045
7: version: "1"
8: priority: Medium
9: created_date: "2026-11-15"
10: ---
11: 
12: # Loosen blocker classification across the review loops (issue #552)
13: 
14: Source: ./source.md
15: Goal: Review gates grade each finding by what changes if the flawed text is corrected, record every non-blocking finding in a follow-up ledger with a once-per-run offer to file them, keep security, data-loss and safety findings blocking, and measure a blocker classifier in shadow mode without giving it any authority.
16: 
17: ## Constraints
18: 
19: - Spec: the merged spec `02-brainstorm/merged-requirements.md` inside the program folder `BLOCKER-CLASSIFICATION-PROGRAM-20261115` (found by that folder name under the repository's task folder). This plan calls that folder PF and the spec file the spec. Section numbers, requirement ids (REQ-nn), loop changes (L1 to L6), guardrails (GR1 to GR12), tests (T1 to T17) and owner decisions (OD1 to OD17) refer to the spec. PF also holds the 5-run results in `08-test/results.md`, the reconciliation in `09-plan-input.md`, the blocker characteristics in `06-blocker-characteristics.md` and the classifier sketch in `07-classifier/`.
20: - Stage gating from spec section 12: Phases 1 to 3 are stages 0, 1 and 2 and can run in one pass. Phase 4 is stage 3 (the pilot) and Phase 5 is stage 4. Their entry conditions need things no executor can produce: the owner's go, at least 5 observed shadow runs with zero safety misses, seeded recall met, and stage 0c done. Run `/sc:implement` on Phases 1 to 3 first; do not start Phase 4 until the owner says so in chat, and do not start Phase 5 until the owner says so after the pilot's audit window.
21: - Owner decisions use the spec's recommendations unless the owner changes them: OD1 skill folder `sc-review-severity`; OD2 once per run plus at any escalation halt; OD4 the classifier has no authority in version 1; OD9 reviewer-named consumer, code-checked where quotable; OD11 replace label-max merging at all 13 lines in 10 files, staged; OD12 yes; OD13 short Note rows; OD14 a finding with an unknown consumer keeps the reviewer's label (no deferral); OD15 consent-bound body file posted by the attended top-level session; OD16 option (b) at stage 3. OD3 (finding text leaving the machine), OD5 to OD8 and OD10 are not decided here and no task depends on a different answer.
22: - Not built here: any Jev or other external judge call, any TypeSafe account or key, a Jev or LLM judge class (they wait for OD3), any change to `src/superclaude/skills/sc-implement-protocol/refs/qa.md` (it keeps its own scale), any change to the own-scale primitives listed in spec section 9.3 as unchanged, the 35 percent score target, and any change to the cap of 2 fix cycles.
23: - Classifier facts that bind every classifier task: the 5-run test of PF `08-test/results.md` used a text-only stand-in judge and got agreement with the panel of 58.5 percent (Cohen's kappa 0.27), and the missing-item, constraint and contradiction questions (M, C, E) were at chance without code-supplied inputs. So M, C and E run only when code supplies the required-item list, the constraint lines and the verified evidence, the "M or C is Y gives BLOCKING" row is never enabled for any gate in this plan, and confidence is reported as an ordinal band, never as a probability.
24: - `src/superclaude/` is the source of truth. Edit there, then run `make sync-dev`; never stage anything under the project `.claude/` folder (only `.claude/settings.json` is tracked). Installed primitives name installed paths (`~/.claude/skills/...`) first and project `.claude/...` second, never a `src/superclaude/` path.
25: - Python work uses UV only: `uv run pytest ...`, never `python -m` or bare `pip`.
26: - Task-owned evidence and generated outputs go under `./artifacts/` in this package.
27: 
28: ## Phase 1: Close the measurement stage (stage 0)
29: 
30: ## Task 1: Freeze the pattern inventory of spec section 10
31: 
32: Re-run, with plain `grep -rn` (not the Grep tool, which skips gitignored folders and so misses the project `.claude/` copies) over `src/superclaude`, `plugins/superclaude` and the project `.claude/` folder, every pattern the spec lists in section 10: the definition sentence `Grade every review finding as blocking or minor` (spec: 11 files), `Blocking is a real defect` (11), `Minor findings never fail a review` (11), `at most 2 fix cycles \(3 reviews\)` (12), `CRITICAL and IMPORTANT findings are blocking` (7), `follow-up candidates` (3 files, 7 lines), `2 fix cycles` (22 files, 120 lines), the two merge-rule patterns of section 10.3 (13 lines in 10 files), the tasklist pattern `High or Medium` and `Medium (blocking)` in `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` (7 lines), and the REQ-30 fixed FAIL-trigger patterns `= FAIL`, `that's a FAIL`, `regardless of severity`, `highest severity`, `never minor`, `always IMPORTANT` over `src/superclaude/agents`, `src/superclaude/skills`, `src/superclaude/templates` and `src/superclaude/rules`. Write the counts and every hit line to `./artifacts/stage0-inventory-freeze.md`.
33: 
34: Acceptance criteria:
35: - `./artifacts/stage0-inventory-freeze.md` exists and has one table row per pattern with the columns pattern, scope, spec count, observed count and difference.
36: - Every REQ-30 FAIL-trigger pattern has its hit lines (file, line number, text) listed, so later tasks use this list and not a remembered one.
```


## Coverage slice

```yaml
coverage_matrix:
  - requirement_id: INF-001
    source: inferred
    matched_task_ids: []
    match_method: none
    best_ratio: 0.222
  - requirement_id: INF-002
    source: inferred
    matched_task_ids: []
    match_method: none
    best_ratio: 0.385
  - requirement_id: INF-003
    source: inferred
    matched_task_ids: []
    match_method: none
    best_ratio: 0.25
  - requirement_id: INF-004
    source: inferred
    matched_task_ids: []
    match_method: none
    best_ratio: 0.579
```

---
You are a read-only reviewer (agent type reflect-reviewer). You never edit, write, move or delete anything and you run no shell or git command. Audit ONLY the plan and the evidence named below, using Read, Grep, Glob (and codegraph tools only because index_state=fresh, with the projectPath above). Every claim you make must cite a repo-relative `file:line` that you have Read. A claim you cannot cite is tagged [INFERRED] or dropped.

Mode: UC-1 pre-execution review. Plan under review: `.dev/tasks/to-do/TASK-WF-loosenBlockerCla-20261115-133045/TASK-WF-loosenBlockerCla-20261115-133045.md` (5 phases, 39 tasks). Driving source: `.dev/tasks/to-do/TASK-WF-loosenBlockerCla-20261115-133045/source.md`. The plan implements a merged spec that lives in the program folder named BLOCKER-CLASSIFICATION-PROGRAM-20261115 (file `02-brainstorm/merged-requirements.md`, find it by Glob under `.dev/tasks/`); read the parts you need, not the whole 1,224 lines.

Return ONE markdown card as your final message, nothing else, with exactly these sections:
## Verdict
one line: PASS, PASS-with-notes or NEEDS-REVISION, then one sentence why.
## Findings
one block per finding: `F<n>` | severity CRITICAL / MAJOR / MINOR | blocking true/false | category (contradiction, missing-requirement, unpassable-check, data-loss, safety, other) | claim (one or two sentences naming WHO acts and WHAT wrong result they get) | citations (1 to 6 `path:line` refs with a short quote). Report only real defects with evidence. A zero-finding result is valid if you state what you checked. Do not invent findings and do not work to a quota. Minor wording or formatting is MINOR and non-blocking.
## Checked
a short list of what you verified and found sound (file:line each).
## Self-report
`confidence: <0.00-1.00>` and `reviewer_model_self_report: <the model you run as, one line>`.

