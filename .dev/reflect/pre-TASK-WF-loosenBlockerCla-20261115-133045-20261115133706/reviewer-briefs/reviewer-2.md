# Reviewer brief 2 (persona: qa; model class: opus)

## T1 card excerpt

## Coverage and acceptance

The source has no labelled requirement ids (parsed_count 0), so Step 1B.0 Pass 2 emitted four inferred rows (`artifacts/coverage-matrix.yaml`). The deterministic containment rule (60 percent of a quote's content words inside ONE task) matched none of them, so the mechanical numbers are `coverage_pct_union: 0.0` and `S_dev_density: 1.0`. That is a limit of the rule on long prose quotes, not proof of non-coverage. Reading the plan against each row:

- INF-001 "Loosen blocker classification across the review loops as specified in the merged spec": Phases 2 to 5 (Tasks 6 to 39) implement the spec's stages 1 to 4; Phase 1 (Tasks 1 to 5) is stage 0. Covered by design; stage 3 and stage 4 execution is gated by a human instruction in `## Constraints`, not by anything the executor can enforce.
- INF-002 "Record non-blocking findings in a follow-up ledger and offer to file them as issues": Task 9 (ledger reference), Task 12 (codec, reader, writer), Task 13 (filing state machine), Tasks 21 and 22 (shadow-mode write and per-run offer in the task skill and tech-research). Covered.
- INF-003 "Apply the reconciliation in the plan-input note": Tasks 3, 4 and 5 and the Constraints bullet on classifier facts carry items 1, 3, 4, 5 and 6 of the note; item 2 (stage 0a already has a stand-in result) is a Constraints sentence only. Covered, with one item carried as prose rather than a task.
- INF-004 "Code and text: task, tech-research, rf-qa family, pragmatic output style plus WORKER-CONTRACT.md": Tasks 21, 22 (task, tech-research), 23 (WORKER-CONTRACT), 26 (pragmatic.md), 27 to 29 (rf-qa, rf-qa-qualitative, rf-analyst). Covered. `agents/rf-task-builder.md` and `skills/task-builder/SKILL.md` appear only in Task 37 as "cap text unchanged".

Persona instructions (qa): audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding. Then check the plan against the merged spec: does each spec stage 0 to 4 element the plan claims to cover have a task, are owner decisions applied as the Constraints say, and does any task contradict the spec (section numbers, requirement ids REQ-nn, tests T1 to T17)? Note the 5-run classifier result the plan cites (PF 08-test/results.md) and check the plan does not enable anything that result argues against.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-15T13:30:53Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### .dev/tasks/to-do/TASK-WF-loosenBlockerCla-20261115-133045/source.md:1-1
```markdown
Loosen blocker classification across the review loops as specified in .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md (issue IronbellyOrg/IronClaude#552). Record non-blocking findings in a follow-up ledger and offer to file them as issues, instead of halting and forcing re-reviews. Apply the reconciliation in .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/09-plan-input.md. Code and text: the review-loop skills and agents listed in section 10 of the spec (task, tech-research, rf-qa family, pragmatic output style) plus WORKER-CONTRACT.md.
```

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

