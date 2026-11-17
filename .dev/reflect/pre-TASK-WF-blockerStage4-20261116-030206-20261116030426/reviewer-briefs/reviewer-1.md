# Reviewer brief 1 (persona: analyzer; model class: sonnet)

## T1 card excerpt

## Deviation and risk observations (new, from splitting the plan)

1. **Task 1 acceptance line 2 cannot be met as written.** It requires the stage 3 summary `./artifacts/stage3-summary-for-owner.md` to "state that one audit window has passed with no revert trigger tripped" (P4:37). The stage 3 plan makes that file say the opposite: it "states that the audit window runs after this package" and "that no revert trigger can be judged until the audit window has run" (S3:158, S3:162). The file is written inside stage 3, before the window, so nobody can satisfy P4:37 unless the owner edits the stage 3 file afterwards, which no package does. The owner's go row in the ledger (P4:36) is the record that exists after the window.
2. **Allow-list location is mis-named in Tasks 1 and 3.** Both say "remove ... from the allow-list of the stage 3 scan test" (P4:33, P4:59) and their acceptance lines say "passes with the two templates removed from its allow-list" (P4:41, P4:63). The scan test reads its allow-list from the "Merge-rule allow-list" section of `refs/scale-map.md` (`S1:59`, OLD:477), so the edit belongs in `scale-map.md`; the test file holds no list. Task 6 names `scale-map.md` correctly (P4:99), Tasks 1 and 3 do not.
3. **Task 3 acceptance line 3 is not literally true for one file.** It says each of the four files "still contains its 'After 2 fix cycles' sentence" (P4:64). `src/superclaude/skills/tdd/refs/build-request-template.md:125` holds the cap only as "Maximum 2 fix cycles - after 2 fix cycles (3 reviews), HALT and escalate ..." with a lowercase "after". A case-sensitive grep for "After 2 fix cycles" finds the other three files (tech-reference :538, readme :464, operational-guide :571) and misses the tdd file. The by-content pin rule (P4:24) lets an executor read it case-insensitively.
4. **Task 5 acceptance line 2 reaches an unlisted line.** `grep -n "follow-up candidates" src/superclaude/commands/spec-panel.md` must print nothing (P4:89), but the phrase also sits in the FR-8 rule at `src/superclaude/commands/spec-panel.md:332` (and the plugin twin :330), outside the bullets Task 5 lists for editing (lines 259 to 261 and 372, P4:84). The sentence "its `follow-up candidates` list becomes the follow-up ledger" can be read to cover it; the edit list does not name it.
5. **Task 5 parity assertion is under-specified.** "a parity assertion for the two files is part of `tests/skills/test_review_severity_registry.py`" (P4:90): the plan names three files in the edit sentence and says the source and plugin spec-panel copies "differ today" (P4:84), so whole-file parity is impossible; the assertion can only be that the pointer and ledger sentence match. Task 5's acceptance lines do not run the registry test, so the new assertion is first run in Task 6.
6. **Task 1 leaves a PASS bullet next to the rewritten FAIL bullet.** `agent_template_qa.md:157` ("No CRITICAL or IMPORTANT issues") sits directly above the FAIL bullet at :158 that Task 1 rewrites or keeps; the plan names only :158 (P4:33, P4:40).
7. **Task 4's acceptance line is not pinned by content.** "contain the consumer-line instruction" (P4:73) names no sentence to quote, although the Constraints require pins by content (P4:24); the spec gives the form `feeds item X, reads column Y` (merged-requirements.md:249, :273).
8. **Pinning tests are run in one task only.** `tests/skills/test_review_prompt_overrides.py` pins "no minimum count" and the "Independent stance" sentence in `agent_template_qa.md` and the two MDTM templates and "no minimum count" in `tech-reference/SKILL.md` (test file lines 259 to 283). Only Task 2 runs it (P4:55); Tasks 1, 3, 4 and 6 edit those files and do not.
9. **Gate checks run after the edits.** The two owner-gate checks are the first two acceptance lines of Task 1 (P4:36 to 37), which QA reads after the task has edited five templates. `/sc:implement` has a user-authorized Ruling path (`src/superclaude/skills/sc-implement-protocol/refs/ledger.md:62`), so the halt exists, but the edits are already on disk when it fires.
10. **Spec section 10.5 lists `skills/tech-research/SKILL.md` and `skills/roadmap` cap lines under "Builders and researchers"** (merged-requirements.md:867); no task of this plan touches them. The request keeps cap sentences by content (`source.md:12`), so this may be intended.

## Recommendations

- Task 1: replace acceptance line 2 so it reads the ledger go row (dated after the audit window) and checks only that the stage 3 summary exists and quotes RT1 and RT2; do not require it to state a passed window.
- Tasks 1 and 3: say "remove the file's path from the 'Merge-rule allow-list' section of `refs/scale-map.md`" and name the file.
- Task 3: restate line 3 as "each file still contains its cap sentence (2 fix cycles, 3 reviews, escalate)", quoting the tdd file's own wording.
- Task 5: list `follow-up candidates` at line 332 (and the plugin twin) in the edit scope, define the parity assertion, and run `tests/skills/test_review_severity_registry.py` in its acceptance.
- Tasks 1, 3, 4: add `tests/skills/test_review_prompt_overrides.py` to an acceptance line, or to Task 6's final run.


Persona instructions (analyzer): for every acceptance criterion of Tasks 1 to 7, ask whether an executor who follows the plan text as written can make it true on the repository as it is on disk today and as it will be after the earlier stage packages (stage 1 plan, stage 3 plan; those are plans, so check them against what they promise, not against disk). Look for checks that cannot be met, checks that name the wrong file or location, line numbers or quoted sentences that do not match the live files, and contradictions between this plan and the stage 1 and stage 3 plans. Classify each as blocking or minor by the severity rule.

Severity rule (use exactly this): grade every finding by consequence as blocking or minor. Blocking = a requirement or check that cannot be met, a wrong or missing result, or data loss. Minor = wording or format. A finding that needs a guess about which of two readings an executor picks is minor unless the worse reading is the only one the text allows. A zero-finding result is valid if you state what you checked; never invent a finding to avoid a zero; there is no minimum count. You are read-only: do not edit, write, move or delete anything, run no shell or git command. Audit the supplied hunks and what you can Read, Grep and Glob from the repository root. Use the codegraph tools only when the run-state line says index_state=fresh, passing the projectPath given; codegraph indexes .py and .yaml, not Markdown.

