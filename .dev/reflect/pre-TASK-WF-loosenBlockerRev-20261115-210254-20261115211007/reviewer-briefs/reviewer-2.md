# Reviewer brief 2 (persona: qa; model class: opus)

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


Persona instructions (qa): audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding. Then check the plan against the merged spec and the revision request: does every change the request lists have a task, does any task contradict the request or the spec (section numbers, requirement ids REQ-nn, tests T1 to T17), and are the three owner gates, the not-built list and the classifier constraints applied as the request says? Check the plan does not enable anything the 5-run classifier result in PF `08-test/results.md` argues against.

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

### .dev/tasks/to-do/TASK-WF-loosenBlockerRev-20261115-210254/source.md:1-55
```markdown
1: # Revised plan request: loosen blocker classification across the review loops (issue #552)
2: 
3: This revises the first plan, package `TASK-WF-loosenBlockerCla-20261115-133045` (5 phases, 39 tasks). A pre-execution review of that plan (report `REPORT.md` in the reflect run folder `pre-TASK-WF-loosenBlockerCla-20261115-133045-20261115133706` under `.dev/reflect/`) returned NEEDS-REVISION with 12 blocking and 5 non-blocking findings. Generate a new plan package that keeps everything the review found sound and applies every change below. Keep the five-phase shape, the stage gating, the constraints and the owner-decision defaults of the first plan; the tasks not named below stay as they were, with their numbers renumbered where tasks are added.
4: 
5: ## Original goal (unchanged)
6: 
7: Loosen blocker classification across the review loops as specified in the merged spec `02-brainstorm/merged-requirements.md` in the program folder `BLOCKER-CLASSIFICATION-PROGRAM-20261115` (issue IronbellyOrg/IronClaude#552). Record non-blocking findings in a follow-up ledger and offer to file them as issues, instead of halting and forcing re-reviews. Apply the reconciliation in `09-plan-input.md` of the same folder. Code and text: the review-loop skills and agents listed in section 10 of the spec (task, tech-research, rf-qa family, pragmatic output style) plus `WORKER-CONTRACT.md`. The first plan's `## Constraints` section (stage gating, owner-decision defaults OD1, OD2, OD4, OD9, OD11 to OD16, the not-built list, the classifier facts from the 5-run test, UV only, `src/superclaude/` as source of truth) carries over unchanged except where a change below says otherwise.
8: 
9: ## Changes to apply
10: 
11: ### Gating and owner checkpoints (review findings F4, F8, F9, F10)
12: 
13: - The Constraints must state three owner gates, not two: Phase 2 (stage 1, offline scaffold) starts only after the owner has read the stage 0 results and said go; Phase 3 (stage 2, shadow) starts only after the stage 1 exit; Phase 4 and Phase 5 need the owner's go as before. Spec section 12 requires "stage 0 result written; owner go" before stage 1 and that the owner has seen the numbers before any stage starts. Remove the sentence that lets Phases 1 to 3 "run in one pass".
14: - Phase 1 gains a task that records stage 0 step 0a: the five runs already on file in the program folder (`08-test/results.md`, produced by a stand-in LLM judge on a text-only variant, not by Jev), written to `./artifacts/stage0a-result.md` with the agreement figures, Cohen's kappa, flip rate and the stated limits, so the owner sees a complete stage 0.
15: - Phase 1 gains a task that defines and sizes the seeded-defect recall set of spec section 8.3: plant known defects of four classes (decision-bearing false claim, missing required section, safety risk, cosmetic) in a held-out deliverable, large enough to see a 5-point change in recall, reviewed under the old and the new rule text by the same reviewers; the output is `./artifacts/seeded-recall-set.md` (the sizing argument and the planted-defect list) and the planted deliverable itself under `./artifacts/seeded/`. The plan must not say seeded recall is something "no executor can produce"; running the set under both rule texts is part of stage 3 entry and is a Phase 4 task.
16: - Phase 1 gains a task that builds the fresh-findings set the reconciliation requires (findings that were not among the 318 scored rows): the 17 merged findings of the review of the first plan (in the reflect report named above, with verified citations) plus the reviewer-called-minor sample from the stage 0b escape test; score each blind with three agents as in the program's scoring step and write `./artifacts/fresh-findings.md`. Task 4's held-out split must keep these as a separate population and must not mix them into the 318.
17: - Phase 1 gains a task that reports, for the 318 scored rows, how many rows had each code-supplied input for the classifier's missing-item (M), constraint (C) and contradiction (E) questions (the required-item list, the constraint lines, the verified evidence excerpt); the expected baseline is zero for all three, and the file `./artifacts/classifier-input-availability.md` states that.
18: - Phase 2 gains a task that builds the supplier of those inputs: a module `src/superclaude/cli/review/classifier_inputs.py` that, given a deliverable file and a finding, returns the required-item list (from the template's or the acceptance criteria's required sections), the constraint lines (quoted constraints and non-goals) and the evidence excerpt marked verified or unverified by re-reading the cited lines; with tests in `tests/review/test_review_classifier_inputs.py`. The classify command and the classifier run the M, C and E questions only when this module supplied their inputs, otherwise the answer is NA or UNSET as the spec defines; add an acceptance check and a test for that, and for the per-run count of rows that had each input.
19: 
20: ### Registry and digest (review findings F1, F2)
21: 
22: - The registry schema gets a `kind` field with the values `digest`, `canonical`, `pointer-only` and `installed-only`. The digest-equality test (T1) applies to `digest` rows only. `refs/rule.md` of the new skill folder, and its plugin mirror, are registered as `canonical` rows: they hold the one source digest, are exempt from the "no unregistered fence opener" scan, and the wording "exactly the 11 carriers" becomes "exactly the 11 definition carriers of kind `digest`, plus the rows of the other kinds listed".
23: - `skills/task/SKILL.md` is not a digest carrier and gets no registry row: at stage 3 it receives only the merge-rule, fix and escalation text. Remove the instruction to set a task-skill registry row to `v2`. `rules/prompts/document_review_loop_prompts.md` and `commands/spec-panel.md` are `pointer-only` rows (pointer plus the ledger sentence, no digest) checked by T3, never by T1; Task 35 and Task 38 set their registry state accordingly and do not mark them `v2` digests.
24: 
25: ### Merge-rule scan (review finding F5)
26: 
27: - Task 33's scan covers Markdown files only, under `src/superclaude/{agents,skills,templates,rules,commands,output-styles}` and `plugins/superclaude`, case-insensitive. Code files (`src/superclaude/cli/**/*.py`, including `fmea_classifier.py` and `remediate_parser.py`) are out of scope by the spec and are excluded. The allow-list is the scale-map rows: `src/superclaude/skills/sc-auggie-review-protocol/SKILL.md`, the GR5 sentence inside the new skill's `refs/rule.md` and its plugin mirror, and, until Phase 5, the six stage 4 files; Phase 5 tasks remove those six from the allow-list in the same task that edits each file (Task 36 for four of them, Task 34 for the two templates).
28: 
29: ### Final-gate sweep, offer and record-only stage 2 (review findings F3, F7, F12)
30: 
31: - The final-gate sweep and the once-per-run offer are wired once, into the task skill's Post-Completion Validation (`src/superclaude/skills/task/SKILL.md`, the section "Post-Completion Validation (Final Phase Only)" near line 288); tech-research runs inside `/task` (its Step "Execution transfers to /task"), so it gets no second sweep and no second offer, only the ledger path, the reviewer-brief fields, the safety route and the shadow classifier call. Task 20's sweep module is consumed by that one call site.
32: - In stage 2 (Phase 3) the sweep only records: it writes the would-be Blocking rows to the ledger as `sweep-flagged` and changes no gate outcome, because the old definition still decides (a Medium finding never fails a review under the legacy rule). Promotion of a swept Medium row to Blocking starts at the Phase 4 task that edits the task skill's consolidation, fix and escalation text. Add a test (extending T12) that the stage 2 sweep changes no gate result.
33: - Add the escalation-halt offer (OD2) at the cap sites: `src/superclaude/skills/task/SKILL.md` lines 258, 372 and 409, `src/superclaude/skills/tech-research/SKILL.md` line 490 and `src/superclaude/agents/rf-qa.md` line 402, so every halt shows the offer once, with the named owner of the offer being the task skill's end-of-run offer (no double offer).
34: 
35: ### Fail-by-label bullets left beside the digest (review findings F6, F11)
36: 
37: - Task 28 (rf-qa-qualitative) also rewrites, or keeps as named mechanical gates recorded in the scale map, the eight verdict pairs that fail a review on "Any CRITICAL or IMPORTANT issue exists": `src/superclaude/agents/rf-qa-qualitative.md` lines 240, 291, 362, 429, 500, 567, 746 and 784 (each with its PASS bullet one line above). Task 34 (templates) does the same for `src/superclaude/templates/documents/agent_template_qa.md` line 158. Task 1's frozen patterns add `Any CRITICAL or IMPORTANT issue exists`, so these are in the frozen inventory. Task 32 re-pins the audit tests for them. Acceptance: `grep -c "Any CRITICAL or IMPORTANT issue exists"` over both files prints 0, or each remaining line is listed in `refs/scale-map.md` with its reason.
38: 
39: ### Pins, paths and wording (review findings F13 to F17, and the validator's corrections)
40: 
41: - Acceptance checks that pin a line number pin the content instead (quote the sentence), because the task's own edit moves the line: Task 21 (the merge-rule lines of the task skill), Task 22 (the tech-research cap lines), Task 26 (the cap and own-scale bullets of `pragmatic.md`, which a multi-line fenced digest displaces from lines 227 and 228). The existence check for the output-style hook uses `src/superclaude/hooks/hooks.json` (the file at the repository root `hooks/hooks.json` does not exist; `plugins/superclaude/hooks/hooks.json` also exists).
42: - Task 26 replaces three bullets of `pragmatic.md` (lines 225 S1, 226 S2 and 229 S5), not two.
43: - Task 24's pin of `pragmatic.md` lines 225 to 231 is keyed to the registry row of `output-styles/pragmatic.md` being `legacy`: the test passes while that row is `legacy` and is skipped once it is `v2`; Task 31's list also names `tests/skills/test_review_brief_rests_on.py` so the test is re-pinned or retired deliberately.
44: - L3 (three choices at the cap) is applied at every cap site, not only `task/SKILL.md:258`: `task/SKILL.md` 372 and 409 and `agents/rf-qa.md` 402 (see the halt offer above).
45: - Task 31 also updates the two plan tables that the fixtures must be byte copies of: `.dev/review-severity-rule/cap-edits.yaml` and `.dev/review-severity-rule/sweep-edits.yaml` (test `test_ej_fixtures_are_byte_copies_of_the_plan_tables` in `tests/skills/test_review_severity_rule.py` compares them), or says which relaxation of that test is chosen.
46: - Task 30's check on the cap text uses the wording the task skill actually has ("After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings", lines 258, 372 and 409), not the output style's `CANONICAL_CAP_TEXT`, which is asserted against the output style only.
47: - Wording slips: Task 11's "exactly the 11 carriers" (it also adds own-scale and installed-only rows; see the registry change above); Task 33 names Task 34 as removing the six stage 4 files from the allow-list (Task 36 removes four, Task 34 removes the two templates, now stated).
48: 
49: ## Review findings that stand as written in the first plan
50: 
51: The 11 definition carriers of spec section 10.1, the 13 merge-rule lines in 10 files plus the auggie line, the anchors in `pragmatic.md`, the task skill, `WORKER-CONTRACT.md` and `cli/review/__init__.py`, the existing test files the plan names, the stated owner decisions and the no-authority classifier constraint were all confirmed by the review and stay.
52: 
53: ## Not to be done by the plan
54: 
55: Edit nothing under `src/`, `tests/`, `.claude/` or `plugins/` while generating the plan. Do not change the cap of 2 fix cycles, the own-scale primitives, `sc-implement-protocol/refs/qa.md`, or the 35 percent target. No Jev call, key or account.
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
