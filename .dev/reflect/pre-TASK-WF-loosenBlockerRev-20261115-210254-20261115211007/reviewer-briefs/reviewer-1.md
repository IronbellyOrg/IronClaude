# Reviewer brief 1 (persona: analyzer; model class: haiku)

## T1 card excerpt

## Deviation and risk observations

- Self-trip risk, found while writing this card: Task 13 puts the three merge-rule phrases `highest severity`, `more severe rating` and `higher severity` into `refs/scale-map.md` (its "Merge-rule allow-list" section names them), and Task 40's scan covers every Markdown file under `src/superclaude/skills` and `plugins/superclaude`, with an allow-list that does not list `scale-map.md` (Task 40 lists the auggie file, `refs/rule.md` and its mirror, and the six stage 4 files). The first run of Task 40's test would fail on `scale-map.md` and on its Task 46 plugin mirror unless that file avoids the literal phrases or is allow-listed.
- Ordering risk: Task 46 copies the skill folder into the plugin and then adds a `canonical` registry row to the registry file that the folder copy already contains, while the T15 parity test requires the mirror to equal the source.
- Gate risk: the three owner gates are prose in `## Constraints`; no task checks that a recorded owner go exists before Phase 3, 4 or 5 starts. Task 11 depends on Task 10 but Tasks 26, 31 and 41 carry no dependency on the earlier phase's last task.
- Evidence risk: line numbers named in Tasks 33 to 45 (pragmatic.md 225, 226 and 229; rf-qa 402 and 549; rule-prompt lines near 11, 27, 28) were re-read from disk for the files verified in the pre-check, and are marked "near" for the template and rule-prompt files that were not re-read.
- Dependency risk: the plan cites the spec by section and requirement id (REQ-01 to REQ-30, GR1 to GR12, T1 to T17) without restating them; a reviewer must open the 1,224-line spec to confirm each citation.


## Recommendations

- Rewrite the Task 13 allow-list section so `scale-map.md` does not contain the three phrases literally, or add `scale-map.md` and its plugin mirror to Task 40's allow-list.
- Make Task 46 add the plugin `canonical` row before the copy, or say the copy is repeated after the row is added.
- Add an explicit "owner go recorded in chat" acceptance line to the first task of each gated phase.