Return your card as one message, at most about 7000 characters, in this shape (no tables): a header `persona:`, `model_class:`, `model:` is added by the orchestrator, so start with `## Verdict` (one sentence), then `## Findings` with one line per finding: `F<n> | MAJOR or MINOR | blocking true or false | category (contradiction, data-loss, missing-requirement, unpassable-check, safety, other) | Who: <the executor or reader affected>. Wrong result: <the concrete wrong outcome>. | citations: <path:line "quote"> (1 to 6 real file:line citations, quotes verbatim, re-Read each before citing)`; then `## Checked` (bullets: what you verified and found fine, with citations), then `## Self-report` with `confidence: <0.00-1.00>` and `reviewer_model_self_report: <the model you are running as, one line>`. Cite repo-relative paths with the line numbers shown in the hunks or re-Read.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-16T03:10:16Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### .dev/tasks/to-do/TASK-WF-blockerStage4-20261116-030206/TASK-WF-blockerStage4-20261116-030206.md:1-116
```markdown
1: ---
2: schema: workflow-plan/1.2
3: source: ./source.md
4: strategy: systematic
5: depth: standard
6: slug: TASK-WF-blockerStage4-20261116-030206
7: version: "1"
8: priority: Medium
9: created_date: "2026-11-16"
10: ---
11: 
12: # Stage 4 plan: propagate the new rule to the remaining carriers (issue #552)
13: 
14: Source: ./source.md
15: Goal: Move the remaining templates, rule prompts, builder and researcher skills and the spec-panel to the new rule, mirror the skill folder into the plugin, switch the drift scan to strict, and give the owner the final summary.
16: 
17: ## Constraints
18: 
19: - Spec: the merged spec `02-brainstorm/merged-requirements.md` inside the program folder `BLOCKER-CLASSIFICATION-PROGRAM-20261115` (found by that folder name under the repository's task folder). This plan calls that folder PF and the spec file the spec. Section numbers, requirement ids (REQ-nn), loop changes (L1 to L6), guardrails (GR1 to GR12), tests (T1 to T17) and owner decisions (OD1 to OD17) refer to the spec. PF also holds the 5-run results in `08-test/results.md`, the reconciliation in `09-plan-input.md` and the stage ledger and the five stage requests in `stage-requests/`. Evidence of earlier stages is read from their packages by package id (the ids are in the stage ledger), found by that folder name in the to-do or done subfolder of the repository task folder.
20: - One package, one stage. This is stage 4 of five packages and the last (one plan per stage). It runs only after the stage 3 package is done, one audit window has passed with no revert trigger tripped (spec section 13.2), the owner has read the stage 3 summary and said go in chat, and the go is recorded in the stage ledger (Task 1 checks that). Strict T2 is switched on here.
21: - Owner decisions use the spec's recommendations unless the owner changes them: OD1 skill folder `sc-review-severity`; OD2 once per run plus at any escalation halt; OD4 the classifier has no authority in version 1; OD9 reviewer-named consumer, code-checked where quotable; OD11 replace label-max merging at all 13 lines in 10 files, staged; OD12 yes; OD13 short Note rows; OD14 a finding with an unknown consumer keeps the reviewer's label (no deferral); OD15 consent-bound body file posted by the attended top-level session; OD16 option (b) at stage 3. OD3 (finding text leaving the machine), OD5 to OD8 and OD10 are not decided here and no task depends on a different answer.
22: - Not built here: any Jev or other external judge call, any TypeSafe account or key, a Jev or LLM judge class (they wait for OD3), any change to `src/superclaude/skills/sc-implement-protocol/refs/qa.md` (it keeps its own scale), any change to the own-scale primitives listed in spec section 9.3 as unchanged, code-assigned severity in `src/superclaude/cli/**/*.py` (for example `fmea_classifier.py` and `remediate_parser.py`, out of scope by spec section 10.3), the 35 percent score target, and any change to the cap of 2 fix cycles.
23: - Classifier facts that bind every classifier task: the 5-run test (stage 0 package, `stage0a-result.md`, from PF `08-test/results.md`) used a text-only stand-in judge and got agreement with the panel of 58.5 percent (Cohen's kappa 0.27), and the missing-item, constraint and contradiction questions (M, C, E) were at chance without code-supplied inputs. So M, C and E run only when code supplies the required-item list, the constraint lines and the verified evidence (the classifier-inputs supplier of stage 1), the "M or C is Y gives BLOCKING" row is never enabled for any gate, and confidence is reported as an ordinal band, never as a probability.
24: - Pins are by content. An acceptance check that must survive a task's own edit quotes the sentence it protects; it does not name a line number, because the edit moves the line. Line numbers in a task body are where the text sits today and are re-read before editing. An acceptance line that a later task of this package makes false carries its end point ("until Task N").
25: - `src/superclaude/` is the source of truth. Edit there, then run `make sync-dev`; never stage anything under the project `.claude/` folder (only `.claude/settings.json` is tracked). Installed primitives name installed paths (`~/.claude/skills/...`) first and project `.claude/...` second, never a `src/superclaude/` path.
26: - Python work uses UV only: `uv run pytest ...`, never `python -m` or bare `pip`.
27: - Task-owned evidence and generated outputs go under `./artifacts/` in this package. `.dev/tasks/` is always staged (`git add .dev/tasks`), packages and their `./artifacts/` included, and no document a task writes says it is never staged. Staging is not committing.
28: 
29: ## Phase 1: Move the templates
30: 
31: ## Task 1: Move the templates to digest v2
32: 
33: Edit the digest carriers in `src/superclaude/templates/`: `documents/agent_template_qa.md` (the definition bullet near line 161, the merge rule near line 85, the Rule 6 text near line 333 per OD16, and the FAIL-by-label bullet "Any CRITICAL or IMPORTANT issue exists" near line 158, rewritten or kept as a named mechanical gate recorded in `refs/scale-map.md`), `documents/agent_template_analysis.md` (the merge rule near line 466), `documents/skill_template.md` (the definition near line 828), `workflow/01_mdtm_template_generic_task.md` (near line 644) and `workflow/02_mdtm_template_complex_task.md` (near line 655). Each of the four digest templates (`agent_template_qa.md`, `skill_template.md` and the two MDTM templates) gets the digest and pointer in place of the definition bullets and the L1 merge text and its registry row is set to `v2`; `agent_template_analysis.md` gets the L1 merge text only (no digest, no fence, no registry row); remove `agent_template_qa.md` and `agent_template_analysis.md` from the allow-list of the stage 3 scan test. Task files already generated from the old templates keep the old text and are not migrated.
34: 
35: Acceptance criteria:
36: - The stage ledger `stage-requests/README.md` in PF has an owner go for stage 4 with a date (the go is a chat message recorded there by the session that received it); when the row has none, this check fails and the run halts for the owner's Ruling.
37: - The stage 3 package's `./artifacts/stage3-summary-for-owner.md` (read by package id) exists and states that one audit window has passed with no revert trigger tripped.
38: - Each of the four digest template files holds exactly one digest; `agent_template_analysis.md` holds no digest and no `more severe rating` text.
39: - The registry rows of the four digest templates say `v2`, T1 passes for them and the registry still has exactly 11 `digest` rows.
40: - `grep -rn "Grade every review finding as blocking or minor" src/superclaude/templates` prints nothing, and `grep -c "Any CRITICAL or IMPORTANT issue exists" src/superclaude/templates/documents/agent_template_qa.md` prints 0 or the remaining line is listed in `refs/scale-map.md`.
41: - `uv run pytest tests/skills/test_review_merge_rule_scan.py -v` passes with the two templates removed from its allow-list.
42: 
43: 
44: ## Phase 2: Move the rule prompts, builders, researchers and the consumer line
45: 
46: ## Task 2: Move the rule prompts to digest v2 and set the two pointer-only rows
47: 
48: Depends on: Task 1
49: 
50: Edit the digest carriers in `src/superclaude/rules/prompts/`: `automated_qa_workflow_qa_prompt.md` (near line 11), `doc_code_analyst_qa_prompt.md` (near line 27), `documentation_expert_qa_prompt.md` (near line 28) and `recruiting_expert_qa_prompt.md` (near line 27); update those four registry rows to `v2`. Edit `document_review_loop_prompts.md` (the Medium wording near lines 31, 32 and 48 becomes the pointer and the ledger sentence inside an existing section; its structure and the `"src/superclaude" not in TEXT` assertion of `tests/review/test_review_rules_text.py` must still hold): its registry row is of kind `pointer-only` and stays so; it is checked by T3 and never by T1.
51: 
52: Acceptance criteria:
53: - Each of the four rule prompts holds exactly one digest and its registry row says `v2`.
54: - `document_review_loop_prompts.md` holds the pointer and the ledger sentence and no digest, and its registry row stays `pointer-only`.
55: - `uv run pytest tests/review/test_review_rules_text.py tests/skills/test_review_prompt_overrides.py tests/skills/test_review_severity_registry.py -v` passes and the zero-finding and "no minimum count" sentences still exist.
56: 
57: ## Task 3: Replace the merge rule in the builder and researcher skills
58: 
59: Edit the stage 4 merge-rule lines of spec section 10.3: `src/superclaude/skills/tech-reference/SKILL.md` (two lines near 510 and 513), `src/superclaude/skills/readme/SKILL.md` (two lines near 542 and 547), `src/superclaude/skills/tdd/refs/build-request-template.md` (near line 122) and `src/superclaude/skills/operational-guide/SKILL.md` (near line 511), each to the L1 text; and remove those four files from the allow-list of the stage 3 scan test in the same change.
60: 
61: Acceptance criteria:
62: - `grep -rniE "highest severity|more severe rating|higher severity" src/superclaude/skills/tech-reference src/superclaude/skills/readme src/superclaude/skills/tdd src/superclaude/skills/operational-guide` prints nothing.
63: - `uv run pytest tests/skills/test_review_merge_rule_scan.py -v` passes with the four skills removed from its allow-list.
64: - The cap text in each of the four files is unchanged (each file still contains its "After 2 fix cycles" sentence).
65: 
66: ## Task 4: Add the consumer line to the task builder and MDTM templates
67: 
68: Depends on: Task 1
69: 
70: Edit `src/superclaude/skills/task-builder/SKILL.md` and the MDTM templates `src/superclaude/templates/workflow/01_mdtm_template_generic_task.md` and `02_mdtm_template_complex_task.md` so the task builder writes a consumer line for each phase output ("feeds item X, reads column Y"), which gives upstream gates a declared consumer list (L4, spec section 4.3 option A for upstream outputs only). Keep the cap sentence in `src/superclaude/skills/task-builder/SKILL.md` ("After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings", one occurrence today) unchanged; `src/superclaude/agents/rf-task-builder.md` holds no such sentence and is not edited.
71: 
72: Acceptance criteria:
73: - Both MDTM templates and the task-builder skill contain the consumer-line instruction.
74: - `uv run pytest tests/skills/test_task_builder_merge.py -v` passes.
75: - The cap sentence is still present in `src/superclaude/skills/task-builder/SKILL.md` (`grep -c` prints 1), and `git diff --stat` shows no edit to `src/superclaude/agents/rf-task-builder.md`.
76: 
77: 
78: ## Phase 3: Narrow spec-panel and update its twins
79: 
80: ## Task 5: Narrow spec-panel and update the plugin twins
81: 
82: Depends on: Task 2
83: 
84: Edit `src/superclaude/commands/spec-panel.md`: the Review Loop bullets (the Grading and Cap bullets near lines 259 to 261) and the always-CRITICAL dimensional-mismatch sentence ("Any dimensional mismatch identified by the Consistency Check is classified as **CRITICAL** severity", near line 372) are narrowed to the three conditions (CRITICAL stays blocking, a MAJOR stays blocking only when it names a concrete wrong outcome), its `follow-up candidates` list becomes the follow-up ledger, and the Unattended mode section gains one line for the ledger and the three contract keys. Apply the same edits to the hand-kept twins `plugins/superclaude/commands/spec-panel.md` and `plugins/superclaude/rules/prompts/document_review_loop_prompts.md`; the `spec-panel` source and plugin copies differ today, so edit each file in place and do not copy one over the other. The `commands/sc/spec-panel.md` registry row stays `pointer-only`.
85: 
86: Acceptance criteria:
87: - The existing `src/superclaude/examples/...` mention in `src/superclaude/commands/spec-panel.md` and its twins is left as it is (T3 does not check `pointer-only` rows for that path).
88: - `uv run pytest tests/skills/test_spec_panel_review_loop.py tests/skills/test_review_loop_extension.py -v` passes and the cap sentence `at most 2 fix cycles (3 reviews)` is still in `src/superclaude/commands/spec-panel.md`.
89: - `grep -n "follow-up candidates" src/superclaude/commands/spec-panel.md` prints nothing and the ledger is named instead.
90: - The plugin twins carry the same pointer and ledger sentence as their source twins, and a parity assertion for the two files is part of `tests/skills/test_review_severity_registry.py`.
91: 
92: 
93: ## Phase 4: Mirror the skill folder into the plugin and write the summary
94: 
95: ## Task 6: Mirror the skill folder into the plugin and make the drift scan strict
96: 
97: Depends on: Task 1, Task 2, Task 3, Task 4, Task 5
98: 
99: Work in this order, because the registry and the allow-list must be correct before the copy. First add the plugin mirror of `refs/rule.md` (`plugins/superclaude/skills/sc-review-severity/refs/rule.md`) as a `canonical` row in `src/superclaude/skills/sc-review-severity/refs/registry.yaml` and as a path in the "Merge-rule allow-list" section of `refs/scale-map.md` (by path only; no merge-rule phrase is written there). Then copy `src/superclaude/skills/sc-review-severity/` to `plugins/superclaude/skills/sc-review-severity/` by hand (the plugin's `skills/` is hand-kept and holds 4 entries today). Then add `tests/skills/test_review_severity_plugin_parity.py` for T15 (the mirror equals the source), set every `digest` row to `v2` where its file now holds the digest (and repeat the copy if the registry changed), and switch T2 of `tests/skills/test_review_severity_registry.py` to strict mode so any legacy definition sentence left in `src/` or `plugins/` fails. Run `make sync-dev` and `make verify-sync`, then the three tests together.
100: 
101: Acceptance criteria:
102: - `uv run pytest tests/skills/test_review_merge_rule_scan.py tests/skills/test_review_severity_plugin_parity.py tests/skills/test_review_severity_registry.py -v` passes with strict T2, and the plugin mirror of `refs/rule.md` is accepted by the reverse scan through its `canonical` row and by the merge-rule scan through the allow-list.
103: - `make verify-sync` passes.
104: - `grep -rn "Grade every review finding as blocking or minor" src/superclaude plugins/superclaude` prints nothing; the five installed-only spec-panel variants are outside the scan and stay listed `installed-only`.
105: - No file under the project `.claude/` folder other than `.claude/settings.json` appears in `git diff --cached --name-only`.
106: 
107: ## Task 7: Write the stage 4 summary for the owner
108: 
109: Depends on: Task 1, Task 2, Task 3, Task 4, Task 5, Task 6
110: 
111: Write `./artifacts/stage4-summary-for-owner.md`: per carrier the digest state and the test that pins it, the final results of the merge-rule scan, the plugin parity test and the strict registry test with their observed pass counts, and the revert command per row (the spec's three-step revert). State that a second audit window is observed by the owner or operator and is not a task of this package, and list the open items.
112: 
113: Acceptance criteria:
114: - `./artifacts/stage4-summary-for-owner.md` lists every carrier row with its state (`v2` or the stated exception) and the test that pins it, and each named test file exists.
115: - The summary shows the observed pass counts of the scan, parity and strict registry tests and the `make verify-sync` result.
116: - The summary states the revert command per row and that the second audit window is not a task of this package.
```

### .dev/tasks/to-do/TASK-WF-blockerStage4-20261116-030206/source.md:1-20
```markdown
1: # Stage 4 plan request: propagate the new rule to the remaining carriers (issue #552)
2: 
3: Last of five plan packages (see `stage-requests/README.md`). Generate it only after the stage 3 package is done, one audit window has passed with no revert trigger tripped (the spec's section 13.2), the owner has read `./artifacts/stage3-summary-for-owner.md`, and the owner's go in chat is recorded in the stage ledger.
4: 
5: ## Base text
6: 
7: Reuse Tasks 41 to 46 of the revised 46-task plan `TASK-WF-loosenBlockerRev-20261115-210254` (Phase 5, stage 4; found by that folder name under `.dev/tasks/to-do/`), renumbered 1 onward, with its `## Constraints` (stage 4 parts). Earlier stages' evidence is read by package id.
8: 
9: ## Changes to apply
10: 
11: - **Templates (the old Task 41).** The digest goes into four templates: `agent_template_qa.md`, `skill_template.md`, `01_mdtm_template_generic_task.md` and `02_mdtm_template_complex_task.md`. `agent_template_analysis.md` gets the merge-rule text only (no digest, no registry row, no fence). The registry keeps exactly 11 `digest` rows. Acceptance: "four template files hold exactly one digest", the analysis template holds none and no `more severe rating` text, and `agent_template_qa.md` holds none of the "Any CRITICAL or IMPORTANT issue exists" FAIL bullet unless it is listed as a kept mechanical gate in `refs/scale-map.md`. Remove `agent_template_qa.md` and `agent_template_analysis.md` from the scan allow-list in the same change.
12: - **Rule prompts, builders and researchers, consumer line (the old Tasks 42 to 44).** As the base text, with the two `pointer-only` rows left at `pointer-only` and the cap sentences kept by content.
13: - **Spec-panel (the old Task 45).** As the base text; the existing `src/superclaude/examples/...` mention in `commands/spec-panel.md` and its twins stays, since T3 does not check `pointer-only` rows for that path.
14: - **Plugin mirror (the old Task 46).** Order the work so the registry and the allow-list are correct BEFORE the copy: first add the plugin mirror of `refs/rule.md` to the `canonical` registry rows and to the allow-list in `refs/scale-map.md` (path only, no merge-rule phrases), then copy the skill folder to `plugins/superclaude/skills/sc-review-severity/`, then run T15 parity, strict T2 and the merge-rule scan. Acceptance includes `uv run pytest tests/skills/test_review_merge_rule_scan.py tests/skills/test_review_severity_plugin_parity.py tests/skills/test_review_severity_registry.py -v` passing, `make verify-sync` passing, and no `.claude/` path other than `.claude/settings.json` staged.
15: - **Constraints.** State this is stage 4 and the last package; strict T2 is switched on here. Acceptance lines that a later task of this package makes false get an end point.
16: - **New final task: stage 4 summary for the owner.** Write `./artifacts/stage4-summary-for-owner.md`: per carrier the digest state and the test that pins it, the final scan and parity results, and the revert command per row (the spec's three-step revert), ending with the sentence that a second audit window is observed by the owner or operator and is not a task of this package.
17: 
18: ## Not to be done by the plan
19: 
20: No change to `sc-implement-protocol/refs/qa.md`, the own-scale primitives, the severity code under `src/superclaude/cli/**/*.py`, the cap of 2 fix cycles or the 35 percent target. No Jev call, key or account.
```

### .dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/TASK-WF-blockerStage3-20261116-030158.md:158-162
```markdown
158: Write `./artifacts/stage3-summary-for-owner.md`: the seeded-recall result headline from Task 1, the re-pinned test results, and the audit-window measures the spec's section 13 defines for stage 3 (read the metric list in section 13.1 including M12, the rf-qa FAIL count per pilot gate, and the revert triggers RT1 and RT2 in section 13.2 with their current state; quote their text from the spec and do not restate it from memory). State that the audit window runs after this package and is observed by the owner or operator, name which runs and gates it covers, and end with the sentence that the owner's go for stage 4 is given in chat and not by this file.
159: 
160: Acceptance criteria:
161: - `./artifacts/stage3-summary-for-owner.md` names the seeded-recall headline and the file that holds it, lists the tests re-pinned with their observed pass counts, and quotes RT1, RT2 and M12 from the spec.
162: - The summary states the revert command per carrier row (the spec's three-step revert) and that no revert trigger can be judged until the audit window has run.
```

### .dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/TASK-WF-blockerStage3-20261116-030158.md:20-20
```markdown
20: - One package, one stage. This is stage 3 of five packages (one plan per stage). It changes the live review rule. It runs only when all of these hold, each checked by reading files and not by memory (Task 1 checks them): the owner's go for stage 3 is recorded in the stage ledger; the stage 2 package's `./artifacts/stage2-summary-for-owner.md` exists and states at least 5 observed shadow runs with zero safety misses (by the definition the stage 0 spec edit drafted) and no capture failure; the stage 0 package's `stage0b-escape-test.md` and `stage0c-regrade.md` exist. `/sc:implement` runs this whole package in order, so the rule switch cannot start unless Task 1's checks and the seeded-recall result pass. Stage 4 starts only after one audit window with no revert trigger tripped (spec section 13.2) and the owner's go in chat.
```

### .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md:59-59
```markdown
59: Create `src/superclaude/skills/sc-review-severity/refs/scale-map.md` with one row per family of spec section 9.3: family, defining file, each native label, the shared outcome per label (Blocking, Medium, Note), and either "graded by the three conditions" or "keeps its own model because <reason>". The rows are the 12 families of that table: the CRITICAL, IMPORTANT, MINOR lens scale; the `/sc:implement` `refs/qa.md` checklist; spec-panel; the stoprule rubric and `finding-grader`; the reflect deviation taxonomy; tasklist High, Medium, Low; roadmap validate; `card_convert.py`; findings-v1 and v2; `sc-auggie-review-protocol/SKILL.md:228`; the PR severity router and Auggie rubric; and the code-assigned family. Include the sentence that a keep of a fixed FAIL trigger (L6) is recorded here, and a section "Merge-rule allow-list" that lists by path only the files allowed to contain the three merge-rule phrases of spec section 10.3 (the auggie file, `refs/rule.md`, and the six stage 4 files until the stage 4 package; this file never writes those phrases or the old definition sentence) so the stage 3 scan test reads its allow-list from one place. The plugin mirror is added to the list by the stage 4 package, not here.
```

### .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md:96-100
```markdown
96: Create `src/superclaude/skills/sc-review-severity/refs/registry.yaml`. Each row has the logical path relative to the install root, a `kind` (`digest`, `canonical`, `pointer-only` or `installed-only`), surfaces (source, installed, project `.claude/`, plugin, or `installed-only`), rollout stage, a state (`legacy` for a digest row until its file is moved), and an own-scale flag. Rows of kind `digest`, exactly the 11 definition carriers of spec section 10.1: `output-styles/pragmatic.md`, `agents/rf-qa.md`, `agents/rf-qa-qualitative.md`, `templates/documents/agent_template_qa.md`, `templates/documents/skill_template.md`, `templates/workflow/01_mdtm_template_generic_task.md`, `templates/workflow/02_mdtm_template_complex_task.md`, `rules/prompts/automated_qa_workflow_qa_prompt.md`, `rules/prompts/doc_code_analyst_qa_prompt.md`, `rules/prompts/documentation_expert_qa_prompt.md`, `rules/prompts/recruiting_expert_qa_prompt.md`. One row of kind `canonical`: `skills/sc-review-severity/refs/rule.md` (the one source digest; the stage 4 package adds its plugin mirror). Two rows of kind `pointer-only` (a pointer plus the ledger sentence, no digest): `rules/prompts/document_review_loop_prompts.md` and `commands/sc/spec-panel.md` (source `commands/spec-panel.md`). Five rows of kind `installed-only`: `commands/sc/spec-panel-armb.md`, `spec-panel-diffgate.md`, `spec-panel-ledger.md`, `spec-panel-ponytail.md` and `spec-panel-stoprule.md`. `skills/task/SKILL.md` gets no row: it is not a digest carrier. `templates/documents/agent_template_analysis.md` gets no row either: it holds no definition sentence, only a merge-rule line, which the stage 4 package edits as text only.
97: 
98: Acceptance criteria:
99: - `refs/registry.yaml` parses with `uv run python -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))" src/superclaude/skills/sc-review-severity/refs/registry.yaml`.
100: - It has exactly 11 rows of kind `digest` (each with a source path that exists, state `legacy`, stage 3 for `pragmatic.md`, `rf-qa.md` and `rf-qa-qualitative.md`, stage 4 for the rest), 1 of kind `canonical`, 2 of kind `pointer-only` and 5 of kind `installed-only`, 19 rows in all.
```

### .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md:209-214
```markdown
209: Create `tests/skills/test_review_severity_registry.py` for T1 (every row of kind `digest` holds, in its file, exactly one digest whose flattened body equals the digest section of `refs/rule.md` for that row's version; a row at `legacy` is accepted; the `canonical` row holds the source digest), T2 (a reverse scan of the tracked `src/` and `plugins/` trees fails on any file that holds the old definition sentence or a fence opener and has no registry row of any kind; `canonical` and `pointer-only` rows count as registered; strict mode is a switch, off in this phase), T3 (each pointer names `~/.claude/skills/sc-review-severity/...` before `.claude/skills/sc-review-severity/...`, ; the check that no carrier contains `src/superclaude` applies to `digest` and `canonical` rows only; `pointer-only` and `installed-only` rows are checked for pointer order only, a `pointer-only` row only once its pointer is present, and the test never reads `~/.claude`), T4 (each scale-map row names an existing file and a label present in it) and T14 (a `digest` row at `v2` holds the precedence sentence).
210: 
211: Acceptance criteria:
212: - A temporary-tree test shows each T3 exemption: a `pointer-only` row whose file holds a `src/superclaude` path passes the path check, a `pointer-only` row without its pointer yet passes, and a `digest` row whose file holds such a path fails.
213: - `uv run pytest tests/skills/test_review_severity_registry.py -v` passes with all `digest` rows at `legacy`.
214: - A test flips one `digest` row to `v2` without editing its file and fails, which shows T1 can fail; a `pointer-only` row at any state does not fail T1.
```

### src/superclaude/templates/documents/agent_template_qa.md:150-163
```markdown
150: ### Stakeholder Personas
151: Read through these lenses simultaneously:
152: - **[Persona 1]:** [What this persona cares about — e.g., "Product Manager: Does this solve the stated problem?"]
153: - **[Persona 2]:** [What this persona cares about — e.g., "Engineering Lead: Is this implementable as described?"]
154: - **[Persona 3]:** [What this persona cares about — e.g., "QA Engineer: Can I write test cases from these requirements?"]
155: 
156: ### Verdict
157: - **PASS** — No CRITICAL or IMPORTANT issues; any MINOR issues are listed as notes.
158: - **FAIL** — Any CRITICAL or IMPORTANT issue exists. List each with specific remediation. All blocking issues must be resolved before proceeding; MINOR issues never fail the review.
159: 
160: Review severity rule (applies to every verdict):
161: - Grade every review finding as blocking or minor. Blocking is a real defect: wrong behaviour, a false claim, a missing required deliverable, or a security or data-loss risk. Minor is cosmetic, wording, formatting, citation format, a nit, style, or a moved line number on a true claim.
162: - Minor findings never fail a review: the reviewer records them in its report as notes, the verdict is PASS (with notes), and work proceeds. Minor findings are not rechecked in later rounds and never trigger a fix pass on their own. Only blocking findings produce FAIL.
163: - A review loop (review, fix, re-review) runs at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings; never run a fourth review and never pass open blocking findings.
```

### src/superclaude/skills/tdd/refs/build-request-template.md:118-126
```markdown
118: 
119: Phase 3 — Research Completeness Verification (ANALYST + QA GATE, PARALLEL):
120: 
121: - Spawn `rf-analyst` (subagent_type: "rf-analyst", analysis_type: "completeness-verification") AND `rf-qa` (subagent_type: "rf-qa", qa_phase: "research-gate") IN PARALLEL. Both agents independently read research files and apply their own checklists. The analyst applies its 8-item completeness checklist (coverage audit, evidence quality, doc staleness, completeness, cross-references, contradictions, gap compilation, depth assessment). The QA agent applies its 10-item research-gate checklist (file inventory, evidence density, scope coverage, doc cross-validation, contradiction resolution, gap severity, depth appropriateness, integration points, pattern documentation, incremental writing compliance). The analyst writes to `${TASK_DIR}qa/analyst-completeness-report.md`. The QA agent writes to `${TASK_DIR}qa/qa-research-gate-report.md`. Embed full prompts from respective agent definitions in each checklist item per B2.
122: - **Parallel partitioning for large workloads:** When >6 research files exist, spawn MULTIPLE analyst + QA instances with assigned_files subsets. The threshold is >6 for research files because research files tend to be longer and more detailed than synthesis files. Each partition instance writes to a numbered report (e.g., `${TASK_DIR}qa/analyst-completeness-report-1.md`). After all instances complete, merge reports: union of findings, take the more severe rating for any item flagged by multiple partitions, deduplicate gaps.
123: - Read ALL reports (or merged report). Determine verdict from QA report(s) (PASS / FAIL), cross-referenced with analyst findings.
124: - If PASS → proceed to Phase 4. If FAIL → fix every blocking finding (minor findings are recorded as notes) before proceeding. Spawn targeted gap-filling agents, then rf-qa fix-cycle.
125: - Maximum 2 fix cycles — after 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings; log all remaining issues in Task Log. Do NOT continue to Phase 4 without user approval.
126: - Compile final gaps into ${TASK_DIR}gaps-and-questions.md
```

### src/superclaude/commands/spec-panel.md:255-262
```markdown
255: 
256: ## Review Loop
257: 
258: 1. **Mode**: `--re-review` applies to `--mode critique` only; without both `--re-review` and `--baseline` the run is a first review of the full document, with `baseline: missing` noted if only one was given; if a named file is unreadable or empty, or the prior report has no `review: N of 3` header, stop and say which, and never fall back to a first review; the report header also records the SHA-256 of the candidate and, when a baseline was given, of the baseline, and the reviewer model actually used, and an input whose hash cannot be taken stops the run like an unreadable file.
259: 2. **Grading**: grade by consequence, not by label; CRITICAL is blocking; a MAJOR or an FR-8/FR-9 finding is blocking only if it names a concrete wrong outcome an implementer would produce or a security, data-loss or safety-boundary risk, otherwise it is Medium (a warning listed under `follow-up candidates`); MINOR is a note; Medium and minor findings never trigger a revision, never fail a review and never appear in the Reviser brief.
260: 3. **Verdict**: a critique-mode report's last line is `verdict: PASS` (minor notes and Medium warnings allowed) or `verdict: FAIL` (a blocking finding is open); the report lists Medium and minor findings under `follow-up candidates`, the session that ran the review asks the user once per loop whether to open an issue for them and creates none without the user's answer, and an `--unattended` run only records the list; a coordinator treats a re-review report with no prior-findings table, any report whose final `verdict:` line is missing or ambiguous, and any report that cites a finding id absent from its table as `verdict: FAIL`, never as PASS and never as zero findings.
261: 4. **Cap**: at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings; the report header is `review: N of 3`, where N is the prior report's N plus 1 (1 for a first review); a prior-findings file at `review: 3` (a higher value counts as 3) with `verdict: FAIL` means do not review (this check runs before the first-review default of bullet 1), HALT and escalate to the user with the open blocking findings; every run is one review whatever `--iterations` says, and with `--re-review` the command ignores `--iterations`, skips the Improve step and writes no revised specification; Iteration 2 and 3 themes set order of attention, not a mandate to add text. The coordinator keeps the review count, the prior-findings file and the saved copy; without them the run is a first review; after the second fix cycle only the third review runs, and a severity or necessity audit before it only reports and edits nothing.
262: 5. **Re-review output**: first a table of prior blocking findings `resolved|open|regressed` (`regressed` = a finding the prior report marked resolved that fails again; each keeps its id from the prior report, and a finding the reviser deferred or withdrew, or one the reviewer cannot match to a prior id with certainty, counts as open); then findings on lines changed against the baseline, ignoring whitespace-only changes, each with `origin=changed|unchanged`; an `origin=unchanged` finding is a minor note unless it quotes the changed line that depends on it; in a re-review FR-8 to FR-10 and the Guard Condition Boundary Table cover guards on changed lines only; an empty diff leaves every prior blocking finding open and still counts as a review; a re-review with no open blocking finding ends `verdict: PASS` with the coverage line `scoped PASS: changed lines + prior blockers`, and whole-document assurance needs a separate, labelled first review whose blockers are escalated and never start a fourth review. The re-check of prior blocking findings follows steps 1-5 of the Process of the Fix Cycle phase in the project `.claude/agents/rf-qa.md` first, else `~/.claude/agents/rf-qa.md`; the rules in this section apply on top of it and stand alone when that file is unread.
```

### src/superclaude/commands/spec-panel.md:330-333
```markdown
330: These rules are **hard gates**, not advisory recommendations. They block synthesis output unconditionally.
331: 
332: 1. **FR-8: GAP Status Rule**: Any cell in the Status column containing "GAP" generates a finding. It is blocking when it names a concrete wrong outcome an implementer would produce or a security, data-loss or safety-boundary risk; otherwise it is Medium (a warning listed under `follow-up candidates`).
333: 2. **FR-9: Blank Behavior Rule**: Any blank or "unspecified" entry in the Specified Behavior column generates a finding, graded like FR-8.
```

### src/superclaude/commands/spec-panel.md:370-373
```markdown
370: #### Severity Classification (FR-19)
371: 
372: Any dimensional mismatch identified by the Consistency Check is classified as **CRITICAL** severity. The finding MUST include a concrete scenario demonstrating the mismatch with specific count values (e.g., "10 items enter filter, 7 pass, but downstream batch processor assumes 10").
373: 
```

### tests/skills/test_review_prompt_overrides.py:255-283
```python
255: 
256: @pytest.mark.parametrize(
257:     "rel",
258:     [
259:         "src/superclaude/agents/rf-qa.md",
260:         "src/superclaude/agents/rf-qa-qualitative.md",
261:         "src/superclaude/templates/documents/agent_template_qa.md",
262:     ],
263: )
264: def test_qa_agents_use_the_independent_stance(rel):
265:     flat = _flat((_REPO / rel).read_text(encoding="utf-8"))
266:     assert "**Independent stance**" in flat, rel
267:     assert "there is no minimum count" in flat, rel
268:     assert "do not invent findings to avoid a zero" in flat, rel
269: 
270: 
271: @pytest.mark.parametrize(
272:     "rel",
273:     [
274:         "src/superclaude/skills/task/SKILL.md",
275:         "src/superclaude/skills/tech-reference/SKILL.md",
276:         "src/superclaude/skills/tech-research/SKILL.md",
277:         "src/superclaude/templates/workflow/01_mdtm_template_generic_task.md",
278:         "src/superclaude/templates/workflow/02_mdtm_template_complex_task.md",
279:     ],
280: )
281: def test_lens_prompts_state_no_minimum_count(rel):
282:     flat = _flat((_REPO / rel).read_text(encoding="utf-8"))
283:     assert "no minimum count" in flat, rel
```

### src/superclaude/skills/sc-implement-protocol/refs/ledger.md:58-70
```markdown
58: ```
59: 
60: `complete` on the verdict line **only if** `verdict=compliant`. `compliant` may carry open minor/note findings recorded in the notes file (`refs/qa.md`). Otherwise status MUST be `blocked` until an operator Ruling + a follow-up complete line.
61: 
62: ## Ruling line (user-authorized, executor-recorded)
63: 
64: ```
65: T<id>: Ruling: <what> — <why> — <cost-if-wrong>
66: ```
67: 
68: Em dashes as shown. Three non-empty fields. On clear user confirmation the executor MUST automatically append this line; the confirmation gate is the Halt table in `refs/qa.md`.
69: 
70: ```
```

### src/superclaude/skills/tech-reference/SKILL.md:508-514
```markdown
508: Phase 3 — Research Completeness Verification (MULTI-AGENT LENS GATE, PARALLEL):
509: - Spawn 5 agents IN PARALLEL, all fix_authorization: false (report only): (1) rf-analyst (completeness-verification lens) — writes to `${TASK_DIR}qa/analyst-completeness-report.md`; (2) rf-analyst (cross-validation lens — do findings from different research agents agree? do cross-references between research files resolve?) — writes to `${TASK_DIR}qa/analyst-crossval-report.md`; (3) rf-qa (evidence-quality lens) — writes to `${TASK_DIR}qa/qa-research-evidence-report.md`; (4) rf-qa (gap-detection lens — are there subsystems, files, or integration points mentioned in scope discovery but absent from research?) — writes to `${TASK_DIR}qa/qa-research-gaps-report.md`; (5) rf-qa-qualitative (research-depth lens — are findings genuinely deep with traced data flows and function signatures, or surface-level file listings?) — writes to `${TASK_DIR}qa/qa-research-depth-report.md`. Each agent gets a lens-specific prompt with adversarial framing: "Look for critical issues in your lens area that these research files missed. Report each one you find with evidence; there is no minimum count, and zero is valid if you state what you checked." Embed full prompts in each checklist item per B2.
510: - **Parallel partitioning for large workloads:** When >6 research files exist, spawn MULTIPLE analyst instances and MULTIPLE QA instances in parallel, each with an `assigned_files` subset. The threshold is >6 for research files because research files tend to be longer and more detailed than synthesis files. For example, with 10 research files: spawn 2 analyst instances (5 files each) + 2 QA instances (5 files each) + 2 qualitative instances (5 files each) = 6 parallel agents. Each partition instance writes to a numbered report (e.g., `analyst-completeness-report-1.md`, `analyst-completeness-report-2.md`). After all instances complete, merge their reports: union of all findings, take the more severe rating for any item flagged by multiple partitions, deduplicate gaps.
511: - Read ALL reports (or the merged report). Determine verdict from the QA report(s) (PASS / FAIL), cross-referenced with analyst findings. If PASS, proceed to Phase 4. If FAIL, follow the serialized fix protocol below.
512: - **Serialized fix protocol for Phase 3 (follows the same consolidate-fix-verify pattern as Phases 5 and 6):**
513:   1. **Consolidate findings:** Merge all 5 agent reports into a single findings list at `${TASK_DIR}qa/qa-research-consolidated-findings.md`. Deduplicate overlapping findings. Preserve the highest severity rating when duplicates disagree.
514:   2. **Gap-filling as fix step:** A "gap" is any FAIL-rated (blocking) finding from the consolidated findings list; minor findings stay as notes and get no gap-filling agent. Spawn additional targeted research agents (one per gap from the consolidated findings). Each gap-filling agent follows the same incremental writing protocol. This is the "fix" step, analogous to the single fix agent in Phases 5 and 6, but using research agents since the remediation is additional investigation, not file editing.
```

### src/superclaude/skills/readme/SKILL.md:540-548
```markdown
540:   **ADVERSARIAL STANCE for ALL 5 agents:** "Look for errors in the research. Report each one you find with evidence; there is no minimum count, and zero is valid if you state what you checked. A verdict of 0 issues requires evidence you thoroughly checked every file."
541:   Each agent writes to a separate report: `${TASK_DIR}qa/analyst-completeness-report-[N].md`, `${TASK_DIR}qa/qa-research-gate-report-[N].md`, `${TASK_DIR}qa/qa-research-depth-report.md`
542: - Step 3.2: Consolidate all 5 reports into `${TASK_DIR}qa/qa-consolidated-research-findings.md`. Union all findings, take more severe rating for duplicates.
543: - **Sub-flow A: Fix existing research content (Steps 3.3-3.4, serialized fix protocol):**
544:   - Step 3.3: If any blocking findings exist in the consolidated report, spawn 1 rf-qa fix agent (fix_authorization: true, per the universal Consolidated Fix Agent Prompt) with the consolidated blocking findings (minor findings stay as notes) to apply all blocking fixes to existing research files.
545:   - Step 3.4: Spawn 2 verification agents (1 rf-qa + 1 rf-qa-qualitative, fix_authorization: false) to confirm fixes applied correctly.
546:   - If verification finds new blocking issues, repeat Steps 3.3-3.4 (new minor findings are notes and do not restart the cycle). Maximum 2 fix cycles for Sub-flow A.
547: - **Parallel partitioning for large workloads:** When >6 research files exist, spawn MULTIPLE instances of each of the 5 agent roles in parallel, each with an `assigned_files` subset. The threshold is >6 for research files because research files tend to be longer and more detailed than synthesis files. For example, with 10 research files: spawn 2 instances of each role (5 files each). Each partition instance writes to a numbered report (e.g., `${TASK_DIR}qa/analyst-completeness-report-1.md`, `${TASK_DIR}qa/analyst-completeness-report-2.md`). After all instances complete, merge their reports: union of all findings, take the more severe rating for any item flagged by multiple partitions, deduplicate gaps.
548: - Read ALL reports (or the merged report). Determine verdict from the QA report(s) (PASS / FAIL), cross-referenced with analyst findings.
```

### src/superclaude/skills/operational-guide/SKILL.md:509-512
```markdown
509:   **ADVERSARIAL STANCE (all agents):** Assume the work contains errors. Your job is to find what was missed, not confirm everything is fine. Verify every claim exhaustively. A verdict of 0 issues requires evidence you thoroughly checked.
510:   Each agent independently reads research files and applies its lens-specific checklist. Embed full lens-specific prompts in each checklist item per B2.
511: - **Parallel partitioning for large workloads:** When >6 research files exist, DOUBLE agent counts: spawn 4 rf-analyst + 4 rf-qa + 2 rf-qa-qualitative = 10 agents. Each partition instance gets an assigned_files subset and writes to a numbered report. After all complete, merge reports: union of all findings, take more severe rating for items flagged by multiple partitions, deduplicate gaps.
512: - **Serialized fix protocol:** Read ALL reports. Consolidate all findings into `${TASK_DIR}qa/qa-research-consolidated-findings.md`. Spawn 1 rf-qa fix agent (fix_authorization: true) with the consolidated blocking findings to apply ALL blocking fixes (minor findings stay as notes). Then spawn a verification round (2 agents: 1 rf-qa + 1 rf-qa-qualitative, fix_authorization: false) to confirm fixes.
```

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|---|---|---|---|
| INF-003 to INF-007 | Task 1 | mapped | P4:33,36-41 carriers, allow-list removal |
| INF-008 | Tasks 2, 3, 4 | mapped | P4:50,54,64,75 pointer-only and cap kept |
| INF-001 | Task 1 | mapped | P4:36-37 owner go and stage 3 summary |