Persona instructions (analyzer): look for deviations and internal contradictions between tasks, and for acceptance checks that cannot pass as written (a check that needs a file or state nothing in that phase produces, or that a task's own edit breaks). Walk the `Depends on:` edges, check each file a task edits exists today or is created by an earlier task, and check that each grep-style acceptance check would print what the task says given the live files. Test the T1 card's observations (self-trip risk of the Task 40 scan, Task 46 ordering, gate risk) against the live files before agreeing or disagreeing.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-15T21:04:00Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### .dev/tasks/to-do/TASK-WF-loosenBlockerRev-20261115-210254/TASK-WF-loosenBlockerRev-20261115-210254.md:1-28
```markdown
1: ---
2: schema: workflow-plan/1.2
3: source: ./source.md
4: strategy: systematic
5: depth: standard
6: slug: TASK-WF-loosenBlockerRev-20261115-210254
7: version: "1"
8: priority: Medium
9: created_date: "2026-11-15"
10: ---
11: 
12: # Loosen blocker classification across the review loops, revised plan (issue #552)
13: 
14: Source: ./source.md
15: Goal: Review gates grade each finding by what changes if the flawed text is corrected, record every non-blocking finding in a follow-up ledger with a once-per-run offer to file them, keep security, data-loss and safety findings blocking, and measure a blocker classifier in shadow mode without giving it any authority. This plan revises the first plan after its pre-execution review found 12 blocking defects.
16: 
17: ## Constraints
18: 
19: - Spec: the merged spec `02-brainstorm/merged-requirements.md` inside the program folder `BLOCKER-CLASSIFICATION-PROGRAM-20261115` (found by that folder name under the repository's task folder). This plan calls that folder PF and the spec file the spec. Section numbers, requirement ids (REQ-nn), loop changes (L1 to L6), guardrails (GR1 to GR12), tests (T1 to T17) and owner decisions (OD1 to OD17) refer to the spec. PF also holds the 5-run results in `08-test/results.md`, the reconciliation in `09-plan-input.md`, the blocker characteristics in `06-blocker-characteristics.md` and the classifier sketch in `07-classifier/`.
20: - Owner gates. Phase 1 is stage 0 (measurement, no change under `src/`). Phase 2 (stage 1, offline scaffold) starts only after the owner has read the stage 0 results (Task 10 writes them in one file) and said go in chat. Phase 3 (stage 2, shadow) starts only after the stage 1 exit (every Phase 2 acceptance check green) and the owner's say-so. Phase 4 (stage 3, the pilot) starts only after the owner says so; its entry conditions per spec section 12 also need at least 5 observed shadow runs with zero safety misses and no capture failure (the owner or operator runs those shadow runs over time; no task here can produce them), the seeded-recall result of Task 31 and stage 0c (Task 4). Phase 5 (stage 4) starts only after the owner says so after the pilot's audit window. Run `/sc:implement` on one phase at a time and stop at each gate.
21: - Owner decisions use the spec's recommendations unless the owner changes them: OD1 skill folder `sc-review-severity`; OD2 once per run plus at any escalation halt; OD4 the classifier has no authority in version 1; OD9 reviewer-named consumer, code-checked where quotable; OD11 replace label-max merging at all 13 lines in 10 files, staged; OD12 yes; OD13 short Note rows; OD14 a finding with an unknown consumer keeps the reviewer's label (no deferral); OD15 consent-bound body file posted by the attended top-level session; OD16 option (b) at stage 3. OD3 (finding text leaving the machine), OD5 to OD8 and OD10 are not decided here and no task depends on a different answer.
22: - Not built here: any Jev or other external judge call, any TypeSafe account or key, a Jev or LLM judge class (they wait for OD3), any change to `src/superclaude/skills/sc-implement-protocol/refs/qa.md` (it keeps its own scale), any change to the own-scale primitives listed in spec section 9.3 as unchanged, code-assigned severity in `src/superclaude/cli/**/*.py` (for example `fmea_classifier.py` and `remediate_parser.py`, out of scope by spec section 10.3), the 35 percent score target, and any change to the cap of 2 fix cycles.
23: - Classifier facts that bind every classifier task: the 5-run test of PF `08-test/results.md` used a text-only stand-in judge and got agreement with the panel of 58.5 percent (Cohen's kappa 0.27), and the missing-item, constraint and contradiction questions (M, C, E) were at chance without code-supplied inputs. So M, C and E run only when code supplies the required-item list, the constraint lines and the verified evidence (Task 20 builds the supplier), the "M or C is Y gives BLOCKING" row is never enabled for any gate in this plan, and confidence is reported as an ordinal band, never as a probability.
24: - Pins are by content. An acceptance check that must survive a task's own edit quotes the sentence it protects; it does not name a line number, because the edit moves the line. Line numbers in a task body are where the text sits today and are re-read before editing.
25: - `src/superclaude/` is the source of truth. Edit there, then run `make sync-dev`; never stage anything under the project `.claude/` folder (only `.claude/settings.json` is tracked). Installed primitives name installed paths (`~/.claude/skills/...`) first and project `.claude/...` second, never a `src/superclaude/` path.
26: - Python work uses UV only: `uv run pytest ...`, never `python -m` or bare `pip`.
27: - Task-owned evidence and generated outputs go under `./artifacts/` in this package.
28: 
```

### .dev/tasks/to-do/TASK-WF-loosenBlockerRev-20261115-210254/TASK-WF-loosenBlockerRev-20261115-210254.md:160-174
```markdown
160: ## Task 13: Write the scale map
161: 
162: Depends on: Task 11
163: 
164: Create `src/superclaude/skills/sc-review-severity/refs/scale-map.md` with one row per family of spec section 9.3: family, defining file, each native label, the shared outcome per label (Blocking, Medium, Note), and either "graded by the three conditions" or "keeps its own model because <reason>". The rows are the 12 families of that table: the CRITICAL, IMPORTANT, MINOR lens scale; the `/sc:implement` `refs/qa.md` checklist; spec-panel; the stoprule rubric and `finding-grader`; the reflect deviation taxonomy; tasklist High, Medium, Low; roadmap validate; `card_convert.py`; findings-v1 and v2; `sc-auggie-review-protocol/SKILL.md:228`; the PR severity router and Auggie rubric; and the code-assigned family. Include the sentence that a keep of a fixed FAIL trigger (L6) is recorded here, and a section "Merge-rule allow-list" that names the files allowed to contain the phrases `highest severity`, `more severe rating` or `higher severity` (the auggie file, `refs/rule.md`, and the six stage 4 files until Phase 5) so Task 40 reads its allow-list from one place.
165: 
166: Acceptance criteria:
167: - `refs/scale-map.md` has a row for each of the 12 families, each naming a defining file that exists in the repository.
168: - The tasklist row states that Medium is blocking today on 7 lines of `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` and that no stage 1 to 4 task changes it.
169: - The `card_convert.py` row states that its word translator maps `important` and `medium` to non-blocking while `src/superclaude/agents/rf-qa.md` treats IMPORTANT as blocking.
170: - The "Merge-rule allow-list" section exists and lists the auggie file, `refs/rule.md` and the six stage 4 files.
171: 
172: ## Task 14: Write the follow-up ledger reference
173: 
174: Depends on: Task 11
```

### .dev/tasks/to-do/TASK-WF-loosenBlockerRev-20261115-210254/TASK-WF-loosenBlockerRev-20261115-210254.md:474-490
```markdown
474: 
475: Depends on: Task 34, Task 35, Task 36, Task 37
476: 
477: Create `tests/skills/test_review_merge_rule_scan.py` for T5. The scan reads Markdown files only (`*.md`), under `src/superclaude/agents`, `src/superclaude/skills`, `src/superclaude/templates`, `src/superclaude/rules`, `src/superclaude/commands`, `src/superclaude/output-styles` and `plugins/superclaude`, matches `highest severity`, `more severe rating` and `higher severity` case-insensitively, and fails on a hit outside the allow-list. Code files (`src/superclaude/cli/**/*.py`) are not scanned: the spec puts `fmea_classifier.py` and `remediate_parser.py` out of scope. The allow-list is read from the "Merge-rule allow-list" section of `refs/scale-map.md`: `src/superclaude/skills/sc-auggie-review-protocol/SKILL.md`, `src/superclaude/skills/sc-review-severity/refs/rule.md` and its plugin mirror path, and, until Phase 5, the six stage 4 files (`src/superclaude/skills/tech-reference/SKILL.md`, `src/superclaude/skills/readme/SKILL.md`, `src/superclaude/skills/tdd/refs/build-request-template.md`, `src/superclaude/skills/operational-guide/SKILL.md`, `src/superclaude/templates/documents/agent_template_qa.md` and `src/superclaude/templates/documents/agent_template_analysis.md`). Each Phase 5 task that edits one of those files removes it from the allow-list in the same change.
478: 
479: Acceptance criteria:
480: - `uv run pytest tests/skills/test_review_merge_rule_scan.py -v` passes on the current tree after Tasks 34 to 37, with no hit in `src/superclaude/cli/` counted.
481: - A temporary-tree test with `highest severity` in a Markdown file that is not allow-listed fails the scan, and a temporary-tree test with the phrase in a Python file under `cli/` passes.
482: - The allow-list is read from `refs/scale-map.md` and a test fails when a file named there does not exist.
483: 
484: ## Phase 5: Propagate to the remaining carriers (stage 4), only after the owner's go
485: 
486: ## Task 41: Move the templates to digest v2
487: 
488: Depends on: Task 40
489: 
490: Edit the digest carriers in `src/superclaude/templates/`: `documents/agent_template_qa.md` (the definition bullet near line 161, the merge rule near line 85, the Rule 6 text near line 333 per OD16, and the FAIL-by-label bullet "Any CRITICAL or IMPORTANT issue exists" near line 158, rewritten or kept as a named mechanical gate recorded in `refs/scale-map.md`), `documents/agent_template_analysis.md` (the merge rule near line 466), `documents/skill_template.md` (the definition near line 828), `workflow/01_mdtm_template_generic_task.md` (near line 644) and `workflow/02_mdtm_template_complex_task.md` (near line 655). Each gets the digest and pointer in place of the definition bullets and the L1 merge text; update their registry rows to `v2`; remove `agent_template_qa.md` and `agent_template_analysis.md` from the allow-list of Task 40. Task files already generated from the old templates keep the old text and are not migrated.
```


## Coverage slice

| Requirement | Quote (source.md line) | Best task | Ratio | Mechanical match |
|---|---|---|---|---|
| INF-001 | The Constraints must state three owner gates, not two (13) | 14 | 0.571 | none |
| INF-002 | Remove the sentence that lets Phases 1 to 3 "run in one pass". (13) | 12 | 0.571 | none |
| INF-003 | Phase 1 gains a task that records stage 0 step 0a (14) | 14 | 0.667 | containment-0.6 |
| INF-004 | Phase 1 gains a task that defines and sizes the seeded-defect recall set of spec section 8 (15) | 7 | 0.636 | containment-0.6 |
| INF-005 | running the set under both rule texts is part of stage 3 entry and is a Phase 4 task (15) | 31 | 0.636 | containment-0.6 |
| INF-006 | Phase 1 gains a task that builds the fresh-findings set the reconciliation requires (16) | 5 | 0.556 | none |
| INF-007 | Phase 1 gains a task that reports, for the 318 scored rows, how many rows had each code-su (17) | 8 | 0.769 | containment-0.6 |
| INF-008 | Phase 2 gains a task that builds the supplier of those inputs (18) | 0 | 0.857 | containment-0.6 |
| INF-009 | The classify command and the classifier run the M, C and E questions only when this module (18) | 22 | 0.7 | containment-0.6 |
| INF-010 | The registry schema gets a `kind` field with the values `digest`, `canonical`, `pointer-on (22) | 16 | 0.7 | containment-0.6 |
| INF-011 | `skills/task/SKILL.md` is not a digest carrier and gets no registry row (23) | 16 | 1.0 | containment-0.6 |
| INF-012 | `rules/prompts/document_review_loop_prompts.md` and `commands/spec-panel.md` are `pointer- (23) | 16 | 1.0 | containment-0.6 |
| INF-013 | Task 33's scan covers Markdown files only (27) | 40 | 0.8 | containment-0.6 |
| INF-014 | Phase 5 tasks remove those six from the allow-list in the same task that edits each file (27) | 40 | 0.909 | containment-0.6 |
| INF-015 | The final-gate sweep and the once-per-run offer are wired once, into the task skill's Post (31) | 27 | 0.923 | containment-0.6 |
| INF-016 | In stage 2 (Phase 3) the sweep only records (32) | 14 | 1.0 | containment-0.6 |
| INF-017 | Add a test (extending T12) that the stage 2 sweep changes no gate result. (32) | 21 | 0.667 | containment-0.6 |
| INF-018 | Add the escalation-halt offer (OD2) at the cap sites (33) | 28 | 0.571 | none |
| INF-019 | Task 28 (rf-qa-qualitative) also rewrites, or keeps as named mechanical gates recorded in  (37) | 35 | 0.786 | containment-0.6 |
| INF-020 | Task 34 (templates) does the same for `src/superclaude/templates/documents/agent_template_ (37) | 40 | 0.8 | containment-0.6 |
| INF-021 | Task 1's frozen patterns add `Any CRITICAL or IMPORTANT issue exists` (37) | 1 | 0.75 | containment-0.6 |
| INF-022 | Acceptance checks that pin a line number pin the content instead (41) | 0 | 0.571 | none |
| INF-023 | Task 26 replaces three bullets of `pragmatic.md` (42) | 31 | 0.8 | containment-0.6 |
| INF-024 | Task 24's pin of `pragmatic.md` lines 225 to 231 is keyed to the registry row (43) | 33 | 0.667 | containment-0.6 |
| INF-025 | L3 (three choices at the cap) is applied at every cap site (44) | 34 | 0.667 | containment-0.6 |
| INF-026 | Task 31 also updates the two plan tables that the fixtures must be byte copies of (45) | 38 | 0.9 | containment-0.6 |
| INF-027 | Task 30's check on the cap text uses the wording the task skill actually has (46) | 0 | 0.778 | containment-0.6 |
| INF-028 | Do not change the cap of 2 fix cycles, the own-scale primitives, `sc-implement-protocol/re (55) | 0 | 1.0 | containment-0.6 |

---
You are a read-only reviewer (agent type reflect-reviewer). You never edit, write, move or delete anything and you run no shell or git command. Audit ONLY the plan and the evidence named below, using Read, Grep, Glob (and codegraph tools only because index_state=fresh, with the projectPath above). Every claim you make must cite a repo-relative `file:line` that you have Read. A claim you cannot cite is tagged [INFERRED] or dropped.

Mode: UC-1 pre-execution review. Plan under review: `.dev/tasks/to-do/TASK-WF-loosenBlockerRev-20261115-210254/TASK-WF-loosenBlockerRev-20261115-210254.md` (5 phases, 46 tasks). Driving source: `.dev/tasks/to-do/TASK-WF-loosenBlockerRev-20261115-210254/source.md` (a revision request that lists the changes to apply to a first plan). The plan implements a merged spec that lives in the program folder named BLOCKER-CLASSIFICATION-PROGRAM-20261115 (file `02-brainstorm/merged-requirements.md`, find it by Glob under `.dev/tasks/`); read the parts you need, not the whole 1,224 lines. The first plan and its review (for comparison only) are `.dev/tasks/to-do/TASK-WF-loosenBlockerCla-20261115-133045/` and `.dev/reflect/pre-TASK-WF-loosenBlockerCla-20261115-133045-20261115133706/adversarial/merged-review-card.md`.

Severity rule for this review. Blocking means: the plan, followed literally, leaves (i) an acceptance check or requirement that cannot be met, whose fix needs a decision the plan does not make, or (ii) a silent wrong or missing result. Wording, mechanical coordinate errors with a stated intent, and extra checks the plan forbids are MINOR and non-blocking. Verify claims against the live files before you report them; a plan statement about a live file that you did not check is not a finding.

Return ONE markdown card as your final message, nothing else, with exactly these sections:
## Verdict
one line: PASS, PASS-with-notes or NEEDS-REVISION, then one sentence why.
## Findings
one block per finding: `F<n>` | severity CRITICAL / MAJOR / MINOR | blocking true/false | category (contradiction, missing-requirement, unpassable-check, data-loss, safety, other) | claim (one or two sentences naming WHO acts and WHAT wrong result they get) | citations (1 to 6 `path:line` refs with a short quote). Report only real defects with evidence. A zero-finding result is valid if you state what you checked. Do not invent findings and do not work to a quota.
## Checked
a short list of what you verified and found sound (file:line each).
## Self-report
`confidence: <0.00-1.00>` and `reviewer_model_self_report: <the model you run as, one line>`.
